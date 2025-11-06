#!/usr/bin/env python3
"""
Example scripts showing different ways to use the Linnstrument Scale Tool
"""

from scales import get_scale_notes, note_name_to_number, get_available_scales
from linnstrument import Linnstrument
import time

def example_basic_scale():
    """Example 1: Light up a basic C major scale"""
    print("Example 1: C Major Scale")

    with Linnstrument() as linn:
        scale_notes = get_scale_notes('C', 'major')
        linn.light_scale(scale_notes, root_color='red', scale_color='blue')
        print("C major scale is now lit up!")

def example_scale_degrees():
    """Example 2: Show scale with colored degrees (I, III, V)"""
    print("\nExample 2: G Major with Colored Scale Degrees")

    with Linnstrument() as linn:
        scale_notes = get_scale_notes('G', 'major')
        color_map = {
            0: 'red',      # Root (I)
            2: 'yellow',   # Third (III)
            4: 'green',    # Fifth (V)
        }
        linn.light_scale_with_degrees(scale_notes, color_map)
        print("G major scale with colored degrees (I=red, III=yellow, V=green)")

def example_pentatonic():
    """Example 3: Minor pentatonic scale"""
    print("\nExample 3: A Minor Pentatonic")

    with Linnstrument() as linn:
        scale_notes = get_scale_notes('A', 'minor_pentatonic')
        linn.light_scale(scale_notes, root_color='blue', scale_color='cyan')
        print("A minor pentatonic scale is lit up!")

def example_mode_exploration():
    """Example 4: Cycle through all modes"""
    print("\nExample 4: Cycling Through All Modes of C")

    modes = ['ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']

    with Linnstrument() as linn:
        for mode in modes:
            print(f"  Showing {mode}...")
            scale_notes = get_scale_notes('C', mode)
            linn.light_scale(scale_notes, root_color='red', scale_color='green')
            time.sleep(2)  # Display each mode for 2 seconds

def example_chord_tones():
    """Example 5: Highlight chord tones in a scale"""
    print("\nExample 5: Highlight Chord Tones (I, III, V, VII) in D Major")

    with Linnstrument() as linn:
        scale_notes = get_scale_notes('D', 'major')
        color_map = {
            0: 'red',      # Root
            2: 'yellow',   # Third
            4: 'green',    # Fifth
            6: 'cyan',     # Seventh
        }
        linn.light_scale_with_degrees(scale_notes, color_map)
        print("D major with chord tones highlighted")

def example_jazz_scales():
    """Example 6: Common jazz scales"""
    print("\nExample 6: Jazz Scales")

    jazz_scales = [
        ('C', 'bebop_major', 'Bebop Major'),
        ('D', 'dorian', 'Dorian'),
        ('G', 'altered', 'Altered (for V7alt)'),
        ('C', 'melodic_minor', 'Melodic Minor'),
    ]

    with Linnstrument() as linn:
        for root, scale, description in jazz_scales:
            print(f"  {root} {description}")
            scale_notes = get_scale_notes(root, scale)
            linn.light_scale(scale_notes, root_color='red', scale_color='blue')
            time.sleep(3)

def example_exotic_scales():
    """Example 7: Exotic and world scales"""
    print("\nExample 7: Exotic Scales")

    exotic_scales = [
        ('A', 'japanese', 'Japanese'),
        ('E', 'spanish', 'Spanish (Phrygian Dominant)'),
        ('D', 'hungarian_minor', 'Hungarian Minor'),
        ('C', 'double_harmonic', 'Double Harmonic (Byzantine)'),
    ]

    with Linnstrument() as linn:
        for root, scale, description in exotic_scales:
            print(f"  {root} {description}")
            scale_notes = get_scale_notes(root, scale)
            linn.light_scale(scale_notes, root_color='magenta', scale_color='orange')
            time.sleep(3)

def example_custom_note_lighting():
    """Example 8: Light up specific notes manually"""
    print("\nExample 8: Custom Note Pattern")

    with Linnstrument() as linn:
        linn.clear_all_lights()

        # Light up a C major triad across all octaves
        triad = [0, 4, 7]  # Root, major third, perfect fifth
        root = note_name_to_number('C')

        for octave in range(-1, 9):
            for interval in triad:
                note = root + (octave * 12) + interval
                if 0 <= note <= 127:
                    if interval == 0:
                        linn.light_note(note, 'red')  # Root
                    elif interval == 4:
                        linn.light_note(note, 'yellow')  # Third
                    else:
                        linn.light_note(note, 'green')  # Fifth

        print("C major triad lit up across all octaves")

def example_list_all_scales():
    """Example 9: List all available scales"""
    print("\nExample 9: All Available Scales")
    print("-" * 40)

    scales = get_available_scales()
    for i, scale in enumerate(scales, 1):
        print(f"{i:2d}. {scale}")

    print(f"\nTotal: {len(scales)} scales available")

def main():
    """Run all examples with user confirmation"""
    examples = [
        example_basic_scale,
        example_scale_degrees,
        example_pentatonic,
        example_chord_tones,
        example_jazz_scales,
        example_exotic_scales,
        example_custom_note_lighting,
        example_mode_exploration,
        example_list_all_scales,
    ]

    print("=== Linnstrument Scale Tool Examples ===\n")

    for i, example_func in enumerate(examples, 1):
        print(f"\n{'='*50}")
        try:
            example_func()
        except Exception as e:
            print(f"Error in example: {e}")

        if i < len(examples):
            input("\nPress Enter to continue to next example...")

    print("\n" + "="*50)
    print("Examples complete!")

if __name__ == '__main__':
    main()
