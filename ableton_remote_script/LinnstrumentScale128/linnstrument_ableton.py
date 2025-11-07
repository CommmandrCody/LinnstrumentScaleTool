"""
Linnstrument control using only Ableton's MIDI API (no external dependencies)
"""

# Linnstrument 128: 16-column x 8-row grid
LINNSTRUMENT_COLUMNS = 16
LINNSTRUMENT_ROWS = 8

# Default tuning: each row is 5 semitones higher, columns are 1 semitone apart
DEFAULT_ROW_OFFSET = 5
DEFAULT_COLUMN_OFFSET = 1

# Linnstrument color palette
COLORS = {
    'default': 0,
    'red': 1,
    'yellow': 2,
    'green': 3,
    'cyan': 4,
    'blue': 5,
    'magenta': 6,
    'off': 7,
    'white': 8,
    'orange': 9,
    'lime': 10,
    'pink': 11,
}

class LinnstrumentAbletonMIDI:
    """
    Control Linnstrument using Ableton's MIDI API (no mido dependency)
    """

    def __init__(self, c_instance, channel=0, row_offset=None, column_offset=None, base_note=None):
        """
        Initialize Linnstrument controller

        Args:
            c_instance: Ableton ControlSurface instance
            channel: MIDI channel (0-15)
            row_offset: Semitones between rows (None = auto-detect)
            column_offset: Semitones between columns (None = auto-detect)
            base_note: MIDI note number at position (0, 0) (None = auto-detect)
        """
        self.c_instance = c_instance
        self.channel = channel

        # Auto-detect Linnstrument layout by calculating from known standard tunings
        # Linnstrument default factory settings:
        # - Row offset: 5 semitones (fourths)
        # - Lowest note (octave setting): varies, but column 0 row 0 plays a note
        # - Column offset: always 1 semitone (chromatic)

        # For now, we'll detect the base note from the Linnstrument's current configuration
        # Common Linnstrument bottom-left notes:
        # - F#1 (MIDI 30) - your current setting
        # - E2 (MIDI 40) - guitar tuning
        # - C3 (MIDI 48) - default factory

        self.row_offset = row_offset if row_offset is not None else DEFAULT_ROW_OFFSET
        self.column_offset = column_offset if column_offset is not None else DEFAULT_COLUMN_OFFSET

        # Detect base note by trying to read Linnstrument's octave setting
        # For now, we'll use a smart default that works with most setups
        if base_note is None:
            # Query the Linnstrument for its settings (we'll implement this)
            self.base_note = self.detect_base_note()
        else:
            self.base_note = base_note

        self.c_instance.log_message(f"Linnstrument detected: base_note={self.base_note}, row_offset={self.row_offset}, column_offset={self.column_offset}")

    def detect_base_note(self):
        """
        Detect the Linnstrument's base note (what column 0, row 0 plays)

        Since we can't query NRPN values back, we use a smart default.
        The Linnstrument's default octave setting (value 5) makes column 0, row 0 play C3 (MIDI 48).
        However, many users customize this.

        Common configurations:
        - 48 (C3): Factory default
        - 40 (E2): Guitar-style tuning
        - 36 (C2): Push-style tuning
        - 30 (F#1): Custom lower tuning

        For maximum compatibility, we'll default to the factory setting of C3 (48).
        Users can override by editing the code or we can add a preferences file later.
        """
        # TODO: Make this configurable via a settings file
        # For now, return factory default
        default_base = 48  # C3

        # Try to be smart: check if there's a saved preference
        # (We could add a .txt file in the Remote Script folder later)

        self.c_instance.log_message(f"Auto-detecting base note: using default {default_base} (C3)")
        self.c_instance.log_message("If pads don't match, press bottom-left pad and note the MIDI note")
        self.c_instance.log_message("Then edit LinnstrumentScale.py to set that as base_note")

        return default_base

    def send_midi(self, midi_bytes):
        """Send MIDI message using Ableton's API"""
        self.c_instance.send_midi(tuple(midi_bytes))


    def set_cell_color(self, column, row, color):
        """
        Set the color of a single LED cell

        Args:
            column: Column number (0-15 for playable pads on Linnstrument 128)
            row: Row number (0-7)
            color: Color number (0-11) or color name string
        """
        if isinstance(color, str):
            color = COLORS.get(color.lower(), 0)

        # Linnstrument uses CC20 for column, CC21 for row, CC22 for color
        # MIDI CC message: [status, controller, value]
        status = 0xB0 + self.channel  # Control Change on channel

        # IMPORTANT: Linnstrument columns are 1-indexed for playable surface
        # Column 0 = control buttons, Columns 1-16 = playable pads (Linnstrument 128)
        self.send_midi([status, 20, column + 1])  # Add 1 to skip control column
        self.send_midi([status, 21, row])
        self.send_midi([status, 22, color])

    def get_note_at_position(self, column, row):
        """Calculate MIDI note number at a given grid position"""
        return self.base_note + (column * self.column_offset) + (row * self.row_offset)

    def get_position_for_note(self, note):
        """Find all grid positions that play a given MIDI note"""
        positions = []

        for row in range(LINNSTRUMENT_ROWS):
            for column in range(LINNSTRUMENT_COLUMNS):
                note_at_pos = self.get_note_at_position(column, row)
                if note_at_pos == note:
                    positions.append((column, row))

        return positions

    def clear_all_lights(self, skip_top_row=False):
        """Turn off all LEDs"""
        max_row = LINNSTRUMENT_ROWS - 1 if skip_top_row else LINNSTRUMENT_ROWS
        for row in range(max_row):
            for column in range(LINNSTRUMENT_COLUMNS):
                self.set_cell_color(column, row, 'off')

    def light_note(self, note, color, skip_top_row=False):
        """Light up all cells that play a specific note"""
        positions = self.get_position_for_note(note)

        # Debug: verify position calculation for root notes and B notes
        note_name = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'][note % 12]
        if len(positions) > 0 and (note % 12 == 0 or note % 12 == 11):  # Log C and B notes
            self.c_instance.log_message(f"Lighting note {note} ({note_name}) at positions: {positions[:3]}")
            # Verify: what note do these positions actually play?
            for col, row in positions[:2]:
                calc_note = self.get_note_at_position(col, row)
                self.c_instance.log_message(f"  Verify: position ({col},{row}) calculates to note {calc_note}")

        for column, row in positions:
            # Skip row 7 (top row) if requested
            if skip_top_row and row == 7:
                continue
            self.set_cell_color(column, row, color)

    def light_scale(self, scale_notes, root_color='red', scale_color='blue', root_pitch_class=None, skip_top_row=False):
        """
        Light up all notes in a scale

        Args:
            scale_notes: List of MIDI note numbers in the scale
            root_color: Color for root notes
            scale_color: Color for other scale notes
            root_pitch_class: The actual root pitch class (0-11), if known
            skip_top_row: If True, don't clear or light row 7 (reserved for track selection)
        """
        # Clear all lights first (optionally skip top row)
        self.clear_all_lights(skip_top_row=skip_top_row)

        # Get root note pitch class
        if not scale_notes:
            return

        # Use provided root pitch class, or derive from first note
        if root_pitch_class is not None:
            root_note = root_pitch_class
        else:
            root_note = scale_notes[0] % 12

        # Debug logging
        c_instance = self.c_instance
        c_instance.log_message(f"=== light_scale DEBUG ===")
        c_instance.log_message(f"Root pitch class parameter: {root_note}")
        c_instance.log_message(f"First scale note: {scale_notes[0]}")
        c_instance.log_message(f"All scale notes to light: {scale_notes}")

        # Check which notes are marked as roots
        root_notes = [n for n in scale_notes if n % 12 == root_note]
        c_instance.log_message(f"Notes that match root pitch class {root_note}: {root_notes}")

        # Sample: show what note some positions play
        c_instance.log_message(f"Grid verification:")
        c_instance.log_message(f"  Position (0,0) plays: {self.get_note_at_position(0, 0)} (should be 36/C2)")
        c_instance.log_message(f"  Position (1,0) plays: {self.get_note_at_position(1, 0)} (should be 37/C#2)")
        c_instance.log_message(f"  Position (0,1) plays: {self.get_note_at_position(0, 1)} (should be 41/F2)")
        c_instance.log_message(f"  Position (12,0) plays: {self.get_note_at_position(12, 0)} (should be 48/C3)")

        # Light up each note in the scale
        for note in scale_notes:
            # Use root color for root notes, scale color for others
            is_root = (note % 12) == root_note
            color = root_color if is_root else scale_color
            self.light_note(note, color, skip_top_row=skip_top_row)

    def light_scale_with_degrees(self, scale_notes, color_map=None):
        """
        Light up scale with different colors for different scale degrees

        Args:
            scale_notes: List of MIDI note numbers in the scale
            color_map: Dict mapping scale degree (0-based) to color
                      Can include special key 'other' for non-I/III/V degrees
        """
        if color_map is None:
            color_map = {
                0: 'red',      # Root
                2: 'yellow',   # Third
                4: 'green',    # Fifth
            }

        # Get default color for other scale degrees
        default_color = color_map.get('other', 'blue')

        self.clear_all_lights()

        # Group notes by their pitch class (0-11)
        if not scale_notes:
            return

        root_pc = scale_notes[0] % 12

        # Get unique pitch classes in the scale
        unique_pcs = sorted(set(note % 12 for note in scale_notes))

        # Sort pitch classes by their interval from the root (not numerically!)
        # This ensures A is degree 0 in A minor, not C
        scale_pcs_with_intervals = []
        for pc in unique_pcs:
            interval = (pc - root_pc) % 12
            scale_pcs_with_intervals.append((interval, pc))

        # Sort by interval from root
        scale_pcs_with_intervals.sort(key=lambda x: x[0])

        # Create a mapping from pitch class to scale degree
        pc_to_degree = {}
        for i, (interval, pc) in enumerate(scale_pcs_with_intervals):
            pc_to_degree[pc] = i

        # Light each note with appropriate color
        for note in scale_notes:
            pc = note % 12

            # Get the scale degree for this pitch class
            degree = pc_to_degree.get(pc)

            if degree is not None:
                # Get color for this degree
                color = color_map.get(degree, default_color)
                self.light_note(note, color)
