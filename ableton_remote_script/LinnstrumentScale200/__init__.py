"""
Linnstrument Scale Light - Ableton MIDI Remote Script
Automatically updates Linnstrument lights when you change scales in Ableton
"""

from .LinnstrumentScale import LinnstrumentScale

def create_instance(c_instance):
    """Create and return the remote script instance"""
    return LinnstrumentScale(c_instance)
