#!/usr/bin/env python3
"""
LinnStrument Drum Note Translator
Translates LinnStrument notes from row_offset=5 to chromatic drum grid (row_offset=4)

Usage: python linnstrument_drum_translator.py

Creates a virtual MIDI port that translates incoming notes from your LinnStrument
and outputs chromatic notes suitable for drum racks.
"""

import mido
import sys

# Note translation table for 4x4 drum grid
# Maps from row_offset=5 to row_offset=4 (chromatic)
TRANSLATION_MAP = {
    # Row 0: no change (36-39)
    36: 36, 37: 37, 38: 38, 39: 39,

    # Row 1: subtract 1 (41-44 -> 40-43)
    41: 40, 42: 41, 43: 42, 44: 43,

    # Row 2: subtract 2 (46-49 -> 44-47)
    46: 44, 47: 45, 48: 46, 49: 47,

    # Row 3: subtract 3 (51-54 -> 48-51)
    51: 48, 52: 49, 53: 50, 54: 51,
}

def translate_note(note):
    """Translate a note from row_offset=5 to chromatic"""
    return TRANSLATION_MAP.get(note, note)

def main():
    print("LinnStrument Drum Translator")
    print("=" * 50)

    # List available MIDI ports
    print("\nAvailable MIDI inputs:")
    for i, name in enumerate(mido.get_input_names()):
        print(f"  {i}: {name}")

    print("\nAvailable MIDI outputs:")
    for i, name in enumerate(mido.get_output_names()):
        print(f"  {i}: {name}")

    # Try to find LinnStrument
    linnstrument_input = None
    for name in mido.get_input_names():
        if 'LinnStrument' in name or 'LINN' in name.upper():
            linnstrument_input = name
            break

    if not linnstrument_input:
        print("\nERROR: Could not find LinnStrument MIDI input")
        print("Please connect your LinnStrument and try again.")
        return

    # Find or create IAC virtual output
    iac_output = None
    for name in mido.get_output_names():
        if 'IAC' in name or 'Bus' in name:
            iac_output = name
            break

    if not iac_output:
        print("\nERROR: Could not find IAC Driver or virtual MIDI bus")
        print("Please create a virtual MIDI port in Audio MIDI Setup")
        return

    print(f"\nUsing:")
    print(f"  Input:  {linnstrument_input}")
    print(f"  Output: {iac_output}")
    print("\nTranslating notes... (Press Ctrl+C to stop)")

    try:
        with mido.open_input(linnstrument_input) as inport:
            with mido.open_output(iac_output) as outport:
                for msg in inport:
                    if msg.type in ['note_on', 'note_off']:
                        # Translate the note
                        translated = translate_note(msg.note)

                        if translated != msg.note:
                            print(f"Translated: {msg.note} -> {translated}")

                        # Send translated message
                        outport.send(msg.copy(note=translated))
                    else:
                        # Pass through all other messages
                        outport.send(msg)

    except KeyboardInterrupt:
        print("\n\nStopped.")
    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == '__main__':
    main()
