# LinnStrument Multi-Mode System for Ableton Livecol 0 row 2 and 
---

## 🚀 Quick Start (20 minutes)

### 1. Install to Ableton

Files are already installed at:
```
/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/
```

✅ **Already done!** Skip to step 2.

### 2. Configure LinnStrument Hardware
yoiuve done AGAIN you broke the pads ad they play tnighgh

You need to set up **2 presets** and **1 button** on your LinnStrument.

#### Preset 1: Keyboard Mode
1. Press **PRESET** button → switch to Preset 1
2. Press and hold **GLOBAL SETTINGS** button (lights YELLOW)
3. Set these (look at printed labels on your panel):
   - **Column 1, Row 3** → MIDI MODE = "One Channel"
   - **Column 2, Row 0** → CHANNEL = 1
   - **Column 4, Row 3** → ROW OFFSET = 5 semitones
   - **Column 5, Row 2-3** → OCTAVE = 5 or 6
4. Press **GLOBAL SETTINGS** to exit (auto-saves)

#### Preset 2: Session/Drum Modes
1. Press **PRESET** button → switch to Preset 2
2. Press and hold **GLOBAL SETTINGS**
3. Set these:
   - **Column 1, Row 1** → MIDI MODE = "Channel Per Row" (CRITICAL!)
   - **Column 4, Row 3** → ROW OFFSET = 5 semitones
   - **Column 3, Row 0** → BEND RANGE = minimal (lowest setting)
4. Press **GLOBAL SETTINGS** to exit (auto-saves)

#### Switch 1: Mode Switching
1. Press and hold **GLOBAL SETTINGS**
2. **Column 7, Row 3** → SELECT SW = Switch 1
3. **Column 8-9** → Find and press "CC65" (or "CC" then enter 65)
4. Press **GLOBAL SETTINGS** to exit

### 3. Find Your Base Note

1. Press **PRESET** → Preset 1
2. In Ableton: Create MIDI track, arm it
3. Press **bottom-left pad** on LinnStrument
4. Note the MIDI number (e.g., 36, 48, 60)
5. Edit this file:
   ```
   /Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/config.py
   ```
6. Change line 8:
   ```python
   LINNSTRUMENT_BASE_NOTE = 36  # Change to YOUR number!
   ```
7. Save and restart Ableton

### 4. Enable in Ableton

1. **Ableton → Preferences → Link/Tempo/MIDI**
2. Find your LinnStrument in MIDI Ports
3. Set:
   - **Control Surface:** LinnstrumentScale128
   - **Input:** Your LinnStrument
   - **Output:** Your LinnStrument
4. **Quit and restart Ableton**

### 5. Test

1. Check Ableton's Log.txt for: `"Linnstrument Multi-Mode System - Ready!"`
   - Location: `~/Library/Preferences/Ableton/Live X.X.X/Log.txt`
2. Press **Switch 1** → status bar should show mode name
3. Try each mode (see usage below)

---

## 🎹 The Three Modes

### Mode 1: Keyboard Mode (Scale Lighting)

**Hardware:** Preset 1
**Use:** Playing melodies with scale guidance

**How to use:**
1. Press **PRESET** → Preset 1
2. Press **Switch 1** → "Keyboard Mode"
3. Set scale in Ableton (e.g., C Major)
4. Scale notes light up on grid (roots = one color, scale = another)

**Features:**
- Auto-detects Ableton's scale settings
- Track color integration
- Real-time updates

---

### Mode 2: Session Mode (Clip Launcher)

**Hardware:** Preset 2
**Use:** Launching clips and scenes

**How to use:**
1. Press **PRESET** → Preset 2
2. Press **Switch 1** → "Session Mode"
3. Create clips in Session View
4. Press pads to launch clips

**LED Colors:**
- **Green** = Playing
- **Yellow** = Triggered/queued
- **Red** = Recording
- **Clip color** = Stopped
- **Off** = Empty slot

**Grid:** 16×8 clip matrix (columns = tracks, rows = scenes)

---

### Mode 3: Drum Mode (Drum Pads + Sequencer)

**Hardware:** Preset 2
**Use:** Finger drumming + beat programming

**How to use:**
1. Press **PRESET** → Preset 2
2. Press **Switch 1** → "Drum Mode"
3. Load Drum Rack on track
4. **Bottom 4 rows** = drum pads (4×4 = 16 pads)
5. **Top row** = 16-step sequencer
6. Press drum pad to select it (turns white)
7. Press sequencer steps to toggle them on/off (cyan = on)
8. Press Play in Ableton → sequence plays in sync

**Sequencer Features:**
- 16 steps (16th notes)
- Per-pad sequences (16 pads × 16 steps)
- Tempo-synced playback
- Visual playhead (yellow/white)

**Workflow:**
1. Press drum pad → triggers sound + selects for editing
2. Top row shows that pad's sequence
3. Toggle steps on/off
4. Press different pad → see its sequence
5. Build complete beat across all 16 pads

---

## ⚙️ Configuration

### Base Note Setup

Your base note depends on LinnStrument's octave setting. Common values:

| MIDI Note | Note Name | What to set in config.py |
|-----------|-----------|--------------------------|
| 36 | C2 | `LINNSTRUMENT_BASE_NOTE = 36` |
| 48 | C3 | `LINNSTRUMENT_BASE_NOTE = 48` |
| 60 | C4 | `LINNSTRUMENT_BASE_NOTE = 60` |

**Find yours:** Press bottom-left pad, check MIDI monitor, update config.py

### Customization

Edit `config.py` to change:
- Base note
- Mode switch CC number
- Drum pad layout
- Session grid size
- Color schemes

---

## 🐛 Troubleshooting

### Scale doesn't light (Keyboard Mode)

**Check:**
- Using Preset 1? (One Channel mode)
- Global Settings button is YELLOW? (User Firmware Mode)
- Base note matches in config.py?
- Scale set in Ableton?

**Fix:**
- Test base note again (press bottom-left pad)
- Update config.py with correct number
- Restart Ableton

---

### Clips don't launch (Session Mode)

**Check:**
- Using Preset 2? (Channel Per Row mode)
- Pitch Bend disabled in Preset 2?
- Clips exist in Session View?

**Fix:**
- Verify Preset 2: MIDI MODE = "Channel Per Row"
- Verify Preset 2: BEND RANGE = minimal
- Create test clip to verify

---

### Drums don't play (Drum Mode)

**Check:**
- Using Preset 2?
- Drum Rack loaded on selected track?
- Track armed/monitoring?

**Fix:**
- Load factory Drum Rack preset (has samples)
- Make sure track is selected in Ableton
- Check track is armed

---

### Mode doesn't switch

**Check:**
- Switch 1 configured to CC65?
- MIDI monitor shows CC65 when pressed?
- Log.txt shows "Mode switch CC received"?

**Fix:**
- Reconfigure Switch 1 in Global Settings
- Or try different CC number and update config.py:
  ```python
  MODE_SWITCH_CC = 65  # Change to your CC
  ```

---

### Nothing works / "Not Ready" in log

**Check:**
- Files in correct location?
  ```
  /Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/
  ```
- Control Surface set in Ableton preferences?
- Ableton fully restarted after installation?

**Fix:**
- Check folder contains: `LinnstrumentScale.py`, `config.py`, `led_manager.py`, `modes/`
- Re-select Control Surface in preferences
- Read error messages in Log.txt

---

## 📁 Project Structure

```
LinnstrumentScale128/
├── LinnstrumentScale.py       # Main controller
├── config.py                  # Settings (EDIT THIS for base note)
├── led_manager.py             # LED control
├── scales.py                  # Scale definitions
├── linnstrument_ableton.py    # MIDI interface
└── modes/
    ├── base_mode.py          # Base class
    ├── keyboard_mode.py      # Scale lighting
    ├── session_mode.py       # Clip launcher
    └── drum_mode.py          # Drum pads + sequencer
```

---

## 💡 Tips & Tricks

### Workflow Ideas

**Live Performance:**
- Load song in Session View
- Use Session Mode to launch clips/scenes
- Switch to Drum Mode for live beat variations
- Switch to Keyboard Mode for solo sections

**Production:**
- Use Keyboard Mode to explore scales while composing
- Session Mode for arranging clips
- Drum Mode for programming beats

**Practice:**
- Keyboard Mode shows scale patterns
- Learn intervals and chord tones visually
- Practice in different keys

### Advanced

**Modify layouts in config.py:**
```python
# Drum mode: Make 2×8 pad layout instead of 4×4
DRUM_PAD_ROWS = 2
DRUM_PAD_COLUMNS = 8

# Session mode: Change visible area
SESSION_ROWS = 8
SESSION_COLUMNS = 16
```

**Add more modes:**
- Create new file in `modes/` directory
- Extend `BaseMode` class
- Register in `LinnstrumentScale.py`

---

## 🎯 Quick Reference

### Physical Buttons

| Button | Function |
|--------|----------|
| **PRESET** | Cycle hardware presets (1→2→...) |
| **GLOBAL SETTINGS** | Enter/exit settings menu |
| **Switch 1** | Cycle software modes (Keyboard→Session→Drum→...) |

### Presets

| Preset | MIDI Mode | Used For |
|--------|-----------|----------|
| **1** | One Channel | Keyboard Mode |
| **2** | Channel Per Row | Session + Drum Modes |

### Workflow

```
Keyboard Mode:
  PRESET → 1
  Switch 1 → "Keyboard Mode"
  Set scale in Ableton
  Play!

Session Mode:
  PRESET → 2
  Switch 1 → "Session Mode"
  Press pads → launch clips

Drum Mode:
  PRESET → 2
  Switch 1 → "Drum Mode"
  Bottom rows → drum pads
  Top row → sequencer
```

---

## 📚 Documentation

- **README.md** (this file) - Complete guide
- **SETUP_CHECKLIST.md** - Step-by-step setup with checkboxes
- **SIMPLE_PRESET_SETUP.md** - Detailed walkthrough
- **PROJECT_SUMMARY.md** - Technical details
- **MULTIMODE_README.md** - Extended user guide

**Additional docs in `_archive_docs/`** (reference only)

---

## 🔧 Support

**Check Ableton's Log:**
```
~/Library/Preferences/Ableton/Live X.X.X/Log.txt
```

Look for:
- "Linnstrument Multi-Mode System - Ready!" = Success
- ERROR messages = Something wrong (read the error)

**Common fixes:**
- Wrong base note → Update config.py
- Wrong preset → Switch to correct preset
- Mode doesn't work → Check Log.txt for errors

---

## 📝 Version Info

**Version:** 1.0
**Compatible with:**
- LinnStrument 128 (16 columns)
- LinnStrument 200 (25 columns) - edit config.py
- Ableton Live 10+
- macOS (tested) / Windows (should work)

**Created:** November 2025
**Status:** Production-ready

---

## 🎵 Ready to Make Music!

You now have a professional multi-mode controller for your LinnStrument.

**Press Switch 1 and explore the three modes!**

Questions? Check **SETUP_CHECKLIST.md** for detailed step-by-step setup.

---

**Enjoy!** 🎹✨
