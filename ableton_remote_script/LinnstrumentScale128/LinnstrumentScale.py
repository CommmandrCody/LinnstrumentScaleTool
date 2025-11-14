"""
Keyboard Scale Mode - Display Ableton's scale on LinnStrument with LED lighting
- Row offset: 5 (fifths) - standard LinnStrument layout
- Lights up scale notes based on Ableton's root/scale settings
- All notes pass through naturally (no interception)
- NO NRPN messages (doesn't change LinnStrument settings)
"""

from _Framework.ControlSurface import ControlSurface

try:
    from .config import LINNSTRUMENT_BASE_NOTE, LINNSTRUMENT_ROW_OFFSET, LINNSTRUMENT_COLUMN_OFFSET
    from .scales import NOTE_NAMES
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


class LinnstrumentScale(ControlSurface):
    """Keyboard mode - scale lighting with row offset 5 (fifths)"""

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self.log_message("=" * 60)
        self.log_message("LinnStrument Keyboard Scale Mode - Starting...")
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

        # Track current state to avoid redundant updates
        self.current_root = None
        self.current_scale = None

        # Add listeners for scale changes (these are safe - only fire on actual changes)
        self.song().add_root_note_listener(self._on_scale_changed)
        self.song().add_scale_name_listener(self._on_scale_changed)

        # Initial display
        self.update_scale_leds()

        self.log_message("Keyboard Scale Mode Ready!")
        self.show_message("Linnstrument: Keyboard Scale Mode")

    def disconnect(self):
        """Clean disconnect"""
        self.log_message("Keyboard Scale Mode disconnecting...")

        # Remove listeners
        try:
            self.song().remove_root_note_listener(self._on_scale_changed)
            self.song().remove_scale_name_listener(self._on_scale_changed)
        except:
            pass

        ControlSurface.disconnect(self)

    def _on_scale_changed(self):
        """Called when scale or root note changes"""
        self.update_scale_leds()

    def update_scale_leds(self):
        """Update LED display with current scale"""
        try:
            # Get scale settings from Ableton
            root = self.song().root_note  # 0-11
            scale_name = self.song().scale_name

            # Check if anything changed
            if root == self.current_root and scale_name == self.current_scale:
                return  # No change, skip update

            self.current_root = root
            self.current_scale = scale_name

            # Map Ableton scale to our scale name
            our_scale_name = ABLETON_SCALE_MAP.get(
                scale_name,
                scale_name.lower().replace(' ', '_')
            )

            root_name = NOTE_NAMES[root]
            self.log_message(f"Displaying scale: {root_name} {scale_name}")

            # Get scale notes
            from .scales import get_scale_notes
            scale_notes = get_scale_notes(root, our_scale_name)

            # Clear all LEDs
            self.led_manager.clear_all()

            # Light up scale notes (root = red, others = blue)
            for note in scale_notes:
                positions = self.linnstrument.get_position_for_note(note)
                is_root = (note % 12) == root
                color = 'red' if is_root else 'blue'

                for column, row in positions:
                    self.led_manager.set_led(column, row, color)

            self.show_message(f"Linnstrument: {root_name} {scale_name}")

        except Exception as e:
            self.log_message(f"Error updating scale LEDs: {e}")
            import traceback
            self.log_message(traceback.format_exc())

    def build_midi_map(self, midi_map_handle):
        """Don't forward anything - let all MIDI pass through naturally"""
        # All notes pass through to track naturally
        pass

    def receive_midi(self, midi_bytes):
        """Don't intercept anything - let everything pass through"""
        # All MIDI passes through - no logging, no handling
        pass

    def update_display(self):
        """Called periodically - do nothing"""
        # Don't update LEDs here - only update on scale changes via listeners
        pass
