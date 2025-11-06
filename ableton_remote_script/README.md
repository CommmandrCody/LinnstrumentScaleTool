# Linnstrument Scale Light - Ableton MIDI Remote Script

Automatic Ableton integration that updates your Linnstrument lights based on track names.

## Installation

### Automatic (Recommended)

Run the installer which will copy the script to Ableton:

```bash
./install.sh
```

### Manual Installation

1. Copy the `LinnstrumentScale` folder to your Ableton MIDI Remote Scripts directory:

**macOS:**
```bash
cp -r ableton_remote_script/LinnstrumentScale ~/Music/Ableton/User\ Library/Remote\ Scripts/
```

**Windows:**
```
Copy ableton_remote_script\LinnstrumentScale to:
%USERPROFILE%\Documents\Ableton\User Library\Remote Scripts\
```

2. Restart Ableton Live

3. Go to **Preferences → Link/Tempo/MIDI**

4. Under **Control Surface**, select **LinnstrumentScale** from the dropdown

5. You should see "Linnstrument Scale: Connected" in Ableton's status bar

## Usage

### Method 1: Track Names (Easiest)

Name your MIDI tracks with the scale you want:
- `C Major`
- `D Minor`
- `G Dorian`
- `A Minor Pentatonic`

When you select the track, the Linnstrument lights will update automatically!

### Method 2: Clip Names

Name your MIDI clips with scales:
- `C Major Melody`
- `D Dorian Solo`

The script will parse the scale from the name.

## Supported Scale Names

The script recognizes Ableton's built-in scale names:
- Major, Minor
- Dorian, Phrygian, Lydian, Mixolydian, Locrian
- Harmonic Minor, Melodic Minor
- Minor Pentatonic, Major Pentatonic
- Blues, Whole Tone, Diminished
- And more!

## Troubleshooting

### "No Linnstrument Found"

- Make sure your Linnstrument is connected via USB
- Check it appears in Audio MIDI Setup (Mac) or Device Manager (Windows)

### Script doesn't appear in Ableton

- Make sure you copied the entire `LinnstrumentScale` folder
- Restart Ableton Live completely
- Check the Log.txt file in Ableton's preferences folder for errors

### Lights don't update

- Make sure you named the track with a valid scale format: `<Note> <Scale>`
- Select the track to trigger the update
- Check Ableton's Log.txt for error messages

## How It Works

The MIDI Remote Script:
1. Monitors the selected track name
2. Parses the scale information (e.g., "C Major")
3. Converts to the appropriate scale notes
4. Sends MIDI CC messages to light up the Linnstrument LEDs
5. Updates automatically when you switch tracks

## Advanced

### Custom Scale Names

Edit `LinnstrumentScale.py` and add to the `ABLETON_SCALE_MAP` dictionary:

```python
ABLETON_SCALE_MAP = {
    'Major': 'major',
    'Your Custom Scale': 'custom_scale_name',
    ...
}
```

Make sure the scale exists in `scales.py`!

### Viewing Logs

Check Ableton's Log.txt file for debug messages:

**macOS:**
```
~/Library/Preferences/Ableton/Live <version>/Log.txt
```

**Windows:**
```
%APPDATA%\Ableton\Live <version>\Preferences\Log.txt
```

## Tips

- Use consistent naming: `C Major`, `D Minor`, etc.
- The script updates when you select a different track
- Works great with Ableton's Scale mode enabled
- Pair with Ableton Push for the ultimate scale visualization!

## Uninstall

1. In Ableton Preferences, set Control Surface back to "None"
2. Delete the LinnstrumentScale folder from Remote Scripts directory
3. Restart Ableton
