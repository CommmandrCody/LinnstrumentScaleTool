"""
Session Mode - Clip launcher grid
Full grid (16x8 for LS128) for launching clips and scenes
"""

from .base_mode import BaseMode
from ..config import SESSION_ROWS, SESSION_COLUMNS
import Live


class SessionMode(BaseMode):
    """
    Session mode - clip launcher matrix
    Each pad launches a clip, LEDs show clip states and colors
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        super().__init__(c_instance, linnstrument, led_manager, song)

        # Session navigation offsets
        self._session_offset_x = 0  # Track offset
        self._session_offset_y = 0  # Scene offset

        # Clip slot state cache
        self._clip_slot_cache = {}

    def enter(self):
        """Enter session mode - set up session grid"""
        super().enter()

        # Add listeners for session changes
        self._add_listener(self.song.view, 'add_selected_track_listener', self._on_session_changed)
        self._add_listener(self.song.view, 'add_selected_scene_listener', self._on_session_changed)
        self._add_listener(self.song, 'add_tracks_listener', self._on_session_changed)
        self._add_listener(self.song, 'add_scenes_listener', self._on_session_changed)

        # Add clip slot listeners
        self._add_clip_slot_listeners()

        # Initial LED update
        self.update_leds()
        self.show_message("Linnstrument: Session Mode")

    def exit(self):
        """Exit session mode"""
        super().exit()
        self.led_manager.clear_all()

    def _on_session_changed(self):
        """Called when session structure changes"""
        self.log_message("Session changed")
        self._add_clip_slot_listeners()  # Refresh listeners
        self.update_leds()

    def _add_clip_slot_listeners(self):
        """Add listeners to all visible clip slots"""
        try:
            tracks = list(self.song.tracks)
            scenes = list(self.song.scenes)

            for track_idx in range(self._session_offset_x,
                                  min(self._session_offset_x + SESSION_COLUMNS, len(tracks))):
                track = tracks[track_idx]

                for scene_idx in range(self._session_offset_y,
                                      min(self._session_offset_y + SESSION_ROWS, len(scenes))):
                    if scene_idx < len(track.clip_slots):
                        clip_slot = track.clip_slots[scene_idx]

                        # Add listeners for clip state changes
                        self._add_listener(clip_slot, 'add_has_clip_listener', self._on_session_changed)
                        if clip_slot.has_clip:
                            clip = clip_slot.clip
                            self._add_listener(clip, 'add_playing_status_listener', self._on_session_changed)
                            self._add_listener(clip, 'add_color_listener', self._on_session_changed)

        except Exception as e:
            self.log_message(f"Error adding clip slot listeners: {e}")

    def update_leds(self):
        """Update session grid LED display"""
        try:
            tracks = list(self.song.tracks)
            scenes = list(self.song.scenes)

            # Clear grid
            self.led_manager.clear_all()

            # Bottom row (row 0) = Navigation controls
            self.led_manager.set_led(0, 0, 'blue')   # Scroll scenes up
            self.led_manager.set_led(1, 0, 'blue')   # Scroll scenes down
            self.led_manager.set_led(2, 0, 'cyan')   # Scroll tracks left
            self.led_manager.set_led(3, 0, 'cyan')   # Scroll tracks right

            # Display each clip slot (rows 1-6)
            for grid_col in range(SESSION_COLUMNS):
                track_idx = self._session_offset_x + grid_col
                if track_idx >= len(tracks):
                    continue

                track = tracks[track_idx]

                # Track stop button on bottom row (columns 4+)
                if grid_col >= 4:
                    self.led_manager.set_led(grid_col, 0, 'red')

                for grid_row in range(1, SESSION_ROWS):  # Skip row 0 (navigation)
                    scene_idx = self._session_offset_y + (grid_row - 1)
                    if scene_idx >= len(scenes) or scene_idx >= len(track.clip_slots):
                        continue

                    clip_slot = track.clip_slots[scene_idx]
                    color = self._get_clip_slot_color(clip_slot, track)

                    # Map to LinnStrument grid (row 1-6 for clips, row 7 for scenes)
                    linnstrument_row = grid_row
                    self.led_manager.set_led(grid_col, linnstrument_row, color)

            # Top row (row 7) = Scene launch buttons
            for grid_col in range(min(SESSION_COLUMNS, len(scenes) - self._session_offset_y)):
                self.led_manager.set_led(grid_col, 7, 'yellow')

        except Exception as e:
            self.log_message(f"Error updating session LEDs: {e}")

    def _get_clip_slot_color(self, clip_slot, track):
        """
        Determine color for a clip slot

        Args:
            clip_slot: Live.ClipSlot.ClipSlot
            track: Live.Track.Track

        Returns:
            Color name string
        """
        try:
            if not clip_slot.has_clip:
                # Empty slot - dim color based on track
                return self._get_dim_track_color(track)

            clip = clip_slot.clip

            # Check playing state
            if clip.is_playing:
                return 'green'  # Playing
            elif clip.is_triggered:
                return 'yellow'  # Triggered/queued
            elif clip.is_recording:
                return 'red'  # Recording
            else:
                # Stopped clip - show clip color
                return self._map_ableton_color_to_linnstrument(clip.color)

        except Exception as e:
            self.log_message(f"Error getting clip slot color: {e}")
            return 'off'

    def _get_dim_track_color(self, track):
        """Get a dimmed version of track color for empty slots"""
        try:
            if hasattr(track, 'color'):
                # Map to a dim color (we don't have brightness control, so use 'off')
                return 'off'
            return 'off'
        except:
            return 'off'

    def _map_ableton_color_to_linnstrument(self, ableton_color):
        """
        Map Ableton clip/track color to closest LinnStrument color

        Args:
            ableton_color: RGB integer

        Returns:
            Color name string
        """
        if ableton_color is None:
            return 'white'

        # Extract RGB
        r = (ableton_color >> 16) & 0xFF
        g = (ableton_color >> 8) & 0xFF
        b = ableton_color & 0xFF

        # Map to closest LinnStrument color
        if r > g and r > b:
            return 'red' if r > 200 else 'orange'
        elif g > r and g > b:
            return 'green' if g > 200 else 'lime'
        elif b > r and b > g:
            return 'blue' if b > 200 else 'cyan'
        elif r > 150 and g > 150 and b < 100:
            return 'yellow'
        elif r > 150 and b > 150:
            return 'magenta'
        elif g > 150 and b > 150:
            return 'cyan'
        else:
            return 'white'

    def handle_note(self, note, velocity, is_note_on):
        """
        Handle grid pad presses - launch clips, navigate, select tracks

        Args:
            note: MIDI note number
            velocity: Note velocity
            is_note_on: True for note on, False for note off

        Returns:
            True (intercepts all notes in session mode)
        """
        if not is_note_on:
            return True  # Ignore note offs

        try:
            # Get grid position
            positions = self.get_grid_position(note)
            if not positions:
                return True

            column, row = positions[0]  # Take first position

            # Top row (row 7) = Scene launch
            if row == 7:
                self._launch_scene(column)
                return True

            # Bottom row (row 0) = Navigation & track controls
            if row == 0:
                if column == 0:
                    # Bottom-left: Scroll scenes up
                    self.navigate_session(0, -1)
                elif column == 1:
                    # Scroll scenes down
                    self.navigate_session(0, 1)
                elif column == 2:
                    # Scroll tracks left
                    self.navigate_session(-1, 0)
                elif column == 3:
                    # Scroll tracks right
                    self.navigate_session(1, 0)
                elif column >= 4:
                    # Stop track
                    track_idx = self._session_offset_x + (column - 4)
                    self._stop_track(track_idx)
                return True

            # Main grid (rows 1-6) = Clip launching
            grid_row = (SESSION_ROWS - 1) - row
            track_idx = self._session_offset_x + column
            scene_idx = self._session_offset_y + grid_row

            # Get clip slot
            tracks = list(self.song.tracks)
            scenes = list(self.song.scenes)

            if track_idx >= len(tracks) or scene_idx >= len(scenes):
                return True

            track = tracks[track_idx]
            if scene_idx >= len(track.clip_slots):
                return True

            clip_slot = track.clip_slots[scene_idx]

            # Launch clip or stop
            self._launch_clip_slot(clip_slot)

            self.log_message(f"Launched clip at track {track_idx}, scene {scene_idx}")

        except Exception as e:
            self.log_message(f"Error handling session note: {e}")

        return True  # Always intercept in session mode

    def _launch_clip_slot(self, clip_slot):
        """
        Launch or stop a clip slot

        Args:
            clip_slot: Live.ClipSlot.ClipSlot
        """
        try:
            if clip_slot.has_clip:
                clip = clip_slot.clip
                if clip.is_playing:
                    # Stop playing clip
                    clip_slot.stop()
                else:
                    # Launch clip
                    clip_slot.fire()
            else:
                # Empty slot - stop track
                clip_slot.fire()

        except Exception as e:
            self.log_message(f"Error launching clip: {e}")

    def navigate_session(self, tracks_delta, scenes_delta):
        """
        Navigate session view

        Args:
            tracks_delta: Horizontal scroll amount
            scenes_delta: Vertical scroll amount
        """
        tracks = list(self.song.tracks)
        scenes = list(self.song.scenes)

        # Update offsets with clamping
        self._session_offset_x = max(0, min(
            self._session_offset_x + tracks_delta,
            len(tracks) - SESSION_COLUMNS
        ))

        self._session_offset_y = max(0, min(
            self._session_offset_y + scenes_delta,
            len(scenes) - SESSION_ROWS
        ))

        self.log_message(f"Session view: tracks {self._session_offset_x}, scenes {self._session_offset_y}")
        self._add_clip_slot_listeners()
        self.update_leds()

    def _launch_scene(self, column):
        """
        Launch a scene (row of clips)

        Args:
            column: Grid column (maps to scene index)
        """
        try:
            scene_idx = self._session_offset_y + (7 - column)  # Map top row to scenes
            scenes = list(self.song.scenes)

            if scene_idx < len(scenes):
                scenes[scene_idx].fire()
                self.log_message(f"Launched scene {scene_idx}")
        except Exception as e:
            self.log_message(f"Error launching scene: {e}")

    def _stop_track(self, track_idx):
        """
        Stop all clips on a track

        Args:
            track_idx: Track index
        """
        try:
            tracks = list(self.song.tracks)
            if track_idx < len(tracks):
                tracks[track_idx].stop_all_clips()
                self.log_message(f"Stopped track {track_idx}")
        except Exception as e:
            self.log_message(f"Error stopping track: {e}")

    def update(self):
        """Per-frame update for session mode"""
        # Could update playing clip animations here
        pass
