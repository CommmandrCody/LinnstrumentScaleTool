# LinnStrument Multi-Mode System

Transform your LinnStrument into a versatile Ableton Live controller with three powerful modes:

## 🎹 Three Modes

### 1. Keyboard Mode
**Traditional scale lighting for expressive playing**

- Automatically detects Ableton's scale and root note
- Lights scale notes on the grid
- Root notes highlighted in one color, scale degrees in another
- Track color integration - colors adapt to selected track
- Perfect for melodic performance and composition

**Use When:**
- Playing melodies or chords
- Learning scales
- Improvising within a key
- Recording MIDI performances

---

### 2. Session Mode
**Full-grid clip launcher (16×8 matrix)**

- Each pad launches a clip
- Real-time clip state feedback:
  - **Green**: Playing
  - **Yellow**: Triggered/queued
  - **Red**: Recording
  - **Clip color**: Stopped (shows clip color)
  - **Off**: Empty slot
- Navigate large sessions (future: shift grid with controls)

**Use When:**
- Live performance with clip launching
- Building arrangements in Session View
- Jamming with loops and scenes
- DJing or live remixing

---

### 3. Drum Mode
**Integrated drum pads + step sequencer**

#### Layout:
- **Bottom 4 rows (rows 0-3)**: 4×4 drum pad matrix (16 pads)
- **Top row (row 7)**: 16-step sequencer

#### Workflow:
1. Press a drum pad to select it and trigger the sound
2. Selected pad shows **white**
3. Top row displays the sequence for that pad
4. Press sequencer steps to toggle them on/off
5. Start Ableton's transport - sequencer plays in sync
6. Press different drum pads to edit their sequences

#### Sequencer Features:
- **Cyan**: Active step (will trigger)
- **Yellow**: Playhead on empty step
- **White**: Playhead on active step (currently playing)
- **Off**: Inactive step
- 16th note quantization (syncs to Ableton's tempo)
- Per-pad sequences (16 pads × 16 steps)

**Use When:**
- Programming drum beats
- Live beat making
- Creating rhythmic patterns
- Performing with finger drumming + sequencing

---

## 🔄 Mode Switching

### Setup (One-Time)
1. Configure **Switch 1** on your LinnStrument to send **CC65**
   - See `HARDWARE_SETUP.md` for detailed instructions
2. Install Remote Script in Ableton
3. Configure your base note in `config.py`

### Switching Modes
Press **Switch 1** to cycle:

```
Keyboard → Session → Drum → Keyboard → ...
```

Mode appears in Ableton's status bar.

### Preset Management

Modes use different LinnStrument presets:

| Mode | Preset | MIDI Mode |
|------|--------|-----------|
| Keyboard | Preset 1 | One Channel |
| Session | Preset 2 | Channel Per Row |
| Drum | Preset 2 | Channel Per Row |

**Manual preset switching required** - see `HARDWARE_SETUP.md` for details.

---

## 🎯 Quick Start

### 1. Install

```bash
# Copy to Ableton's Remote Scripts folder
cp -r ableton_remote_script/LinnstrumentScale128 \
  ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

### 2. Configure LinnStrument

See `HARDWARE_SETUP.md` for:
- Preset 1 configuration (One Channel for Keyboard mode)
- Preset 2 configuration (Channel Per Row for Session/Drum)
- Switch 1 setup (CC65 for mode switching)
- Base note detection and configuration

### 3. Enable in Ableton

1. Open Ableton Live Preferences
2. Go to **Link/Tempo/MIDI**
3. Under **MIDI Ports**, find your LinnStrument
4. Set **Control Surface**: LinnstrumentScale128
5. Set **Input/Output**: Your LinnStrument ports
6. Restart Ableton or toggle Remote Script off/on

### 4. Verify

Check Ableton's Log.txt:
```
~/Library/Preferences/Ableton/Live X.X.X/Log.txt
```

Look for:
```
Linnstrument Multi-Mode System - Ready!
Press Switch 1 (CC65) to cycle modes
```

---

## 📖 Usage Guide

### Keyboard Mode Workflow

1. **Switch to Keyboard Mode**
   - Press Switch 1 until status shows "Linnstrument: Keyboard Mode"
   - Switch LinnStrument to Preset 1

2. **Set Scale in Ableton**
   - Create a MIDI track
   - In MIDI Effect Rack or Track Settings, set Scale and Root
   - Or: Enable Push's scale mode

3. **Play**
   - Scale notes light up automatically
   - Root notes in one color, scale degrees in another
   - Colors adapt to selected track color
   - Change scale/root in Ableton → LEDs update instantly

**Tips:**
- Use with Ableton's Scale MIDI effect for constrained playing
- Change track colors for visual organization
- Switch scales mid-performance for modal shifts

---

### Session Mode Workflow

1. **Switch to Session Mode**
   - Press Switch 1 until status shows "Linnstrument: Session Mode"
   - Switch LinnStrument to Preset 2

2. **Setup Session**
   - Create clips in Ableton's Session View
   - Grid shows clips as colored pads
   - Empty slots are dark

3. **Launch Clips**
   - Press any pad to launch the corresponding clip
   - Playing clips glow green
   - Press again to stop

4. **Visual Feedback**
   - Green = Playing
   - Yellow = Queued (triggered, will start at next quantize point)
   - Red = Recording
   - Clip color = Stopped (ready to launch)
   - Off = Empty slot

**Tips:**
- Use clip colors to organize your session visually
- Set up scenes for full arrangement launching
- Combine with MIDI keyboard mode for performance

---

### Drum Mode Workflow

1. **Switch to Drum Mode**
   - Press Switch 1 until status shows "Linnstrument: Drum Mode"
   - Switch LinnStrument to Preset 2

2. **Load Drum Rack**
   - Create a MIDI track
   - Add Drum Rack (Instrument → Drum Rack)
   - Load samples into drum pads

3. **Select & Play Drums**
   - Bottom 4 rows = drum pads (4×4 = 16 pads)
   - Press pad to trigger sound
   - Selected pad turns white
   - Pads with samples show green, empty pads show off

4. **Program Sequence**
   - Top row shows 16 steps for selected pad
   - Press steps to toggle them on/off
   - Cyan = active step
   - Off = inactive step

5. **Playback**
   - Press Play in Ableton
   - Playhead moves through steps (yellow/white)
   - Active steps trigger drum sounds
   - Synced to Ableton's tempo (16th notes)

6. **Edit Multiple Pads**
   - Press different drum pads to switch between their sequences
   - Each pad has its own 16-step pattern
   - Build complete beats across all 16 pads

**Tips:**
- Start with kick on pad 0, snare on pad 4, hi-hats on pad 8
- Create variations by switching between pads
- Combine with Ableton's MIDI effects (Random, Scale, etc.)
- Use velocity-sensitive pads for dynamics
- Record sequencer output as MIDI clips in Ableton

---

## 🎛️ Configuration

### Base Note Setup

Your LinnStrument's bottom-left pad must match the software configuration.

1. **Find your base note:**
   - Open MIDI monitor in Ableton
   - Press bottom-left pad on LinnStrument
   - Note the MIDI note number

2. **Configure software:**
   - Edit `config.py`
   - Set `LINNSTRUMENT_BASE_NOTE` to your note number
   - Common values: 36 (C2), 40 (E2), 48 (C3)

### Mode Switch Button

Default: **Switch 1** sends **CC65**

To use a different button:
1. Configure hardware to send any CC number
2. Edit `config.py`: `MODE_SWITCH_CC = XX`
3. Reload Remote Script

### Grid Layout Customization

Edit `config.py` to change layouts:

```python
# Drum mode layout
DRUM_PAD_ROWS = 4  # Drum pad height
DRUM_PAD_COLUMNS = 4  # Drum pad width
SEQUENCER_STEPS = 16  # Number of steps (LinnStrument 128)

# Session mode layout
SESSION_ROWS = 8  # Clip grid height
SESSION_COLUMNS = 16  # Clip grid width (LinnStrument 128)
```

---

## 🔧 Advanced Features

### LinnStrument 200 Support

LinnStrument 200 has 25 columns (vs 16 on LS128):

1. Edit `config.py`:
   ```python
   LINNSTRUMENT_COLUMNS = 25
   SESSION_COLUMNS = 25
   SEQUENCER_STEPS = 32  # Can show 32 steps!
   ```

2. Sequencer can display 2 banks of 16 steps

### Sequence Persistence

Current implementation: Sequences reset when Ableton restarts.

**Future enhancement:** Save/load sequences to Ableton project.

### Session Navigation

Current implementation: Shows first 16×8 clips.

**Future enhancement:** Navigate session view with dedicated controls.

---

## 🐛 Troubleshooting

### Mode switching doesn't work

**Symptoms:**
- Pressing Switch 1 does nothing
- No mode change message in status bar

**Solutions:**
1. Check LinnStrument Switch 1 is set to CC65, Channel 1
2. Verify Remote Script is loaded (check Log.txt)
3. Look for "Mode switch CC received" in Log.txt
4. Ensure Switch 1 is in Toggle or Momentary mode (not Off)

### LEDs don't light up

**Symptoms:**
- Grid stays dark in any mode
- No visual feedback

**Solutions:**
1. Check LinnStrument is in User Firmware Mode
   - Global Settings button should be **YELLOW**
2. Verify MIDI connection in Ableton settings
3. Check Log.txt for "User Firmware Mode enabled"
4. Try toggling LinnStrument's User Firmware Mode manually

### Keyboard mode scale is wrong

**Symptoms:**
- Wrong notes light up
- Scale doesn't match Ableton setting

**Solutions:**
1. Verify base note configuration matches hardware
2. Check LinnStrument is in Preset 1 (One Channel)
3. Ensure Row Offset = 5 semitones
4. Look for scale detection logs in Log.txt

### Clips don't launch in Session mode

**Symptoms:**
- Pressing pads doesn't launch clips
- No response from grid

**Solutions:**
1. Verify LinnStrument is in Preset 2 (Channel Per Row)
2. Check Pitch Bend is OFF in Preset 2
3. Ensure clips exist in Session View
4. Look for "Launched clip" messages in Log.txt

### Drum sequencer doesn't play

**Symptoms:**
- Steps are lit but no sound
- Playhead doesn't move

**Solutions:**
1. Check Ableton transport is playing (spacebar)
2. Verify Drum Rack is on selected track
3. Ensure drum pads have samples loaded
4. Check MIDI note range (pads use notes 36-51)
5. Look for "Playback: playing" in Log.txt

### Notes pass through in Session/Drum mode

**Symptoms:**
- Pads trigger sounds instead of launching clips/drums
- MIDI notes leak through

**Solutions:**
- This is expected! Modes can intercept OR pass through
- Keyboard mode: Always passes through (for playing)
- Session mode: Always intercepts (for clip launching)
- Drum mode: Always intercepts (for drum pads/sequencer)

---

## 📁 Project Structure

```
LinnstrumentScale128/
├── LinnstrumentScale.py       # Main controller
├── config.py                  # Configuration constants
├── led_manager.py             # LED control system
├── scales.py                  # Scale definitions
├── linnstrument_ableton.py    # LinnStrument MIDI interface
├── modes/
│   ├── __init__.py
│   ├── base_mode.py          # Abstract base class
│   ├── keyboard_mode.py      # Scale lighting mode
│   ├── session_mode.py       # Clip launcher mode
│   └── drum_mode.py          # Drum pads + sequencer
└── (other files...)
```

---

## 🚀 Future Enhancements

### Planned Features

- [ ] Sequence save/load (persist with Ableton project)
- [ ] Session view navigation (shift grid with controls)
- [ ] Velocity-sensitive step sequencer
- [ ] Per-step note length/gate
- [ ] Swing parameter
- [ ] Pattern copy/paste
- [ ] Automatic preset switching (via MIDI)
- [ ] Mode indicator LED on LinnStrument
- [ ] Multi-row sequencer (show multiple pads at once)

### Experimental Features

- [ ] Track selection row (top row for track switching)
- [ ] Device control mode (map to Ableton devices)
- [ ] Note repeat/arpeggiator integration
- [ ] Scale locking in keyboard mode

---

## 🤝 Contributing

Found a bug? Have an enhancement idea?

1. Check existing issues
2. Create new issue with:
   - Mode where issue occurs
   - Steps to reproduce
   - Log.txt excerpt
   - Expected vs actual behavior

Pull requests welcome!

---

## 📜 License

[Your License Here]

---

## 🙏 Credits

Built for the LinnStrument community.

Special thanks to:
- Roger Linn for creating the LinnStrument
- Ableton for the Remote Script API
- The open-source Ableton controller community

---

## 📚 Additional Resources

- `HARDWARE_SETUP.md` - Detailed hardware configuration guide
- `PROJECT_SUMMARY.md` - Development notes and architecture
- Ableton Remote Script documentation
- LinnStrument MIDI implementation guide

---

**Enjoy your multi-mode LinnStrument! 🎵**
