"""
Configuration constants for LinnStrument multi-mode system
Works with both LinnStrument 128 and LinnStrument 200
"""

# LinnStrument Hardware Configuration
# Set to your device: 16 for LinnStrument 128, 25 for LinnStrument 200
LINNSTRUMENT_COLUMNS = 16  # Change to 25 for LinnStrument 200
LINNSTRUMENT_ROWS = 8
LINNSTRUMENT_BASE_NOTE = 36  # C2 - IMPORTANT: Adjust your LinnStrument's octave setting to match!
LINNSTRUMENT_ROW_OFFSET = 5  # Semitones per row
LINNSTRUMENT_COLUMN_OFFSET = 1  # Semitones per column

# Mode Types
MODE_KEYBOARD = 0
MODE_SESSION = 1
MODE_DRUM = 2
MODE_COUNT = 3  # Total number of modes

# Mode Button Configuration
# Using Switch 1 (left panel button) for mode cycling
# Configure in LinnStrument: Global Settings > Switch 1 > CC65
MODE_SWITCH_CC = 65  # CC number for mode switch button
MODE_SWITCH_CHANNEL = 0  # MIDI channel (0-indexed)

# Mode Colors (for visual feedback via Switch 1 LED)
MODE_COLORS = {
    MODE_KEYBOARD: 'green',
    MODE_SESSION: 'blue',
    MODE_DRUM: 'red',
}

# Drum Mode Configuration
DRUM_PAD_ROWS = 4  # Bottom 4 rows (0-3) for drum pads
DRUM_PAD_COLUMNS = 4  # 4x4 grid on left side (like Push)
DRUM_PAD_EXTENDED_COLUMNS = LINNSTRUMENT_COLUMNS  # Can extend to show more pads
SEQUENCER_ROWS = 4  # Top 4 rows (4-7) for sequencer
SEQUENCER_STEPS = LINNSTRUMENT_COLUMNS  # Full width of device

# Session Mode Configuration
SESSION_ROWS = 8  # Full grid height
SESSION_COLUMNS = LINNSTRUMENT_COLUMNS  # Full grid width
SESSION_SCENE_LAUNCH_COLUMN = None  # Optional: column for scene launch

# Keyboard Mode Configuration
KEYBOARD_SKIP_TOP_ROW = False  # Whether to reserve top row for track selection

# Color Schemes
DEFAULT_ROOT_COLOR = 'red'
DEFAULT_SCALE_COLOR = 'blue'

# NRPN for User Firmware Mode (LED control)
NRPN_USER_FIRMWARE_MODE = 245
NRPN_ENABLE_VALUE = 1
NRPN_DISABLE_VALUE = 0

# NRPN for Row Offset (chromatic vs. scale mode)
NRPN_ROW_OFFSET = 6  # NRPN 6 controls row offset
CHROMATIC_ROW_OFFSET = 1  # Chromatic (semitone per row)
SCALE_ROW_OFFSET = 5  # Default scale mode (5 semitones per row)
