# Claude Code Directives for LinnStrument Project

## CRITICAL: Always Clear Python Cache Before Testing

**EVERY TIME** you modify any `.py` file in the Remote Scripts directory, you **MUST**:

1. **Clear Python cache** BEFORE telling user to restart Ableton:
```bash
cd "$HOME/Music/Ableton/User Library/Remote Scripts/LinnStrument"
find . -name "*.pyc" -delete
find . -type d -name "__pycache__" -exec rm -rf {} +
```

2. Or use the helper script:
```bash
cd "$HOME/Music/Ableton/User Library/Remote Scripts/LinnStrument"
./clear_cache.sh
```

**WHY**: Ableton loads cached `.pyc` files. If cache isn't cleared, old code runs and changes won't take effect. This causes confusion and wasted time debugging "changes that don't work."

## ALWAYS Review Documentation Before Coding

Before answering questions or writing code related to LinnStrument NRPN or MIDI, **ALWAYS** check these files first:

1. **NRPN_REFERENCE.md** - Quick reference for critical NRPNs with examples
2. **linnstrument_midi_spec.txt** - Complete official MIDI specification
3. **user_firmware_mode.txt** - User Firmware Mode documentation
4. **DEVELOPMENT_NOTES.md** - Known issues, recent changes, testing checklist

**Location**: `/Users/wagner/LinnstrumentScaleTool/docs/`

**WHY**: The documentation contains critical information that's easy to forget:
- NRPN 227 value meanings (3=minor third, 4=major third, 5=fourth, etc.)
- User Firmware Mode changes note behavior (coordinate system vs musical notes)
- LED control (CC 20/21/22) works WITHOUT User Firmware Mode
- Complete NRPN message format (6-message sequence)

## Key Facts to Remember

### User Firmware Mode (NRPN 245)
- **Value 1**: Enable - Changes notes to coordinate system (0-25 on channels 1-8)
- **Value 0**: Disable - Normal musical notes based on LinnStrument settings
- **LED Control (CC 20/21/22) works in BOTH modes**
- **DO NOT enable User Firmware Mode for drum mode** - it breaks normal MIDI notes

### Row Offset (NRPN 227)
- Value 3 = 3 semitones (minor third)
- **Value 4 = 4 semitones (major third)** ← Use for drum mode
- **Value 5 = 5 semitones (perfect fourth)** ← Default for keyboard mode
- Value 6 = 6 semitones (tritone)
- Value 7 = 7 semitones (perfect fifth)
- Value 12 = 12 semitones (octave)
- Value 13 = Guitar tuning
- Value 127 = 0 offset

### Octave (NRPN 36)
- Values 0-10: -5 to +5 octaves
- Value 5 = default (no transposition)
- **Only change if user's LinnStrument is set to wrong octave**
- Better to ask user to set octave in LinnStrument Global Settings

### Standard Drum Rack Layout
- Notes 36-51 (C2-D#3) for main 16 pads
- With row_offset=4, bottom-left should be note 36 (C2)
- User's LinnStrument octave setting determines actual note

## Testing Workflow

1. **Make code changes**
2. **Clear Python cache** (see above)
3. **Restart Ableton**
4. **Check log file**: `tail -f ~/Library/Preferences/Ableton/Live\ 12.2.7/Log.txt | grep -i linnstrument`
5. **Test functionality**
6. **If changes don't work**: Verify cache was cleared, check log for errors

## Common Mistakes to Avoid

1. ❌ **Forgetting to clear Python cache** → Old code runs
2. ❌ **Enabling User Firmware Mode for drum pads** → Notes become coordinates
3. ❌ **Using wrong row_offset value** → Wrong note spacing
4. ❌ **Changing octave when user hasn't configured LinnStrument** → Wrong starting note
5. ❌ **Not checking documentation** → Re-discovering known issues

## File Locations Reference

```
/Users/wagner/LinnstrumentScaleTool/
├── docs/
│   ├── NRPN_REFERENCE.md          ← Read this first!
│   ├── DEVELOPMENT_NOTES.md       ← Current status, known issues
│   ├── linnstrument_midi_spec.txt ← Complete NRPN list
│   ├── user_firmware_mode.txt     ← User mode behavior
│   └── README.md                  ← Quick reference
└── emergency_disable_user_mode.py ← Emergency recovery tool

/Users/wagner/Music/Ableton/User Library/Remote Scripts/LinnStrument/
├── Linnstrument.py                ← Main control surface (ACTIVE)
├── linnstrument_ableton.py        ← MIDI communication layer
├── led_manager.py                 ← LED control with caching
├── scales.py                      ← Scale definitions
├── config.py                      ← Configuration constants
├── clear_cache.sh                 ← Cache clearing helper
└── modes/                         ← Alternative implementation (not used)
    ├── drum_mode.py
    ├── keyboard_mode.py
    └── base_mode.py
```

## Before Making Changes

Ask yourself:
1. Have I checked the documentation?
2. Do I understand User Firmware Mode behavior?
3. Do I know what NRPN values I need?
4. Will I remember to clear cache after changes?

## After Making Changes

Checklist:
- [ ] Clear Python cache
- [ ] Tell user to restart Ableton
- [ ] Check log file for initialization messages
- [ ] Verify changes took effect
- [ ] Update DEVELOPMENT_NOTES.md with status

## Emergency Recovery

If LinnStrument gets stuck in User Firmware Mode:
```bash
cd /Users/wagner/LinnstrumentScaleTool
python emergency_disable_user_mode.py
```

This sends NRPN 245=0 to disable User Firmware Mode and restore normal operation.
