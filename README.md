# Linnstrument Scale Tool

Automatically set the lights on your Linnstrument to reflect any musical scale of your choice. This tool uses MIDI CC messages to control the LED colors on each pad, making it easy to visualize scales, modes, and other musical patterns.

## Three Ways to Use

1. **Command Line Tool** - Simple, fast, universal (recommended)
2. **Ableton MIDI Remote Script** - Automatic Ableton integration via track names
3. **MIDI Effect Plugin** - Works with any DAW, auto-detects scales (advanced)

## Features

- **30+ Built-in Scales**: Major, minor, modes, pentatonics, blues, jazz, exotic scales, and more
- **Flexible Coloring**: Root notes, scale degrees, or custom color schemes
- **Auto-detection**: Automatically finds your Linnstrument MIDI port
- **Configurable**: Supports custom Linnstrument tunings and layouts
- **Multiple Interfaces**: Command-line, Ableton MIDI Remote Script, and MIDI effect plugin
- **Ableton Integration**: Name your tracks "C Major" and lights update automatically!

## Quick Install

Run the setup script for guided installation:

```bash
python setup.py
```

Or install manually:

## Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Make the script executable (optional):

```bash
chmod +x scale_tool.py
```

## Quick Start

### Basic Usage

Light up a C major scale:
```bash
python scale_tool.py C major
```

Light up D minor pentatonic:
```bash
python scale_tool.py D minor_pentatonic
```

Light up F# Dorian mode:
```bash
python scale_tool.py F# dorian
```

### Color Options

Use custom colors for root and scale notes:
```bash
python scale_tool.py G major --root-color red --scale-color green
```

Highlight scale degrees (I, III, V) with different colors:
```bash
python scale_tool.py C major --degrees
```

Use custom color mapping for specific scale degrees:
```bash
python scale_tool.py A minor --colors '{"0": "red", "2": "yellow", "4": "green", "6": "cyan"}'
```

### Available Colors

- red
- yellow
- green
- cyan
- blue
- magenta
- white
- orange
- lime
- pink
- off

List all colors:
```bash
python scale_tool.py --list-colors
```

## Available Scales

### Major Scales and Modes
- `major` (Ionian)
- `dorian`
- `phrygian`
- `lydian`
- `mixolydian`
- `aeolian` (Natural Minor)
- `locrian`

### Minor Scales
- `minor` (Natural Minor)
- `harmonic_minor`
- `melodic_minor`

### Pentatonic Scales
- `major_pentatonic`
- `minor_pentatonic`

### Blues
- `blues`

### Other Common Scales
- `whole_tone`
- `chromatic`
- `diminished`
- `augmented`

### Jazz/Advanced
- `bebop_major`
- `bebop_minor`
- `altered` (Super Locrian)

### Exotic Scales
- `harmonic_major`
- `double_harmonic` (Byzantine)
- `hungarian_minor`
- `japanese`
- `spanish` (Phrygian Dominant)

List all available scales:
```bash
python scale_tool.py --list-scales
```

## Advanced Usage

### Custom Linnstrument Tuning

If you've customized your Linnstrument tuning, you can specify the offsets:

```bash
python scale_tool.py C major --row-offset 7 --column-offset 1
```

### Specify MIDI Port

If you have multiple MIDI devices, specify the port:

```bash
python scale_tool.py C major --port "Linnstrument MIDI 1"
```

List available MIDI ports:
```bash
python scale_tool.py --list-ports
```

### Clear All Lights

Turn off all LEDs:
```bash
python scale_tool.py --clear
```

## Using as a Python Library

You can also use the modules directly in your own Python code:

```python
from scales import get_scale_notes, note_name_to_number
from linnstrument import Linnstrument

# Get scale notes
root = note_name_to_number('C')
scale_notes = get_scale_notes(root, 'major')

# Connect to Linnstrument
with Linnstrument() as linn:
    # Light up the scale
    linn.light_scale(scale_notes, root_color='red', scale_color='blue')

    # Or use degree coloring
    linn.light_scale_with_degrees(scale_notes)

    # Or light individual notes
    linn.light_note(60, 'green')  # Middle C
```

## How It Works

The tool uses MIDI Control Change (CC) messages to control the Linnstrument LEDs:

- **CC 20**: Column coordinate (0-25)
- **CC 21**: Row coordinate (0-7)
- **CC 22**: Color value (0-11)

The tool calculates which pads on the Linnstrument correspond to notes in your chosen scale, then sends MIDI messages to light them up with your specified colors.

## Troubleshooting

### "No Linnstrument MIDI port found"

1. Make sure your Linnstrument is connected via USB
2. Check that it appears in your system's MIDI devices
3. Run `python scale_tool.py --list-ports` to see available ports
4. If it appears with a different name, use `--port "exact name"`

### LEDs not lighting up

1. Make sure your Linnstrument firmware is up to date
2. Check that MIDI CC is enabled in your Linnstrument settings
3. Try clearing all lights first: `python scale_tool.py --clear`

### Wrong notes are lighting up

1. Check your Linnstrument tuning settings
2. Adjust `--row-offset` and `--column-offset` to match your configuration
3. Default is: row offset = 5 semitones, column offset = 1 semitone

## Examples

### Jazz Practice
```bash
# Dorian mode for modal jazz
python scale_tool.py D dorian --degrees

# Altered scale for dominant chords
python scale_tool.py G altered --root-color red --scale-color cyan
```

### Blues
```bash
# Classic blues scale
python scale_tool.py E blues --root-color blue --scale-color cyan
```

### World Music
```bash
# Japanese pentatonic
python scale_tool.py A japanese --degrees

# Hungarian minor
python scale_tool.py D hungarian_minor --degrees
```

## License

MIT License - feel free to use and modify as you wish.

## Contributing

Found a bug or want to add a scale? Feel free to submit issues or pull requests!

## Credits

Built using:
- [mido](https://mido.readthedocs.io/) - MIDI library for Python
- [python-rtmidi](https://github.com/SpotlightKid/python-rtmidi) - Python bindings for RtMidi

Linnstrument is a product of Roger Linn Design.
