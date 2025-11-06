# 🎹 START HERE - Linnstrument Scale Tool

Welcome! This tool automatically lights up your Linnstrument to show any musical scale.

## ⚡ Quick Start (30 seconds)

```bash
# 1. Install (one time)
./install.sh

# 2. Try it!
./run.sh C major
```

Your Linnstrument should now light up with C major scale! 🎉

**Note**: The installer creates a virtual environment (required on macOS with Homebrew Python)

## 🎯 Choose Your Method

### For Quick Use → **Command Line Tool** (Recommended)
Fast and simple!
- **Try**: `./run.sh D minor`
- **Time**: Instant
- **Difficulty**: Very Easy

### For Ableton Live Users → **Max for Live Device**
Perfect integration with Ableton!
- **See**: `max_for_live/README.md`
- **Time**: 5 minutes to setup
- **Difficulty**: Easy

### For Any DAW (Advanced) → **MIDI Effect Plugin**
Auto-detects scales as you play!
- **See**: `vst_plugin/README.md`
- **Works with**: Logic, FL Studio, Cubase, Reaper, etc.
- **Time**: 10 minutes to setup
- **Difficulty**: Medium (requires virtual MIDI routing)

## 📚 Documentation

- **`QUICK_START.md`** - Get started in 5 minutes
- **`README.md`** - Full documentation
- **`PROJECT_SUMMARY.md`** - Overview of everything
- **`ARCHITECTURE.md`** - Technical details

## 🎼 30+ Scales Available

Major, minor, dorian, phrygian, lydian, mixolydian, pentatonics, blues, jazz scales, exotic scales, and more!

```bash
python scale_tool.py --list-scales
```

## 🎨 11 Colors Available

Red, yellow, green, cyan, blue, magenta, white, orange, lime, pink, off

```bash
python scale_tool.py C major --root-color red --scale-color blue
```

## 💡 Examples

```bash
# If you used install.sh, use ./run.sh:
./run.sh C major
./run.sh A minor
./run.sh D dorian --degrees

# Or activate venv manually and use python:
source venv/bin/activate

# Basic scales
python scale_tool.py C major
python scale_tool.py A minor
python scale_tool.py D dorian

# Pentatonics
python scale_tool.py E minor_pentatonic
python scale_tool.py G major_pentatonic

# Jazz
python scale_tool.py D dorian --degrees
python scale_tool.py G altered

# Blues
python scale_tool.py E blues

# Exotic
python scale_tool.py A japanese
python scale_tool.py D hungarian_minor

# Custom colors
python scale_tool.py F# lydian --root-color magenta --scale-color cyan

# Clear lights
python scale_tool.py --clear
```

## 🎮 Interactive Demo

```bash
python examples.py
```

This will walk you through various examples interactively!

## 🔧 Troubleshooting

### Linnstrument not found?
```bash
# Check your ports:
python scale_tool.py --list-ports

# Make sure Linnstrument is connected via USB
```

### Dependencies not installed?
```bash
pip install -r requirements.txt
```

### Need help?
```bash
python scale_tool.py --help
```

## 🎯 Common Workflows

### Practice Session
```bash
# Show the scale you're practicing
python scale_tool.py G major --degrees

# The I, III, and V will be different colors
```

### Composition
```bash
# Try different scales quickly
python scale_tool.py C ionian
python scale_tool.py C dorian
python scale_tool.py C phrygian
# ... cycle through modes
```

### Live Performance (with Ableton)
1. Open Ableton Live
2. Add the Max for Live device to a MIDI track
3. Select your scale
4. Click "Update Lights"
5. Play!

## 📖 What Each File Does

| File | Purpose |
|------|---------|
| `scale_tool.py` | Command-line interface (easiest to start) |
| `scales.py` | All scale definitions |
| `linnstrument.py` | Controls the LED lights |
| `examples.py` | Interactive demonstrations |
| `setup.py` | Guided installation |
| `max_for_live/` | Ableton Live integration |
| `vst_plugin/` | MIDI effect with auto-detect |

## 🚀 Next Steps

1. **Try the command line tool** - Start with `python scale_tool.py C major`
2. **Explore scales** - Try different modes and scales
3. **Try degree coloring** - Add `--degrees` to highlight chord tones
4. **Run examples** - `python examples.py` for guided tour
5. **If using Ableton** - Install the Max for Live device
6. **Advanced users** - Try the MIDI effect plugin with auto-detection

## 💬 Questions?

Check these docs:
- **QUICK_START.md** - Quick reference
- **README.md** - Complete guide
- **max_for_live/README.md** - Ableton setup
- **vst_plugin/README.md** - MIDI effect setup

## 🎵 Tips

- Use **degree coloring** (`--degrees`) to learn scale shapes
- Try **exotic scales** for inspiration (japanese, spanish, hungarian_minor)
- Match scales to **Ableton's scale highlighting** for consistency
- Use **blues scale** for jam sessions
- Try **altered scale** for jazz dominant chords

---

**Ready? Let's light it up! 🎹✨**

```bash
python scale_tool.py C major
```

Enjoy your illuminated Linnstrument!
