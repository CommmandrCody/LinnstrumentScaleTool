# Linnstrument Scale Light - Max for Live Device

A Max for Live MIDI Effect that automatically sets your Linnstrument lights to match the scale you're playing in Ableton Live.

## Features

- Drop-down menus for root note and scale selection
- Option to use degree coloring (I=red, III=yellow, V=green)
- One-click update and clear buttons
- Works as a MIDI Effect in Ableton Live
- Can sync with Ableton's scale settings

## Installation

### Step 1: Install Python Dependencies

Open Terminal and run:

```bash
cd /Users/wagner/LinnstrumentScaleTool
pip install -r requirements.txt
```

### Step 2: Install the Max for Live Device

1. Open Ableton Live
2. Locate your User Library folder:
   - Mac: `~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/`
   - Windows: `\Users\[username]\Documents\Ableton\User Library\Presets\MIDI Effects\Max MIDI Effect\`

3. Copy the entire `max_for_live` folder to this location, or:
   - Just drag `LinnstrumentScaleLight.maxpat` into the location above

4. Restart Ableton Live (if it was open)

### Step 3: Using in Ableton Live

1. Create a MIDI track
2. In the Browser, go to **Max for Live > Max MIDI Effect**
3. Drag **LinnstrumentScaleLight** onto your MIDI track
4. The device will appear with controls for:
   - Root Note (C, C#, D, etc.)
   - Scale Type (major, minor, dorian, etc.)
   - Use Degree Colors toggle
   - Update Lights button
   - Clear Lights button

## Usage

### Basic Workflow

1. **Set your scale**: Choose a root note and scale type from the drop-downs
2. **Click "Update Lights"**: The Linnstrument lights will update to show the scale
3. **Play**: The pads that light up are in your chosen scale
4. **Change scales**: Select a new scale and click "Update Lights" again
5. **Clear**: Click "Clear Lights" to turn off all LEDs

### Syncing with Ableton's Scale

Ableton Live has built-in scale highlighting:
1. Enable Scale mode in Ableton (lower left corner)
2. Select a scale in Ableton's scale selector
3. Match the same root and scale in the Max for Live device
4. Click "Update Lights"

Now your Linnstrument lights will match Ableton's scale highlighting!

### Degree Coloring

When "Use Degree Colors" is enabled:
- **Red**: Root notes (I)
- **Yellow**: Third (III)
- **Green**: Fifth (V)
- **Blue**: Other scale degrees

This helps visualize chord tones and important scale degrees.

## Available Scales

The device includes 20+ scales:
- major, minor
- dorian, phrygian, lydian, mixolydian, aeolian, locrian
- harmonic_minor, melodic_minor
- major_pentatonic, minor_pentatonic
- blues
- whole_tone, chromatic, diminished, augmented
- bebop_major, bebop_minor, altered
- And more!

## Advanced: Editing the Max Patch

If you want to customize the device:

1. Open the `.maxpat` file in Max/MSP
2. Unlock the patch (padlock icon)
3. Edit the UI or add features
4. You can add more scales by editing the `scale_type` menu
5. Save and reload in Ableton

### Adding More Scales

To add scales to the menu:
1. Open `LinnstrumentScaleLight.maxpat` in Max
2. Find the `live.menu` object for scales (obj-3)
3. Edit the `parameter_enum` list to add scale names
4. Make sure the scale names match those in `scales.py`

## Troubleshooting

### "No module named 'scales'" error

The Python script can't find the scale definitions. Fix:
1. Make sure you're running the script from the correct directory
2. Edit `linnstrument_scale_light.py` and update the path:
   ```python
   sys.path.insert(0, '/full/path/to/LinnstrumentScaleTool')
   ```

### "No Linnstrument MIDI port found"

1. Make sure your Linnstrument is connected via USB
2. Check it appears in Audio MIDI Setup (Mac) or Device Manager (Windows)
3. Try disconnecting and reconnecting

### Lights don't update

1. Click "Clear Lights" first, then "Update Lights"
2. Check the Max console (⌘+M) for error messages
3. Make sure Python dependencies are installed
4. Try running the Python script directly from Terminal to test

### Performance Issues

If you notice latency:
1. The device only updates lights when you click "Update Lights"
2. It doesn't process MIDI in real-time, so there's no latency
3. The MIDI signal passes through unchanged

## Alternative: MIDI Effect Plugin

If Max for Live doesn't work for you, use the standalone MIDI effect:

```bash
cd /Users/wagner/LinnstrumentScaleTool/vst_plugin
python3 midi_effect_plugin.py --input "IAC Bus 1" --output "Linnstrument" --auto-detect
```

This version:
- Runs outside Ableton
- Auto-detects scales from what you play
- Requires setting up a virtual MIDI bus

## Tips and Tricks

### Workflow Ideas

1. **Live Performance**: Set scales in advance for different sections of your song
2. **Practice**: Enable degree coloring to learn scale shapes
3. **Composition**: Quickly try different modes and scales
4. **Teaching**: Show students scale patterns visually

### Automating Scale Changes

You can automate the Max for Live parameters in Ableton:
1. Click the parameter automation button
2. Select "Root Note" or "Scale Type"
3. Draw automation in the arrangement view
4. Note: You still need to click "Update Lights" manually (or add an automation to trigger it)

### Custom Colors

To customize colors, edit `linnstrument_scale_light.py`:
- Change the `root_color` and `scale_color` parameters
- Available colors: red, yellow, green, cyan, blue, magenta, white, orange, lime, pink

## Support

For issues:
1. Check the Max console for errors
2. Test the Python script directly
3. Make sure all dependencies are installed
4. Check MIDI connections

## Credits

Built with:
- Max for Live (Ableton Live)
- Python + mido library
- Linnstrument MIDI specification from Roger Linn Design
