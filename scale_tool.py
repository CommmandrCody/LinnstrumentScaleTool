#!/usr/bin/env python3
"""
Linnstrument Scale Tool - Main Command Line Interface
Automatically sets Linnstrument lights to reflect musical scales
"""

import argparse
import sys
from scales import get_scale_notes, get_available_scales, note_name_to_number, NOTE_NAMES
from linnstrument import Linnstrument

def main():
    parser = argparse.ArgumentParser(
        description='Set Linnstrument lights to display musical scales',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s C major                    # Light up C major scale
  %(prog)s D minor --root-color red   # D minor with red root notes
  %(prog)s F# dorian --degrees        # F# Dorian with colored scale degrees
  %(prog)s G minor_pentatonic --colors '{"0": "red", "2": "yellow"}'
  %(prog)s --list-scales              # Show all available scales
  %(prog)s --list-ports               # Show MIDI ports
  %(prog)s --clear                    # Clear all lights
        """
    )

    # Positional arguments
    parser.add_argument('root', nargs='?', type=str,
                       help='Root note (e.g., C, D#, Eb)')
    parser.add_argument('scale', nargs='?', type=str,
                       help='Scale name (e.g., major, minor, dorian)')

    # Options
    parser.add_argument('--port', type=str,
                       help='MIDI port name (auto-detected if not specified)')
    parser.add_argument('--channel', type=int, default=0,
                       help='MIDI channel (0-15, default: 0)')
    parser.add_argument('--root-color', type=str, default='red',
                       help='Color for root notes (default: red)')
    parser.add_argument('--scale-color', type=str, default='blue',
                       help='Color for other scale notes (default: blue)')
    parser.add_argument('--degrees', action='store_true',
                       help='Use different colors for scale degrees (I=red, III=yellow, V=green)')
    parser.add_argument('--colors', type=str,
                       help='Custom color map as JSON string (e.g., \'{"0": "red", "2": "yellow"}\')')

    # Linnstrument tuning
    parser.add_argument('--row-offset', type=int, default=5,
                       help='Semitones between rows (default: 5)')
    parser.add_argument('--column-offset', type=int, default=1,
                       help='Semitones between columns (default: 1)')
    parser.add_argument('--base-note', type=int, default=0,
                       help='MIDI note at position (0,0) (default: 0=C-1)')

    # Info commands
    parser.add_argument('--list-scales', action='store_true',
                       help='List all available scales')
    parser.add_argument('--list-ports', action='store_true',
                       help='List available MIDI ports')
    parser.add_argument('--list-colors', action='store_true',
                       help='List available colors')
    parser.add_argument('--clear', action='store_true',
                       help='Clear all lights')

    args = parser.parse_args()

    # Handle info commands
    if args.list_scales:
        print("Available scales:")
        for scale in get_available_scales():
            print(f"  {scale}")
        return 0

    if args.list_ports:
        print("Available MIDI ports:")
        for port in Linnstrument.list_available_ports():
            print(f"  {port}")
        return 0

    if args.list_colors:
        print("Available colors:")
        for color in Linnstrument.get_color_names():
            print(f"  {color}")
        return 0

    # Connect to Linnstrument
    try:
        linn = Linnstrument(
            port_name=args.port,
            channel=args.channel,
            row_offset=args.row_offset,
            column_offset=args.column_offset,
            base_note=args.base_note
        )
    except Exception as e:
        print(f"Error connecting to Linnstrument: {e}", file=sys.stderr)
        return 1

    try:
        # Clear lights if requested
        if args.clear:
            print("Clearing all lights...")
            linn.clear_all_lights()
            print("Done!")
            return 0

        # Validate required arguments
        if not args.root or not args.scale:
            parser.error("root and scale are required (unless using --clear, --list-scales, etc.)")

        # Get scale notes
        try:
            root_note = note_name_to_number(args.root)
            scale_notes = get_scale_notes(root_note, args.scale)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

        # Display the scale
        print(f"Lighting up {args.root} {args.scale} scale...")

        if args.colors:
            # Custom color map
            import json
            try:
                color_map = json.loads(args.colors)
                # Convert string keys to integers
                color_map = {int(k): v for k, v in color_map.items()}
                linn.light_scale_with_degrees(scale_notes, color_map)
            except json.JSONDecodeError as e:
                print(f"Error parsing color map: {e}", file=sys.stderr)
                return 1
        elif args.degrees:
            # Use default degree coloring
            linn.light_scale_with_degrees(scale_notes)
        else:
            # Simple two-color mode
            linn.light_scale(scale_notes, args.root_color, args.scale_color)

        print("Done!")
        return 0

    finally:
        linn.close()

if __name__ == '__main__':
    sys.exit(main())
