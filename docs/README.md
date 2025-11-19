# LinnStrument Documentation

This folder contains reference documentation for LinnStrument MIDI programming.

## ✅ Status: ALL FEATURES WORKING (2025-11-19)

- Keyboard mode with scale lighting
- Drum mode with 4x4 pad grid + LED feedback
- Automatic mode switching based on drum rack detection
- LED clearing when switching between modes

## Quick Reference

| Document | Purpose |
|----------|---------|
| [NRPN_REFERENCE.md](./NRPN_REFERENCE.md) | Complete guide to critical NRPNs with examples |
| [DEVELOPMENT_NOTES.md](./DEVELOPMENT_NOTES.md) | Development log, known issues, testing checklist |
| [linnstrument_midi_spec.txt](./linnstrument_midi_spec.txt) | Official MIDI spec from LinnStrument firmware repo |
| [user_firmware_mode.txt](./user_firmware_mode.txt) | User Firmware Mode documentation |

## ⚠️ Setup Requirement

**IMPORTANT**: Configure your LinnStrument so the lower-left pad plays C2 (note 36):
1. Press both "Per-Split Settings" buttons simultaneously (Global Settings)
2. Navigate to: Per-Split Settings > Octave
3. Adjust octave until lower-left pad plays C2
4. This ensures drum pads align with Ableton's standard drum rack (notes 36-51)

## Key NRPN Values (Current Implementation)

### Drum Mode Setup
```python
# Set 4x4 chromatic grid (4 semitones per row)
send_nrpn(227, 4)  # Row offset = 4 semitones (major third)

# NOTE: User Firmware Mode (NRPN 245) is NOT used
# LED control (CC 20/21/22) works without it
# Notes pass through naturally to Ableton
```

### Keyboard Mode Restore
```python
# Restore fourths tuning for keyboard mode
send_nrpn(227, 5)  # Row offset = 5 semitones (perfect fourth)
```

### Cleanup on Disconnect
```python
# Restore default tuning
send_nrpn(227, 5)  # Restore row offset to fifths
```

## Drum Mode Note Layout

With `row_offset=4` (4 semitones per row) and LinnStrument octave set to C2:

```
Row 3: [ 48] [ 49] [ 50] [ 51]  C3  C#3  D3  D#3  (Pads 12-15)
Row 2: [ 44] [ 45] [ 46] [ 47]  G#2  A2  A#2  B2  (Pads 8-11)
Row 1: [ 40] [ 41] [ 42] [ 43]  E2   F2  F#2  G2  (Pads 4-7)
Row 0: [ 36] [ 37] [ 38] [ 39]  C2  C#2  D2  D#2  (Pads 0-3)
        Col0  Col1  Col2  Col3
```

Standard Ableton drum rack uses notes 36-51 for main 16 pads.
**Note**: User must configure LinnStrument octave so lower-left pad = C2 (see Setup Requirement above)

## Troubleshooting

**Problem**: LEDs stay lit in wrong mode (drum LEDs persist in keyboard mode)
- ✅ FIXED: LED clearing now forces update with `clear_all(force=True)`
- Scale-change optimization removed to ensure LED updates on mode switch

**Problem**: Wrong octave / notes don't match drum rack
- Configure LinnStrument Global Settings > Octave
- Lower-left pad should play C2 (note 36)
- Do NOT use NRPN 36 to change octave - it can cause side effects

**Problem**: Mode not switching when changing tracks
- ✅ FIXED: Track listener was always working correctly
- Check logs for "=== TRACK CHANGED - checking mode ==="

## External Links
- [LinnStrument Support](https://www.rogerlinndesign.com/support/linnstrument-getting-started)
- [LinnStrument Firmware](https://github.com/rogerlinndesign/linnstrument-firmware)
- [Panel Settings Guide](https://www.rogerlinndesign.com/support/linnstrument-support-panel-settings)
