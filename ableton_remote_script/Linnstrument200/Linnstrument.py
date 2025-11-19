"""
Main MIDI Remote Script for Linnstrument Scale Light
"""

import sys
import os
from pathlib import Path

# Import from the same directory (modules are bundled with the script)
try:
    from .scales import get_scale_notes, note_name_to_number, NOTE_NAMES
    from .linnstrument_ableton import LinnstrumentAbletonMIDI
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Ableton Live API
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *

# Import diagnostic tool
try:
    from .diagnostic import find_scale_properties
    DIAGNOSTIC_AVAILABLE = True
except ImportError:
    DIAGNOSTIC_AVAILABLE = False

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


class Linnstrument(ControlSurface):
    """
    MIDI Remote Script that monitors Ableton's scale settings
    and updates Linnstrument lights accordingly
    """

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)

        self.log_message("Linnstrument Scale Light - Starting...")

        # Check if modules are available
        if not MODULES_AVAILABLE:
            self.log_message(f"ERROR: Could not import scale modules: {IMPORT_ERROR}")
            self.log_message(f"Tool path: {tool_path}")
            self.show_message("Linnstrument Scale: Import Error - Check Log")
            return

        self.linnstrument = None
        self.current_scale = None
        self.current_root = None
        self.current_track_color = None

        # Note history for auto-detection
        self.note_history = []
        self.max_history = 50

        # Initialize Linnstrument MIDI controller
        try:
            # ============================================================
            # CONFIGURATION: Set your Linnstrument's bottom-left note here
            # ============================================================
            # Press the bottom-left pad on your Linnstrument and check what MIDI note it plays.
            # Common values:
            #   30 = F#1 (custom low tuning)
            #   36 = C2  (Push-style)
            #   40 = E2  (guitar tuning)
            #   48 = C3  (factory default)
            #
            # Set YOUR value here:
            LINNSTRUMENT_BASE_NOTE = 30  # <<< CHANGE THIS to match your Linnstrument!

            self.linnstrument = LinnstrumentAbletonMIDI(
                c_instance,
                base_note=LINNSTRUMENT_BASE_NOTE,
                row_offset=5,      # Semitones per row (standard = 5)
                column_offset=1    # Semitones per column (always 1)
            )
            self.log_message("Linnstrument MIDI controller initialized")
            self.log_message(f"Linnstrument config: base_note={LINNSTRUMENT_BASE_NOTE}, row_offset=5, column_offset=1")
            self.show_message("Linnstrument Scale: Ready")
        except Exception as e:
            self.log_message(f"Warning: Could not initialize Linnstrument: {e}")
            self.show_message("Linnstrument Scale: Initialization Error")

        # Add listeners for scale changes
        self.song().add_root_note_listener(self._on_scale_changed)
        self.song().add_scale_name_listener(self._on_scale_changed)

        # Add listener for track changes
        self.song().view.add_selected_track_listener(self._on_track_changed)

        # Run diagnostic to find scale API
        if DIAGNOSTIC_AVAILABLE:
            self.log_message("Running diagnostic to find scale properties...")
            find_scale_properties(c_instance)

        # Initial update
        self._update_scale()

        self.log_message("Linnstrument Scale Light - Ready!")

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log_message("Linnstrument Scale Light - Disconnecting...")

        # Remove listeners
        try:
            self.song().remove_root_note_listener(self._on_scale_changed)
            self.song().remove_scale_name_listener(self._on_scale_changed)
            self.song().view.remove_selected_track_listener(self._on_track_changed)
        except:
            pass

        ControlSurface.disconnect(self)
        self.log_message("Linnstrument Scale Light - Disconnected")

    def _on_track_changed(self):
        """Called when selected track changes"""
        self.log_message("Track changed, updating scale...")
        self.note_history = []  # Clear note history when changing tracks
        self._update_scale()

    def _on_scale_changed(self):
        """Called when scale or root note changes"""
        self.log_message("Scale changed, updating Linnstrument...")
        self._update_scale()

    def _update_scale(self):
        """Check Ableton's scale settings and update Linnstrument"""
        if not self.linnstrument:
            return

        try:
            song = self.song()

            # Get scale settings from Ableton's song object
            root = song.root_note  # 0-11 (C to B)
            scale_name = song.scale_name  # String like "Major", "Minor", etc.

            # Get track color
            selected_track = song.view.selected_track
            track_color = None
            if hasattr(selected_track, 'color'):
                track_color = selected_track.color

            # Check if anything changed
            scale_changed = (root != self.current_root or scale_name != self.current_scale)
            color_changed = (track_color != self.current_track_color)

            if scale_changed or color_changed:
                self.current_root = root
                self.current_scale = scale_name
                self.current_track_color = track_color

                # Map Ableton scale name to our scale name
                our_scale_name = ABLETON_SCALE_MAP.get(scale_name, scale_name.lower().replace(' ', '_'))

                self.log_message(f"Scale changed to: {NOTE_NAMES[root]} {scale_name} (track color: {track_color})")
                self._light_scale(root, our_scale_name, track_color)

        except Exception as e:
            self.log_message(f"Error updating scale: {e}")

    def _parse_scale_from_name(self, name):
        """
        Parse scale info from track/clip name
        Expected format: "C Major", "D minor", etc.
        """
        if not name:
            return None

        parts = name.strip().split()
        if len(parts) < 2:
            return None

        # Try to find note name
        note_name = parts[0].upper()
        if note_name not in NOTE_NAMES and note_name not in ['DB', 'EB', 'GB', 'AB', 'BB']:
            return None

        # Convert flat notation
        flat_map = {'DB': 'C#', 'EB': 'D#', 'GB': 'F#', 'AB': 'G#', 'BB': 'A#'}
        note_name = flat_map.get(note_name, note_name)

        # Get scale name
        scale_part = ' '.join(parts[1:])
        scale_name = ABLETON_SCALE_MAP.get(scale_part)

        if not scale_name:
            # Try lowercase match
            scale_name = scale_part.lower().replace(' ', '_')

        try:
            root = note_name_to_number(note_name)
            return (root, scale_name)
        except:
            return None

    def _map_ableton_color_to_linnstrument(self, ableton_color):
        """Map Ableton track color (RGB int) to Linnstrument root/scale colors"""
        if ableton_color is None:
            # Default: red for root, blue for other scale notes
            return {'root': 'red', 'other': 'blue'}

        # Ableton colors are RGB integers (0-16777215)
        # Extract RGB components
        r = (ableton_color >> 16) & 0xFF
        g = (ableton_color >> 8) & 0xFF
        b = ableton_color & 0xFF

        # Map to closest Linnstrument color based on dominant RGB channel
        # Use bright color for root, dimmer/related color for other scale notes
        if r > g and r > b:
            # Red dominant
            if r > 200 and g < 100:
                return {'root': 'red', 'other': 'pink'}
            else:
                return {'root': 'orange', 'other': 'yellow'}
        elif g > r and g > b:
            # Green dominant
            if g > 200:
                return {'root': 'green', 'other': 'lime'}
            else:
                return {'root': 'lime', 'other': 'green'}
        elif b > r and b > g:
            # Blue dominant
            if b > 200:
                return {'root': 'blue', 'other': 'cyan'}
            else:
                return {'root': 'cyan', 'other': 'blue'}
        elif r > 150 and g > 150 and b < 100:
            # Yellow
            return {'root': 'yellow', 'other': 'lime'}
        elif r > 150 and b > 150:
            # Magenta
            return {'root': 'magenta', 'other': 'pink'}
        elif g > 150 and b > 150:
            # Cyan
            return {'root': 'cyan', 'other': 'blue'}
        else:
            # Default/White
            return {'root': 'white', 'other': 'blue'}

    def _light_scale(self, root, scale_name, track_color=None):
        """Update Linnstrument lights with the scale"""
        try:
            # Get scale notes, but only in the Linnstrument's actual range
            # Linnstrument 128: 16 columns x 8 rows
            # Linnstrument 200: 26 columns x 8 rows
            # Calculate range based on base_note and grid size
            from .linnstrument_ableton import LINNSTRUMENT_COLUMNS, LINNSTRUMENT_ROWS
            min_note = self.linnstrument.base_note
            max_note = self.linnstrument.base_note + (LINNSTRUMENT_COLUMNS * 1) + (LINNSTRUMENT_ROWS * 5)

            # Generate all scale notes
            all_scale_notes = get_scale_notes(root, scale_name)

            # Filter to only notes in Linnstrument range
            scale_notes = [note for note in all_scale_notes if min_note <= note <= max_note]

            # Get color map based on track color
            color_scheme = self._map_ableton_color_to_linnstrument(track_color)

            # Use simple two-color scheme: root color for root, other color for rest of scale
            # This makes it easy to see which notes are the root
            root_color = color_scheme['root']
            scale_color = color_scheme['other']

            # Log detailed info for debugging
            root_name = NOTE_NAMES[root]
            self.log_message(f"=== Lighting {root_name} {scale_name} scale ===")
            self.log_message(f"Root pitch class: {root} ({root_name})")
            self.log_message(f"Total scale notes across all octaves: {len(scale_notes)}")
            self.log_message(f"First 20 scale notes: {scale_notes[:20]}")

            # Show which pitch classes are in the scale
            pitch_classes = sorted(set(note % 12 for note in scale_notes))
            pitch_class_names = [NOTE_NAMES[pc] for pc in pitch_classes]
            self.log_message(f"Scale pitch classes ({len(pitch_classes)}): {pitch_class_names}")
            self.log_message(f"Scale pitch class numbers: {pitch_classes}")

            self.linnstrument.light_scale(scale_notes, root_color, scale_color)

            self.show_message(f"Linnstrument: {root_name} {scale_name}")

        except Exception as e:
            self.log_message(f"Error lighting scale: {e}")

    def build_midi_map(self, midi_map_handle):
        """Build MIDI map (required by API but not used)"""
        pass

    def update_display(self):
        """Update display (required by API but not used)"""
        pass

    def receive_midi(self, midi_bytes):
        """Receive MIDI and analyze for scale detection"""
        # Parse MIDI message
        if len(midi_bytes) >= 3:
            status = midi_bytes[0]
            note = midi_bytes[1]
            velocity = midi_bytes[2]

            # Check if it's a note-on message (status 144-159)
            if 144 <= status <= 159 and velocity > 0:
                # Add to note history
                pitch_class = note % 12
                self.note_history.append(pitch_class)

                # Keep history limited
                if len(self.note_history) > self.max_history:
                    self.note_history.pop(0)

                # Try to detect scale after we have enough notes
                if len(self.note_history) >= 5:
                    self._detect_and_update_scale()
