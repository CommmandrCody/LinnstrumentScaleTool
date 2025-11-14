# Quick Start Guide - Linnstrument Scale Tool

Choose your preferred method:

## Option 1: Max for Live (Best for Ableton Users)

Perfect integration with Ableton Live!

### Setup (5 minutes)

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Copy Max device to Ableton**:
   - Copy `max_for_live/LinnstrumentScaleLight.maxpat` to:
     - Mac: `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/`
     - Windows: `\Users\[username]\Documents\Ableton\User Library\Presets\MIDI Effects\Max MIDI Effect\`

3. **Restart Ableton Live**

### Usage

1. Drag the device onto any MIDI track
2. Choose root note and scale from drop-downs
3. Click "Update Lights"
4. Your Linnstrument pads light up showing the scale!

**See**: `max_for_live/README.md` for full details

---

## Option 2: Command Line Tool (Universal)

Works with any DAW or standalone!

### Setup (2 minutes)

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Light up C major
python scale_tool.py C major

# D minor with custom colors
python scale_tool.py D minor --root-color red --scale-color cyan

# F# Dorian with degree colors (I, III, V highlighted)
python scale_tool.py F# dorian --degrees

# Clear all lights
python scale_tool.py --clear

# See all available scales
python scale_tool.py --list-scales
```

**See**: `README.md` for full documentation

---

## Option 3: MIDI Effect Plugin (Advanced)

Automatically detects scales as you play!

### Setup

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Auto-detect mode
python vst_plugin/midi_effect_plugin.py \
  --input "IAC Bus 1" \
  --output "Linnstrument MIDI 1"

# Manual scale mode
python vst_plugin/midi_effect_plugin.py \
  --input "IAC Bus 1" \
  --output "Linnstrument MIDI 1" \
  --root C --scale major --no-auto-detect
```

**See**: `vst_plugin/README.md` for setup guide

---

## Which Method Should I Use?

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **Command Line** | Quick use, any DAW | Simple, fast, universal | Manual operation |
| **Max for Live** | Ableton users | Perfect integration, GUI controls | Requires Ableton + Max for Live |
| **MIDI Effect** | Any DAW (advanced) | Auto-detects scales, live use | Requires MIDI routing setup |

---

## Troubleshooting

### "No Linnstrument MIDI port found"
1. Connect Linnstrument via USB
2. Check it appears in your system's MIDI devices
3. Run: `python scale_tool.py --list-ports`

### "No module named 'mido'"
Install dependencies: `pip install -r requirements.txt`

### Lights don't update
1. Try clearing first: `python scale_tool.py --clear`
2. Check your Linnstrument firmware is up to date
3. Verify MIDI CC is enabled in Linnstrument settings

---

## Examples

### Jazz Practice
```bash
python scale_tool.py D dorian --degrees
python scale_tool.py G altered --root-color red --scale-color cyan
```

### Blues
```bash
python scale_tool.py E blues --root-color blue --scale-color cyan
```

### World Music
```bash
python scale_tool.py A japanese --degrees
python scale_tool.py D hungarian_minor --degrees
```

### Interactive Examples
```bash
python examples.py
```

---

## Available Scales (30+)

**Modes**: major, dorian, phrygian, lydian, mixolydian, aeolian, locrian

**Minor**: minor, harmonic_minor, melodic_minor

**Pentatonic**: major_pentatonic, minor_pentatonic

**Jazz**: bebop_major, bebop_minor, altered

**Blues**: blues

**Exotic**: spanish, hungarian_minor, japanese, double_harmonic

**Other**: whole_tone, chromatic, diminished, augmented

*Run `python scale_tool.py --list-scales` for complete list*

---

## Available Colors

red, yellow, green, cyan, blue, magenta, white, orange, lime, pink, off

---

## Getting Help

- Command line help: `python scale_tool.py --help`
- Max for Live help: See `max_for_live/README.md`
- Full documentation: See `README.md`
- Examples: Run `python examples.py`

---

## What's Next?

1. Try different scales and color combinations
2. Match your Linnstrument lights to Ableton's scale highlighting
3. Use degree coloring to learn scale patterns
4. Automate scale changes in your performances
5. Create custom scale visualizations for teaching

Enjoy your illuminated Linnstrument!
