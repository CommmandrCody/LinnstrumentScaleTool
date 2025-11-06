#!/usr/bin/env python3
"""
Linnstrument Scale Light - Python backend for Max for Live device

This script is called by Max/MSP to control Linnstrument lights
based on the scale selected in Ableton Live.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from scales import get_scale_notes, note_name_to_number
from linnstrument import Linnstrument

def set_scale(root_note, scale_name, root_color='red', scale_color='blue',
              use_degrees=False, linnstrument_port=None):
    """
    Set Linnstrument lights to show a scale

    Args:
        root_note: Root note name (e.g., 'C', 'D#') or number (0-11)
        scale_name: Scale name from scales.py
        root_color: Color for root notes
        scale_color: Color for other scale notes
        use_degrees: Use degree coloring (I, III, V)
        linnstrument_port: Specific port name or None for auto-detect

    Returns:
        dict: Status message
    """
    try:
        # Convert root note if string
        if isinstance(root_note, str):
            root_note = note_name_to_number(root_note)

        # Get scale notes
        scale_notes = get_scale_notes(root_note, scale_name)

        # Connect to Linnstrument
        with Linnstrument(port_name=linnstrument_port) as linn:
            if use_degrees:
                linn.light_scale_with_degrees(scale_notes)
            else:
                linn.light_scale(scale_notes, root_color, scale_color)

        return {
            'success': True,
            'message': f'Lit up {root_note} {scale_name}',
            'note_count': len(scale_notes)
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def clear_lights(linnstrument_port=None):
    """Clear all Linnstrument lights"""
    try:
        with Linnstrument(port_name=linnstrument_port) as linn:
            linn.clear_all_lights()

        return {'success': True, 'message': 'Lights cleared'}

    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    """Command-line interface for Max/MSP to call"""
    if len(sys.argv) < 2:
        print(json.dumps({'success': False, 'error': 'No command specified'}))
        return 1

    command = sys.argv[1]

    if command == 'set_scale':
        # Expected: set_scale <root> <scale> [root_color] [scale_color] [use_degrees] [port]
        if len(sys.argv) < 4:
            print(json.dumps({'success': False, 'error': 'Missing arguments'}))
            return 1

        root = sys.argv[2]
        scale = sys.argv[3]
        root_color = sys.argv[4] if len(sys.argv) > 4 else 'red'
        scale_color = sys.argv[5] if len(sys.argv) > 5 else 'blue'
        use_degrees = sys.argv[6].lower() == 'true' if len(sys.argv) > 6 else False
        port = sys.argv[7] if len(sys.argv) > 7 else None

        result = set_scale(root, scale, root_color, scale_color, use_degrees, port)
        print(json.dumps(result))

    elif command == 'clear':
        # Expected: clear [port]
        port = sys.argv[2] if len(sys.argv) > 2 else None
        result = clear_lights(port)
        print(json.dumps(result))

    else:
        print(json.dumps({'success': False, 'error': f'Unknown command: {command}'}))
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
