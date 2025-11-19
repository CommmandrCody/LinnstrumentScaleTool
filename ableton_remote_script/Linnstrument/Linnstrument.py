"""
LinnStrument Multi-Mode System
- Keyboard Mode: Scale lighting (row offset 5)
- Drum Mode: 4x4 drum grid + 16-step sequencer (Push-style)
- Auto-switches to drum mode when drum rack detected
- Sends NRPN to switch row offset: 5 for keyboard, 4 for drum
- Restores offset to 5 on disconnect
"""

from _Framework.ControlSurface import ControlSurface
import Live

try:
    from .config import LINNSTRUMENT_BASE_NOTE, LINNSTRUMENT_ROW_OFFSET, LINNSTRUMENT_COLUMN_OFFSET
    from .scales import NOTE_NAMES, get_scale_notes
    from .linnstrument_ableton import LinnstrumentAbletonMIDI
    from .led_manager import LEDManager
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)


# Ableton scale name mapping
ABLETON_SCALE_MAP = {
    'Major': 'major',
    'Minor': 'minor',
    'Dorian': 'dorian',
    'Mixolydian': 'mixolydian',
    'Lydian': 'lydian',
    'Phrygian': 'phrygian',
    'Locrian': 'locrian',
    'Diminished': 'diminished',
    'Whole Half': 'diminished',
    'Whole Tone': 'whole_tone',
    'Minor Blues': 'blues',
    'Minor Pentatonic': 'minor_pentatonic',
    'Major Pentatonic': 'major_pentatonic',
    'Harmonic Minor': 'harmonic_minor',
    'Melodic Minor': 'melodic_minor',
    'Super Locrian': 'altered',
}


class Linnstrument(ControlSurface):
    """Multi-mode system: Keyboard + Drum modes"""

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self.log_message("=" * 60)
        self.log_message("LinnStrument Multi-Mode System - Starting...")
        self.log_message("=" * 60)

        if not MODULES_AVAILABLE:
            self.log_message(f"ERROR: Could not import modules: {IMPORT_ERROR}")
            self.show_message("Linnstrument: Import Error")
            return

        # Initialize LinnStrument controller
        self.linnstrument = LinnstrumentAbletonMIDI(
            c_instance,
            base_note=LINNSTRUMENT_BASE_NOTE,
            row_offset=LINNSTRUMENT_ROW_OFFSET,  # 5 = fifths
            column_offset=LINNSTRUMENT_COLUMN_OFFSET
        )

        # Initialize LED manager
        self.led_manager = LEDManager(self.linnstrument, c_instance)

        # Mode state
        self._mode = 'keyboard'  # 'keyboard' or 'drum'

        # Octave control
        self._octave_offset = 0  # -5 to +5 (NRPN 36 values: 0-10, where 5=default)

        # Keyboard mode state
        self.current_root = None
        self.current_scale = None

        # Drum mode state
        self._drum_rack = None
        self._selected_pad = 0  # 0-15
        self._sequences = [[0 for _ in range(16)] for _ in range(16)]  # 16 pads x 16 steps
        self._is_playing = False
        self._current_step = 0
        self._needs_led_update = False

        # Add listeners
        self.song().add_root_note_listener(self._on_scale_changed)
        self.song().add_scale_name_listener(self._on_scale_changed)
        self.song().view.add_selected_track_listener(self._on_track_changed)
        self.log_message("Track change listener registered successfully")

        # DON'T enable User Firmware Mode - it changes note behavior!
        # LED control (CC 20/21/22) works without User Firmware Mode
        self.log_message("Using standard MIDI mode (User Firmware Mode disabled)")

        # Initial mode
        self._auto_switch_mode()

        self.log_message("Multi-Mode System Ready!")

    def disconnect(self):
        """Clean disconnect"""
        self.log_message("Multi-Mode System disconnecting...")

        # Restore row offset to 5 (fifths)
        self._send_nrpn(227, 5)
        self.log_message("Restored row offset to 5 (fifths)")

        # Restore octave to default (0)
        self._send_nrpn(36, 5)
        self.log_message("Restored octave to default (0)")

        # Remove listeners
        try:
            self.song().remove_root_note_listener(self._on_scale_changed)
            self.song().remove_scale_name_listener(self._on_scale_changed)
            self.song().view.remove_selected_track_listener(self._on_track_changed)
        except:
            pass

        ControlSurface.disconnect(self)

    def _send_nrpn(self, nrpn_number, value):
        """Send NRPN message to LinnStrument"""
        status = 0xB0  # CC on channel 1
        nrpn_msb = (nrpn_number >> 7) & 0x7F
        nrpn_lsb = nrpn_number & 0x7F
        value_msb = (value >> 7) & 0x7F
        value_lsb = value & 0x7F

        self._c_instance.send_midi((status, 99, nrpn_msb))
        self._c_instance.send_midi((status, 98, nrpn_lsb))
        self._c_instance.send_midi((status, 6, value_msb))
        self._c_instance.send_midi((status, 38, value_lsb))
        self._c_instance.send_midi((status, 101, 127))
        self._c_instance.send_midi((status, 100, 127))

    def _on_scale_changed(self):
        """Scale changed - update if in keyboard mode"""
        if self._mode == 'keyboard':
            self._update_keyboard_leds()

    def _on_track_changed(self):
        """Track changed - check if we should switch modes"""
        self.log_message("=== TRACK CHANGED - checking mode ===")
        self._auto_switch_mode()

    def _auto_switch_mode(self):
        """Auto-switch to drum mode if drum rack detected"""
        track = self.song().view.selected_track
        self.log_message(f"Auto-switch mode check: track={track.name}, current_mode={self._mode}")

        # Check for drum rack
        has_drum_rack = False
        if hasattr(track, 'devices'):
            for device in track.devices:
                if device.class_name == 'DrumGroupDevice':
                    has_drum_rack = True
                    self._drum_rack = device
                    break

        self.log_message(f"Has drum rack: {has_drum_rack}")

        # Switch mode
        if has_drum_rack and self._mode != 'drum':
            self.log_message("Drum rack detected - switching to Drum Mode")
            self._mode = 'drum'
            # Set row offset to 4 (major third = 4 semitones) for drum mode
            # This gives us a chromatic 4x4 grid
            self._send_nrpn(227, 4)
            self.linnstrument.row_offset = 4
            # DON'T change base_note or transpose - just light the correct pads
            # The hardware will send whatever notes it's configured to send
            self.log_message("Set row offset to 4 (chromatic grid)")
            self._update_drum_leds()
            self.show_message("Linnstrument: Drum Mode")
        elif not has_drum_rack and self._mode != 'keyboard':
            self.log_message("No drum rack - switching to Keyboard Mode")
            self._mode = 'keyboard'
            self._drum_rack = None
            # Restore row offset to 5 (fifths) for keyboard mode
            self._send_nrpn(227, 5)
            self.linnstrument.row_offset = 5
            # DON'T change base_note - it's already correct from initialization
            self.log_message("Restored row offset to 5 (fifths)")
            self._update_keyboard_leds()
            self.show_message("Linnstrument: Keyboard Mode")
        elif self._mode == 'drum':
            # Already in drum mode, just update LEDs
            self._update_drum_leds()
        elif self._mode == 'keyboard':
            # Already in keyboard mode, just update LEDs
            self._update_keyboard_leds()

    def _update_keyboard_leds(self):
        """Update LEDs for keyboard mode"""
        try:
            # ALWAYS clear ALL LEDs first when switching to keyboard mode
            self.led_manager.clear_all(force=True)

            # Get scale settings
            root = self.song().root_note
            scale_name = self.song().scale_name

            # ALWAYS update when switching modes (don't skip if scale unchanged)
            # if root == self.current_root and scale_name == self.current_scale:
            #     return

            self.current_root = root
            self.current_scale = scale_name

            # Map scale name
            our_scale_name = ABLETON_SCALE_MAP.get(
                scale_name,
                scale_name.lower().replace(' ', '_')
            )

            root_name = NOTE_NAMES[root]
            self.log_message(f"Displaying scale: {root_name} {scale_name}")

            # Get scale notes
            scale_notes = get_scale_notes(root, our_scale_name)

            # Light scale notes (already cleared above)
            # self.led_manager.clear_all()

            for note in scale_notes:
                positions = self.linnstrument.get_position_for_note(note)
                is_root = (note % 12) == root
                color = 'red' if is_root else 'blue'

                for column, row in positions:
                    self.led_manager.set_led(column, row, color)

        except Exception as e:
            self.log_message(f"Error updating keyboard LEDs: {e}")

    def _update_drum_leds(self):
        """Update LEDs for drum mode"""
        try:
            # Clear all
            self.led_manager.clear_all()

            # Log which pads have samples (first time only)
            if self._drum_rack and not hasattr(self, '_logged_drum_pads'):
                self._logged_drum_pads = True
                loaded_pads = []
                for i in range(16):
                    drum_note = 36 + i  # C2 = 36 (standard drum rack)
                    if drum_note < len(self._drum_rack.drum_pads):
                        drum_pad = self._drum_rack.drum_pads[drum_note]
                        if hasattr(drum_pad, 'chains') and len(drum_pad.chains) > 0:
                            loaded_pads.append(f"{i}(note{drum_note})")
                self.log_message(f"Drum pads with samples: {loaded_pads}")

            # Bottom 4 rows: 4x4 drum grid (pads 0-15, notes 36-51 = C2-D#3)
            for row in range(4):
                for col in range(4):
                    pad_index = row * 4 + col
                    color = self._get_drum_pad_color(pad_index)
                    self.led_manager.set_led(col, row, color)

            # Top 4 rows: 16-step sequencer (all rows show selected pad's sequence)
            sequence = self._sequences[self._selected_pad]
            for step in range(16):
                is_active = sequence[step] > 0
                is_current = (step == self._current_step and self._is_playing)

                if is_current and is_active:
                    color = 'white'  # Playing step
                elif is_current:
                    color = 'yellow'  # Playhead on empty
                elif is_active:
                    color = 'green'  # Active step
                else:
                    color = 'off'  # Empty

                # Show same sequence on all 4 rows (like Push)
                for seq_row in range(4, 8):
                    self.led_manager.set_led(step, seq_row, color)

        except Exception as e:
            self.log_message(f"Error updating drum LEDs: {e}")

    def _get_drum_pad_color(self, pad_index):
        """Get color for drum pad (0-15)"""
        # Highlight selected pad
        if pad_index == self._selected_pad:
            return 'white'

        # Check if pad has sample
        if self._drum_rack:
            try:
                drum_note = 36 + pad_index  # C2 = 36 (standard drum rack)
                if drum_note < len(self._drum_rack.drum_pads):
                    drum_pad = self._drum_rack.drum_pads[drum_note]
                    has_chains = hasattr(drum_pad, 'chains') and len(drum_pad.chains) > 0
                    if has_chains:
                        return 'green'  # Has sample
                    else:
                        return 'off'  # No sample
            except Exception as e:
                self.log_message(f"Error checking pad {pad_index} (note {drum_note}): {e}")

        return 'off'  # No drum rack or no sample


    def _shift_octave(self, direction):
        """Shift octave up (+1) or down (-1)"""
        # Update offset
        new_offset = self._octave_offset + direction

        # Clamp to valid range (-5 to +5)
        new_offset = max(-5, min(5, new_offset))

        if new_offset != self._octave_offset:
            self._octave_offset = new_offset

            # Convert to NRPN value (0-10, where 5=default)
            nrpn_value = new_offset + 5

            # Send NRPN to change octave
            self._send_nrpn(36, nrpn_value)

            # Show feedback
            sign = "+" if new_offset > 0 else ""
            self.show_message(f"Octave: {sign}{new_offset}")
            self.log_message(f"Octave shifted to {sign}{new_offset} (NRPN 36 = {nrpn_value})")

    def build_midi_map(self, midi_map_handle):
        """Forward switch CC messages so we can intercept them"""
        # Forward Switch 1 and Switch 2 CC messages (65 and 66)
        script_handle = self._c_instance.handle()
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, 0, 65)  # Switch 1
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, 0, 66)  # Switch 2
        # Notes pass directly to Ableton tracks

    def receive_midi(self, midi_bytes):
        """Handle MIDI input for octave switches"""
        if len(midi_bytes) < 3:
            return

        status = midi_bytes[0]
        data1 = midi_bytes[1]  # CC number or note
        data2 = midi_bytes[2]  # CC value or velocity

        # Check for CC messages (0xB0-0xBF)
        if 0xB0 <= status <= 0xBF:
            cc_num = data1
            cc_value = data2

            # Only respond to button press (value > 0)
            if cc_value > 0:
                # Switch 1 (left) = Octave Down (CC 65)
                if cc_num == 65:
                    self._shift_octave(-1)
                # Switch 2 (right) = Octave Up (CC 66)
                elif cc_num == 66:
                    self._shift_octave(+1)

    def update_display(self):
        """Called periodically - update LEDs if needed"""
        if self._needs_led_update:
            self._needs_led_update = False
            if self._mode == 'drum':
                self._update_drum_leds()
