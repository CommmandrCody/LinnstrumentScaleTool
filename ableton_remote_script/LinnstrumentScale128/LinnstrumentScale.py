"""
MINIMAL BASELINE - Just passthrough, NO features
- NO NRPN messages
- NO listeners
- NO LED updates
- NO logging in MIDI path
- All notes pass through naturally
"""

from _Framework.ControlSurface import ControlSurface


class LinnstrumentScale(ControlSurface):
    """Minimal baseline - just initialize and pass notes through"""

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message("=== MINIMAL BASELINE LOADED ===")
        self.log_message("NO NRPN, NO listeners, NO LED updates")
        self.log_message("All notes pass through naturally")
        self.show_message("Linnstrument: Minimal Baseline")

    def disconnect(self):
        """Clean disconnect"""
        self.log_message("Minimal baseline disconnecting...")
        ControlSurface.disconnect(self)

    def build_midi_map(self, midi_map_handle):
        """Don't forward anything - let all MIDI pass through naturally"""
        # Do NOT forward notes or CCs
        # LinnStrument sends to track naturally
        pass

    def receive_midi(self, midi_bytes):
        """Don't intercept anything - no logging, no handling"""
        # Do NOTHING - let everything pass through
        pass

    def update_display(self):
        """Don't update anything"""
        # Do NOTHING
        pass
