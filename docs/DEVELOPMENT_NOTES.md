# LinnStrument Drum Mode Development Notes

## Project Status (2025-11-19)

### Working Features
- ✅ Keyboard mode with scale lighting
- ✅ Automatic mode switching based on drum rack detection
- ✅ NRPN messaging to control LinnStrument settings
- ✅ User Firmware Mode control for LED management

### Current Issues
✅ **ALL CORE FEATURES WORKING** (2025-11-19)

### Setup Requirement
⚠️ **IMPORTANT**: User must configure LinnStrument hardware so lower-left pad plays C2 (note 36)
   - Go to LinnStrument: Global Settings > Per-Split Settings > Octave
   - Adjust octave until lower-left pad in drum mode plays C2
   - This ensures drum pads align with Ableton's standard drum rack (notes 36-51)

## Implementation Details

### File Structure
- `Linnstrument.py` - Main control surface (simple version, active)
- `modes/drum_mode.py` - Complex drum mode with sequencer (not currently used)
- `modes/keyboard_mode.py` - Keyboard mode (not currently used)
- `linnstrument_ableton.py` - MIDI communication layer
- `led_manager.py` - LED control with caching
- `scales.py` - Musical scale definitions
- `config.py` - Configuration constants

### Active Implementation
The **simple** implementation in `Linnstrument.py` is currently active:
- Auto-switches modes based on drum rack detection
- Drum mode: 4x4 pad grid + 16-step sequencer
- Keyboard mode: Scale lighting based on Ableton's scale settings

The **complex** implementation in `modes/` exists but is not used by `__init__.py`.

### Drum Mode Configuration

#### Hardware Settings (via NRPN)
- **Row Offset**: NRPN 227 = 4 (4 semitones per row, major third interval)
- **Octave**: NRPN 36 = 4 (-1 octave transposition)
- **User Firmware Mode**: NRPN 245 = 1 (enable LED control)

#### Software Settings
- **base_note**: 36 (C2, standard drum rack start note)
- **row_offset**: 4 (matches hardware NRPN setting)
- **column_offset**: 1 (chromatic, one semitone per column)

#### Expected Note Layout (4x4 drum grid)
```
Row 3: 48  49  50  51  (C3  C#3 D3  D#3) - Pads 12-15
Row 2: 44  45  46  47  (G#2 A2  A#2 B2)  - Pads 8-11
Row 1: 40  41  42  43  (E2  F2  F#2 G2)  - Pads 4-7
Row 0: 36  37  38  39  (C2  C#2 D2  D#2) - Pads 0-3
       Col 0  1   2   3
```

## Code Changes (Session 2025-11-19)

### Fixed Issues
1. ✅ **Missing `_enable_user_firmware_mode()` method**
   - Was called but never defined
   - Fixed by replacing call with direct NRPN send: `_send_nrpn(245, 1)`

2. ✅ **Wrong note range for drum pads**
   - Was using 24-39 (C1-D#3)
   - Changed to 36-51 (C2-D#3) for standard drum rack compatibility
   - Updated all references in `build_midi_map()`, `receive_midi()`, drum pad color checks

3. ✅ **Added octave control**
   - Added NRPN 36=4 to shift octave down by one
   - Makes bottom-left pad play C2 (36) instead of C3 (48)

4. ✅ **Added comprehensive logging**
   - Log mode switch checks
   - Log NRPN sends
   - Log drum rack detection

5. ✅ **Added disconnect cleanup**
   - Restore row offset to 5 (fifths)
   - Restore octave to 5 (default)
   - Disable User Firmware Mode

### Testing Checklist
- ✅ All 4 rows of drum pads light up
- ✅ All 4 rows send MIDI notes
- ✅ Pad colors match drum rack state:
  - White: selected pad
  - Green: has sample
  - Off: no sample
- ✅ Mode switches correctly when changing tracks
- ✅ LED clearing works when switching back to keyboard mode
- ✅ Keyboard mode works (scale lighting)
- ✅ Script properly disconnects and restores settings
- ⚠️ User must set LinnStrument octave so lower-left = C2

## Known NRPN Pitfalls

1. **Incomplete message sequence causes issues**
   - MUST send all 6 CC messages (99, 98, 6, 38, 101, 100)
   - Skipping the reset messages (101, 100) causes unpredictable behavior

2. **User Firmware Mode gets disabled**
   - Entering Global Settings on LinnStrument hardware disables it
   - No way to detect when user exits Global Settings
   - May need to periodically re-send NRPN 245=1

3. **Row offset values are NOT semitone counts**
   - Value 4 = 4 semitones (major third)
   - Value 5 = 5 semitones (perfect fourth)
   - But value 0, 13, 127 have special meanings

4. **Octave settings interact with base note**
   - LinnStrument factory default: bottom-left plays C3 (48)
   - To get C2 (36) for drum rack, must:
     - Set octave to -1 (NRPN 36 = 4), OR
     - Configure LinnStrument's Global Settings > Octave manually

## Next Steps

1. **Test current fixes**
   - Restart Ableton
   - Load drum rack track
   - Verify all 4 rows work
   - Test mode switching

2. **If still broken**
   - Check Ableton log for NRPN messages
   - Use MIDI monitor to see what hardware is actually sending
   - May need to manually configure LinnStrument octave setting

3. **Future enhancements**
   - Add manual octave calibration tool
   - Detect when User Firmware Mode gets disabled
   - Add configuration UI for base note
   - Document user workflow for initial setup

## Development Environment

### Testing Setup
1. Ableton Live 12.2.7
2. LinnStrument 128 (16 columns x 8 rows)
3. Log file: `~/Library/Preferences/Ableton/Live 12.2.7/Log.txt`
4. Remote Script path: `~/Music/Ableton/User Library/Remote Scripts/LinnStrument/`

### Quick Testing
```bash
# CRITICAL: Clear Python cache BEFORE restarting Ableton
# Otherwise old cached .pyc files will run instead of your changes!
cd ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument/
./clear_cache.sh

# OR manually:
find ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument -name "*.pyc" -delete
find ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument -type d -name "__pycache__" -exec rm -rf {} +

# Watch log in real-time
tail -f ~/Library/Preferences/Ableton/Live\ 12.2.7/Log.txt | grep -i linnstrument

# Reload script (restart Ableton required)
# 1. Clear cache (see above)
# 2. Restart Ableton
# 3. Check log for new messages

# Emergency disable User Firmware Mode
python emergency_disable_user_mode.py
```

### Git Status
```
On branch: main
Modified: requirements.txt (has junk text, needs cleanup)
Untracked: emergency_disable_user_mode.py
Recent commit: 49eb731 - FIX: Simplify drum mode to match Push layout
```

## References
- [LinnStrument MIDI Spec](./linnstrument_midi_spec.txt) - Complete NRPN list
- [NRPN Reference](./NRPN_REFERENCE.md) - Key NRPNs with examples
- [LinnStrument Panel Settings](https://www.rogerlinndesign.com/support/linnstrument-support-panel-settings)
- [LinnStrument Firmware GitHub](https://github.com/rogerlinndesign/linnstrument-firmware)
