# LinnStrument Setup - Simple Method (Physical Buttons Only)

**No grid navigation needed! Just use the physical buttons on the left panel.**

---

## 🎯 Step 1: Configure Preset 1 (Keyboard Mode)

### A. Switch to Preset 1

**Press the PRESET button** (left panel) repeatedly until Preset 1 is active
- You'll see a small indicator or LED showing which preset is active
- Keep pressing until you reach Preset 1

### B. Enter Settings

**Press and hold GLOBAL SETTINGS** button (left panel)
- Button lights up YELLOW
- Bottom 4 rows become settings menu

### C. Change Settings

Look at the **printed labels on your panel** below the grid. Press the pads above each label:

1. **MIDI MODE (Column 1):**
   - Press **Row 3** (topmost setting) = "ONE CHANNEL"
   - Pad lights up

2. **CHANNEL (Column 2):**
   - Press **Row 0** (bottom setting) = Channel 1

3. **ROW OFFSET (Column 4):**
   - Press **Row 3** = 5 semitones
   - (Standard guitar-like tuning)

4. **OCTAVE (Column 5 or 6):**
   - Press **Row 2 or 3** (middle options) = Octave 5 or 6
   - Try Octave 5 first

### D. Save and Exit

**Press GLOBAL SETTINGS** button again
- Settings automatically save to Preset 1!
- You're done with Preset 1!

---

## 🎯 Step 2: Configure Preset 2 (Session/Drum Modes)

### A. Switch to Preset 2

**Press the PRESET button** (left panel) repeatedly until Preset 2 is active
- Usually just one or two presses from Preset 1

### B. Enter Settings

**Press and hold GLOBAL SETTINGS** button

### C. Change Settings

1. **MIDI MODE (Column 1):**
   - Press **Row 1** = "CHANNEL PER ROW"
   - **CRITICAL: Must be Channel Per Row, not One Channel!**

2. **ROW OFFSET (Column 4):**
   - Press **Row 3** = 5 semitones
   - (Same as Preset 1)

3. **OCTAVE (Column 5 or 6):**
   - Press **same row** as you chose for Preset 1
   - (Keeps note layout consistent)

4. **BEND RANGE (Column 3):**
   - Press **Row 0** (lowest setting) = Minimal pitch bend
   - **IMPORTANT: Prevents interference with clip launching**

### D. Save and Exit

**Press GLOBAL SETTINGS** button again
- Settings automatically save to Preset 2!
- You're done with Preset 2!

---

## 🎯 Step 3: Configure Switch 1 (Mode Button)

### A. Enter Settings

**Press and hold GLOBAL SETTINGS** button

### B. Select Switch 1

**Look for Column 7** (might be labeled "SELECT SW" on your panel)
- Press **Row 3** = Switch 1
- This tells the LinnStrument you're about to configure Switch 1

### C. Assign CC65 Function

**Look at Columns 8-9** (might be labeled "ASSIGN SWITCH")

You'll see function options. Look for one of these:

**Option 1: You see "CC65" labeled on a pad**
- **Press that pad!** You're done!

**Option 2: You see "CC" (generic) and "SUSTAIN" and other functions**
- **Press the "CC" pad**
- You'll see a number display or entry method
- **Enter the number 65**
  - Method A: Swipe left/right on pads to scroll to 65
  - Method B: Use +/- pads to reach 65
  - Method C: Press number pads if shown

**Option 3: You see "CC65" in a different column**
- Just **press the pad labeled CC65**

### D. Save and Exit

**Press GLOBAL SETTINGS** button
- Switch 1 is now configured to send CC65!

---

## 🎯 Step 4: Find Your Base Note

### A. Make Sure You're on Preset 1

**Press PRESET button** until Preset 1 is active

### B. Open Ableton MIDI Monitor

1. Open Ableton Live
2. Create a MIDI track
3. Set Input to "LinnStrument"
4. **Arm the track** (red record button)
5. You should see MIDI activity indicator

### C. Press Bottom-Left Pad

On your LinnStrument:
- Press the **very bottom-left corner pad**
- Look at Ableton - what MIDI note number appears?

**Write down this number!** Common values:
- 36 = C2
- 40 = E2
- 48 = C3
- 60 = C4

### D. Update config.py

1. **Open Finder**
2. **Navigate to:**
   ```
   /Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/
   ```

3. **Right-click on `config.py`**
4. **Open With → TextEdit** (or any text editor)

5. **Find line 8:**
   ```python
   LINNSTRUMENT_BASE_NOTE = 36  # C2 - matches Push
   ```

6. **Change `36` to YOUR base note number**
   ```python
   LINNSTRUMENT_BASE_NOTE = 48  # (use your number!)
   ```

7. **Save the file** (Cmd+S)

8. **Close TextEdit**

---

## 🎯 Step 5: Enable in Ableton

### A. Open Ableton Preferences

**Ableton Live menu → Preferences** (or press Cmd+,)

### B. Go to MIDI Settings

Click the **"Link/Tempo/MIDI"** tab

### C. Find Your LinnStrument

In the **MIDI Ports** section, find the row with your LinnStrument (usually called "LinnStrument MIDI 1")

### D. Configure Control Surface

In that row:

1. **Control Surface** dropdown → Select **"LinnstrumentScale128"**
2. **Input** dropdown → Select your LinnStrument input
3. **Output** dropdown → Select your LinnStrument output
4. **Track** and **Remote** checkboxes → Both ON

### E. Close Preferences

**Close the Preferences window**

### F. Restart Ableton

1. **Quit Ableton completely** (Cmd+Q)
2. **Reopen Ableton Live**
3. The Remote Script will load!

---

## ✅ Test Everything!

### Test 1: Check the Log

1. **Open Finder**
2. **Go to:**
   ```
   ~/Library/Preferences/Ableton/Live X.X.X/
   ```
   (X.X.X = your Live version, like 11.3.25)

3. **Open `Log.txt`** (double-click, opens in TextEdit)

4. **Scroll to the bottom** and look for:
   ```
   Linnstrument Multi-Mode System - Starting...
   Linnstrument MIDI controller initialized
   All modes initialized
   Linnstrument Multi-Mode System - Ready!
   ```

**✓ If you see "Ready!" - installation successful!**

### Test 2: Mode Switching

1. **Press Switch 1** (left panel button)
2. **Look at Ableton's status bar** (bottom center of window)
3. You should see one of:
   - "Linnstrument: Keyboard Mode"
   - "Linnstrument: Session Mode"
   - "Linnstrument: Drum Mode"

**✓ If mode name appears - Switch 1 works!**

### Test 3: Keyboard Mode

1. **Press PRESET button** → switch to Preset 1
2. **Press Switch 1** → until you see "Keyboard Mode"
3. In Ableton, **set a scale** (try C Major)
4. **Look at your LinnStrument grid**

**✓ Scale notes should light up!**
- Root notes = one color
- Scale notes = another color

### Test 4: Session Mode

1. **Press PRESET button** → switch to Preset 2
2. **Press Switch 1** → until you see "Session Mode"
3. Create some **clips in Session View**
4. **Look at your LinnStrument grid**

**✓ Clip colors should appear on pads!**
- Press a pad → clip launches
- Playing clips glow green

### Test 5: Drum Mode

1. **Keep Preset 2 active**
2. **Press Switch 1** → until you see "Drum Mode"
3. **Load a Drum Rack** on a MIDI track
4. **Look at your LinnStrument**

**✓ You should see:**
- Bottom 4 rows = drum pad colors
- Top row = sequencer (all off initially)
- Press a drum pad → it triggers sound + turns white
- Press top row pads → they toggle on (cyan)
- Press Play in Ableton → sequence plays!

---

## 🆘 Troubleshooting

### "I don't see Ready! in the log"

**Check:**
1. Files are in the right place: `/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/`
2. Folder contains: `LinnstrumentScale.py`, `config.py`, `led_manager.py`, `modes/` directory
3. Control Surface is set to "LinnstrumentScale128" in preferences
4. Ableton was completely restarted after installation

**Fix:** Look for ERROR messages in Log.txt - they'll tell you what's wrong

### "Scale doesn't light up in Keyboard Mode"

**Check:**
1. Using Preset 1? (press PRESET button)
2. Global Settings button is YELLOW? (User Firmware Mode enabled)
3. Base note in config.py matches your hardware?
4. Scale is actually set in Ableton?

**Fix:** Re-test base note (press bottom-left pad, check MIDI monitor)

### "Switch 1 doesn't cycle modes"

**Check:**
1. Switch 1 is configured to CC65?
2. When you press Switch 1, does MIDI monitor show CC65?
3. Log.txt shows "Mode switch CC received"?

**Fix:**
- Reconfigure Switch 1 (Step 3 above)
- Or try a different CC number and update config.py

### "Clips don't launch in Session Mode"

**Check:**
1. Using Preset 2? (Channel Per Row)
2. Bend range is minimal?
3. Clips actually exist in Session View?

**Fix:**
- Switch to Preset 2 manually
- Make sure you configured Preset 2 correctly (CHANNEL PER ROW)

### "Drum pads don't make sound"

**Check:**
1. Drum Rack is loaded on selected track?
2. Drum Rack has samples loaded in the pads?
3. Track is armed/monitoring input?

**Fix:**
- Load a factory Drum Rack preset (has samples pre-loaded)
- Make sure track is selected in Ableton

---

## 📋 Quick Reference Card

### Physical Button Functions:

```
PRESET button (left panel)
  → Cycles through presets (1→2→3→4→5→6→1...)
  → Use this to switch between Preset 1 and Preset 2

GLOBAL SETTINGS button (left panel)
  → Press and hold: Enter/exit settings menu
  → Button turns YELLOW when active

Switch 1 button (left panel)
  → Configured to send CC65
  → Cycles software modes: Keyboard → Session → Drum
```

### Preset Usage:

```
Preset 1 (One Channel)
  → Use for: Keyboard Mode
  → Settings: MIDI MODE = One Channel, ROW OFFSET = 5

Preset 2 (Channel Per Row)
  → Use for: Session Mode + Drum Mode
  → Settings: MIDI MODE = Channel Per Row, BEND RANGE = minimal
```

### Workflow:

```
For Keyboard Mode:
  1. PRESET button → Preset 1
  2. Switch 1 → "Keyboard Mode"
  3. Play with scale lighting

For Session Mode:
  1. PRESET button → Preset 2
  2. Switch 1 → "Session Mode"
  3. Launch clips

For Drum Mode:
  1. PRESET button → Preset 2 (same as Session)
  2. Switch 1 → "Drum Mode"
  3. Play drums + program sequence
```

---

## 🎵 You're Ready!

**All set up! Now just:**
1. Press PRESET to switch hardware presets
2. Press Switch 1 to cycle software modes
3. Make music!

**Need help? Check the full guides:**
- `MULTIMODE_README.md` - Complete user guide
- `LINNSTRUMENT_VISUAL_SETUP_GUIDE.md` - Visual reference
- `IMPLEMENTATION_COMPLETE.md` - What was built

---

**Happy music-making!** 🎹🎵
