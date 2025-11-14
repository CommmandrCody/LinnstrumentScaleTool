# Linnstrument Scale Tool - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Linnstrument Scale Tool                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                           │
├─────────────────┬──────────────────┬──────────────────┬─────────┤
│  Command Line   │  Max for Live    │  MIDI Effect     │ Python  │
│  scale_tool.py  │  .maxpat device  │  Plugin          │ Library │
└────────┬────────┴─────────┬────────┴────────┬─────────┴────┬────┘
         │                  │                 │              │
         └──────────────────┴─────────────────┴──────────────┘
                                   │
         ┌─────────────────────────┴──────────────────────────┐
         │              CORE PYTHON MODULES                    │
         ├──────────────────────┬──────────────────────────────┤
         │    scales.py         │      linnstrument.py         │
         │  - Scale defs        │    - MIDI control            │
         │  - Note mapping      │    - LED functions           │
         │  - 30+ scales        │    - Color management        │
         └──────────────────────┴──────────────────────────────┘
                                   │
         ┌─────────────────────────┴──────────────────────────┐
         │              EXTERNAL DEPENDENCIES                  │
         ├──────────────────────┬──────────────────────────────┤
         │     mido             │      python-rtmidi           │
         │  MIDI library        │    Real-time MIDI I/O        │
         └──────────────────────┴──────────────────────────────┘
                                   │
                                   │ MIDI CC Messages
                                   │ (CC 20, 21, 22)
                                   ▼
                        ┌─────────────────────┐
                        │    LINNSTRUMENT     │
                        │    Hardware Device  │
                        │    26x8 LED Grid    │
                        └─────────────────────┘
```

## Component Flow Diagrams

### 1. Command Line Tool Flow

```
User Command
    │
    ▼
scale_tool.py
    │
    ├──► Parse arguments (root, scale, colors)
    │
    ├──► scales.get_scale_notes(root, scale)
    │         │
    │         └──► Return list of MIDI note numbers
    │
    ├──► Linnstrument(port)
    │         │
    │         └──► Connect to MIDI port
    │
    ├──► linn.light_scale(notes, colors)
    │         │
    │         ├──► For each note:
    │         │      ├──► Find grid positions
    │         │      └──► Send CC 20, 21, 22
    │         │
    │         └──► LEDs light up
    │
    └──► Close connection
```

### 2. Max for Live Device Flow

```
Ableton Live
    │
    ▼
Max for Live Device (UI)
    │
    ├──► User selects root note & scale
    │
    ├──► User clicks "Update Lights"
    │
    ├──► Trigger shell command
    │         │
    │         └──► python linnstrument_scale_light.py set_scale C major
    │                    │
    │                    ├──► Parse command
    │                    │
    │                    ├──► Import scales & linnstrument modules
    │                    │
    │                    ├──► Get scale notes
    │                    │
    │                    ├──► Light up Linnstrument
    │                    │
    │                    └──► Return JSON status
    │
    └──► Display status in Max device
```

### 3. MIDI Effect Plugin Flow

```
DAW (Ableton, Logic, etc.)
    │
    │ MIDI Out
    ▼
Virtual MIDI Bus (IAC Driver / loopMIDI)
    │
    │ MIDI In
    ▼
midi_effect_plugin.py
    │
    ├──► MIDI Pass-Through (real-time)
    │         │
    │         └──► Linnstrument MIDI In (for playing)
    │
    ├──► Note Analysis (background thread)
    │         │
    │         ├──► Collect note-on messages
    │         │
    │         ├──► Add to history buffer (last 50 notes)
    │         │
    │         └──► Every 2 seconds:
    │                  │
    │                  ├──► Extract pitch classes
    │                  │
    │                  ├──► Compare vs all scales
    │                  │
    │                  ├──► Find best match (60%+ confidence)
    │                  │
    │                  └──► If scale changed:
    │                           │
    │                           └──► Update lights via CC messages
    │
    └──► Linnstrument LED control
```

## Data Structures

### Scale Definition

```python
SCALES = {
    'major': [0, 2, 4, 5, 7, 9, 11],  # Intervals from root
    'minor': [0, 2, 3, 5, 7, 8, 10],
    # ... 30+ more scales
}
```

### Scale Notes

```python
# get_scale_notes('C', 'major') returns:
[0, 2, 4, 5, 7, 9, 11,    # Octave -1
 12, 14, 16, 17, 19, 21, 23,  # Octave 0
 24, 26, 28, 29, 31, 33, 35,  # Octave 1
 # ... up to MIDI note 127
]
```

### Linnstrument Grid

```python
# 26 columns × 8 rows
# Default tuning:
#   - Each column = +1 semitone
#   - Each row = +5 semitones
#
# Note at position (column, row):
note = base_note + (column * 1) + (row * 5)

# Example: Position (0, 0) = MIDI note 0 (C-1)
#          Position (5, 2) = 0 + 5 + 10 = 15 (D#0)
```

### MIDI CC Messages

```python
# Set LED at column 10, row 3 to red:
CC 20, value=10  # Column
CC 21, value=3   # Row
CC 22, value=1   # Color (1=red)
```

## Module Dependencies

```
scale_tool.py
    │
    ├──► scales.py
    │       └──► (no external deps)
    │
    └──► linnstrument.py
            └──► mido
                    └──► python-rtmidi

examples.py
    │
    ├──► scales.py
    └──► linnstrument.py

midi_effect_plugin.py
    │
    ├──► scales.py
    ├──► linnstrument.py
    └──► mido (for MIDI I/O)

linnstrument_scale_light.py (Max for Live backend)
    │
    ├──► scales.py
    ├──► linnstrument.py
    └──► json (for status output)
```

## MIDI Message Flow

### Lighting a Single LED

```
Python Code:
    linn.set_cell_color(column=5, row=2, color='red')

MIDI Messages Sent:
    1. Control Change, channel=0, control=20, value=5
    2. Control Change, channel=0, control=21, value=2
    3. Control Change, channel=0, control=22, value=1

Linnstrument Hardware:
    → LED at position (5, 2) turns red
```

### Lighting a Scale

```
Python Code:
    scale_notes = [0, 2, 4, 5, 7, 9, 11, 12, 14, ...]  # C major
    linn.light_scale(scale_notes, root_color='red', scale_color='blue')

Process:
    1. Clear all lights (208 LEDs × 3 CC messages = 624 messages)
    2. For each note in scale:
          a. Find all grid positions that play this note
          b. Determine color (red for root, blue for others)
          c. Send 3 CC messages per position
    3. Total: ~700-1000 MIDI messages

Timing:
    - Sent as fast as MIDI allows (~1 ms per message)
    - Total time: ~0.7-1.0 seconds
    - Includes small delays for stability
```

## Threading Model (MIDI Effect Plugin)

```
Main Thread:
    │
    ├──► MIDI Input Loop (blocking)
    │         │
    │         └──► For each message:
    │                  ├──► Pass through to output (immediate)
    │                  └──► If note-on: add to detector
    │
    └──► Background Thread (daemon)
              │
              └──► Every 2 seconds:
                      ├──► Analyze note history
                      ├──► Detect scale
                      └──► Update lights if changed
```

## Error Handling

```
All Components:
    │
    ├──► Port Detection
    │         ├──► Try: Find Linnstrument port
    │         └──► Fail: Show available ports & exit
    │
    ├──► MIDI Connection
    │         ├──► Try: Open MIDI port
    │         └──► Fail: Show error & available ports
    │
    ├──► Scale Validation
    │         ├──► Try: Get scale from SCALES dict
    │         └──► Fail: Show available scales & exit
    │
    └──► Graceful Shutdown
              ├──► Close MIDI ports
              └──► Cleanup resources
```

## Configuration Options

### Linnstrument Tuning

```python
Linnstrument(
    row_offset=5,      # Semitones per row (default: 5)
    column_offset=1,   # Semitones per column (default: 1)
    base_note=0        # MIDI note at (0,0) (default: 0 = C-1)
)

# Custom tuning example: Guitar-style (4 semitones per row)
Linnstrument(row_offset=4, column_offset=1, base_note=40)
```

### Color Schemes

```python
# Simple two-color
linn.light_scale(notes, root_color='red', scale_color='blue')

# Degree-based coloring
linn.light_scale_with_degrees(notes, color_map={
    0: 'red',      # Root (I)
    2: 'yellow',   # Third (III)
    4: 'green',    # Fifth (V)
    6: 'cyan'      # Seventh (VII)
})
```

## Performance Characteristics

| Operation | Time | MIDI Messages |
|-----------|------|---------------|
| Light single note | ~3 ms | 3-9 (depends on positions) |
| Light full scale | ~0.7-1.0s | ~700-1000 |
| Clear all lights | ~0.6s | 624 (208 × 3) |
| Scale detection | ~10 ms | 0 (computation only) |
| MIDI pass-through | <1 ms | 1 (per message) |

## Extensibility Points

### Adding New Scales

```python
# In scales.py:
SCALES['custom_scale'] = [0, 2, 3, 6, 7, 9]

# Use immediately:
python scale_tool.py C custom_scale
```

### Custom Color Mapping

```python
# In your code:
color_map = {
    0: 'magenta',   # Root
    1: 'orange',    # Second
    3: 'lime',      # Fourth
    # ... etc
}
linn.light_scale_with_degrees(notes, color_map)
```

### Alternative Grid Layouts

```python
# Support for other controllers (future):
class GridController:
    def get_note_at_position(self, x, y):
        # Custom layout logic
        pass

    def set_led_color(self, x, y, color):
        # Custom LED control
        pass
```

## Integration Points

### DAW Integration

```
Command Line ←→ Any DAW (manual triggering)
Max for Live ←→ Ableton Live (native)
MIDI Effect  ←→ Any DAW (via virtual MIDI)
```

### External Control

```
Python Library ←→ Other Python scripts
MIDI In       ←→ External MIDI controllers
OSC/WebSocket ←→ Network control (future)
```

---

*This architecture supports the current implementation and allows for future enhancements.*
