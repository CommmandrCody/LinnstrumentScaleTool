"""
Centralized LED management for LinnStrument
Handles LED updates across all modes with optimization and batching
"""

from .linnstrument_ableton import COLORS
from .config import LINNSTRUMENT_COLUMNS, LINNSTRUMENT_ROWS


class LEDManager:
    """
    Manages LED state and updates for the LinnStrument grid
    - Caches LED states to minimize MIDI traffic
    - Batches updates for efficiency
    - Mode-specific LED update methods
    """

    def __init__(self, linnstrument, c_instance):
        """
        Initialize LED Manager

        Args:
            linnstrument: LinnstrumentAbletonMIDI instance
            c_instance: Ableton ControlSurface instance for logging
        """
        self.linnstrument = linnstrument
        self.c_instance = c_instance

        # Cache LED states [column][row] = color_value
        self._led_cache = [[0 for _ in range(LINNSTRUMENT_ROWS)]
                          for _ in range(LINNSTRUMENT_COLUMNS)]

        # Dirty flag to track if cache needs refresh
        self._dirty = True

    def set_led(self, column, row, color, force=False):
        """
        Set single LED with caching

        Args:
            column: Column index (0-15)
            row: Row index (0-7)
            color: Color name or number
            force: If True, bypass cache and force update
        """
        if not (0 <= column < LINNSTRUMENT_COLUMNS and 0 <= row < LINNSTRUMENT_ROWS):
            return

        # Convert color name to number
        if isinstance(color, str):
            color_num = COLORS.get(color.lower(), 0)
        else:
            color_num = color

        # Check cache to avoid redundant MIDI messages
        if not force and self._led_cache[column][row] == color_num:
            return

        # Update cache and hardware
        self._led_cache[column][row] = color_num
        self.linnstrument.set_cell_color(column, row, color_num)

    def set_leds_batch(self, led_list, force=False):
        """
        Set multiple LEDs efficiently

        Args:
            led_list: List of (column, row, color) tuples
            force: If True, bypass cache
        """
        for column, row, color in led_list:
            self.set_led(column, row, color, force=force)

    def clear_all(self, skip_rows=None, force=True):
        """
        Clear all LEDs

        Args:
            skip_rows: List of row indices to skip (e.g., [7] to preserve top row)
            force: Force clear even if cache says LED is already off
        """
        skip_rows = skip_rows or []

        for row in range(LINNSTRUMENT_ROWS):
            if row in skip_rows:
                continue
            for column in range(LINNSTRUMENT_COLUMNS):
                self.set_led(column, row, 'off', force=force)

    def clear_row(self, row):
        """Clear all LEDs in a specific row"""
        for column in range(LINNSTRUMENT_COLUMNS):
            self.set_led(column, row, 'off')

    def clear_column(self, column):
        """Clear all LEDs in a specific column"""
        for row in range(LINNSTRUMENT_ROWS):
            self.set_led(column, row, 'off')

    def clear_region(self, start_col, end_col, start_row, end_row):
        """
        Clear a rectangular region

        Args:
            start_col, end_col: Column range (inclusive)
            start_row, end_row: Row range (inclusive)
        """
        for row in range(start_row, end_row + 1):
            for column in range(start_col, end_col + 1):
                self.set_led(column, row, 'off')

    def invalidate_cache(self):
        """Mark cache as dirty, forcing next update to refresh all LEDs"""
        self._dirty = True

    def refresh_all(self):
        """Force refresh of all cached LEDs to hardware"""
        for column in range(LINNSTRUMENT_COLUMNS):
            for row in range(LINNSTRUMENT_ROWS):
                color = self._led_cache[column][row]
                self.linnstrument.set_cell_color(column, row, color)
        self._dirty = False

    def get_cached_color(self, column, row):
        """Get cached LED color without querying hardware"""
        if 0 <= column < LINNSTRUMENT_COLUMNS and 0 <= row < LINNSTRUMENT_ROWS:
            return self._led_cache[column][row]
        return None

    def fill_region(self, start_col, end_col, start_row, end_row, color):
        """
        Fill a rectangular region with a solid color

        Args:
            start_col, end_col: Column range (inclusive)
            start_row, end_row: Row range (inclusive)
            color: Color to fill with
        """
        for row in range(start_row, end_row + 1):
            for column in range(start_col, end_col + 1):
                self.set_led(column, row, color)

    def set_row_colors(self, row, colors):
        """
        Set an entire row with a list of colors

        Args:
            row: Row index
            colors: List of colors (length should match LINNSTRUMENT_COLUMNS)
        """
        for column, color in enumerate(colors[:LINNSTRUMENT_COLUMNS]):
            self.set_led(column, row, color)

    def pulse_led(self, column, row, color, duration_frames=10):
        """
        Create a pulsing effect (placeholder for future animation system)

        Args:
            column, row: LED position
            color: Color to pulse
            duration_frames: How many update cycles to pulse for
        """
        # For now, just set the LED
        # TODO: Implement animation queue system
        self.set_led(column, row, color)
