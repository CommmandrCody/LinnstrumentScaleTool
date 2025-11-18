"""
Base class for all LinnStrument modes
Defines common interface that all modes must implement
"""

from abc import ABC, abstractmethod


class BaseMode(ABC):
    """
    Abstract base class for LinnStrument operating modes
    Each mode handles a different use case (keyboard, session, drum sequencer)
    """

    def __init__(self, c_instance, linnstrument, led_manager, song):
        """
        Initialize mode

        Args:
            c_instance: Ableton ControlSurface instance
            linnstrument: LinnstrumentAbletonMIDI instance
            led_manager: LEDManager instance
            song: Ableton Song instance
        """
        self.c_instance = c_instance
        self.linnstrument = linnstrument
        self.led_manager = led_manager
        self.song = song
        self._is_active = False
        self._listeners = []

    @abstractmethod
    def enter(self):
        """
        Called when entering this mode
        Should set up listeners, update LEDs, etc.
        """
        self._is_active = True
        self.log_message(f"Entering {self.__class__.__name__}")

    @abstractmethod
    def exit(self):
        """
        Called when leaving this mode
        Should clean up listeners, clear LEDs, etc.
        """
        self._is_active = False
        self._remove_all_listeners()
        self.log_message(f"Exiting {self.__class__.__name__}")

    @abstractmethod
    def update_leds(self):
        """
        Update LED display for current mode state
        Called whenever mode state changes
        """
        pass

    @abstractmethod
    def handle_note(self, note, velocity, is_note_on):
        """
        Handle MIDI note input from LinnStrument

        Args:
            note: MIDI note number
            velocity: Note velocity
            is_note_on: True for note on, False for note off

        Returns:
            True if note was handled, False to pass through
        """
        pass

    def handle_cc(self, cc_number, value):
        """
        Handle MIDI CC input (optional for modes to override)

        Args:
            cc_number: CC number
            value: CC value

        Returns:
            True if CC was handled, False to pass through
        """
        return False

    def update(self):
        """
        Called periodically (from update_display)
        Override to implement per-frame updates (e.g., sequencer playhead)
        """
        pass

    def is_active(self):
        """Check if this mode is currently active"""
        return self._is_active

    def log_message(self, message):
        """Log message to Ableton's log"""
        self.c_instance.log_message(f"[{self.__class__.__name__}] {message}")

    def show_message(self, message):
        """Show message in Ableton's status bar"""
        self.c_instance.show_message(message)

    def _add_listener(self, subject, method, listener_name):
        """
        Helper to add a listener and track it for cleanup

        Args:
            subject: Object to add listener to
            method: Listener method name (e.g., 'add_root_note_listener')
            listener_name: Callback function
        """
        add_method = getattr(subject, method, None)
        if add_method:
            add_method(listener_name)
            # Store for cleanup: (subject, remove_method_name, callback)
            remove_method = method.replace('add_', 'remove_')
            self._listeners.append((subject, remove_method, listener_name))

    def _remove_all_listeners(self):
        """Remove all tracked listeners"""
        for subject, remove_method_name, callback in self._listeners:
            try:
                remove_method = getattr(subject, remove_method_name, None)
                if remove_method:
                    remove_method(callback)
            except Exception as e:
                self.log_message(f"Error removing listener: {e}")

        self._listeners.clear()

    def get_grid_position(self, note):
        """
        Get grid position(s) for a MIDI note

        Returns:
            List of (column, row) tuples
        """
        return self.linnstrument.get_position_for_note(note)

    def get_note_at_position(self, column, row):
        """Get MIDI note number at grid position"""
        return self.linnstrument.get_note_at_position(column, row)
