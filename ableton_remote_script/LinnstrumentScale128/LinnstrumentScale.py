"""
Main MIDI Remote Script for Linnstrument Multi-Mode System
Supports 3 modes: Keyboard, Session, and Drum Sequencer
"""

import sys
import os
from pathlib import Path

# Import configuration
try:
    from .config import (
        MODE_KEYBOARD, MODE_SESSION, MODE_DRUM, MODE_COUNT,
        MODE_SWITCH_CC, MODE_SWITCH_CHANNEL, MODE_COLORS,
        LINNSTRUMENT_BASE_NOTE, LINNSTRUMENT_ROW_OFFSET, LINNSTRUMENT_COLUMN_OFFSET,
        NRPN_USER_FIRMWARE_MODE, NRPN_ENABLE_VALUE
    )
    from .scales import NOTE_NAMES
    from .linnstrument_ableton import LinnstrumentAbletonMIDI
    from .led_manager import LEDManager
    from .modes import KeyboardMode, SessionMode, DrumMode
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Ableton Live API
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
import Live


class LinnstrumentScale(ControlSurface):
    """
    Multi-mode MIDI Remote Script for LinnStrument
    - Keyboard Mode: Scale lighting (original functionality)
    - Session Mode: Clip launcher grid
    - Drum Mode: Drum pads + step sequencer
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self.log_message("=" * 60)
        self.log_message("Linnstrument Multi-Mode System - Starting...")
        self.log_message("=" * 60)

        # Check if modules are available
        if not MODULES_AVAILABLE:
            self.log_message(f"ERROR: Could not import modules: {IMPORT_ERROR}")
            self.show_message("Linnstrument: Import Error - Check Log")
            return

        # Core components
        self.linnstrument = None
        self.led_manager = None

        # Mode system
        self._current_mode_index = MODE_KEYBOARD
        self._modes = {}
        self._active_mode = None

        # Initialize LinnStrument MIDI controller
        try:
            self.linnstrument = LinnstrumentAbletonMIDI(
                c_instance,
                base_note=LINNSTRUMENT_BASE_NOTE,
                row_offset=LINNSTRUMENT_ROW_OFFSET,
                column_offset=LINNSTRUMENT_COLUMN_OFFSET
            )
            self.log_message("Linnstrument MIDI controller initialized")
            self.log_message(f"Config: base_note={LINNSTRUMENT_BASE_NOTE}, "
                           f"row_offset={LINNSTRUMENT_ROW_OFFSET}, "
                           f"column_offset={LINNSTRUMENT_COLUMN_OFFSET}")

        except Exception as e:
            self.log_message(f"ERROR: Could not initialize Linnstrument: {e}")
            self.show_message("Linnstrument: Initialization Error")
            return

        # Initialize LED Manager
        try:
            self.led_manager = LEDManager(self.linnstrument, c_instance)
            self.log_message("LED Manager initialized")
        except Exception as e:
            self.log_message(f"ERROR: Could not initialize LED Manager: {e}")
            return

        # Initialize modes
        try:
            song = self.song()
            self._modes = {
                MODE_KEYBOARD: KeyboardMode(c_instance, self.linnstrument, self.led_manager, song),
                MODE_SESSION: SessionMode(c_instance, self.linnstrument, self.led_manager, song),
                MODE_DRUM: DrumMode(c_instance, self.linnstrument, self.led_manager, song),
            }
            self.log_message("All modes initialized")
        except Exception as e:
            self.log_message(f"ERROR: Could not initialize modes: {e}")
            import traceback
            self.log_message(traceback.format_exc())
            return

        # Enable LED User Firmware Mode via NRPN
        self._enable_user_firmware_mode()

        # Add listener for track selection changes
        self.song().view.add_selected_track_listener(self._on_track_changed)

        # Auto-select appropriate mode based on current track
        self._auto_switch_mode()

        self.log_message("=" * 60)
        self.log_message("Linnstrument Multi-Mode System - Ready!")
        self.log_message("Auto-switches to Drum Mode when Drum Rack detected")
        self.log_message("Press Switch 1 (CC65) to manually cycle modes")
        self.log_message("=" * 60)
        self.show_message("Linnstrument: Multi-Mode Ready")

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log_message("Linnstrument Multi-Mode System - Disconnecting...")

        # Exit current mode
        if self._active_mode:
            self._active_mode.exit()

        # Clean up
        ControlSurface.disconnect(self)
        self.log_message("Linnstrument Multi-Mode System - Disconnected")

    def _enable_user_firmware_mode(self):
        """Enable LinnStrument User Firmware Mode for LED control"""
        try:
            self.log_message("Enabling LED User Firmware Mode...")

            # Send NRPN 245 = 1 to enable User Firmware Mode
            # NRPN format: CC99 (MSB), CC98 (LSB), CC6 (data MSB), CC38 (data LSB)
            channel = MODE_SWITCH_CHANNEL
            status = 0xB0 + channel

            self._c_instance.send_midi((status, 99, 0))    # NRPN MSB = 0
            self._c_instance.send_midi((status, 98, NRPN_USER_FIRMWARE_MODE))  # NRPN LSB = 245
            self._c_instance.send_midi((status, 6, 0))     # Data MSB = 0
            self._c_instance.send_midi((status, 38, NRPN_ENABLE_VALUE))    # Data LSB = 1 (enable)

            self.log_message("User Firmware Mode enabled (Global Settings button should be YELLOW)")

        except Exception as e:
            self.log_message(f"Error enabling User Firmware Mode: {e}")

    def _switch_to_mode(self, mode_index):
        """
        Switch to a different mode

        Args:
            mode_index: MODE_KEYBOARD, MODE_SESSION, or MODE_DRUM
        """
        try:
            if mode_index not in self._modes:
                self.log_message(f"Invalid mode index: {mode_index}")
                return

            # Exit current mode
            if self._active_mode:
                self._active_mode.exit()

            # Force clear all LEDs between modes to prevent ghosting
            self.led_manager.clear_all()
            self.log_message("Cleared all LEDs during mode switch")

            # Switch to new mode
            self._current_mode_index = mode_index
            self._active_mode = self._modes[mode_index]
            self._active_mode.enter()

            # Rebuild MIDI map for new mode
            self.request_rebuild_midi_map()

            # Log mode switch
            mode_names = {
                MODE_KEYBOARD: "Keyboard",
                MODE_SESSION: "Session",
                MODE_DRUM: "Drum Sequencer"
            }
            self.log_message(f"Switched to {mode_names.get(mode_index, 'Unknown')} Mode")

        except Exception as e:
            self.log_message(f"Error switching to mode {mode_index}: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def _cycle_mode(self):
        """Cycle to next mode"""
        next_mode = (self._current_mode_index + 1) % MODE_COUNT
        self._switch_to_mode(next_mode)

    def _translate_drum_note(self, note):
        """
        Translate drum pad notes from row_offset=5 to chromatic (row_offset=4)

        With row_offset=5, 4x4 grid produces: 36-39, 41-44, 46-49, 51-54
        We want chromatic: 36-39, 40-43, 44-47, 48-51

        Args:
            note: Input MIDI note number

        Returns:
            Translated MIDI note number
        """
        # Translation map
        translation = {
            # Row 0: no change
            36: 36, 37: 37, 38: 38, 39: 39,
            # Row 1: subtract 1
            41: 40, 42: 41, 43: 42, 44: 43,
            # Row 2: subtract 2
            46: 44, 47: 45, 48: 46, 49: 47,
            # Row 3: subtract 3
            51: 48, 52: 49, 53: 50, 54: 51,
        }
        return translation.get(note, note)

    def _on_track_changed(self):
        """Called when track selection changes - auto-detect drum rack"""
        try:
            self._auto_switch_mode()
        except Exception as e:
            self.log_message(f"Error in track change handler: {e}")

    def _auto_switch_mode(self):
        """Automatically switch to Drum Mode if drum rack detected"""
        try:
            track = self.song().view.selected_track

            # Check if track has a drum rack
            if hasattr(track, 'devices'):
                for device in track.devices:
                    if device.class_name == 'DrumGroupDevice':
                        self.log_message(f"Drum rack detected: {device.name} - auto-switching to Drum Mode")
                        self._switch_to_mode(MODE_DRUM)
                        return

            # No drum rack found - switch to keyboard mode if currently in drum mode
            if self._current_mode_index == MODE_DRUM:
                self.log_message("No drum rack - auto-switching to Keyboard Mode")
                self._switch_to_mode(MODE_KEYBOARD)

        except Exception as e:
            self.log_message(f"Error in auto mode switch: {e}")

    def _translate_to_chromatic(self, note):
        """
        Translate LinnStrument note (with row_offset=5) to chromatic for drum rack

        The LinnStrument grid (row_offset=5):
        Row 0: 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51
        Row 1: 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56
        Row 2: 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61
        Row 3: 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66

        We want to map the 4x4 grid to chromatic: 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51

        Args:
            note: Incoming MIDI note from LinnStrument

        Returns:
            Chromatic note number for drum rack, or None if not in drum pad area
        """
        try:
            # Get position on grid
            positions = self.linnstrument.get_position_for_note(note)
            if not positions:
                return None

            column, row = positions[0]

            # Only translate drum pad area (bottom 4 rows, 4 columns)
            if row < 4 and column < 4:
                # Map to chromatic: row * 4 + column
                chromatic_index = row * 4 + column
                chromatic_note = 36 + chromatic_index
                return chromatic_note

            # Not in drum pad area - don't translate
            return None

        except Exception as e:
            self.log_message(f"Error translating note {note}: {e}")
            return None

    def build_midi_map(self, midi_map_handle):
        """Build MIDI map to receive MIDI from LinnStrument"""
        try:
            import Live

            script_handle = self._c_instance.handle()

            # Forward mode switch CC
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle,
                                        MODE_SWITCH_CHANNEL, MODE_SWITCH_CC)
            self.log_message(f"Forwarding CC{MODE_SWITCH_CC} (mode switch) to receive_midi")
            self.log_message("All notes pass through to track")

        except Exception as e:
            self.log_message(f"Error building MIDI map: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def receive_midi(self, midi_bytes):
        """
        Receive MIDI and route to active mode

        Args:
            midi_bytes: Tuple of MIDI bytes (status, data1, data2)
        """
        try:
            if len(midi_bytes) < 3:
                return

            status = midi_bytes[0]
            data1 = midi_bytes[1]
            data2 = midi_bytes[2]

            # Check for mode switch CC
            if 0xB0 <= status <= 0xBF:  # Control Change
                channel = status & 0x0F
                cc_number = data1
                value = data2

                if channel == MODE_SWITCH_CHANNEL and cc_number == MODE_SWITCH_CC:
                    # Mode switch button pressed (only trigger on value > 0)
                    if value > 0:
                        self.log_message(f"Mode switch CC received (CC{cc_number}={value})")
                        self._cycle_mode()
                    return

                # Pass CC to active mode
                if self._active_mode and hasattr(self._active_mode, 'handle_cc'):
                    if self._active_mode.handle_cc(cc_number, value):
                        return  # Mode handled it

            # Check for note on/off
            elif 0x80 <= status <= 0x9F:  # Note On or Note Off
                channel = status & 0x0F
                note = data1
                velocity = data2

                # Determine if note on or off
                is_note_on = (status & 0xF0) == 0x90 and velocity > 0

                # Debug: log all notes in drum mode
                if self._current_mode_index == MODE_DRUM and is_note_on:
                    # Calculate which row/column this note is on
                    positions = self.linnstrument.get_position_for_note(note)
                    if positions:
                        col, row = positions[0]
                        self.log_message(f"receive_midi: note={note} row={row} col={col} vel={velocity}")
                    else:
                        self.log_message(f"receive_midi: note={note} (unknown position) vel={velocity}")

                # Pass to active mode
                if self._active_mode and hasattr(self._active_mode, 'handle_note'):
                    self._active_mode.handle_note(note, velocity, is_note_on)

        except Exception as e:
            self.log_message(f"Error in receive_midi: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def update_display(self):
        """
        Called periodically by Ableton
        Update active mode
        """
        try:
            if self._active_mode:
                self._active_mode.update()
        except Exception as e:
            self.log_message(f"Error in update_display: {e}")
