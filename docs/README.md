# LinnStrument Documentation

This folder contains reference documentation for LinnStrument MIDI programming.

## Quick Reference

| Document | Purpose |
|----------|---------|
| [NRPN_REFERENCE.md](./NRPN_REFERENCE.md) | Complete guide to critical NRPNs with examples |
| [DEVELOPMENT_NOTES.md](./DEVELOPMENT_NOTES.md) | Development log, known issues, testing checklist |
| [linnstrument_midi_spec.txt](./linnstrument_midi_spec.txt) | Official MIDI spec from LinnStrument firmware repo |
| [user_firmware_mode.txt](./user_firmware_mode.txt) | User Firmware Mode documentation |

## Key NRPN Values (Quick Ref)

### Drum Mode Setup
```python
# Enable LED control
send_nrpn(245, 1)  # User Firmware Mode ON

# Set 4x4 chromatic grid
send_nrpn(227, 4)  # Row offset = 4 semitones
send_nrpn(36, 4)   # Octave = -1 (shift C3 to C2)
```

### Keyboard Mode Restore
```python
send_nrpn(227, 5)  # Row offset = 5 semitones (fourths)
send_nrpn(36, 5)   # Octave = 0 (default)
```

### Cleanup on Disconnect
```python
send_nrpn(227, 5)  # Restore default row offset
send_nrpn(36, 5)   # Restore default octave
send_nrpn(245, 0)  # Disable User Firmware Mode
```

## Drum Mode Note Layout

With `row_offset=4` and `octave=-1`:

```
Row 3: [ 48] [ 49] [ 50] [ 51]  C3  C#3  D3  D#3  (Pads 12-15)
Row 2: [ 44] [ 45] [ 46] [ 47]  G#2  A2  A#2  B2  (Pads 8-11)
Row 1: [ 40] [ 41] [ 42] [ 43]  E2   F2  F#2  G2  (Pads 4-7)
Row 0: [ 36] [ 37] [ 38] [ 39]  C2  C#2  D2  D#2  (Pads 0-3)
```

Standard Ableton drum rack uses notes 36-51 for main 16 pads.

## Troubleshooting

**Problem**: Only top row lights up
- Check `row_offset=4` and `octave=4` are sent correctly
- Verify NRPN messages have all 6 CCs (99, 98, 6, 38, 101, 100)

**Problem**: Mode switching stops after Global Settings
- Global Settings disables User Firmware Mode
- Re-send `NRPN 245=1` to re-enable

**Problem**: Wrong octave
- Check LinnStrument's Global Settings > Octave
- Should be set to make bottom-left play C2 (note 36)
- Or use NRPN 36 to shift octave

## External Links
- [LinnStrument Support](https://www.rogerlinndesign.com/support/linnstrument-getting-started)
- [LinnStrument Firmware](https://github.com/rogerlinndesign/linnstrument-firmware)
- [Panel Settings Guide](https://www.rogerlinndesign.com/support/linnstrument-support-panel-settings)
