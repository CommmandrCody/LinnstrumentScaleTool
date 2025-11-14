"""
Drum Mode - Drum rack + step sequencer
Bottom 4 rows: 4x4 drum pad matrix (16 pads) - standard drum rack layout
Top 4 rows: 16-step sequencer (4 drum sounds visible at once)
"""

from .base_mode import BaseMode
from ..config import (
    DRUM_PAD_ROWS,
    DRUM_PAD_COLUMNS,
    DRUM_PAD_EXTENDED_COLUMNS,
    SEQUENCER_ROWS,
    SEQUENCER_STEPS
)
import Live


class DrumMode(BaseMode):
    """
    Drum mode with integrated step sequencer
    - Bottom 4 rows (0-3): 4x4 drum pad grid (like Push)
    - Top 4 rows (4-7): 16-step sequencer (4 sounds visible at once)
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        super().__init__(c_instance, linnstrument, led_manager, song)

        # Drum rack reference
        self._drum_rack = None
        self._drum_rack_device = None

        # Pad selection
        self._selected_pad = 0  # 0-63

        # Sequencer state - 64 pads x 16 steps
        # Format: _sequences[pad_index][step_index] = velocity (0 = off, 1-127 = on)
        self._sequences = [[0 for _ in range(SEQUENCER_STEPS)] for _ in range(64)]

        # Playback state
        self._is_playing = False
        self._current_step = 0
        self._last_song_time = 0

        # Quantization (16th notes)
        self._step_length = 0.25  # Quarter note / 4 = 16th note

        # Initialize duplicate map variables
        # Will be built in _build_duplicate_map() after row_offset is set correctly
        self._note_to_first_position = {}
        self._allowed_positions = set()

        # Build initial duplicate map (will be wrong until enter() sets row_offset=4)
        self._build_duplicate_map()

    def _build_duplicate_map(self):
        """
        Build map of which grid positions to allow (prevent duplicates)

        This must be called AFTER row_offset is set correctly, otherwise the map will be wrong.
        With row_offset=5 (fifths layout), notes appear at multiple positions.
        With row_offset=4 (chromatic), each note appears at exactly one position in the 4x4 grid.
        """
        # Clear existing maps
        self._note_to_first_position = {}
        self._allowed_positions = set()

        # Build map: key=MIDI note, value=first (col, row) that produces it
        for row in range(DRUM_PAD_ROWS):
            for col in range(DRUM_PAD_EXTENDED_COLUMNS):
                note = self.linnstrument.base_note + (col * self.linnstrument.column_offset) + (row * self.linnstrument.row_offset)
                if note not in self._note_to_first_position:
                    self._note_to_first_position[note] = (col, row)
                    self._allowed_positions.add((col, row))

        # Manual overrides - shouldn't be needed if duplicate detection works
        # But adding for safety
        manual_blocks = [
            # (7, 0),  # Example: block row 0 col 7 if needed
        ]
        for pos in manual_blocks:
            if pos in self._allowed_positions:
                self._allowed_positions.remove(pos)
                self.log_message(f"Manually blocked position: {pos}")

        self.log_message(f"Built duplicate map: {len(self._allowed_positions)} unique positions out of {DRUM_PAD_ROWS * DRUM_PAD_EXTENDED_COLUMNS} total")

        # Debug: show which positions are duplicates
        blocked_positions = []
        for row in range(DRUM_PAD_ROWS):
            for col in range(DRUM_PAD_EXTENDED_COLUMNS):
                if (col, row) not in self._allowed_positions:
                    note = self.linnstrument.base_note + (col * self.linnstrument.column_offset) + (row * self.linnstrument.row_offset)
                    blocked_positions.append(f"({col},{row})=note{note}")
        if blocked_positions:
            self.log_message(f"BLOCKED duplicate positions: {blocked_positions}")

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

            # Set LinnStrument to row_offset=4 (chromatic) via NRPN
            self.log_message("Setting row offset to 4 (chromatic) via NRPN 227...")
            self._send_nrpn(227, 4)  # NRPN 227 = Global Row Offset, value 4 = chromatic

            # Update our internal row_offset so position calculations work correctly
            self.linnstrument.row_offset = 4
            self.log_message(f"Row offset set to 4 via NRPN (internal value updated: {self.linnstrument.row_offset})")

            # CRITICAL: Rebuild duplicate map NOW that row_offset is correct!
            # The map built in __init__() used row_offset=5 and is wrong
            self.log_message("Rebuilding duplicate map with row_offset=4...")
            self._build_duplicate_map()

            # Find drum rack on selected track
            self._find_drum_rack()

            # Add listeners
            self._add_listener(self.song.view, 'add_selected_track_listener', self._on_track_changed)
            self._add_listener(self.song, 'add_is_playing_listener', self._on_playback_changed)
            self._add_listener(self.song, 'add_current_song_time_listener', self._on_song_time_changed)

            # Add note listener to track for pad selection
            try:
                track = self.song.view.selected_track
                if hasattr(track, 'add_playing_notes_listener'):
                    self._add_listener(track, 'add_playing_notes_listener', self._on_note_played)
            except:
                pass

            # Force clear all LEDs with cache bypass
            self.log_message("Force clearing all LEDs...")
            self.led_manager.clear_all(force=True)

            # Initial display
            self.log_message("About to update LEDs...")
            self.update_leds()
            self.log_message("LED update complete")
            self.show_message("Linnstrument: Drum Mode")
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

    def _on_note_played(self):
        """Note played on track - update pad selection"""
        try:
            track = self.song.view.selected_track
            if hasattr(track, 'playing_notes'):
                notes = track.playing_notes
                if notes and len(notes) > 0:
                    # Get most recent note
                    note = notes[-1][0] if isinstance(notes[-1], tuple) else notes[-1]

                    # Convert note to pad index (note 36 = pad 0, note 51 = pad 15)
                    if note >= 36 and note <= 51:
                        pad_index = note - 36
                        if pad_index < 16:  # Only first 16 pads (4x4)
                            old_selected = self._selected_pad
                            self._selected_pad = pad_index
                            self.log_message(f"Note listener: selected pad {pad_index} from note {note}")
                            if old_selected != self._selected_pad:
                                self._update_drum_pad_leds()
                                self._update_sequencer_leds()
        except Exception as e:
            self.log_message(f"Error in note listener: {e}")

    def _on_track_changed(self):
        """Track changed - find new drum rack"""
        self.log_message("Track changed")
        self._find_drum_rack()
        self.update_leds()

    def _on_playback_changed(self):
        """Playback started/stopped"""
        self._is_playing = self.song.is_playing
        self.log_message(f"Playback: {'playing' if self._is_playing else 'stopped'}")

        if self._is_playing:
            self._last_song_time = self.song.current_song_time
        else:
            self._current_step = 0

        self.update_leds()

    def _on_song_time_changed(self):
        """Song position changed - update sequencer playhead"""
        if not self._is_playing:
            return

        # Calculate current step based on song time
        current_time = self.song.current_song_time
        beats = current_time  # Song time is in beats

        # Calculate which 16th note step we're on
        step = int((beats % (SEQUENCER_STEPS * self._step_length)) / self._step_length)

        if step != self._current_step:
            old_step = self._current_step
            self._current_step = step

            # Trigger notes for this step
            self._trigger_step(step)

            # Update LEDs for playhead movement (only update changed rows)
            self._update_playhead_leds(old_step, step)

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
        """Update drum mode LED display"""
        try:
            # Clear all
            self.led_manager.clear_all()

            # Update drum pads (bottom 4 rows)
            self._update_drum_pad_leds()

            # Update sequencer (top 4 rows)
            self._update_sequencer_leds()

        except Exception as e:
            self.log_message(f"Error updating drum mode LEDs: {e}")

    def _update_drum_pad_leds(self):
        """Update drum pad LED colors - 4x4 grid LIKE PUSH"""
        # Simple 4x4 grid showing pads 0-15 (notes 36-51)
        # Just like Push - no extended columns, just 4x4

        for row in range(DRUM_PAD_ROWS):
            for col in range(DRUM_PAD_COLUMNS):  # Only 4 columns like Push
                # Simple mapping: pad_index = row * 4 + col
                pad_index = row * 4 + col

                # Get color based on whether this pad has a sample
                color = self._get_drum_pad_color(pad_index)
                self.led_manager.set_led(col, row, color)

        # Turn off columns 4-15 (we only use 4x4 like Push)
        for row in range(DRUM_PAD_ROWS):
            for col in range(4, 16):
                self.led_manager.set_led(col, row, 'off')

    def _get_drum_pad_color(self, pad_index):
        """
        Get color for a drum pad

        Args:
            pad_index: Pad index (0-63) in expanded grid

        Returns:
            Color name
        """
        # Map pad index directly to drum rack note
        drum_rack_note = 36 + pad_index

        # Highlight selected pad
        if pad_index == self._selected_pad:
            return 'white'

        # If drum rack exists, check if this MIDI note has a sample
        if self._drum_rack:
            try:
                drum_pads = self._drum_rack.drum_pads

                # Drum rack pads array is indexed by MIDI note (0-127)
                if drum_rack_note < len(drum_pads):
                    drum_pad = drum_pads[drum_rack_note]

                    # Check if pad has a sample
                    if hasattr(drum_pad, 'chains') and len(drum_pad.chains) > 0:
                        # Has sample - show as green (will add track color later)
                        return 'green'

            except Exception as e:
                self.log_message(f"Error getting drum pad {pad_index} color: {e}")

        # No sample - hide it
        return 'off'

    def _update_sequencer_leds(self):
        """Update sequencer LED display - show selected pad's sequence (LIKE PUSH)"""
        # All 4 sequencer rows show the SAME pad's 16-step sequence
        # This is exactly how Push works - select a pad, see its pattern

        sequence = self._sequences[self._selected_pad]

        for step in range(SEQUENCER_STEPS):
            color = self._get_sequencer_step_color(step, sequence[step], self._selected_pad)

            # Show the same sequence on all 4 rows (like Push does)
            for seq_row in range(4, 8):
                self.led_manager.set_led(step, seq_row, color)

    def _get_sequencer_step_color(self, step, velocity, pad_index=None):
        """
        Get color for a sequencer step

        Args:
            step: Step index (0-15)
            velocity: Step velocity (0 = off, 1-127 = on)
            pad_index: Which drum pad (optional, for multi-row display)

        Returns:
            Color name
        """
        is_active = velocity > 0
        is_current_step = (step == self._current_step and self._is_playing)
        is_selected_pad = (pad_index == self._selected_pad) if pad_index is not None else True

        if is_current_step and is_active:
            return 'white'  # Playing step - bright
        elif is_current_step:
            return 'yellow'  # Playhead on empty step
        elif is_active:
            # Show active steps differently for selected vs unselected pads
            return 'green' if is_selected_pad else 'cyan'
        else:
            # No background - all rows dark when empty
            return 'off'

    def _update_playhead_leds(self, old_step, new_step):
        """
        Update only the changed sequencer LEDs for playhead movement

        Args:
            old_step: Previous step position
            new_step: New step position
        """
        # Update all 4 visible rows for playhead movement
        start_pad = (self._selected_pad // 4) * 4

        for row_offset in range(4):
            pad_index = start_pad + row_offset
            if pad_index >= 64:
                continue

            sequence = self._sequences[pad_index]
            linnstrument_row = 7 - row_offset

            # Update old step
            color_old = self._get_sequencer_step_color(old_step, sequence[old_step], pad_index)
            self.led_manager.set_led(old_step, linnstrument_row, color_old)

            # Update new step
            color_new = self._get_sequencer_step_color(new_step, sequence[new_step], pad_index)
            self.led_manager.set_led(new_step, linnstrument_row, color_new)

    def handle_note(self, note, velocity, is_note_on):
        """
        Handle drum pad and sequencer input - just update LEDs, let notes pass through

        Args:
            note: MIDI note number
            velocity: Note velocity
            is_note_on: True for note on, False for note off

        Returns:
            False (let notes pass through to track)
        """
        try:
            positions = self.get_grid_position(note)
            if not positions:
                return False  # Pass through

            # With chromatic layout (row_offset=4), notes can appear at multiple positions
            # e.g., note 40 at both (col=4, row=0) and (col=0, row=1)
            # Prefer the position with the lowest row (actual pad location)
            if len(positions) > 1:
                self.log_message(f"Note {note} found at multiple positions: {positions}")
            positions_sorted = sorted(positions, key=lambda p: (p[1], p[0]))  # Sort by row, then column
            column, row = positions_sorted[0]
            if len(positions) > 1:
                self.log_message(f"Selected position (row={row}, col={column}) from {len(positions)} options")

            # Check if in drum pad area (bottom 4 rows, ONLY 4 columns like Push)
            if row < DRUM_PAD_ROWS and column < DRUM_PAD_COLUMNS:
                if is_note_on:
                    # Select this pad when pressed
                    pad_index = row * 4 + column
                    if pad_index != self._selected_pad:
                        self._selected_pad = pad_index
                        self.log_message(f"Selected drum pad {pad_index} (row={row}, col={column})")
                        # Update sequencer to show this pad's sequence
                        self._update_sequencer_leds()
                        # Update drum pad LEDs to show selection
                        self._update_drum_pad_leds()

                # Re-send the note to the track so it plays
                # (forwarded notes are intercepted, so we must re-send them)
                status = 0x90 if is_note_on else 0x80  # Note on/off, channel 1
                self.linnstrument.send_midi([status, note, velocity])
                return True  # We handled it (by re-sending)

            # Check if in sequencer area (rows 4-7)
            elif row >= DRUM_PAD_ROWS:
                self.log_message(f"Sequencer press: col={column}, row={row}")
                if is_note_on:
                    self._handle_sequencer_press(column, row)
                return True  # Intercept sequencer presses

        except Exception as e:
            self.log_message(f"Error handling drum mode note: {e}")
            import traceback
            self.log_message(traceback.format_exc())

        return False  # Pass through by default

    def _handle_sequencer_press(self, column, row):
        """
        Handle sequencer step toggle (LIKE PUSH)

        Args:
            column, row: Grid position (any of rows 4-7 toggles the same step)
        """
        # Column = step (0-15)
        step = column

        if step >= SEQUENCER_STEPS:
            return

        # All sequencer rows edit the SELECTED pad (like Push)
        pad_index = self._selected_pad

        # Toggle step for the selected pad
        sequence = self._sequences[pad_index]
        if sequence[step] > 0:
            # Turn off
            sequence[step] = 0
            self.log_message(f"Step {step} OFF for pad {pad_index}")
        else:
            # Turn on with default velocity
            sequence[step] = 100
            self.log_message(f"Step {step} ON for pad {pad_index}")

        # Update the actual clip with this note
        self._update_clip_notes(pad_index, step, sequence[step])

        # Update ALL sequencer rows (they all show the same thing)
        self._update_sequencer_leds()

    def _update_clip_notes(self, pad_index, step, velocity):
        """
        Add or remove a note in the active MIDI clip

        Args:
            pad_index: Drum pad index (0-15 for first 16 pads)
            step: Step index (0-15)
            velocity: Note velocity (0 = remove, >0 = add)
        """
        try:
            # Get the selected track's clip slot
            track = self.song.view.selected_track
            if not track or not hasattr(track, 'playing_slot_index'):
                self.log_message("No track selected")
                return

            # Get the currently playing or selected clip slot
            slot_index = track.playing_slot_index
            if slot_index < 0:
                # Not playing, try to find first clip
                for i, slot in enumerate(track.clip_slots):
                    if slot.has_clip:
                        slot_index = i
                        break

            if slot_index < 0:
                self.log_message("No clip found - create a MIDI clip first")
                return

            clip_slot = track.clip_slots[slot_index]
            if not clip_slot.has_clip:
                self.log_message(f"Clip slot {slot_index} is empty")
                return

            clip = clip_slot.clip
            if not clip.is_midi_clip:
                self.log_message("Not a MIDI clip")
                return

            # Calculate the MIDI note for this drum pad (chromatic, starting at 36)
            midi_note = 36 + pad_index

            # Calculate time position based on step
            # Assume 16 steps per bar, 4 beats per bar = 0.25 beats per step
            step_time = step * 0.25
            note_length = 0.25

            # Get existing notes for this pitch
            notes = clip.get_notes(step_time, midi_note, note_length, 1)

            if velocity > 0:
                # Add note
                if len(notes) == 0:
                    # No existing note - add new one
                    clip.add_new_notes(((midi_note, step_time, note_length, velocity, False),))
                    self.log_message(f"Added note: pad={pad_index} note={midi_note} step={step} time={step_time}")
                else:
                    # Note already exists - update velocity
                    note_data = notes[0]
                    clip.remove_notes(step_time, midi_note, note_length, 1)
                    clip.add_new_notes(((midi_note, step_time, note_length, velocity, False),))
                    self.log_message(f"Updated note: pad={pad_index} note={midi_note} step={step}")
            else:
                # Remove note
                if len(notes) > 0:
                    clip.remove_notes(step_time, midi_note, note_length, 1)
                    self.log_message(f"Removed note: pad={pad_index} note={midi_note} step={step} time={step_time}")

        except Exception as e:
            self.log_message(f"Error updating clip notes: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def _trigger_drum_pad(self, pad_index, velocity):
        """
        Trigger a drum pad sound (for sequencer playback)

        Args:
            pad_index: Pad index (0-63)
            velocity: Note velocity
        """
        try:
            # Drum pads start at MIDI note 36
            drum_note = 36 + pad_index

            # Send MIDI note directly
            status = 0x90  # Note on, channel 1
            self.c_instance.send_midi((status, drum_note, velocity))

        except Exception as e:
            self.log_message(f"Error triggering drum pad {pad_index}: {e}")

    def _trigger_step(self, step):
        """
        Trigger all active pads for a given step

        Args:
            step: Step index (0-15)
        """
        try:
            for pad_index in range(64):
                velocity = self._sequences[pad_index][step]
                if velocity > 0:
                    self._trigger_drum_pad(pad_index, velocity)

        except Exception as e:
            self.log_message(f"Error triggering step {step}: {e}")

    def clear_sequence(self, pad_index=None):
        """
        Clear sequence for a pad (or current selected pad)

        Args:
            pad_index: Pad to clear, or None for currently selected
        """
        if pad_index is None:
            pad_index = self._selected_pad

        self._sequences[pad_index] = [0] * SEQUENCER_STEPS
        self.log_message(f"Cleared sequence for pad {pad_index}")
        self._update_sequencer_leds()

    def update(self):
        """Per-frame update for drum mode"""
        # Sequencer updates happen via song time listener
        pass
