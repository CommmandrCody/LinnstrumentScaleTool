"""
Drum Mode - Push-style drum sequencer
Bottom 4 rows (0-3): 4x4 drum pad grid (16 pads)
Top 4 rows (4-7): 8-step sequencer for selected pad (4 rows x 8 columns)
"""

from .base_mode import BaseMode
from ..config import (
    DRUM_PAD_ROWS,
    DRUM_PAD_COLUMNS,
    SEQUENCER_ROWS,
    SEQUENCER_COLUMNS,
    SEQUENCER_STEPS
)
import Live


class DrumMode(BaseMode):
    """
    Push-style drum sequencer
    - Bottom: 4x4 drum pads (16 pads)
    - Top: 4x8 sequencer grid (8 steps, displayed across 4 rows)
    - Select pad = white, sequence steps = cyan, playhead = yellow VERTICAL BAR
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        super().__init__(c_instance, linnstrument, led_manager, song)

        # Selected pad (0-15)
        self._selected_pad = 0

        # Sequences: 16 pads x 8 steps
        # _sequences[pad_index][step_index] = velocity (0 = off, 1-127 = on)
        self._sequences = [[0 for _ in range(SEQUENCER_STEPS)] for _ in range(16)]

        # Playback
        self._is_playing = False
        self._current_step = 0

        # Step length (16th notes)
        self._step_length = 0.25

    def enter(self):
        """Enter drum mode"""
        super().enter()

        # Add listeners
        self._add_listener(self.song, 'add_is_playing_listener', self._on_playback_changed)
        self._add_listener(self.song, 'add_current_song_time_listener', self._on_song_time_changed)

        # Initial display
        self.update_leds()
        self.show_message("Linnstrument: Drum Mode (Push-style)")

    def exit(self):
        """Exit drum mode"""
        super().exit()
        self.led_manager.clear_all()

    def _on_playback_changed(self):
        """Playback started/stopped"""
        self._is_playing = self.song.is_playing

        if not self._is_playing:
            self._current_step = 0

        self.update_leds()

    def _on_song_time_changed(self):
        """Update sequencer playhead"""
        if not self._is_playing:
            return

        # Calculate current step (16th notes)
        beats = self.song.current_song_time
        step = int((beats % (SEQUENCER_STEPS * self._step_length)) / self._step_length)

        if step != self._current_step:
            old_step = self._current_step
            self._current_step = step

            # Trigger notes for this step
            self._trigger_step(step)

            # Update entire sequencer display (old and new columns)
            self._update_sequencer_column(old_step)
            self._update_sequencer_column(step)

    def update_leds(self):
        """Update all LEDs"""
        self.led_manager.clear_all()

        # Drum pads (rows 0-3)
        for row in range(DRUM_PAD_ROWS):
            for col in range(DRUM_PAD_COLUMNS):
                pad_index = (row * DRUM_PAD_COLUMNS) + col
                color = 'white' if pad_index == self._selected_pad else 'blue'
                self.led_manager.set_led(col, row, color)

        # Sequencer grid (rows 4-7, columns 0-7)
        for col in range(SEQUENCER_STEPS):
            self._update_sequencer_column(col)

    def _update_sequencer_column(self, step):
        """Update entire vertical column for a step (all 4 sequencer rows)"""
        if step >= SEQUENCER_STEPS:
            return

        sequence = self._sequences[self._selected_pad]
        velocity = sequence[step]

        # Determine if this step is active
        is_active = velocity > 0
        is_playhead = (step == self._current_step and self._is_playing)

        # Set color for entire column
        if is_playhead:
            color = 'yellow'  # Playhead - entire column lights up yellow
        elif is_active:
            color = 'cyan'  # Active step - entire column lights up cyan
        else:
            color = 'off'  # Inactive - entire column is off

        # Light up all 4 rows for this step column
        for seq_row in range(4):  # 4 sequencer rows
            actual_row = SEQUENCER_ROWS + seq_row  # Rows 4-7
            self.led_manager.set_led(step, actual_row, color)

    def handle_note(self, note, velocity, is_note_on):
        """Handle pad presses"""
        if not is_note_on:
            return True

        positions = self.get_grid_position(note)
        if not positions:
            return True

        column, row = positions[0]

        # Bottom 4 rows = drum pads
        if row < DRUM_PAD_ROWS:
            self._handle_drum_pad(column, row, velocity)
        # Top 4 rows = sequencer
        elif row >= SEQUENCER_ROWS:
            self._handle_sequencer_pad(column, row)

        return True

    def _handle_drum_pad(self, column, row, velocity):
        """Handle drum pad press - select pad and trigger sound"""
        pad_index = (row * DRUM_PAD_COLUMNS) + column

        if pad_index >= 16:
            return

        # Update selection
        old_pad = self._selected_pad
        self._selected_pad = pad_index

        self.log_message(f"Selected pad {pad_index} at ({column}, {row})")

        # Update drum pad LEDs
        old_row = old_pad // DRUM_PAD_COLUMNS
        old_col = old_pad % DRUM_PAD_COLUMNS
        self.led_manager.set_led(old_col, old_row, 'blue')
        self.led_manager.set_led(column, row, 'white')

        # Update entire sequencer display for new pad's sequence
        for step in range(SEQUENCER_STEPS):
            self._update_sequencer_column(step)

        # Trigger sound
        drum_note = 36 + pad_index
        self.c_instance.send_midi((0x90, drum_note, velocity))

    def _handle_sequencer_pad(self, column, row):
        """Handle sequencer step toggle - ANY row in sequencer area"""
        step = column  # Column directly maps to step (0-7)

        if step >= SEQUENCER_STEPS:
            return

        # Toggle step for selected pad
        sequence = self._sequences[self._selected_pad]
        if sequence[step] > 0:
            sequence[step] = 0
            self.log_message(f"Step {step} OFF for pad {self._selected_pad}")
        else:
            sequence[step] = 100
            self.log_message(f"Step {step} ON for pad {self._selected_pad}")

        # Update entire column for this step
        self._update_sequencer_column(step)

    def _trigger_step(self, step):
        """Trigger all active pads for current step"""
        for pad_index in range(16):
            velocity = self._sequences[pad_index][step]
            if velocity > 0:
                drum_note = 36 + pad_index
                self.c_instance.send_midi((0x90, drum_note, velocity))

    def update(self):
        """Per-frame update"""
        pass
