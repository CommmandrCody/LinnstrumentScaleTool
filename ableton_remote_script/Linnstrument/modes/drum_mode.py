"""
Drum Mode - Push-style 4x4 drum pad grid
Bottom 4 rows: 4x4 drum pad matrix (16 pads) matching Push layout
Top 4 rows: Reserved for future sequencer
"""

from .base_mode import BaseMode
from ..config import (
    DRUM_PAD_ROWS,
    DRUM_PAD_COLUMNS
)
import Live


class DrumMode(BaseMode):
    """
    Push-style drum pad mode
    - Bottom 4 rows (0-3): 4x4 drum pad grid (notes 36-51 like Push)
    - Row offset = 4 semitones (chromatic blocks: 36-39, 40-43, 44-47, 48-51)
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        super().__init__(c_instance, linnstrument, led_manager, song)

        # Drum rack reference
        self._drum_rack = None
        self._drum_rack_device = None

        # Pad selection (0-15)
        self._selected_pad = 0

    def _send_nrpn(self, nrpn_number, value):
        """
        Send complete NRPN message to LinnStrument

        Args:
            nrpn_number: NRPN parameter number (0-16383)
            value: Parameter value (0-16383)
        """
        # Split NRPN number into MSB and LSB
        nrpn_msb = (nrpn_number >> 7) & 0x7F
        nrpn_lsb = nrpn_number & 0x7F

        # Split value into MSB and LSB
        value_msb = (value >> 7) & 0x7F
        value_lsb = value & 0x7F

        # CC status byte (0xB0 = CC on channel 1)
        status = 0xB0

        # Send complete NRPN sequence (6 messages required!)
        self.linnstrument.send_midi([status, 99, nrpn_msb])   # CC 99: NRPN MSB
        self.linnstrument.send_midi([status, 98, nrpn_lsb])   # CC 98: NRPN LSB
        self.linnstrument.send_midi([status, 6, value_msb])   # CC 6: Data MSB
        self.linnstrument.send_midi([status, 38, value_lsb])  # CC 38: Data LSB
        self.linnstrument.send_midi([status, 101, 127])       # CC 101: RPN reset MSB
        self.linnstrument.send_midi([status, 100, 127])       # CC 100: RPN reset LSB

        self.log_message(f"Sent NRPN {nrpn_number}={value} (complete 6-message sequence)")

    def enter(self):
        """Enter drum mode"""
        try:
            super().enter()
            self.log_message("=== DRUM MODE ACTIVATED ===")

            # Set LinnStrument to row_offset=4 (4 semitones per row for Push layout)
            # This gives us: Row 0=36-39, Row 1=40-43, Row 2=44-47, Row 3=48-51
            self.log_message("Setting row offset to 4 (Push layout) via NRPN 227...")
            self._send_nrpn(227, 4)  # NRPN 227 = Global Row Offset, value 4 = 4 semitones/row

            # Update our internal row_offset so position calculations work correctly
            self.linnstrument.row_offset = 4
            self.log_message(f"Row offset set to 4 (internal value updated)")

            # Find drum rack on selected track
            self._find_drum_rack()

            # Add listener for track changes
            self._add_listener(self.song.view, 'add_selected_track_listener', self._on_track_changed)

            # Force clear all LEDs
            self.log_message("Clearing all LEDs...")
            self.led_manager.clear_all(force=True)

            # Initial display - light up the 4x4 drum pad grid
            self.log_message("Lighting up drum pads...")
            self.update_leds()
            self.log_message("Drum mode ready")
            self.show_message("Linnstrument: Drum Mode (Push Layout)")
        except Exception as e:
            self.log_message(f"ERROR in drum mode enter: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def exit(self):
        """Exit drum mode"""
        # Restore row offset to 5 (default scale mode)
        self.log_message("Restoring row offset to 5 (scale mode) via NRPN 227...")
        self._send_nrpn(227, 5)  # NRPN 227 = Global Row Offset, value 5 = default

        # Restore our internal row_offset
        self.linnstrument.row_offset = 5
        self.log_message(f"Row offset restored to 5 via NRPN (internal value updated: {self.linnstrument.row_offset})")

        super().exit()
        self.led_manager.clear_all()

    def build_midi_map(self, midi_map_handle):
        """
        Build MIDI map for drum mode - let notes pass through naturally
        """
        try:
            # Don't forward or map anything - let all notes pass through to track
            # The track is already receiving from LinnStrument
            self.log_message("Drum mode: Notes pass through naturally to track")

        except Exception as e:
            self.log_message(f"Error building drum mode MIDI map: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def _on_track_changed(self):
        """Track changed - find new drum rack"""
        self.log_message("Track changed - updating drum rack")
        self._find_drum_rack()
        self.update_leds()

    def _find_drum_rack(self):
        """Find drum rack on selected track"""
        try:
            track = self.song.view.selected_track
            self.log_message(f"Looking for drum rack on track: {track.name}")

            # Check if it's a MIDI track
            if not hasattr(track, 'devices'):
                self._drum_rack = None
                self._drum_rack_device = None
                self.log_message("Selected track has no devices")
                return

            # Find first drum rack
            self.log_message(f"Track has {len(track.devices)} devices")
            for device in track.devices:
                self.log_message(f"  Device: {device.name} (class: {device.class_name})")
                if device.class_name == 'DrumGroupDevice':
                    self._drum_rack_device = device
                    self._drum_rack = device
                    self.log_message(f"Found drum rack: {device.name}")

                    # Debug drum pads - check which ones have samples
                    if hasattr(device, 'drum_pads'):
                        self.log_message(f"  Drum rack has {len(device.drum_pads)} pads")
                        loaded_pads = []
                        for i in range(len(device.drum_pads)):
                            pad = device.drum_pads[i]
                            has_chains = hasattr(pad, 'chains') and len(pad.chains) > 0
                            if has_chains:
                                loaded_pads.append(i)
                        self.log_message(f"  Loaded pads (indices with samples): {loaded_pads}")
                        self.log_message(f"  Total loaded: {len(loaded_pads)}")
                    return

            self._drum_rack = None
            self._drum_rack_device = None
            self.log_message("No drum rack found on track")

        except Exception as e:
            self.log_message(f"Error finding drum rack: {e}")
            import traceback
            self.log_message(traceback.format_exc())
            self._drum_rack = None
            self._drum_rack_device = None

    def update_leds(self):
        """Update drum pad LED display - simple 4x4 grid"""
        try:
            self.log_message("=== UPDATING DRUM PAD LEDS ===")

            # Clear all LEDs first
            self.led_manager.clear_all()

            # Light up 4x4 drum pad grid (rows 0-3, columns 0-3)
            for row in range(DRUM_PAD_ROWS):
                for col in range(DRUM_PAD_COLUMNS):
                    # Calculate pad index (0-15)
                    pad_index = row * DRUM_PAD_COLUMNS + col

                    # Get color for this pad
                    color = self._get_drum_pad_color(pad_index)

                    self.log_message(f"  Setting LED ({col},{row}) pad={pad_index} color={color}")
                    self.led_manager.set_led(col, row, color)

            self.log_message("Drum pad LED update complete")

        except Exception as e:
            self.log_message(f"Error updating drum mode LEDs: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def _get_drum_pad_color(self, pad_index):
        """
        Get color for a drum pad

        Args:
            pad_index: Pad index (0-15)

        Returns:
            Color name
        """
        # Highlight selected pad in white
        if pad_index == self._selected_pad:
            return 'white'

        # Map pad index to MIDI note (36-51)
        drum_rack_note = 36 + pad_index

        # If drum rack exists, check if this note has a sample
        if self._drum_rack and hasattr(self._drum_rack, 'drum_pads'):
            try:
                # Drum rack pads array is indexed by MIDI note (0-127)
                if drum_rack_note < len(self._drum_rack.drum_pads):
                    drum_pad = self._drum_rack.drum_pads[drum_rack_note]

                    # Check if pad has chains (samples loaded)
                    has_sample = hasattr(drum_pad, 'chains') and len(drum_pad.chains) > 0

                    if has_sample:
                        # Has sample - show as green
                        return 'green'

            except Exception as e:
                self.log_message(f"Error checking pad {pad_index} (note {drum_rack_note}): {e}")

        # No sample or no drum rack - show dim blue so pads are visible
        return 'blue'

    def handle_note(self, note, velocity, is_note_on):
        """
        Handle drum pad input - select pad and let notes pass through

        Args:
            note: MIDI note number
            velocity: Note velocity
            is_note_on: True for note on, False for note off

        Returns:
            False (let notes pass through to track)
        """
        # Only process note-on events for pad selection
        if not is_note_on:
            return False

        try:
            # Get grid position(s) for this note
            positions = self.get_grid_position(note)
            if not positions:
                return False  # Not in our grid, pass through

            # With row_offset=4, each note should appear at unique position in 4x4 grid
            # But may appear at multiple positions if grid extends beyond column 3
            # Prefer the leftmost position (lowest column)
            positions_sorted = sorted(positions, key=lambda p: (p[0], p[1]))  # Sort by column, then row
            column, row = positions_sorted[0]

            self.log_message(f"Note {note} at position ({column},{row}), velocity={velocity}")

            # Only handle drum pad area (rows 0-3, columns 0-3)
            if row < DRUM_PAD_ROWS and column < DRUM_PAD_COLUMNS:
                # Calculate pad index (0-15)
                pad_index = row * DRUM_PAD_COLUMNS + column

                # Update selection if different
                if pad_index != self._selected_pad:
                    old_selected = self._selected_pad
                    self._selected_pad = pad_index
                    self.log_message(f"Selected pad {pad_index} (was {old_selected})")

                    # Update only the two affected pads to save MIDI bandwidth
                    self._update_single_pad_led(old_selected)
                    self._update_single_pad_led(pad_index)

                # Let note pass through to drum rack
                return False

        except Exception as e:
            self.log_message(f"Error handling drum pad note: {e}")
            import traceback
            self.log_message(traceback.format_exc())

        return False  # Pass through by default

    def _update_single_pad_led(self, pad_index):
        """Update LED for a single pad"""
        if pad_index < 0 or pad_index >= 16:
            return

        row = pad_index // DRUM_PAD_COLUMNS
        col = pad_index % DRUM_PAD_COLUMNS
        color = self._get_drum_pad_color(pad_index)

        self.led_manager.set_led(col, row, color)
        self.log_message(f"Updated pad {pad_index} LED to {color}")

    def update(self):
        """Per-frame update for drum mode"""
        pass
