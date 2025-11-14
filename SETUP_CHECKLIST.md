# LinnStrument Multi-Mode Setup Checklist

**Follow this step-by-step. Check off each box as you go.**

---

## ☐ Part 1: Preset 1 Setup (5 minutes)

### ☐ 1. Switch to Preset 1
- [ ] Press **PRESET** button (left panel) until Preset 1 is active

### ☐ 2. Enter settings
- [ ] Press and hold **GLOBAL SETTINGS** button
- [ ] Button turns YELLOW

### ☐ 3. Set MIDI Mode
- [ ] Find Column 1 (look for "MIDI MODE" label on panel)
- [ ] Press **Column 1, Row 3** (topmost pad) = "ONE CHANNEL"

### ☐ 4. Set Channel
- [ ] Find Column 2 (look for "CHANNEL" label)
- [ ] Press **Column 2, Row 0** (bottom pad) = Channel 1

### ☐ 5. Set Row Offset
- [ ] Find Column 4 (look for "ROW OFFSET" label)
- [ ] Press **Column 4, Row 3** = 5 semitones

### ☐ 6. Set Octave
- [ ] Find Column 5 or 6 (look for "OCTAVE" label)
- [ ] Press **Row 2 or Row 3** (middle option) = Octave 5 or 6

### ☐ 7. Save
- [ ] Press **GLOBAL SETTINGS** button again
- [ ] Settings auto-saved to Preset 1!

---

## ☐ Part 2: Preset 2 Setup (5 minutes)

### ☐ 1. Switch to Preset 2
- [ ] Press **PRESET** button until Preset 2 is active

### ☐ 2. Enter settings
- [ ] Press and hold **GLOBAL SETTINGS** button

### ☐ 3. Set MIDI Mode
- [ ] Find Column 1
- [ ] Press **Column 1, Row 1** = "CHANNEL PER ROW"
- [ ] ⚠️ IMPORTANT: Must be Row 1, not Row 3!

### ☐ 4. Set Row Offset
- [ ] Find Column 4
- [ ] Press **Column 4, Row 3** = 5 semitones (same as Preset 1)

### ☐ 5. Set Octave
- [ ] Find Column 5 or 6
- [ ] Press **same row** as you chose for Preset 1

### ☐ 6. Set Bend Range
- [ ] Find Column 3 (look for "BEND RANGE" label)
- [ ] Press **Column 3, Row 0** (lowest pad) = Minimal bend

### ☐ 7. Save
- [ ] Press **GLOBAL SETTINGS** button
- [ ] Settings auto-saved to Preset 2!

---

## ☐ Part 3: Switch 1 Setup (3 minutes)

### ☐ 1. Enter settings
- [ ] Press and hold **GLOBAL SETTINGS** button

### ☐ 2. Select Switch 1
- [ ] Find Column 7 (look for "SELECT SW" label)
- [ ] Press **Column 7, Row 3** = Switch 1

### ☐ 3. Assign CC65
- [ ] Find Columns 8-9 (look for "ASSIGN SWITCH" label)
- [ ] Look for "CC65" or "CC" option
- [ ] Press the **"CC65"** pad
  - OR press **"CC"** pad and enter number **65**

### ☐ 4. Save
- [ ] Press **GLOBAL SETTINGS** button
- [ ] Switch 1 configured!

---

## ☐ Part 4: Find Base Note (2 minutes)

### ☐ 1. Switch to Preset 1
- [ ] Press **PRESET** button → Preset 1

### ☐ 2. Open MIDI Monitor in Ableton
- [ ] Create MIDI track
- [ ] Set Input to "LinnStrument"
- [ ] Arm track (red button)

### ☐ 3. Press bottom-left pad
- [ ] Press **bottom-left corner pad** on LinnStrument
- [ ] Look at Ableton MIDI monitor
- [ ] Write down the MIDI note number: **___________**

### ☐ 4. Update config.py
- [ ] Navigate to: `/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/`
- [ ] Open `config.py` in TextEdit
- [ ] Find line 8: `LINNSTRUMENT_BASE_NOTE = 36`
- [ ] Change `36` to your number: **___________**
- [ ] Save file (Cmd+S)

---

## ☐ Part 5: Enable in Ableton (3 minutes)

### ☐ 1. Open Preferences
- [ ] **Ableton Live → Preferences** (or Cmd+,)

### ☐ 2. Go to MIDI tab
- [ ] Click **"Link/Tempo/MIDI"** tab

### ☐ 3. Find LinnStrument
- [ ] Locate row with "LinnStrument MIDI 1" (or similar)

### ☐ 4. Set Control Surface
- [ ] **Control Surface** dropdown → **"LinnstrumentScale128"**
- [ ] **Input** dropdown → Your LinnStrument input
- [ ] **Output** dropdown → Your LinnStrument output

### ☐ 5. Restart Ableton
- [ ] Quit Ableton (Cmd+Q)
- [ ] Reopen Ableton Live
- [ ] Wait for it to fully load

---

## ☐ Part 6: Test (5 minutes)

### ☐ Test 1: Check Log
- [ ] Open Finder → `~/Library/Preferences/Ableton/Live X.X.X/`
- [ ] Open `Log.txt`
- [ ] Look for: **"Linnstrument Multi-Mode System - Ready!"**
- [ ] ✓ If you see "Ready!" → SUCCESS!

### ☐ Test 2: Mode Switching
- [ ] Press **Switch 1** button (left panel)
- [ ] Look at Ableton status bar (bottom center)
- [ ] Should show: **"Linnstrument: [Mode Name]"**
- [ ] Press Switch 1 again → mode name changes
- [ ] ✓ If mode name appears → SUCCESS!

### ☐ Test 3: Keyboard Mode
- [ ] Press **PRESET** button → Preset 1
- [ ] Press **Switch 1** → "Keyboard Mode" appears
- [ ] In Ableton, set scale to **C Major**
- [ ] Look at LinnStrument grid
- [ ] ✓ If scale notes light up → SUCCESS!

### ☐ Test 4: Session Mode
- [ ] Press **PRESET** button → Preset 2
- [ ] Press **Switch 1** → "Session Mode" appears
- [ ] Create a clip in Session View
- [ ] Look at LinnStrument grid
- [ ] ✓ If clip colors appear → SUCCESS!
- [ ] Press a pad
- [ ] ✓ If clip launches → SUCCESS!

### ☐ Test 5: Drum Mode
- [ ] Keep Preset 2 active
- [ ] Press **Switch 1** → "Drum Mode" appears
- [ ] Load a Drum Rack on track
- [ ] Look at LinnStrument
- [ ] ✓ If bottom rows show drum pads → SUCCESS!
- [ ] Press a drum pad
- [ ] ✓ If sound plays + pad turns white → SUCCESS!

---

## 🎉 All Done!

### ☐ Final Checklist:
- [ ] Preset 1 configured (One Channel)
- [ ] Preset 2 configured (Channel Per Row)
- [ ] Switch 1 sends CC65
- [ ] Base note configured in config.py
- [ ] Control Surface enabled in Ableton
- [ ] Log shows "Ready!"
- [ ] Mode switching works
- [ ] Keyboard Mode lights scale
- [ ] Session Mode launches clips
- [ ] Drum Mode plays drums

---

## 🆘 If Something Doesn't Work:

### Check these common issues:

**Scale doesn't light (Keyboard Mode):**
- [ ] Using Preset 1?
- [ ] Global Settings button is YELLOW?
- [ ] Base note matches in config.py?
- [ ] Scale set in Ableton?

**Clips don't launch (Session Mode):**
- [ ] Using Preset 2?
- [ ] MIDI Mode = Channel Per Row?
- [ ] Clips exist in Session View?

**Drums don't play (Drum Mode):**
- [ ] Using Preset 2?
- [ ] Drum Rack loaded?
- [ ] Track selected and armed?

**Mode doesn't change:**
- [ ] Switch 1 configured to CC65?
- [ ] Check MIDI monitor: does Switch 1 send CC65?
- [ ] Check Log.txt for "Mode switch CC received"

---

## 📚 Full Documentation:

- **SIMPLE_PRESET_SETUP.md** - Detailed walkthrough
- **MULTIMODE_README.md** - Complete user guide
- **LINNSTRUMENT_VISUAL_SETUP_GUIDE.md** - Visual reference

---

**Ready to make music! 🎵**

**Time to complete: ~20 minutes**
**Difficulty: Easy (just follow the steps!)**
