#!/bin/bash
# Clear Python cache before reloading Ableton Remote Script
# Run this BEFORE restarting Ableton to ensure fresh code loads

SCRIPT_DIR="$HOME/Music/Ableton/User Library/Remote Scripts/LinnStrument"

echo "Clearing Python cache for LinnStrument Remote Script..."

# Remove __pycache__ directories
find "$SCRIPT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove .pyc files
find "$SCRIPT_DIR" -name "*.pyc" -delete 2>/dev/null

echo "✓ Cache cleared!"
echo "Now restart Ableton Live to reload the script."
