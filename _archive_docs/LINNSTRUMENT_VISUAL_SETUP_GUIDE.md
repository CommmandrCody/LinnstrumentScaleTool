# LinnStrument Visual Setup Guide - Multi-Mode System

This guide uses the **actual LinnStrument panel layout** to show you exactly which pads to press.

---

## Understanding the LinnStrument Global Settings Interface

### When you press GLOBAL SETTINGS:

The **bottom 4 rows** of your playing surface become the settings menu.

```
Your LinnStrument Grid (looking down at it):

Row 7 ┌────────────────────────────────────────────┐
Row 6 │                                            │
Row 5 │     NORMAL PLAYING SURFACE                 │
Row 4 │     (stays as playing area)                │
      │                                            │
Row 3 ├────────────────────────────────────────────┤
Row 2 │                                            │  ← SETTINGS MENU
Row 1 │     SETTINGS DISPLAYED HERE                │     (4 rows)
Row 0 └────────────────────────────────────────────┘
      Col0  Col1  Col2 ... Col15
```

### Important: Read the Panel Labels

**Look at the PRINTED LABELS below each column** on your physical LinnStrument.

The bottom 4 rows correspond to the settings printed on the panel below them.

---

## Part 1: Configure Preset 1 (One Channel Mode)

### Step 1: Enter Global Settings

**Press GLOBAL SETTINGS button** (left panel, bottom row of buttons)
- Button lights up **YELLOW**
- Bottom 4 rows of grid now show settings

### Step 2: Go to Preset Selection

**Look at Column 0** (far left column of the grid)
- You should see printed label **"PRESET"** on the panel below it
- The bottom 4 rows of Column 0 show preset-related options

**Press the pad at:**
- **Column 0, Row 1** (second row from bottom)
- This shows the "PRESET SELECT" screen

### Step 3: Select Preset 1

You'll now see a **6-button grid** on the right side (presets 1-6)

```
Preset buttons layout:
┌────┬────┬────┐
│ 1  │ 2  │ 3  │  ← Top row
├────┼────┼────┤
│ 4  │ 5  │ 6  │  ← Bottom row
└────┴────┴────┘
```

**Press the top-left button** for Preset 1
- It lights up showing it's selected

### Step 4: Set MIDI Mode to "One Channel"

**Look at Column 1** (second column from left)
- Printed label below should say **"MIDI MODE"**

**What you'll see in Column 1:**
- Row 3 (top setting row): "ONE CHANNEL"
- Row 2: "CHANNEL PER NOTE"
- Row 1: "CHANNEL PER ROW"
- Row 0: (other options)

**Press Column 1, Row 3** (topmost pad in Column 1)
- This selects "ONE CHANNEL" mode
- Pad lights up to confirm selection

### Step 5: Set MIDI Channel

**Look at Column 2**
- Printed label: **"MAIN"** or **"CHANNEL"**

**Press Column 2, Row 0** (bottom pad in Column 2)
- This sets Channel 1 (most common)
- Or press higher rows for channels 2-16

### Step 6: Set Row Offset

**Look at Column 4**
- Printed label might say **"ROW OFFSET"** or **"INTERVAL"**

The pads show different semitone intervals:
- Row 0: 0 semitones (unison)
- Row 1: 3 semitones (minor third)
- Row 2: 4 semitones (major third)
- Row 3: **5 semitones (fourth)** ← WE WANT THIS
- Or you might see: 7 semitones, 12 semitones

**Press the pad for 5 semitones** (usually Row 3)
- This gives you guitar-like fourths tuning
- Standard isomorphic layout

### Step 7: Set Octave/Low Row

**Look at Column 5 or 6**
- Printed label: **"OCTAVE"** or **"LOW ROW"**

You'll see octave numbers (-1, 0, 1, 2, 3, 4, 5, 6, etc.)

**Recommended: Press Row 2 or 3** (middle options)
- Try **Octave 5** first (makes bottom-left = C3)
- You can adjust this later based on your base note test

### Step 8: SAVE Preset 1

**IMPORTANT: Must save or changes will be lost!**

1. **Press Column 0, Row 1** again (go back to Preset Select screen)
2. You'll see the 6 preset buttons again
3. **Press and HOLD the Preset 1 button for 2+ seconds**
   - Button will flash RED
   - Then turn solid - SAVED!

### Step 9: Exit Global Settings

**Press GLOBAL SETTINGS button** again
- Button turns off
- You're back to normal playing surface

---

## Part 2: Configure Preset 2 (Channel Per Row Mode)

### Step 1: Enter Global Settings

**Press GLOBAL SETTINGS button**
- Bottom 4 rows = settings menu

### Step 2: Go to Preset Selection

**Press Column 0, Row 1** (Preset Select)

### Step 3: Select Preset 2

**Press the top-middle button** in the preset grid
- This is Preset 2
- Lights up when selected

### Step 4: Set MIDI Mode to "Channel Per Row"

**Look at Column 1** (MIDI MODE column)

**Press Column 1, Row 1** (second row from bottom)
- This selects "CHANNEL PER ROW"
- **CRITICAL for Session/Drum modes!**

### Step 5: Set Row Offset (Same as Preset 1)

**Look at Column 4** (ROW OFFSET)

**Press the pad for 5 semitones** (same as Preset 1)
- Keeps layout consistent

### Step 6: Set Octave (Same as Preset 1)

**Look at Column 5-6** (OCTAVE)

**Select the same octave** you chose for Preset 1
- Keeps note mapping consistent

### Step 7: DISABLE Pitch Bend (IMPORTANT!)

**Look for Column that says "BEND RANGE" or "PITCH BEND"**
- Usually around Column 3 or elsewhere

**Options you'll see:**
- Row 3: 48 semitones
- Row 2: 24 semitones
- Row 1: 12 semitones
- Row 0: **2 semitones** ← PRESS THIS (minimal bend)

**Press Row 0** (lowest setting - 2 semitones or OFF)
- Minimizes pitch bend interference with clip launching

### Step 8: SAVE Preset 2

1. **Press Column 0, Row 1** (back to Preset Select)
2. **Press and HOLD Preset 2 button for 2+ seconds**
   - Flashes RED, then solid
   - SAVED!

### Step 9: Exit Global Settings

**Press GLOBAL SETTINGS button**

---

## Part 3: Configure Switch 1 for Mode Switching

This is the trickiest part. Let me break it down carefully.

### Step 1: Enter Global Settings

**Press GLOBAL SETTINGS button**

### Step 2: Navigate to Switch Assignment

**Look for columns 7-9** (might be labeled on your panel)

#### Column 7: "SELECT SW" (Select which switch to configure)
- Row 3: Switch 1 ← **PRESS THIS**
- Row 2: Switch 2
- Row 1: Foot Left
- Row 0: Foot Right

**Press Column 7, Row 3** (Switch 1)

#### Column 8-9: "ASSIGN SWITCH" (What function to assign)

After selecting Switch 1, **look at Columns 8-9**.

You'll see function options spread across multiple pads:
- "SUSTAIN"
- "CC65" ← **WE WANT THIS!**
- "OCTAVE +"
- "OCTAVE -"
- "ARPEGGIATOR"
- etc.

**Press the pad labeled "CC65"**
- This assigns Switch 1 to send CC65
- Perfect for mode switching!

### Alternative: If you don't see "CC65" label:

Some firmware versions show **"CC"** function, then ask for the number.

**If you see "CC" option:**
1. Press the "CC" pad
2. You'll see a number entry interface
3. **Enter 65** (might need to swipe or use +/- buttons)
4. Confirm

### Step 3: Exit Global Settings

**Press GLOBAL SETTINGS button**
- Switch 1 is now configured!

---

## Part 4: Find Your Base Note

### Step 1: Switch to Preset 1

**Press the PRESET button** (left panel)
- Cycles through presets
- Watch the LEDs or display to see which preset is active
- Get to Preset 1

### Step 2: Open MIDI Monitor in Ableton

1. Create a MIDI track in Ableton
2. Set Input to your LinnStrument
3. Arm the track (red button)
4. Open **View → MIDI Monitor** (or check track input)

### Step 3: Press Bottom-Left Pad

**On your LinnStrument:**
- Press the **very bottom-left corner pad** (Column 0, Row 0)
- **Look at Ableton's MIDI Monitor**
- Note the MIDI note number shown

### Step 4: Write Down the Number

Common values:
- 36 = C2
- 40 = E2
- 48 = C3 (factory default)
- 60 = C4

**This is your BASE NOTE!**

### Step 5: Update config.py

1. On your Mac, open:
   ```
   /Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnstrumentScale128/config.py
   ```

2. Find line 8:
   ```python
   LINNSTRUMENT_BASE_NOTE = 36  # C2 - matches Push
   ```

3. Change `36` to **your base note number**

4. **Save the file**

5. **Restart Ableton Live**

---

## Visual Reference: Column Layout

Here's what the typical Global Settings columns control:

```
Column   Setting          Options
──────   ──────────────   ────────────────────────────
0        PRESET           Select/Save presets
1        MIDI MODE        One Channel / Channel Per Row / etc.
2        CHANNEL/MAIN     MIDI channel (1-16)
3        BEND RANGE       Pitch bend amount
4        ROW OFFSET       Semitones between rows (we want 5)
5-6      OCTAVE/LOW ROW   Which octave for bottom row
7        SELECT SW        Choose which switch to configure
8-9      ASSIGN SWITCH    Function for selected switch
10-15    Other settings   Velocity, pressure, etc.
```

**Look at the printed labels on YOUR panel** - they're the authoritative guide!

---

## Quick Test Checklist

After configuration, verify:

### ✓ Preset 1 Check
1. Switch to Preset 1 (PRESET button)
2. Play a note - should send on ONE channel
3. All pads send same MIDI channel

### ✓ Preset 2 Check
1. Switch to Preset 2 (PRESET button)
2. Play bottom row - sends on Channel 1
3. Play second row - sends on Channel 2
4. Each row = different channel

### ✓ Switch 1 Check
1. In Ableton, open MIDI Monitor
2. Press Switch 1 button (left panel)
3. Should see **CC65** message
4. If not, reconfigure Switch assignment

### ✓ Base Note Check
1. Preset 1 active
2. Press bottom-left pad
3. Note the MIDI note number
4. Update config.py to match

---

## Still Stuck?

### Can't find the right column?

**Method: Trial and Error**
1. Press GLOBAL SETTINGS
2. Press each pad in the bottom 4 rows, one by one
3. Watch what happens on the grid
4. When you see preset numbers → Column 0
5. When you see "One Channel" options → Column 1
6. Keep exploring!

### Can't save preset?

**Make sure:**
- You're in the Preset Select screen (Column 0, Row 1)
- You **HOLD** the preset button for 2+ seconds (not just tap)
- Button flashes RED = saving
- Button turns solid = saved

### Switch 1 doesn't send CC65?

**Alternatives:**
- Use a foot pedal instead (configure FOOT L or FOOT R to CC65)
- Use a specific grid pad (we can modify software to detect)
- Tell me what options YOU see in Column 8-9 and we can work with that

---

## Need More Help?

Tell me:
1. **What labels** do you see printed on YOUR panel below the grid?
2. **What happens** when you press Column 1, Row 3? (should be MIDI mode)
3. **What options** appear when you press Column 7-9 pads?

I can guide you through YOUR specific LinnStrument layout!

---

**Once configured, you're ready to test the multi-mode system!** 🎵
