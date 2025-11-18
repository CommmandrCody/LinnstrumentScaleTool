"""
Keyboard Mode - Traditional scale lighting mode
Displays scale notes with colored pads based on Ableton's scale settings
"""

from .base_mode import BaseMode
from ..scales import get_scale_notes, NOTE_NAMES
from ..config import (
    LINNSTRUMENT_COLUMNS,
    LINNSTRUMENT_ROWS,
    KEYBOARD_SKIP_TOP_ROW,
    DEFAULT_ROOT_COLOR,
    DEFAULT_SCALE_COLOR
)


# Scale name mapping from Ableton to our scale names
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
    'Bhairav': 'double_harmonic',
    'Hungarian Minor': 'hungarian_minor',
    'Minor Gypsy': 'hungarian_minor',
    'Hirojoshi': 'japanese',
    'In-Sen': 'japanese',
    'Iwato': 'japanese',
    'Kumoi': 'japanese',
    'Pelog': 'japanese',
    'Spanish': 'spanish',
}


class KeyboardMode(BaseMode):
    """
    Keyboard mode - displays musical scales on the LinnStrument grid
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        super().__init__(c_instance, linnstrument, led_manager, song)
        self.current_scale = None
        self.current_root = None
        self.current_track_color = None

    def enter(self):
        """Enter keyboard mode - set up listeners and display scale"""
        super().enter()

        # Add listeners for scale changes
        self._add_listener(self.song, 'add_root_note_listener', self._on_scale_changed)
        self._add_listener(self.song, 'add_scale_name_listener', self._on_scale_changed)
        self._add_listener(self.song.view, 'add_selected_track_listener', self._on_track_changed)
        self._add_listener(self.song, 'add_tracks_listener', self._on_tracks_changed)

        # Display current scale
        self.update_leds()
        self.show_message("Linnstrument: Keyboard Mode")

    def exit(self):
        """Exit keyboard mode - clean up"""
        super().exit()
        # Clear LEDs (base class removes listeners)
        self.led_manager.clear_all()

    def _on_scale_changed(self):
        """Called when scale or root note changes"""
        self.log_message("Scale changed")
        self.update_leds()

    def _on_track_changed(self):
        """Called when selected track changes"""
        self.log_message("Track changed")
        self.update_leds()

    def _on_tracks_changed(self):
        """Called when track list changes"""
        self.log_message("Track list changed")
        self.update_leds()

    def update_leds(self):
        """Update LED display with current scale"""
        try:
            # Get scale settings from Ableton
            root = self.song.root_note  # 0-11
            scale_name = self.song.scale_name

            # Get track color
            selected_track = self.song.view.selected_track
            track_color = None
            if hasattr(selected_track, 'color'):
                track_color = selected_track.color

            # Check if anything changed
            if (root == self.current_root and
                scale_name == self.current_scale and
                track_color == self.current_track_color):
                return  # No change, skip update

            self.current_root = root
            self.current_scale = scale_name
            self.current_track_color = track_color

            # Map Ableton scale to our scale
            our_scale_name = ABLETON_SCALE_MAP.get(
                scale_name,
                scale_name.lower().replace(' ', '_')
            )

            root_name = NOTE_NAMES[root]
            self.log_message(f"Displaying scale: {root_name} {scale_name}")

            # Light the scale
            self._light_scale(root, our_scale_name, track_color)

            # Update status message
            self.show_message(f"Linnstrument: {root_name} {scale_name}")

        except Exception as e:
            self.log_message(f"Error updating scale LEDs: {e}")

    def _light_scale(self, root, scale_name, track_color=None):
        """
        Light up scale notes on the grid

        Args:
            root: Root note (0-11)
            scale_name: Scale name from scales.py
            track_color: Optional Ableton track color (RGB int)
        """
        try:
            # Calculate note range for LinnStrument
            min_note = self.linnstrument.base_note
            max_note = self.linnstrument.base_note + \
                      (LINNSTRUMENT_COLUMNS * 1) + (LINNSTRUMENT_ROWS * 5)

            # Get all scale notes
            all_scale_notes = get_scale_notes(root, scale_name)
            scale_notes = [n for n in all_scale_notes if min_note <= n <= max_note]

            # Get colors based on track color
            color_scheme = self._map_track_color_to_scheme(track_color)
            root_color = color_scheme['root']
            scale_color = color_scheme['other']

            # Log for debugging
            root_name = NOTE_NAMES[root]
            pitch_classes = sorted(set(note % 12 for note in scale_notes))
            pitch_class_names = [NOTE_NAMES[pc] for pc in pitch_classes]
            self.log_message(f"Scale notes: {pitch_class_names}")

            # Clear and light scale
            self.led_manager.clear_all()

            for note in scale_notes:
                positions = self.linnstrument.get_position_for_note(note)
                is_root = (note % 12) == root
                color = root_color if is_root else scale_color

                for column, row in positions:
                    # Skip top row if configured
                    if KEYBOARD_SKIP_TOP_ROW and row == 7:
                        continue
                    self.led_manager.set_led(column, row, color)

        except Exception as e:
            self.log_message(f"Error lighting scale: {e}")

    def _map_track_color_to_scheme(self, ableton_color):
        """
        Map Ableton track color to LinnStrument color scheme

        Args:
            ableton_color: RGB integer or None

        Returns:
            Dict with 'root' and 'other' color names
        """
        if ableton_color is None:
            return {'root': DEFAULT_ROOT_COLOR, 'other': DEFAULT_SCALE_COLOR}

        # Extract RGB components
        r = (ableton_color >> 16) & 0xFF
        g = (ableton_color >> 8) & 0xFF
        b = ableton_color & 0xFF

        # Map to LinnStrument colors
        if r > g and r > b:
            if r > 200 and g < 100:
                return {'root': 'red', 'other': 'pink'}
            else:
                return {'root': 'orange', 'other': 'yellow'}
        elif g > r and g > b:
            if g > 200:
                return {'root': 'green', 'other': 'lime'}
            else:
                return {'root': 'lime', 'other': 'green'}
        elif b > r and b > g:
            if b > 200:
                return {'root': 'blue', 'other': 'cyan'}
            else:
                return {'root': 'cyan', 'other': 'blue'}
        elif r > 150 and g > 150 and b < 100:
            return {'root': 'yellow', 'other': 'lime'}
        elif r > 150 and b > 150:
            return {'root': 'magenta', 'other': 'pink'}
        elif g > 150 and b > 150:
            return {'root': 'cyan', 'other': 'blue'}
        else:
            return {'root': 'white', 'other': 'blue'}

    def handle_note(self, note, velocity, is_note_on):
        """
        Keyboard mode doesn't intercept notes - passes through for playing

        Args:
            note: MIDI note number
            velocity: Note velocity
            is_note_on: True for note on, False for note off

        Returns:
            False (always pass through in keyboard mode)
        """
        # Don't intercept notes - let them pass through for normal playing
        return False

    def update(self):
        """Per-frame update (not needed for keyboard mode)"""
        pass
