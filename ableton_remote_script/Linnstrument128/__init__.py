"""
Linnstrument - Ableton MIDI Remote Script
Multi-mode system: Keyboard mode with scale lighting, Drum mode with sequencer
"""

from .Linnstrument import Linnstrument

def create_instance(c_instance):
    """Create and return the remote script instance"""
    return Linnstrument(c_instance)
