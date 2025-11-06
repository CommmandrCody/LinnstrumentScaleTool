"""
Main MIDI Remote Script for Linnstrument Scale Light
"""

import sys
import os
from pathlib import Path

# Add the LinnstrumentScaleTool directory to the path
tool_path = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tool_path))

try:
    from scales import get_scale_notes, note_name_to_number, NOTE_NAMES
    from linnstrument import Linnstrument
    MODULES_AVAILABLE = True
except ImportError as e:
    MODULES_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Ableton Live API
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *

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


class LinnstrumentScale(ControlSurface):
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

        # Try to connect to Linnstrument
        try:
            self.linnstrument = Linnstrument()
            self.log_message("Connected to Linnstrument!")
            self.show_message("Linnstrument Scale: Connected")
        except Exception as e:
            self.log_message(f"Warning: Could not connect to Linnstrument: {e}")
            self.show_message("Linnstrument Scale: No Linnstrument Found")

        # Monitor the song for scale changes
        self.song().add_current_song_time_listener(self._on_song_time_changed)

        # Initial update
        self._update_scale()

        self.log_message("Linnstrument Scale Light - Ready!")

    def disconnect(self):
        """Called when the script is unloaded"""
        self.log_message("Linnstrument Scale Light - Disconnecting...")

        if self.linnstrument:
            try:
                self.linnstrument.close()
            except:
                pass

        # Remove listeners
        try:
            self.song().remove_current_song_time_listener(self._on_song_time_changed)
        except:
            pass

        ControlSurface.disconnect(self)
        self.log_message("Linnstrument Scale Light - Disconnected")

    def _on_song_time_changed(self):
        """Called periodically - check if scale has changed"""
        # Only check every ~1 second to avoid performance issues
        song_time = self.song().current_song_time
        if int(song_time) % 1 == 0:  # Check every second
            self._update_scale()

    def _update_scale(self):
        """Check Ableton's scale settings and update Linnstrument"""
        if not self.linnstrument:
            return

        try:
            # Get the first track (or could monitor selected track)
            tracks = self.song().tracks
            if not tracks:
                return

            # Check if any track has scale mode enabled
            # Note: This is a simplified approach. Ableton's scale info
            # is not directly accessible via the API in older versions.
            # We'll monitor clip properties instead.

            # For now, let's use a different approach:
            # Monitor the selected track and update based on clip properties
            track = self.song().view.selected_track

            # Try to get scale info from clip name or track name
            # Format: "C Major" or "D minor" in track/clip name
            scale_info = self._parse_scale_from_name(track.name)

            if scale_info:
                root, scale_name = scale_info

                # Only update if changed
                if root != self.current_root or scale_name != self.current_scale:
                    self.current_root = root
                    self.current_scale = scale_name

                    self.log_message(f"Scale changed to: {NOTE_NAMES[root]} {scale_name}")
                    self._light_scale(root, scale_name)

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

    def _light_scale(self, root, scale_name):
        """Update Linnstrument lights with the scale"""
        try:
            scale_notes = get_scale_notes(root, scale_name)
            self.linnstrument.light_scale_with_degrees(scale_notes)

            root_name = NOTE_NAMES[root]
            self.show_message(f"Linnstrument: {root_name} {scale_name}")
            self.log_message(f"Lit up {root_name} {scale_name} scale")

        except Exception as e:
            self.log_message(f"Error lighting scale: {e}")

    def build_midi_map(self, midi_map_handle):
        """Build MIDI map (required by API but not used)"""
        pass

    def update_display(self):
        """Update display (required by API but not used)"""
        pass

    def receive_midi(self, midi_bytes):
        """Receive MIDI (required by API but not used)"""
        pass
