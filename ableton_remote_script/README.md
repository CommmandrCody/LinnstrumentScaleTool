# Linnstrument Scale Light - Ableton MIDI Remote Script

Automatic Ableton integration that lights up your Linnstrument to match Ableton's scale settings in real-time.

## Features

- **Automatic Scale Detection**: Reads Ableton's global scale settings directly from the API
- **Real-time Updates**: Lights update instantly when you change the scale or root note
- **Track Color Integration**: LED colors adapt based on selected track color (like Ableton Push)
- **Two-Color Display**: Root notes highlighted in one color, other scale notes in another
- **User Firmware Mode**: Automatically enables Linnstrument's User Firmware Mode for LED control
- **Supports Both Models**: Separate optimized scripts for Linnstrument 128 and 200

## Installation

### Choose Your Model

- **Linnstrument 128** (16 columns): Use `LinnstrumentScale128`
- **Linnstrument 200** (26 columns): Use `LinnstrumentScale200`

### Steps

1. **Copy the appropriate folder to your Ableton Remote Scripts directory:**

   **macOS:**
   ```bash
   cp -r LinnstrumentScale128 ~/Music/Ableton/User\ Library/Remote\ Scripts/
   ```

   **Windows:**
   ```
   Copy LinnstrumentScale128 to:
   %USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
   ```

2. **Configure your Linnstrument base note:**

   - Press the **bottom-left pad** on your Linnstrument and note what MIDI note it plays
   - Open `LinnstrumentScale.py` in a text editor
   - Find line 99: `LINNSTRUMENT_BASE_NOTE = 36`
   - Change the value to match your Linnstrument's bottom-left note:
     - `36` = C2 (Push-style layout) **← recommended**
     - `48` = C3 (factory default)
     - `40` = E2 (guitar tuning)
   - Save the file

3. **Enable in Ableton:**

   - Open Ableton Live Preferences → **Link/Tempo/MIDI**
   - In the MIDI Ports section, find your Linnstrument
   - Under **Control Surface**, select **LinnstrumentScale128** (or 200)
   - Under **Input**, select your Linnstrument MIDI port
   - Under **Output**, select your Linnstrument MIDI port

4. **Restart Ableton** (if already running)

## Usage

The script works completely automatically:

1. **Change Scale**: Press **Cmd+Shift+S** (Mac) or **Ctrl+Shift+S** (Windows) to open Scale settings
2. **Select Root & Scale**: Choose your root note and scale type
3. **Watch Lights Update**: Your Linnstrument LEDs automatically update!

### What You'll See

- **Root notes**: Displayed in a brighter color (e.g., red)
- **Other scale notes**: Displayed in a related color (e.g., pink or blue)
- **Track colors**: LED colors change based on the selected track's color in Ableton

### Track Color Behavior

Similar to Ableton Push, the script maps track colors to Linnstrument LED colors:
- **Red tracks** → Red roots, pink scale notes
- **Green tracks** → Green roots, lime scale notes
- **Blue tracks** → Blue roots, cyan scale notes
- And so on...

## Supported Scales

The script automatically recognizes all Ableton scale types:

- Major, Minor
- Dorian, Phrygian, Lydian, Mixolydian, Locrian
- Harmonic Minor, Melodic Minor
- Major Pentatonic, Minor Pentatonic
- Blues, Whole Tone, Diminished
- Super Locrian (Altered), Hungarian Minor
- Spanish, Japanese, and more!

## How It Works

The MIDI Remote Script:
1. **Enables User Firmware Mode** on the Linnstrument (via NRPN 245)
2. **Monitors Ableton's scale settings** using `song.root_note` and `song.scale_name` listeners
3. **Tracks color changes** when you select different tracks
4. **Calculates which pads** on the Linnstrument correspond to scale notes
5. **Sends LED commands** via MIDI CC20 (column), CC21 (row), CC22 (color)
6. **Updates in real-time** whenever scale settings change

### Technical Details

- Uses Ableton's Live API to monitor scale changes
- Automatically detects Linnstrument grid layout (16 or 26 columns)
- Handles LED addressing correctly (columns 1-16/26 for playable surface, column 0 for controls)
- Filters scale notes to only those within the Linnstrument's playable range

## Troubleshooting

### LEDs not lighting up

1. Check that **LinnstrumentScale128** (or 200) is selected as Control Surface in Ableton MIDI preferences
2. Make sure both **Input** and **Output** are set to your Linnstrument MIDI port
3. Check Ableton's **Log.txt** file for error messages (Help → Show Log)
4. Verify the **Global Settings** button on your Linnstrument is lit **yellow** (indicates User Firmware Mode is active)
5. **Restart Ableton** Live after installing the script

### Wrong pads lighting up

1. Verify you're using the correct script:
   - **LinnstrumentScale128** for 16-column Linnstrument 128
   - **LinnstrumentScale200** for 26-column Linnstrument 200
2. Check the `LINNSTRUMENT_BASE_NOTE` setting in `LinnstrumentScale.py` line 99:
   - Press bottom-left pad and note the MIDI note number
   - Update the setting to match
3. Verify row offset (line 104):
   - Most common: `5` semitones (fourths, like Push)
   - Should match your Linnstrument's row offset setting

### Global Settings button not turning yellow

- The script sends **NRPN 245 = 1** to enable User Firmware Mode
- If it doesn't activate automatically, try manually:
  - Press and hold **"OS Update"** in Global Settings for half a second
  - This toggles User Firmware Mode on/off

### Script doesn't appear in Ableton

- Make sure you copied the entire `LinnstrumentScale128` (or 200) folder
- **Restart Ableton** Live completely
- Check the **Log.txt** file for errors:
  - macOS: `~/Library/Preferences/Ableton/Live <version>/Log.txt`
  - Windows: `%APPDATA%\Ableton\Live <version>\Preferences\Log.txt`

## Advanced Configuration

### Custom Row Offset

If you've customized your Linnstrument's row offset, edit line 104 in `LinnstrumentScale.py`:

```python
row_offset=5,      # Semitones per row (change if needed)
```

Common values:
- `5` = Fourths (standard, matches Push)
- `4` = Major thirds
- `7` = Fifths
- `12` = Octaves

### Disable User Firmware Mode

User Firmware Mode is required for LED control. To disable it:
- Press and hold **"OS Update"** in Global Settings for half a second
- Or send **NRPN 245 = 0** via MIDI

## Viewing Logs

The script logs useful debug information to Ableton's Log.txt:

**macOS:**
```
~/Library/Preferences/Ableton/Live <version>/Log.txt
```

**Windows:**
```
%APPDATA%\Ableton\Live <version>\Preferences\Log.txt
```

Look for messages starting with "Linnstrument" to see what the script is doing.

## Tips

- The script updates automatically when you change Ableton's scale settings
- Works great with Ableton's **Scale mode** enabled on MIDI clips
- Pair with Ableton Push for the ultimate scale visualization setup!
- LED colors are based on the **selected track's color** in Ableton
- Try changing track colors to see different LED color schemes

## Uninstall

1. In Ableton Preferences, set **Control Surface** back to **"None"**
2. Delete the `LinnstrumentScale128` (or 200) folder from Remote Scripts directory
3. **Restart Ableton**
4. (Optional) Disable User Firmware Mode on your Linnstrument

## Files

- `LinnstrumentScale.py` - Main Remote Script
- `linnstrument_ableton.py` - LED control using Ableton's MIDI API
- `scales.py` - Scale definitions (30+ scales)
- `__init__.py` - Required by Ableton
- `diagnostic.py` - API exploration tool (used during development)
- `clear_leds.py` - Utility to clear all LEDs
- `test_single_pad.py` - Diagnostic test script

## Credits

Built for Linnstrument by Roger Linn Design.

Uses Ableton Live's MIDI Remote Script API.
