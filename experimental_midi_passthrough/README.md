# MIDI Passthrough Plugin (Experimental)

> **Note:** This is an experimental tool. For Ableton Live users, we strongly recommend using the [Ableton MIDI Remote Script](../ableton_remote_script/) instead, which provides automatic integration with zero setup complexity.

A standalone Python MIDI passthrough effect that sits between your DAW and Linnstrument, automatically updating the lights based on scales.

**Why use the Ableton script instead:**
- No MIDI routing setup needed
- Reads Ableton's scale settings directly
- Track color integration
- Zero latency
- Much simpler installation

**When to use this tool:**
- You're not using Ableton Live
- You want automatic scale detection from played notes
- You need a DAW-agnostic solution

## Two Modes

### 1. Auto-Detect Mode
Analyzes the notes you play and automatically detects the scale:

```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1"
```

### 2. Manual Scale Mode
You specify the scale, and it stays lit:

```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1" \
  --root C --scale major --no-auto-detect
```

## Setup

### Step 1: Install Dependencies

```bash
cd /Users/wagner/LinnstrumentScaleTool
pip install -r requirements.txt
```

### Step 2: Create Virtual MIDI Bus

You need a virtual MIDI bus to route MIDI from your DAW through this plugin to the Linnstrument.

#### macOS

1. Open **Audio MIDI Setup** (in Applications/Utilities)
2. Go to **Window > Show MIDI Studio**
3. Double-click **IAC Driver**
4. Check "Device is online"
5. You should see "IAC Driver Bus 1" in the Ports list
6. Click Apply

#### Windows

1. Download and install **loopMIDI** from https://www.tobias-erichsen.de/software/loopmidi.html
2. Create a new virtual MIDI port (click the + button)
3. Name it something like "Linnstrument Bridge"

### Step 3: Set Up MIDI Routing

The signal flow should be:
```
DAW → Virtual MIDI Bus → This Plugin → Linnstrument
```

#### In Ableton Live:

1. **Preferences > Link/Tempo/MIDI**
2. Under **MIDI Ports**:
   - Enable **Track** for "IAC Driver Bus 1" (or your virtual bus)
3. Create a MIDI track
4. Set the track's MIDI output to "IAC Driver Bus 1"
5. Set the channel to match your setup (usually 1)

#### In Logic Pro:

1. Create a MIDI track
2. Set the output to "IAC Driver Bus 1"

#### In FL Studio:

1. **Options > MIDI Settings**
2. Enable your virtual MIDI port
3. Set MIDI track output to the virtual port

### Step 4: Run the Plugin

```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1"
```

## Usage Examples

### Auto-detect scale as you play
```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1"
```

The plugin will:
- Pass all MIDI through to Linnstrument
- Analyze note-on messages
- Detect the most likely scale
- Update lights every 2 seconds

### Manual scale (for live performance)
```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1" \
  --root C --scale major --no-auto-detect
```

### Faster updates
```bash
python midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1" \
  --update-interval 1.0
```

### List available MIDI ports
```bash
python midi_effect_plugin.py --list-ports
```

## How It Works

### Auto-Detect Mode

1. MIDI notes from your DAW are passed through to the Linnstrument
2. Every note-on message is analyzed
3. The last 50 notes are kept in a history buffer
4. Every 2 seconds (configurable), the plugin:
   - Extracts unique pitch classes from the history
   - Compares them against all known scales
   - Finds the best match (requires 60%+ confidence)
   - Updates Linnstrument lights if the scale changed

### Manual Mode

1. MIDI notes are passed through
2. The specified scale is lit up immediately
3. Lights stay constant (no analysis)

## Performance Tips

1. **No Latency**: The plugin passes MIDI through immediately - there's no processing delay on the MIDI data
2. **Light Updates**: Only the light control messages have a delay (every 2 seconds by default)
3. **CPU Usage**: Very low - just MIDI message passing and occasional scale analysis

## Troubleshooting

### "No such port" error

Run `--list-ports` to see available ports:
```bash
python midi_effect_plugin.py --list-ports
```

Then use the exact name shown.

### MIDI not passing through

1. Check your virtual MIDI bus is enabled
2. Verify the plugin shows "MIDI Effect Plugin running!"
3. Check your DAW is sending to the virtual bus
4. Make sure the Linnstrument is receiving (play notes and check if sound comes out)

### Scale detection not working

1. Play at least 5-6 different notes
2. Wait 2 seconds for the analysis
3. Check console output - it shows detected scales
4. Try manual mode if auto-detect isn't working well

### Lights update too slowly/quickly

Adjust the update interval:
```bash
--update-interval 0.5  # Update every 0.5 seconds
--update-interval 5.0  # Update every 5 seconds
```

## Advanced Usage

### Script for Live Performance

Create a shell script to launch with your preferred settings:

**linnstrument_lights.sh**:
```bash
#!/bin/bash
cd /Users/wagner/LinnstrumentScaleTool/vst_plugin
python3 midi_effect_plugin.py \
  --input "IAC Driver Bus 1" \
  --output "Linnstrument MIDI 1" \
  --update-interval 1.5
```

Make it executable:
```bash
chmod +x linnstrument_lights.sh
```

Run it:
```bash
./linnstrument_lights.sh
```

### Integration with Other Software

The plugin works with any software that can send MIDI to a virtual bus:
- DAWs (Ableton, Logic, FL Studio, Cubase, etc.)
- Notation software (Sibelius, Finale, MuseScore)
- Max/MSP, Pure Data
- Custom MIDI applications

## Comparison with Other Methods

| Method | Pros | Cons |
|--------|------|------|
| **MIDI Effect Plugin** | Auto-detects scales, works live | Requires MIDI routing setup |
| **Command Line Tool** | Simple, instant | Must run manually for each scale |
| **Max for Live** | GUI, Ableton integration | Requires Ableton + Max for Live |

## Tips

1. **Practice Sessions**: Use auto-detect mode to visualize what you're playing
2. **Composition**: Use manual mode to explore scales
3. **Live Performance**: Set up manual mode for each song section
4. **Teaching**: Auto-detect helps students see what they're playing

## Stopping the Plugin

Press **Ctrl+C** in the terminal to stop the plugin gracefully.

The plugin will:
1. Stop processing MIDI
2. Close all MIDI ports
3. Disconnect from Linnstrument

## Future Enhancements

Possible additions:
- GUI for easier control
- Preset manager for saving scale configurations
- Support for custom scale definitions
- Integration with DAW track names/colors
- Multiple Linnstrument support

## Credits

Uses the same scale definitions and Linnstrument control as the main tool.
