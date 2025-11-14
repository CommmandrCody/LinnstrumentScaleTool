# LinnStrument Preset Configuration - Step-by-Step Guide

This guide walks you through configuring your LinnStrument presets with **screenshots described** and **button-by-button instructions**.

---

## Overview: What We're Setting Up

You need **2 presets** configured on your LinnStrument:

| Preset | MIDI Mode | Used For |
|--------|-----------|----------|
| **Preset 1** | One Channel | Keyboard Mode (scale lighting) |
| **Preset 2** | Channel Per Row | Session Mode + Drum Mode |

Plus one hardware button for mode switching.

---

## Part 1: Configure Preset 1 (Keyboard Mode)

### Step 1: Enter Global Settings

1. **Press and hold** the **GLOBAL SETTINGS** button (far left, bottom row)
   - Button will light up **YELLOW**
   - Grid now shows settings menu

### Step 2: Navigate to Preset Settings

1. Look at the grid - you'll see columns labeled with settings categories
2. Find the column that says **"PRESET"** (usually column 2 or 3)
3. **Press** the top pad in the **PRESET** column
   - This enters preset selection mode

### Step 3: Select Preset 1

1. You'll see numbered pads representing presets (1-8)
2. **Press** the pad for **Preset 1** (usually top-left of the preset number area)
   - Preset 1 pad will light up showing it's selected

### Step 4: Configure MIDI Mode (One Channel)

1. Look for the column labeled **"MIDI MODE"** or **"MIDI"**
2. **Press** the top pad in that column to enter MIDI mode settings
3. You'll see options:
   - **One Channel** (this is what we want!)
   - Channel Per Note
   - Channel Per Row
4. **Press** the **"One Channel"** option
   - It should light up indicating it's selected

### Step 5: Set MIDI Channel

1. Look for **"CHANNEL"** column (next to MIDI MODE)
2. **Press** the top pad in the CHANNEL column
3. You'll see numbers 1-16
4. **Press** pad for **Channel 1**
   - Most common setup - you can use any channel

### Step 6: Configure Row Offset

1. Find the column labeled **"ROW OFFSET"** or **"INTERVAL"**
2. **Press** the top pad in that column
3. You'll see numbers representing semitones (0, 3, 4, 5, 7, 12)
4. **Press** the pad for **5** semitones
   - This is the standard isomorphic layout (fourths)
   - Same as guitar tuning (EADG)

### Step 7: Set Octave/Low Row

1. Find **"OCTAVE"** or **"LOW ROW"** column
2. **Press** the top pad in that column
3. You'll see octave numbers (usually -1 to 9)
4. **Recommended:** Select **Octave 5** or **6**
   - Octave 5 makes bottom-left pad = **C3** (MIDI 48)
   - Octave 6 makes bottom-left pad = **C4** (MIDI 60)
   - We're using **C2** in config, so try different octaves and test

### Step 8: Configure Pitch Bend Range (Optional)

1. Find **"BEND RANGE"** or **"PITCH BEND"** column
2. **Press** the top pad
3. You'll see numbers (2, 12, 24, 48)
4. Suggested: **24** or **48** semitones
   - Allows 2-4 octave pitch bends for expressive playing
   - Personal preference - try what feels good

### Step 9: Save Preset 1

1. **Press and hold** the **PRESET** button (in the left panel)
   - Hold for 2-3 seconds until it flashes
2. **Release** - Preset 1 is now saved!

### Step 10: Exit Global Settings

1. **Press** the **GLOBAL SETTINGS** button again
   - Button turns off
   - You're back to playing surface

---

## Part 2: Configure Preset 2 (Session/Drum Modes)

### Step 1: Enter Global Settings

1. **Press and hold** the **GLOBAL SETTINGS** button
   - Button lights up **YELLOW**

### Step 2: Select Preset 2

1. Find **"PRESET"** column
2. **Press** the top pad in PRESET column
3. **Press** the pad for **Preset 2** (second preset number)
   - Preset 2 is now selected

### Step 3: Configure MIDI Mode (Channel Per Row)

1. Find **"MIDI MODE"** column
2. **Press** the top pad in that column
3. You'll see mode options
4. **Press "Channel Per Row"**
   - **CRITICAL:** This is required for Session and Drum modes!
   - Each row will send on a different MIDI channel (1-8)

### Step 4: Set Channel Range

1. In Channel Per Row mode, channels are automatic (rows 0-7 = channels 1-8)
2. No need to configure - it's automatic!

### Step 5: Row Offset (Keep Same as Preset 1)

1. Find **"ROW OFFSET"** column
2. **Press** top pad
3. **Press** the pad for **5** semitones
   - Keep this the same as Preset 1 for consistency
   - Maintains isomorphic layout

### Step 6: Low Row/Octave (Keep Same as Preset 1)

1. Find **"OCTAVE"** or **"LOW ROW"** column
2. **Press** top pad
3. Select the **same octave** you chose for Preset 1
   - Keeps note mapping consistent across presets

### Step 7: DISABLE Pitch Bend (IMPORTANT!)

1. Find **"PITCH BEND"** or **"BEND RANGE"** column
2. **Press** top pad
3. Look for an **"OFF"** option or **"0"** semitones
4. **Press "OFF"** or **"0"**
   - **WHY:** Pitch bend can interfere with clip launching and drum triggering
   - Session/Drum modes need clean note-on messages

### Step 8: Pressure/Velocity (Optional)

1. Adjust if you want lighter touch for button-press feel
2. Find **"PRESSURE SENS"** or **"VELOCITY SENS"**
3. Try lowering sensitivity for easier clip launching
4. Personal preference - test and adjust

### Step 9: Save Preset 2

1. **Press and hold** the **PRESET** button (left panel)
   - Hold 2-3 seconds until it flashes
2. **Release** - Preset 2 saved!

### Step 10: Exit Global Settings

1. **Press** **GLOBAL SETTINGS** button
   - Back to playing surface

---

## Part 3: Configure Switch 1 (Mode Switching Button)

This button will cycle through Keyboard → Session → Drum modes.

### Step 1: Enter Global Settings

1. **Press and hold** **GLOBAL SETTINGS**
   - Button lights YELLOW

### Step 2: Navigate to Switch Assign

1. Look for column labeled **"SWITCH 1"** or **"ASSIGN SW1"**
2. If you don't see it immediately, look for **"ASSIGN"** section
3. **Press** the top pad in the **SWITCH 1** column

### Step 3: Set Function to CC (Control Change)

1. You'll see function options:
   - CC (Control Change) ← **SELECT THIS**
   - Note
   - Octave
   - Arpeggiator
   - Other functions
2. **Press "CC"**

### Step 4: Set CC Number to 65

1. After selecting CC, you'll see a number picker
2. You need to set this to **CC 65**
3. **Methods to enter 65:**

   **Method A: Direct Entry**
   - Look for number display (large digits on grid)
   - Swipe left/right across the grid to scroll through numbers
   - Find **65** and release

   **Method B: Button Presses**
   - Some firmware versions show number pads
   - Press **6**, then **5**
   - Or use +/- buttons to reach 65

### Step 5: Set Channel to 1

1. Look for **"CHANNEL"** setting for Switch 1
2. **Press** to enter channel selection
3. Select **Channel 1**
   - Matches our MIDI configuration

### Step 6: Set Mode to Toggle (Optional)

1. Look for **"MODE"** or **"TYPE"** setting
2. You'll see:
   - **Toggle** (press once = on, press again = off)
   - **Momentary** (only on while held)
3. Choose **Toggle** or **Momentary** - either works!
   - Toggle: One press cycles mode
   - Momentary: Press and release cycles mode

### Step 7: Save

1. Settings usually save automatically
2. **Press and hold GLOBAL SETTINGS** to exit
   - Or just press GLOBAL SETTINGS once to exit

### Step 8: Test Switch 1

1. **Press Switch 1** (left panel button)
2. Watch for it to send MIDI CC 65
3. You can verify in Ableton's MIDI monitor if needed

---

## Part 4: Find Your Base Note

The software needs to know which MIDI note your bottom-left pad plays.

### Step 1: Switch to Preset 1

1. **Press PRESET button** (left panel) to cycle presets
2. Or in Global Settings, select Preset 1
3. Ensure you're in **One Channel** mode

### Step 2: Enable MIDI Monitor in Ableton

1. Open Ableton Live
2. Create a new MIDI track
3. Arm the track for recording
4. Open **View → MIDI Monitor** (or use built-in monitor)

### Step 3: Press Bottom-Left Pad

1. On your LinnStrument, press the **bottom-left corner pad**
   - This is column 0, row 0
2. Look at MIDI monitor in Ableton
3. Note the **MIDI note number** displayed

### Common Base Notes:

| MIDI Note | Note Name | Octave Setting |
|-----------|-----------|----------------|
| 36 | C2 | Octave ~4-5 |
| 40 | E2 | Octave ~5 |
| 48 | C3 | Octave 5 (factory default) |
| 60 | C4 | Octave 6 |

### Step 4: Configure in Software

1. Navigate to:
   ```
   /Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/config.py
   ```

2. Open `config.py` in a text editor

3. Find the line:
   ```python
   LINNSTRUMENT_BASE_NOTE = 36  # C2 - matches Push
   ```

4. Change `36` to **your base note number**

5. **Save** the file

6. **Restart Ableton** (or toggle Remote Script off/on in MIDI preferences)

---

## Part 5: Enable in Ableton Live

### Step 1: Open Ableton Preferences

1. **Ableton Live** menu → **Preferences**
2. Or **Cmd+,** (Mac) / **Ctrl+,** (Windows)

### Step 2: Go to MIDI Settings

1. Click **Link/Tempo/MIDI** tab
2. Scroll to **MIDI Ports** section

### Step 3: Find Your LinnStrument

1. Look in the list of MIDI devices
2. Find your LinnStrument (usually named "LinnStrument MIDI 1" or similar)

### Step 4: Set Control Surface

1. In the row for your LinnStrument, find the **Control Surface** dropdown
2. Click it and select **LinnstrumentScale128**
   - If you don't see it, the files weren't copied correctly
   - Check: `/Users/wagner/Music/Ableton/User Library/Remote Scripts/`

### Step 5: Set Input and Output

1. **Input** column: Select your LinnStrument input port
2. **Output** column: Select your LinnStrument output port
3. Both should be enabled (checkbox checked)

### Step 6: Restart Ableton

1. Close Ableton completely
2. Reopen Ableton Live
3. The Remote Script will initialize

### Step 7: Verify in Log

1. Open Ableton's Log.txt:
   ```
   ~/Library/Preferences/Ableton/Live X.X.X/Log.txt
   ```

2. Look for these messages:
   ```
   Linnstrument Multi-Mode System - Starting...
   Linnstrument MIDI controller initialized
   All modes initialized
   Linnstrument Multi-Mode System - Ready!
   Press Switch 1 (CC65) to cycle modes
   ```

3. If you see errors, check the log for details

---

## Part 6: Quick Test

### Test 1: Mode Switching

1. **Press Switch 1**
2. Look at Ableton's **status bar** (bottom center)
3. You should see:
   - "Linnstrument: Keyboard Mode" (first press, or at startup)
   - "Linnstrument: Session Mode" (second press)
   - "Linnstrument: Drum Mode" (third press)
   - Cycles back to Keyboard...

### Test 2: Keyboard Mode

1. Switch to **Preset 1** on LinnStrument
2. Press **Switch 1** until you see "Linnstrument: Keyboard Mode"
3. In Ableton, create a MIDI track
4. Set scale in Ableton (or use Push's scale mode)
5. **Look at LinnStrument grid** - scale notes should light up!
   - Root notes in one color
   - Other scale notes in another color

### Test 3: Session Mode

1. Switch to **Preset 2** on LinnStrument
2. Press **Switch 1** until you see "Linnstrument: Session Mode"
3. Create some clips in Session View
4. **Look at grid** - clip colors should appear
5. **Press a pad** - clip should launch
6. **Press again** - clip should stop

### Test 4: Drum Mode

1. Keep **Preset 2** active
2. Press **Switch 1** until you see "Linnstrument: Drum Mode"
3. Load a Drum Rack on a MIDI track
4. **Bottom 4 rows** should show drum pads
5. **Press a drum pad** - sound should trigger, pad turns white
6. **Top row** shows sequencer for that pad
7. **Press steps** to toggle them on/off
8. **Press Play in Ableton** - sequence should play

---

## Troubleshooting

### "Scale doesn't light up in Keyboard mode"

**Check:**
- LinnStrument is in Preset 1 (One Channel)
- Global Settings button is YELLOW (User Firmware Mode enabled)
- Base note in config.py matches your hardware
- Scale is set in Ableton (try C Major to start)

**Fix:**
- Verify base note: press bottom-left pad, check MIDI monitor
- Restart Ableton after changing config.py

---

### "Switch 1 doesn't cycle modes"

**Check:**
- Switch 1 is set to CC 65, Channel 1
- Log.txt shows "Mode switch CC received" when you press it
- Remote Script is loaded in Ableton preferences

**Fix:**
- Re-configure Switch 1 in Global Settings
- Verify in MIDI monitor that Switch 1 sends CC 65
- Check Ableton's MIDI preferences (Control Surface selected)

---

### "Clips don't launch in Session mode"

**Check:**
- LinnStrument is in Preset 2 (Channel Per Row)
- Pitch Bend is OFF in Preset 2
- Clips exist in Session View

**Fix:**
- Switch to Preset 2 manually
- Verify Pitch Bend is disabled
- Check Log.txt for "Launched clip" messages

---

### "Sequencer doesn't play in Drum mode"

**Check:**
- Ableton transport is running (press Space)
- Drum Rack is on selected track
- Steps are toggled on (cyan color)
- LinnStrument is in Preset 2

**Fix:**
- Start Ableton playback
- Load a Drum Rack
- Press sequencer steps to enable them (should turn cyan)

---

## Summary Checklist

Before using the multi-mode system:

- [ ] Preset 1 configured (One Channel, 5-semitone row offset)
- [ ] Preset 2 configured (Channel Per Row, Pitch Bend OFF)
- [ ] Switch 1 set to CC 65, Channel 1
- [ ] Base note detected and configured in config.py
- [ ] Files copied to Ableton Remote Scripts folder
- [ ] Control Surface selected in Ableton MIDI preferences
- [ ] Ableton restarted
- [ ] Log.txt shows "Multi-Mode System - Ready!"
- [ ] Mode switching works (Switch 1 cycles modes)
- [ ] Each mode tested and working

---

## Still Having Issues?

1. **Check Log.txt** for error messages:
   ```
   ~/Library/Preferences/Ableton/Live X.X.X/Log.txt
   ```

2. **Verify file installation**:
   ```bash
   ls -la "/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/"
   ```
   Should see: config.py, led_manager.py, modes/ directory

3. **Test base note** detection:
   - Open MIDI monitor
   - Press bottom-left pad
   - Note the MIDI note number
   - Ensure it matches config.py

4. **Check MIDI connection**:
   - LinnStrument USB connected
   - Shows up in Ableton's MIDI devices
   - Input and Output both enabled

---

**You're all set! Press Switch 1 to start exploring the three modes!** 🎵
