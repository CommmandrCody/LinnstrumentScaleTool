#!/bin/bash
# Installation script for LinnStrument Multi-Mode System

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   LinnStrument Multi-Mode System - Installation Script    ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Detect Ableton User Library location
ABLETON_USER_LIB="$HOME/Music/Ableton/User Library"
REMOTE_SCRIPTS_DIR="$ABLETON_USER_LIB/Remote Scripts"

if [ ! -d "$ABLETON_USER_LIB" ]; then
    echo -e "${RED}Error: Ableton User Library not found at:${NC}"
    echo "  $ABLETON_USER_LIB"
    echo ""
    echo "Please ensure Ableton Live is installed."
    exit 1
fi

# Create Remote Scripts directory if it doesn't exist
if [ ! -d "$REMOTE_SCRIPTS_DIR" ]; then
    echo -e "${YELLOW}Creating Remote Scripts directory...${NC}"
    mkdir -p "$REMOTE_SCRIPTS_DIR"
fi

echo -e "${GREEN}✓${NC} Found Ableton User Library"
echo ""

# Detect LinnStrument model
echo "Which LinnStrument model do you have?"
echo "  1) LinnStrument 128 (16 columns)"
echo "  2) LinnStrument 200 (25 columns)"
echo ""
read -p "Enter choice (1 or 2): " MODEL_CHOICE

if [ "$MODEL_CHOICE" = "1" ]; then
    SOURCE_DIR="ableton_remote_script/LinnstrumentScale128"
    TARGET_DIR="$REMOTE_SCRIPTS_DIR/LinnstrumentScale128"
    MODEL_NAME="LinnStrument 128"
elif [ "$MODEL_CHOICE" = "2" ]; then
    SOURCE_DIR="ableton_remote_script/LinnstrumentScale200"
    TARGET_DIR="$REMOTE_SCRIPTS_DIR/LinnstrumentScale200"
    MODEL_NAME="LinnStrument 200"
else
    echo -e "${RED}Invalid choice. Exiting.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Installing for $MODEL_NAME${NC}"
echo ""

# Check if source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo -e "${RED}Error: Source directory not found:${NC}"
    echo "  $SOURCE_DIR"
    echo ""
    echo "Please run this script from the LinnstrumentScaleTool directory."
    exit 1
fi

# Backup existing installation if present
if [ -d "$TARGET_DIR" ]; then
    BACKUP_DIR="${TARGET_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}Backing up existing installation to:${NC}"
    echo "  $BACKUP_DIR"
    mv "$TARGET_DIR" "$BACKUP_DIR"
    echo -e "${GREEN}✓${NC} Backup created"
    echo ""
fi

# Copy files
echo "Installing Remote Script..."
cp -r "$SOURCE_DIR" "$TARGET_DIR"
echo -e "${GREEN}✓${NC} Files copied to Remote Scripts folder"
echo ""

# Set permissions
chmod -R 755 "$TARGET_DIR"
echo -e "${GREEN}✓${NC} Permissions set"
echo ""

# Configuration
echo "═══════════════════════════════════════════════════════════"
echo "  CONFIGURATION REQUIRED"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Before using the Multi-Mode system, you need to:"
echo ""
echo "1. Configure your LinnStrument base note:"
echo "   - Open MIDI monitor in Ableton"
echo "   - Press bottom-left pad on LinnStrument"
echo "   - Note the MIDI note number"
echo "   - Edit: $TARGET_DIR/config.py"
echo "   - Set LINNSTRUMENT_BASE_NOTE to your note number"
echo ""
echo "2. Configure LinnStrument hardware:"
echo "   See: HARDWARE_SETUP.md for detailed instructions"
echo "   - Set up Preset 1 (One Channel for Keyboard mode)"
echo "   - Set up Preset 2 (Channel Per Row for Session/Drum)"
echo "   - Configure Switch 1 to send CC65 (mode switching)"
echo ""
echo "3. Enable in Ableton Live:"
echo "   - Open Preferences > Link/Tempo/MIDI"
echo "   - Set Control Surface: $(basename $TARGET_DIR)"
echo "   - Set Input/Output to your LinnStrument ports"
echo "   - Restart Ableton or toggle Remote Script off/on"
echo ""
echo "4. Verify installation:"
echo "   - Check Ableton's Log.txt:"
echo "     ~/Library/Preferences/Ableton/Live X.X.X/Log.txt"
echo "   - Look for: 'Linnstrument Multi-Mode System - Ready!'"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${GREEN}Installation complete!${NC}"
echo ""
echo "Documentation:"
echo "  - MULTIMODE_README.md - Usage guide"
echo "  - HARDWARE_SETUP.md - Hardware configuration"
echo ""
echo "Press Switch 1 (CC65) to cycle through modes:"
echo "  Keyboard → Session → Drum → Keyboard → ..."
echo ""
