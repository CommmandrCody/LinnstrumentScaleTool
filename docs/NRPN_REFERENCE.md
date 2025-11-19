# LinnStrument NRPN Reference

## Critical NRPNs for Drum Mode

### NRPN 227: Global Row Offset
Controls the pitch interval between rows.

| Value | Interval | Semitones | Use Case |
|-------|----------|-----------|----------|
| 0 | No overlap | varies | Each row starts one pitch higher than previous row's end |
| 3 | Minor third | 3 | Compact layout |
| **4** | **Major third** | **4** | **DRUM MODE - chromatic 4x4 grid** |
| 5 | Perfect fourth | 5 | DEFAULT - keyboard mode, guitar/bass tuning |
| 6 | Tritone | 6 | Alternative layout |
| 7 | Perfect fifth | 7 | Alternative layout |
| 12 | Octave | 12 | Octave layout |
| 13 | Guitar | varies | Guitar tuning (upper 6 rows + 2 bass strings) |
| 127 | Zero offset | 0 | No row offset |

**For Drum Mode**: Use value **4** (4 semitones per row) to get chromatic 4x4 layout:
- Row 0: notes 36-39 (C2, C#2, D2, D#2)
- Row 1: notes 40-43 (E2, F2, F#2, G2)
- Row 2: notes 44-47 (G#2, A2, A#2, B2)
- Row 3: notes 48-51 (C3, C#3, D3, D#3)

**For Keyboard Mode**: Use value **5** (5 semitones per row) - default fourths tuning

### NRPN 245: User Firmware Mode
Controls whether custom firmware can control LEDs.

| Value | Mode | Description |
|-------|------|-------------|
| 0 | Disabled | Normal operation - LinnStrument firmware controls LEDs |
| 1 | Enabled | User Firmware Mode - allow external LED control via CC messages |

**Important**: User Firmware Mode is automatically DISABLED when:
- User enters Global Settings on the LinnStrument hardware
- User manually disables it via hardware

We must re-enable it (value=1) when our script initializes and potentially periodically to maintain LED control.

### NRPN 36: Split Left Octave
Controls octave transposition for left split.

| Value | Octave Shift | Semitones | Description |
|-------|--------------|-----------|-------------|
| 0 | -5 octaves | -60 | Extremely low |
| 1 | -4 octaves | -48 | Very low |
| 2 | -3 octaves | -36 | Low |
| 3 | -2 octaves | -24 | Lower |
| **4** | **-1 octave** | **-12** | **DRUM MODE - shifts C3(48) down to C2(36)** |
| 5 | 0 octaves | 0 | DEFAULT - no transposition |
| 6 | +1 octave | +12 | Higher |
| 7 | +2 octaves | +24 | High |
| 8 | +3 octaves | +36 | Very high |
| 9 | +4 octaves | +48 | Extremely high |
| 10 | +5 octaves | +60 | Extremely high |

**For Drum Mode**: Use value **4** (-1 octave) to shift from C3 (48) to C2 (36) for standard drum rack layout

**For Keyboard Mode**: Use value **5** (no transposition) to restore default

## Complete NRPN Message Format

LinnStrument requires a 6-message sequence for each NRPN:

```python
def send_nrpn(nrpn_number, value):
    """Send complete NRPN to LinnStrument"""
    status = 0xB0  # CC on channel 1

    # Split NRPN number into MSB and LSB
    nrpn_msb = (nrpn_number >> 7) & 0x7F
    nrpn_lsb = nrpn_number & 0x7F

    # Split value into MSB and LSB
    value_msb = (value >> 7) & 0x7F
    value_lsb = value & 0x7F

    # Send 6-message sequence
    send_midi([status, 99, nrpn_msb])    # CC 99: NRPN MSB
    send_midi([status, 98, nrpn_lsb])    # CC 98: NRPN LSB
    send_midi([status, 6, value_msb])    # CC 6: Data Entry MSB
    send_midi([status, 38, value_lsb])   # CC 38: Data Entry LSB
    send_midi([status, 101, 127])        # CC 101: RPN reset MSB
    send_midi([status, 100, 127])        # CC 100: RPN reset LSB
```

**Critical**: Must send ALL 6 messages in sequence. Skipping the reset messages (CC 101/100) can cause unpredictable behavior.

## Drum Mode Setup Sequence

When entering drum mode:
1. Send NRPN 245 = 1 (Enable User Firmware Mode)
2. Send NRPN 227 = 4 (Row offset = 4 semitones)
3. Send NRPN 36 = 4 (Octave = -1)
4. Update internal base_note = 36
5. Update internal row_offset = 4

When exiting drum mode (back to keyboard):
1. Send NRPN 227 = 5 (Row offset = 5 semitones, default)
2. Send NRPN 36 = 5 (Octave = 0, default)
3. Restore internal base_note = 36 (or user's configured value)
4. Restore internal row_offset = 5

When disconnecting:
1. Send NRPN 227 = 5 (Restore default row offset)
2. Send NRPN 36 = 5 (Restore default octave)
3. Send NRPN 245 = 0 (Disable User Firmware Mode)

## Standard Drum Rack Note Layout

Drum racks in Ableton use notes 36-51 for the main 16 pads (C2-D#3).

With row_offset=4 and octave=-1:
- **Row 0** (bottom): 36-39 = C2, C#2, D2, D#2 (pads 0-3)
- **Row 1**: 40-43 = E2, F2, F#2, G2 (pads 4-7)
- **Row 2**: 44-47 = G#2, A2, A#2, B2 (pads 8-11)
- **Row 3** (top of drum grid): 48-51 = C3, C#3, D3, D#3 (pads 12-15)

This matches Ableton Push and other standard drum controllers.

## Troubleshooting

### Problem: LEDs don't light up
- Check if User Firmware Mode is enabled (NRPN 245 = 1)
- User may have disabled it by entering Global Settings
- Solution: Re-send NRPN 245 = 1

### Problem: Only top row lights up in drum mode
- Check row_offset is set to 4, not 5
- Check octave is set to 4 (-1 octave), not 5 (default)
- Check base_note is 36, not 48

### Problem: Mode doesn't switch back after entering Global Settings
- Global Settings disables User Firmware Mode
- Our script can't detect when user exits Global Settings
- Solution: Re-send initialization sequence when track changes
