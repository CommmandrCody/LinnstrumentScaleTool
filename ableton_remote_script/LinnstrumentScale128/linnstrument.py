"""
Linnstrument MIDI Control Module
Handles MIDI communication with Linnstrument for LED control
"""

import mido
import time

# Linnstrument uses a 26-column x 8-row grid
LINNSTRUMENT_COLUMNS = 26
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

class Linnstrument:
    """
    Interface for controlling Linnstrument LEDs via MIDI
    """

    def __init__(self, port_name=None, channel=0, row_offset=DEFAULT_ROW_OFFSET,
                 column_offset=DEFAULT_COLUMN_OFFSET, base_note=0):
        """
        Initialize Linnstrument controller

        Args:
            port_name: MIDI port name (None for auto-detect)
            channel: MIDI channel (0-15)
            row_offset: Semitones between rows (default 5)
            column_offset: Semitones between columns (default 1)
            base_note: MIDI note number at position (0, 0)
        """
        self.channel = channel
        self.row_offset = row_offset
        self.column_offset = column_offset
        self.base_note = base_note

        # Find and open MIDI port
        if port_name is None:
            port_name = self._find_linnstrument_port()

        if port_name is None:
            raise RuntimeError("No Linnstrument MIDI port found. Available ports: " +
                             ", ".join(mido.get_output_names()))

        self.port = mido.open_output(port_name)
        print(f"Connected to Linnstrument on port: {port_name}")

    def _find_linnstrument_port(self):
        """Auto-detect Linnstrument MIDI port"""
        ports = mido.get_output_names()
        for port in ports:
            if 'linnstrument' in port.lower():
                return port
        return None

    def close(self):
        """Close MIDI port"""
        if hasattr(self, 'port'):
            self.port.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get_note_at_position(self, column, row):
        """
        Calculate MIDI note number at a given grid position

        Args:
            column: Column number (0-25)
            row: Row number (0-7)

        Returns:
            MIDI note number
        """
        return self.base_note + (column * self.column_offset) + (row * self.row_offset)

    def get_position_for_note(self, note):
        """
        Find all grid positions that play a given MIDI note

        Args:
            note: MIDI note number

        Returns:
            List of (column, row) tuples
        """
        positions = []

        for row in range(LINNSTRUMENT_ROWS):
            for column in range(LINNSTRUMENT_COLUMNS):
                if self.get_note_at_position(column, row) == note:
                    positions.append((column, row))

        return positions

    def set_cell_color(self, column, row, color):
        """
        Set the color of a single LED cell

        Args:
            column: Column number (0-25)
            row: Row number (0-7)
            color: Color number (0-11) or color name string
        """
        if isinstance(color, str):
            color = COLORS.get(color.lower(), 0)

        # Linnstrument uses CC20 for column, CC21 for row, CC22 for color
        self.port.send(mido.Message('control_change', channel=self.channel,
                                    control=20, value=column))
        self.port.send(mido.Message('control_change', channel=self.channel,
                                    control=21, value=row))
        self.port.send(mido.Message('control_change', channel=self.channel,
                                    control=22, value=color))

    def clear_all_lights(self):
        """Turn off all LEDs"""
        for row in range(LINNSTRUMENT_ROWS):
            for column in range(LINNSTRUMENT_COLUMNS):
                self.set_cell_color(column, row, 'off')
        time.sleep(0.1)  # Brief pause to ensure all messages are processed

    def light_note(self, note, color):
        """
        Light up all cells that play a specific note

        Args:
            note: MIDI note number
            color: Color number (0-11) or color name string
        """
        positions = self.get_position_for_note(note)
        for column, row in positions:
            self.set_cell_color(column, row, color)

    def light_scale(self, scale_notes, root_color='red', scale_color='blue'):
        """
        Light up all notes in a scale

        Args:
            scale_notes: List of MIDI note numbers in the scale
            root_color: Color for root notes
            scale_color: Color for other scale notes
        """
        # Clear all lights first
        self.clear_all_lights()

        # Get root note (first note in scale)
        root_note = scale_notes[0] % 12 if scale_notes else None

        # Light up each note in the scale
        for note in scale_notes:
            # Use root color for root notes, scale color for others
            is_root = (note % 12) == root_note
            color = root_color if is_root else scale_color
            self.light_note(note, color)

        time.sleep(0.05)  # Brief pause

    def light_scale_with_degrees(self, scale_notes, color_map=None):
        """
        Light up scale with different colors for different scale degrees

        Args:
            scale_notes: List of MIDI note numbers in the scale
            color_map: Dict mapping scale degree (0-based) to color
                      Default: {0: 'red', 2: 'yellow', 4: 'green'} (I, III, V)
        """
        if color_map is None:
            color_map = {
                0: 'red',      # Root
                2: 'yellow',   # Third
                4: 'green',    # Fifth
            }

        self.clear_all_lights()

        # Group notes by their pitch class (0-11)
        pitch_classes = {}
        for note in scale_notes:
            pc = note % 12
            if pc not in pitch_classes:
                pitch_classes[pc] = []
            pitch_classes[pc].append(note)

        # Determine scale degrees
        if not scale_notes:
            return

        root_pc = scale_notes[0] % 12
        scale_pcs = sorted(set(note % 12 for note in scale_notes))

        # Light each note with appropriate color
        for note in scale_notes:
            pc = note % 12
            # Find scale degree
            degree = None
            for i, scale_pc in enumerate(scale_pcs):
                if (root_pc + scale_pc) % 12 == pc:
                    degree = i
                    break

            # Get color for this degree
            color = color_map.get(degree, 'blue')  # Default to blue
            self.light_note(note, color)

        time.sleep(0.05)

    @staticmethod
    def list_available_ports():
        """List all available MIDI output ports"""
        return mido.get_output_names()

    @staticmethod
    def get_color_names():
        """Get list of available color names"""
        return list(COLORS.keys())
