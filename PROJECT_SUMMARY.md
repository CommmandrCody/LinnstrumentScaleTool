# Linnstrument Scale Tool - Project Summary

## Overview

A complete toolset for automatically controlling Linnstrument LED lights to display musical scales. Built with Python and available in multiple interfaces to suit different workflows.

## Project Structure

```
LinnstrumentScaleTool/
├── Core Python Modules
│   ├── scales.py                    # 30+ scale definitions
│   ├── linnstrument.py              # MIDI LED control
│   └── scale_tool.py                # Command-line interface
│
├── Max for Live Device
│   ├── max_for_live/
│   │   ├── LinnstrumentScaleLight.maxpat   # M4L device
│   │   ├── linnstrument_scale_light.py     # Python backend
│   │   └── README.md                       # M4L documentation
│
├── MIDI Effect Plugin
│   ├── vst_plugin/
│   │   ├── midi_effect_plugin.py           # Standalone MIDI effect
│   │   └── README.md                       # Plugin documentation
│
├── Documentation
│   ├── README.md                    # Full documentation
│   ├── QUICK_START.md              # Quick start guide
│   ├── PROJECT_SUMMARY.md          # This file
│   └── examples.py                 # Interactive examples
│
└── Setup
    ├── setup.py                    # Guided installation
    ├── requirements.txt            # Python dependencies
    └── .gitignore                  # Git ignore rules
```

## Components

### 1. Core Library (`scales.py`, `linnstrument.py`)

**Purpose**: Reusable Python modules for scale logic and MIDI control

**Features**:
- 30+ scale definitions (modes, pentatonics, jazz, exotic)
- MIDI CC-based LED control (CC 20, 21, 22)
- Automatic Linnstrument port detection
- Configurable tuning (row/column offsets)
- Color palette (11 colors)

**Usage**:
```python
from scales import get_scale_notes
from linnstrument import Linnstrument

scale_notes = get_scale_notes('C', 'major')
with Linnstrument() as linn:
    linn.light_scale(scale_notes)
```

### 2. Command-Line Tool (`scale_tool.py`)

**Purpose**: Fast, simple CLI for lighting up scales

**Best For**:
- Quick scale reference
- Practice sessions
- Any DAW or standalone use

**Usage**:
```bash
python scale_tool.py C major
python scale_tool.py D minor_pentatonic --degrees
python scale_tool.py --list-scales
```

**Pros**: Simple, fast, no dependencies on DAW
**Cons**: Manual operation for each scale change

### 3. Max for Live Device

**Purpose**: Native Ableton Live integration

**Best For**:
- Ableton Live users
- Live performance with preset scales
- Visual workflow with GUI

**Features**:
- Drop-down menus for root note and scale
- Toggle for degree coloring
- Update/Clear buttons
- Live parameter automation

**Usage**:
1. Install in Ableton User Library
2. Drag onto MIDI track
3. Select scale from menus
4. Click "Update Lights"

**Pros**: Perfect Ableton integration, GUI, automatable
**Cons**: Requires Ableton Live + Max for Live

### 4. MIDI Effect Plugin (`vst_plugin/midi_effect_plugin.py`)

**Purpose**: Standalone MIDI effect with scale auto-detection

**Best For**:
- Live performance
- Practice (shows what you're playing)
- Advanced users comfortable with MIDI routing

**Features**:
- Auto-detects scales from played notes
- Manual scale mode
- Passes MIDI through (no latency)
- Works with any DAW

**Usage**:
```bash
python midi_effect_plugin.py \
  --input "IAC Bus 1" \
  --output "Linnstrument MIDI 1" \
  --auto-detect
```

**Pros**: Auto-detection, works with any DAW
**Cons**: Requires virtual MIDI bus setup

## Technical Details

### MIDI Implementation

Linnstrument LED control uses three MIDI CC messages:
- **CC 20**: Column coordinate (0-25)
- **CC 21**: Row coordinate (0-7)
- **CC 22**: Color value (0-11)

### Default Linnstrument Layout

- **26 columns × 8 rows** = 208 pads
- **Default tuning**: 5 semitones per row, 1 semitone per column
- **Base note**: C-1 (MIDI note 0) at position (0, 0)

### Scale Detection Algorithm

For MIDI Effect Plugin auto-detect mode:
1. Maintains history of last 50 played notes
2. Extracts unique pitch classes (0-11)
3. Compares against all known scales
4. Calculates match score (intersection/union)
5. Requires 60%+ confidence
6. Updates every 2 seconds (configurable)

### Color Palette

0. Default (as configured)
1. Red
2. Yellow
3. Green
4. Cyan
5. Blue
6. Magenta
7. Off
8. White
9. Orange
10. Lime
11. Pink

### Degree Coloring

When enabled:
- **Red**: Root notes (I)
- **Yellow**: Third (III)
- **Green**: Fifth (V)
- **Blue**: Other scale degrees

## Use Cases

### Practice & Learning
- **Command Line**: Quick reference while practicing
- **MIDI Effect**: See what you're playing in real-time
- **Degree Colors**: Learn chord tones and scale shapes

### Composition
- **Command Line**: Explore different scales quickly
- **Max for Live**: Integrate with Ableton workflow
- **Manual Mode**: Lock in a scale while composing

### Live Performance
- **Max for Live**: Preset scales per song section
- **MIDI Effect (Manual)**: Run in background with fixed scale
- **Command Line**: Quick changes between songs

### Teaching
- **Any Method**: Visualize scale theory for students
- **Degree Colors**: Show important scale degrees
- **MIDI Effect (Auto)**: Show what student is playing

## Dependencies

### Python Packages
- `mido>=1.3.0` - MIDI library
- `python-rtmidi>=1.5.0` - Real-time MIDI backend

### Optional
- **Max for Live** - For Ableton integration (requires Ableton Live Suite or Standard + Max for Live)
- **Virtual MIDI Bus** - For MIDI effect plugin:
  - macOS: IAC Driver (built-in)
  - Windows: loopMIDI (free download)

## Installation Methods

### Method 1: Guided Setup (Recommended)
```bash
python setup.py
```

### Method 2: Manual
```bash
pip install -r requirements.txt
python scale_tool.py C major
```

### Method 3: Max for Live Only
```bash
pip install -r requirements.txt
# Copy max_for_live/LinnstrumentScaleLight.maxpat to Ableton User Library
```

## Performance

- **Command Line**: Instant (<1 second)
- **Max for Live**: ~0.5 seconds (depends on Python startup)
- **MIDI Effect**: No MIDI latency (lights update every 2 seconds)
- **CPU Usage**: Negligible (just MIDI messages)

## Limitations

1. **Linnstrument Only**: Designed specifically for Linnstrument MIDI protocol
2. **MIDI CC Required**: Linnstrument must have MIDI CC enabled in settings
3. **Python Required**: All methods require Python 3.7+
4. **Max for Live**: Requires Ableton Live Suite or Max for Live license
5. **Scale Detection**: Auto-detect works best with 5+ notes played

## Future Enhancements

Potential additions:
- GUI application (standalone)
- Proper VST3/AU plugin (requires C++/JUCE)
- Custom scale editor
- Scale preset manager
- Support for other grid controllers
- Ableton Push integration
- Integration with DAW track colors
- MIDI learn for scale changes
- Multi-Linnstrument support

## Compatibility

### Tested On
- macOS (should work on 10.13+)
- Python 3.7 - 3.11

### Should Work On
- Windows (with python-rtmidi)
- Linux (with python-rtmidi)

### DAW Compatibility
- **Max for Live**: Ableton Live only
- **MIDI Effect**: Any DAW with MIDI routing
- **Command Line**: Universal (no DAW required)

## Resources

### Documentation
- `README.md` - Complete user guide
- `QUICK_START.md` - Get started in 5 minutes
- `max_for_live/README.md` - Max for Live setup
- `vst_plugin/README.md` - MIDI effect plugin guide

### Code Examples
- `examples.py` - Interactive demonstrations
- `scale_tool.py` - CLI implementation
- `midi_effect_plugin.py` - MIDI effect with auto-detect

### External Resources
- [Linnstrument MIDI Spec](https://github.com/rogerlinndesign/linnstrument-firmware/blob/master/midi.txt)
- [Mido Documentation](https://mido.readthedocs.io/)
- [Max for Live Docs](https://docs.cycling74.com/max8/vignettes/live_object_model)

## License

MIT License - free to use and modify

## Author

Built for Linnstrument users who want visual scale feedback!

## Support

Issues, questions, or suggestions:
1. Check the README files
2. Run the examples
3. Test with `python scale_tool.py --list-ports`
4. Verify Linnstrument connection

---

*Last Updated: 2025*
