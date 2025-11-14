# LinnStrument Hardware Setup for Multi-Mode System

## Overview

The LinnStrument Multi-Mode system requires specific hardware configuration on your LinnStrument to work properly. This guide walks you through setting up the necessary presets and mode switch button.

---

## Required Presets

You need to configure **2 presets** on your LinnStrument:

### Preset 1: Keyboard Mode (One Channel)

**Use:** Scale lighting and traditional keyboard playing

1. Press **Global Settings** button
2. Navigate to **Per-Split Settings** > **Preset** and select **Preset 1**
3. Configure the following settings:
   - **MIDI Mode**: One Channel
   - **Channel**: 1
   - **Pitch Bend Range**: 24-48 semitones (your preference)
   - **Row Offset**: 5 semitones (fourths - standard isomorphic)
   - **Low Row**: Set to your preferred octave (default: Octave 5 = C3)
   - **Velocity Sensitivity**: Your preference
   - **Pressure Sensitivity**: Your preference

4. Save preset by holding **Preset** button

### Preset 2: Session & Drum Modes (Channel Per Row)

**Use:** Clip launching (Session mode) and Drum sequencer (Drum mode)

1. Press **Global Settings** button
2. Navigate to **Per-Split Settings** > **Preset** and select **Preset 2**
3. Configure the following settings:
   - **MIDI Mode**: Channel Per Row
   - **Channels**: 1-8 (one per row)
   - **Row Offset**: 5 semitones (keep consistent with Preset 1)
   - **Pitch Bend**: OFF (important! - prevents conflicts)
   - **Low Row**: Same as Preset 1 (for consistency)
   - **Velocity Sensitivity**: Your preference
   - **Pressure Sensitivity**: Your preference (can be lower for button-press feel)

4. Save preset by holding **Preset** button

**Why Channel Per Row?**
- Session Mode: Allows different clip colors per row
- Drum Mode: Separates drum pad rows from sequencer rows
- Software handles the interpretation - both modes use the same preset

---

## Mode Switch Button Configuration

Configure **Switch 1** (left panel button) to send CC65 for mode cycling:

### Setup Steps

1. Press **Global Settings** button
2. Navigate to **Switch Assign** > **Switch 1**
3. Set the following:
   - **Function**: CC
   - **CC Number**: 65
   - **Channel**: 1
   - **Mode**: Toggle (or Momentary - your preference)
   - **Value**: 127 (max value when pressed)

4. Exit Global Settings

### Usage

- **Press Switch 1** to cycle through modes:
  - Keyboard → Session → Drum → Keyboard → ...
- Current mode displays in Ableton's status bar
- LEDs update automatically when switching modes

---

## Base Note Configuration

The software needs to know which MIDI note your bottom-left pad plays.

### Find Your Base Note

1. Open a MIDI monitor in Ableton (MIDI > MIDI Monitor)
2. Press the **bottom-left pad** on your LinnStrument
3. Note the MIDI note number displayed

Common base notes:
- **36 (C2)**: Push-style layout (recommended)
- **40 (E2)**: Guitar-style tuning
- **48 (C3)**: Factory default
- **30 (F#1)**: Custom low tuning

### Configure in Software

1. Open `config.py` in the LinnstrumentScale128 folder:
   ```
   ~/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/config.py
   ```

2. Find the line:
   ```python
   LINNSTRUMENT_BASE_NOTE = 36  # C2 - matches Push
   ```

3. Change `36` to your base note number

4. Save and reload the script in Ableton (restart Live or toggle MIDI Remote Script off/on)

---

## Preset Switching

### Manual Switching

The Remote Script does NOT automatically switch presets. You need to manually switch when changing modes:

- **Keyboard Mode**: Switch to **Preset 1** (One Channel)
- **Session Mode**: Switch to **Preset 2** (Channel Per Row)
- **Drum Mode**: Switch to **Preset 2** (Channel Per Row)

### Quick Preset Switch

Set up **Switch 2** for quick preset switching:

1. Press **Global Settings**
2. Navigate to **Switch Assign** > **Switch 2**
3. Set function to **Preset +** (cycle through presets)
4. Exit Global Settings

**Workflow:**
1. Press **Switch 1** to change software mode
2. Press **Switch 2** to match hardware preset
3. (Session and Drum both use Preset 2, so you only switch for Keyboard mode)

---

## Verification

### Test Keyboard Mode

1. Switch to **Preset 1** on LinnStrument
2. Press **Switch 1** until status bar shows "Linnstrument: Keyboard Mode"
3. Set a scale in Ableton (e.g., C Major)
4. Verify scale notes light up on grid
5. Root notes should be one color, other scale notes another color

### Test Session Mode

1. Switch to **Preset 2** on LinnStrument
2. Press **Switch 1** until status bar shows "Linnstrument: Session Mode"
3. Create some clips in Ableton's Session View
4. Verify pads show clip colors
5. Press pads to launch clips
6. Playing clips should turn green

### Test Drum Mode

1. Switch to **Preset 2** on LinnStrument
2. Press **Switch 1** until status bar shows "Linnstrument: Drum Mode"
3. Load a Drum Rack on the selected track
4. Bottom 4 rows should show drum pads
5. Press drum pads to trigger sounds
6. Top row shows sequencer steps for selected pad
7. Press sequencer steps to toggle them on/off
8. Press play in Ableton - sequencer should play in sync

---

## Troubleshooting

### Mode switch doesn't work

- Verify Switch 1 is set to CC65 on Channel 1
- Check Ableton's Log.txt for "Mode switch CC received" messages
- Ensure Remote Script is loaded (should see "Multi-Mode Ready" in log)

### Scale lighting doesn't work in Keyboard mode

- Verify you're using Preset 1 (One Channel)
- Check base note configuration matches your hardware
- Verify User Firmware Mode is enabled (Global Settings button should be YELLOW)

### Clip launching doesn't work in Session mode

- Verify you're using Preset 2 (Channel Per Row)
- Ensure Pitch Bend is OFF in Preset 2
- Check that clips exist in the visible session area

### Drum pads don't trigger sounds

- Verify a Drum Rack is loaded on the selected track
- Drum pads send MIDI notes 36-51 (C1-D#2)
- Check your Drum Rack is listening to the same MIDI notes

### Sequencer doesn't play

- Ensure Ableton's transport is playing
- Check song time listener is working (should see playhead move)
- Verify steps are toggled on (cyan color) before playing

---

## Advanced Configuration

### Custom Mode Switch Button

Don't want to use Switch 1? You can use any CC or even a foot switch:

1. Configure your hardware button to send a different CC number
2. Edit `config.py`:
   ```python
   MODE_SWITCH_CC = 65  # Change to your CC number
   ```
3. Reload Remote Script

### Alternative Layouts

Want different grid layouts? Edit in `config.py`:

```python
# Drum mode layout
DRUM_PAD_ROWS = 4  # Change to 2 for 2x8 layout
DRUM_PAD_COLUMNS = 4  # Change to 8 for 2x8 layout
SEQUENCER_STEPS = 16  # Keep at 16 for LinnStrument 128
```

### LinnStrument 200 Support

LinnStrument 200 has 25 columns instead of 16:

1. Edit `config.py`:
   ```python
   LINNSTRUMENT_COLUMNS = 25  # Was 16
   SESSION_COLUMNS = 25  # Was 16
   SEQUENCER_STEPS = 32  # Could support 32 steps!
   ```

2. Sequencer can show 2 banks of 16 steps across the grid

---

## Next Steps

- Configure your presets
- Set up mode switch button
- Test each mode
- Explore the workflow!
- See README.md for usage tips and workflows

---

## Support

If you encounter issues:

1. Check Ableton's Log.txt (`~/Library/Preferences/Ableton/Live X.X.X/Log.txt`)
2. Look for error messages from "LinnstrumentScale" or mode names
3. Verify all hardware settings match this guide
4. File an issue with log excerpts if problems persist
