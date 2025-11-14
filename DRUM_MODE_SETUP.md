# LinnStrument Drum Mode Setup

## Required LinnStrument Configuration

For drum mode to work correctly with a 4x4 chromatic drum pad layout, you need to configure your LinnStrument:

### One-Time Setup

1. **Press Global Settings** on your LinnStrument
2. Navigate to **Per-Split Settings**
3. Set **Row Offset = 4** (instead of the default 5)
4. Exit Global Settings

### Why Row Offset 4?

With row_offset=4 and column_offset=1, your LinnStrument grid becomes a perfect 4x4 chromatic drum layout:

```
Row 0: C(36)  C#(37) D(38)  D#(39)
Row 1: E(40)  F(41)  F#(42) G(43)
Row 2: G#(44) A(45)  A#(46) B(47)
Row 3: C(48)  C#(49) D(50)  D#(51)
```

This matches standard drum rack layouts (notes 36-51 for 16 pads).

### For Scale/Keyboard Mode

When you want to use keyboard mode for playing scales, change the row offset back to 5:
1. Press Global Settings
2. Per-Split Settings → Row Offset = 5
3. Exit

### Alternative: Save Two Presets

You can save two LinnStrument presets:
- **Preset 1**: Row Offset = 5 (for scales/keyboard mode)
- **Preset 2**: Row Offset = 4 (for drum mode)

Then just switch presets depending on which mode you're using.

## Current Limitation

NRPN commands (227 and 253) for programmatically changing row offset don't work reliably in real-time, despite being documented in the LinnStrument firmware. Manual configuration is required.

The Remote Script will display reminder messages when entering/exiting drum mode:
- **Entering Drum Mode**: "DRUM MODE: Set LinnStrument Row Offset to 4"
- **Exiting Drum Mode**: "Restore LinnStrument Row Offset to 5"

## Alternative Solutions

### Option 1: Max for Live MIDI Effect (Recommended)
A Max for Live MIDI Effect can translate incoming notes on-the-fly, which would allow row_offset=5 to work for both modes. A basic version is available at:
- `experimental_midi_passthrough/linnstrument_drum_mapper.amxd`

### Option 2: Python MIDI Translator
A standalone Python script (`linnstrument_drum_translator.py`) can translate notes in software using virtual MIDI ports.
