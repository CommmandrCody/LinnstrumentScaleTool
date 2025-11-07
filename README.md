# Linnstrument Scale Tool

Automatically light up your Linnstrument to show any musical scale. Works standalone or integrates with Ableton Live to automatically match the project's scale settings.

## Two Ways to Use

1. **Ableton Live MIDI Remote Script** - Automatic integration with Ableton's scale settings (recommended for Ableton users)
2. **Command Line Tool** - Simple, fast, universal - works with any DAW or standalone

## Features

- **Automatic Ableton Integration**: Lights update automatically when you change Ableton's scale settings
- **Track Color Matching**: LED colors adapt based on selected track color (like Ableton Push)
- **30+ Built-in Scales**: Major, minor, modes, pentatonics, blues, jazz, exotic scales, and more
- **Supports Linnstrument 128 and 200**: Separate optimized scripts for each model
- **Two-Color Display**: Root notes in one color, other scale notes in another
- **Auto-detection**: Automatically finds your Linnstrument MIDI port (command-line tool)
- **Configurable**: Supports custom Linnstrument tunings and layouts

## Installation

### Option 1: Ableton Live MIDI Remote Script (Recommended for Ableton Users)

This provides seamless integration with Ableton Live - lights update automatically when you change the scale!

1. **Choose your Linnstrument model:**
   - For **Linnstrument 128** (16 columns): Use `LinnstrumentScale128`
   - For **Linnstrument 200** (26 columns): Use `LinnstrumentScale200`

2. **Copy the appropriate folder to your Ableton Remote Scripts directory:**

   **macOS:**
   ```bash
   cp -r ableton_remote_script/LinnstrumentScale128 ~/Music/Ableton/User\ Library/Remote\ Scripts/
   ```

   **Windows:**
   ```
   Copy ableton_remote_script\LinnstrumentScale128 to:
   %USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
   ```

3. **Configure your Linnstrument:**
   - Press bottom-left pad and note what MIDI note it plays
   - Edit `LinnstrumentScale.py` line 99 and set `LINNSTRUMENT_BASE_NOTE` to that note number
   - Common values: 36 (C2, Push-style), 48 (C3, factory default), 40 (E2, guitar tuning)

4. **Enable in Ableton:**
   - Open Ableton Live Preferences > Link/Tempo/MIDI
   - In the MIDI Ports section, find your Linnstrument
   - Under "Control Surface", select "LinnstrumentScale128" (or 200)
   - Under "Input", select your Linnstrument MIDI port
   - Under "Output", select your Linnstrument MIDI port

5. **Done!** Now when you change Ableton's scale (Cmd+Shift+S or Preferences > Scales), your Linnstrument lights will update automatically!

### Option 2: Command Line Tool

For standalone use or with other DAWs:

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

### Ableton Live Integration

Once installed, the script works automatically:

1. **Change Scale**: Press Cmd+Shift+S (Mac) or Ctrl+Shift+S (Windows) to open Scale settings
2. **Select Root & Scale**: Choose your root note and scale type
3. **Watch Lights Update**: Your Linnstrument LEDs automatically update to show the scale!

**Track Colors**: The LED colors adapt based on your selected track's color in Ableton, similar to how Push works.

**What You'll See**:
- Brighter color for root notes
- Related color for other scale notes
- Colors change with track selection

### Command Line Tool Usage

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

### Ableton Integration Issues

**LEDs not lighting up in Ableton:**
1. Check that "LinnstrumentScale128" (or 200) is selected as Control Surface in Ableton MIDI preferences
2. Make sure both Input and Output are set to your Linnstrument MIDI port
3. Check the Ableton Log.txt file for error messages (Help > Show Log)
4. Verify Global Settings button on Linnstrument is lit (yellow = User Firmware Mode active)
5. Restart Ableton Live after installing the script

**Wrong pads lighting up:**
1. Verify you're using the correct script (LinnstrumentScale128 for 16 columns, LinnstrumentScale200 for 26 columns)
2. Check the `LINNSTRUMENT_BASE_NOTE` setting matches your Linnstrument configuration
   - Press bottom-left pad and note the MIDI note number
   - Edit line 99 in `LinnstrumentScale.py` to match
3. Verify row offset is set correctly (line 104):
   - Most common: 5 semitones (fourths, like Push)
   - Guitar tuning: 5 semitones
   - Factory default: 5 semitones

**Global Settings button not turning yellow:**
- The script sends NRPN 245=1 to enable User Firmware Mode
- If it doesn't activate, try manually: Press and hold "OS Update" in Global Settings for half a second

### Command Line Tool Issues

**"No Linnstrument MIDI port found":**
1. Make sure your Linnstrument is connected via USB
2. Check that it appears in your system's MIDI devices
3. Run `python scale_tool.py --list-ports` to see available ports
4. If it appears with a different name, use `--port "exact name"`

**LEDs not lighting up:**
1. Make sure your Linnstrument firmware is up to date
2. Try clearing all lights first: `python scale_tool.py --clear`

**Wrong notes are lighting up:**
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
