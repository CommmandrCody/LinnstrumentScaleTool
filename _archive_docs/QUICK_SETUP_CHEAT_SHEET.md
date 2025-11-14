# LinnStrument Multi-Mode - Quick Setup Cheat Sheet

Print this page and keep it next to your LinnStrument!

---

## 🎯 PRESET 1 - Keyboard Mode (One Channel)

### Settings:
```
Column 0, Row 1  → Open Preset Select
  → Press Preset 1 button (top-left of 6-button grid)

Column 1, Row 3  → MIDI MODE = "ONE CHANNEL"
Column 2, Row 0  → CHANNEL = 1
Column 4, Row 3  → ROW OFFSET = 5 semitones
Column 5-6       → OCTAVE = 5 or 6

Column 0, Row 1  → Back to Preset Select
  → HOLD Preset 1 button for 2+ seconds to SAVE
```

---

## 🎯 PRESET 2 - Session/Drum Modes (Channel Per Row)

### Settings:
```
Column 0, Row 1  → Open Preset Select
  → Press Preset 2 button (top-middle of 6-button grid)

Column 1, Row 1  → MIDI MODE = "CHANNEL PER ROW"
Column 4, Row 3  → ROW OFFSET = 5 semitones (same as Preset 1)
Column 5-6       → OCTAVE = same as Preset 1
Column 3         → BEND RANGE = 2 semitones or lowest setting

Column 0, Row 1  → Back to Preset Select
  → HOLD Preset 2 button for 2+ seconds to SAVE
```

---

## 🎯 SWITCH 1 - Mode Button (CC65)

### Settings:
```
Column 7, Row 3  → SELECT SWITCH = Switch 1

Column 8-9       → Find "CC65" or "CC" option
  → Press "CC65" pad
  OR
  → Press "CC" pad, then enter number 65
```

---

## 📝 Column Reference (Look at YOUR panel labels!)

```
Col 0:  PRESET
Col 1:  MIDI MODE
Col 2:  CHANNEL/MAIN
Col 3:  BEND RANGE
Col 4:  ROW OFFSET
Col 5:  OCTAVE/LOW ROW
Col 7:  SELECT SW
Col 8-9: ASSIGN SWITCH
```

---

## 🧪 Find Base Note

```
1. Switch to Preset 1 (press PRESET button)
2. Open Ableton MIDI Monitor
3. Press bottom-left pad (Column 0, Row 0)
4. Note the MIDI number (e.g., 36, 48, 60)
5. Edit config.py:
   LINNSTRUMENT_BASE_NOTE = [your number]
6. Save and restart Ableton
```

---

## ✅ Quick Test

### Preset 1 Test:
- All pads → same MIDI channel ✓

### Preset 2 Test:
- Bottom row → Channel 1
- Second row → Channel 2
- Each row → different channel ✓

### Switch 1 Test:
- Press Switch 1 → see "CC65" in MIDI monitor ✓

### Mode Cycling Test:
- Press Switch 1 → status bar shows mode name ✓

---

## 🎹 Using the System

### Keyboard Mode:
1. Preset 1 (PRESET button)
2. Switch 1 → "Keyboard Mode"
3. Set scale in Ableton
4. Scale lights up!

### Session Mode:
1. Preset 2 (PRESET button)
2. Switch 1 → "Session Mode"
3. Press pads to launch clips

### Drum Mode:
1. Preset 2 (PRESET button)
2. Switch 1 → "Drum Mode"
3. Bottom 4 rows = drum pads
4. Top row = sequencer

---

## 🆘 Troubleshooting

**Scale doesn't light:**
- Check base note in config.py
- Global Settings button = YELLOW?
- Using Preset 1?

**Clips don't launch:**
- Using Preset 2?
- Bend range = minimal?

**Switch 1 doesn't work:**
- Check CC65 in MIDI monitor
- Reconfigure in Column 7-9

**Mode doesn't change:**
- Check Ableton Log.txt
- Remote Script enabled?

---

## 📄 Files Installed

```
/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/
```

Contains: LinnstrumentScale.py, config.py, led_manager.py, modes/

---

**Full documentation:**
- LINNSTRUMENT_VISUAL_SETUP_GUIDE.md (detailed walkthrough)
- MULTIMODE_README.md (complete user guide)
- PRESET_SETUP_STEP_BY_STEP.md (super detailed)

---

🎵 **Ready to make music!** 🎵
