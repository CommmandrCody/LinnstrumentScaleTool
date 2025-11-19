# LinnStrument Ableton Remote Scripts

Choose the correct folder for your LinnStrument model:

## Installation

Copy **ONE** of these folders to your Ableton Remote Scripts directory:

### For LinnStrument 128 (16 columns)
```bash
cp -r Linnstrument128 ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument
```

### For LinnStrument 200 (25 columns)
```bash
cp -r Linnstrument200 ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument
```

### Generic Version (auto-detects, currently set to 128)
```bash
cp -r Linnstrument ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument
```

## Differences

| Feature | LinnStrument 128 | LinnStrument 200 |
|---------|------------------|------------------|
| Columns | 16 | 25 |
| Keyboard Mode | ✅ Full width | ✅ Full width |
| Drum Mode | 4x4 pads | 4x4 pads |
| Sequencer | 16 steps | 25 steps |

## Features

Both versions include:
- ✅ **Keyboard Mode**: Scale lighting based on Ableton's current scale/root
- ✅ **Drum Mode**: 4x4 drum pad grid + step sequencer
- ✅ **Auto-Switching**: Automatically switches modes when drum rack detected
- ✅ **LED Feedback**: Visual feedback for drum pads and sequencer

## Setup Requirement

⚠️ **IMPORTANT**: Configure your LinnStrument so the lower-left pad plays C2 (note 36):
1. Press both "Per-Split Settings" buttons simultaneously (Global Settings)
2. Navigate to: Per-Split Settings > Octave
3. Adjust octave until lower-left pad plays C2
4. This ensures drum pads align with Ableton's standard drum rack (notes 36-51)

## After Installation

1. Clear Python cache before first use:
   ```bash
   cd ~/Music/Ableton/User\ Library/Remote\ Scripts/LinnStrument
   ./clear_cache.sh
   ```

2. Restart Ableton Live

3. In Ableton Preferences > Link, Tempo & MIDI:
   - Set Control Surface to "LinnStrument"
   - Set Input to "LinnStrument MIDI"
   - Set Output to "LinnStrument MIDI"

## Troubleshooting

See `../docs/README.md` for complete documentation and troubleshooting guide.
