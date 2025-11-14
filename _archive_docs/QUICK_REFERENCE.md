# Quick Reference Card - Linnstrument Scale Tool

## Installation (One Time)

```bash
./install.sh
```

## Basic Usage

```bash
# Simple way (auto-activates venv)
./run.sh C major
./run.sh D minor
./run.sh G dorian

# Manual way (activate venv first)
source venv/bin/activate
python scale_tool.py C major
```

## Common Commands

```bash
# Basic scales
./run.sh C major
./run.sh A minor
./run.sh E dorian

# With degree coloring (I, III, V)
./run.sh C major --degrees

# Custom colors
./run.sh D minor --root-color red --scale-color cyan

# Pentatonics
./run.sh A minor_pentatonic
./run.sh G major_pentatonic

# Blues
./run.sh E blues

# Jazz
./run.sh D dorian --degrees
./run.sh G altered
./run.sh C bebop_major

# Clear all lights
./run.sh --clear

# List options
./run.sh --list-scales
./run.sh --list-colors
./run.sh --list-ports
```

## Popular Scales

| Scale | Description | Example |
|-------|-------------|---------|
| `major` | Major scale (Ionian) | `./run.sh C major` |
| `minor` | Natural minor (Aeolian) | `./run.sh A minor` |
| `dorian` | Dorian mode (jazz) | `./run.sh D dorian` |
| `phrygian` | Phrygian mode | `./run.sh E phrygian` |
| `lydian` | Lydian mode | `./run.sh F lydian` |
| `mixolydian` | Mixolydian mode | `./run.sh G mixolydian` |
| `major_pentatonic` | 5-note major scale | `./run.sh C major_pentatonic` |
| `minor_pentatonic` | 5-note minor scale | `./run.sh A minor_pentatonic` |
| `blues` | Blues scale | `./run.sh E blues` |
| `harmonic_minor` | Harmonic minor | `./run.sh A harmonic_minor` |
| `melodic_minor` | Melodic minor | `./run.sh C melodic_minor` |
| `altered` | Altered scale (jazz) | `./run.sh G altered` |
| `whole_tone` | Whole tone scale | `./run.sh C whole_tone` |

## Colors

| Color | Example |
|-------|---------|
| `red` | Root notes |
| `yellow` | Thirds |
| `green` | Fifths |
| `cyan` | Cool accent |
| `blue` | Scale notes |
| `magenta` | Bright accent |
| `white` | Bright |
| `orange` | Warm |
| `lime` | Bright green |
| `pink` | Soft accent |
| `off` | Turn off |

## Advanced Options

```bash
# Different Linnstrument port
./run.sh C major --port "LinnStrument MIDI 2"

# Different MIDI channel
./run.sh C major --channel 1

# Custom tuning (if you changed row/column offsets)
./run.sh C major --row-offset 7 --column-offset 1
```

## For Ableton Live Users

### Max for Live Device

1. Copy `max_for_live/LinnstrumentScaleLight.maxpat` to:
   - Mac: `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/`
2. Restart Ableton
3. Drag device onto MIDI track
4. Select scale and click "Update Lights"

### MIDI Effect Plugin (Auto-detect)

```bash
# In terminal (while Ableton is running):
source venv/bin/activate
python vst_plugin/midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "LinnStrument MIDI"
```

See `vst_plugin/README.md` for full setup.

## Troubleshooting

### Command not found: ./run.sh
```bash
chmod +x install.sh run.sh
./install.sh
```

### No Linnstrument found
```bash
# Check it's connected and appears in ports
./run.sh --list-ports
```

### Dependencies error
```bash
# Re-run installer
./install.sh
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf venv
./install.sh
```

## Files

| File | Purpose |
|------|---------|
| `./run.sh` | Quick launcher (use this!) |
| `scale_tool.py` | Main CLI tool |
| `examples.py` | Interactive demos |
| `max_for_live/` | Ableton device |
| `vst_plugin/` | MIDI effect |

## Help

```bash
./run.sh --help                    # Command help
cat START_HERE.md                  # Getting started
cat README.md                      # Full docs
cat max_for_live/README.md         # Ableton setup
python examples.py                 # Interactive demos
```

## Tips

1. **Degree coloring** shows chord tones (I=red, III=yellow, V=green)
2. **Match Ableton scales** for consistency
3. **Blues scale** great for jam sessions
4. **Exotic scales** for inspiration
5. **Clear before switching** for best results

---

**Quick Start:** `./run.sh C major`

**Your Linnstrument is ready! 🎹✨**
