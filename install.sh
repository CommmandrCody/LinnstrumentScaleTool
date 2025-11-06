#!/bin/bash
# Linnstrument Scale Tool - One-line installer for macOS/Linux

echo "🎹 Linnstrument Scale Tool - Installer"
echo "======================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed."
    echo "   Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

# Show Python version
PYTHON_VERSION=$(python3 --version)
echo "✅ Found $PYTHON_VERSION"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "================================"
echo "IMPORTANT: Activate the virtual environment first!"
echo "================================"
echo ""
echo "Every time you use the tool, run:"
echo "  source venv/bin/activate"
echo ""
echo "Then you can use:"
echo "  python scale_tool.py C major"
echo "  python scale_tool.py --help"
echo "  python examples.py"
echo ""
echo "To deactivate the virtual environment:"
echo "  deactivate"
echo ""
echo "See START_HERE.md for full getting started guide"
echo ""

# Create a convenient launcher script
cat > run.sh << 'EOF'
#!/bin/bash
# Convenience script to run with virtual environment
source venv/bin/activate
python scale_tool.py "$@"
EOF

chmod +x run.sh

echo "💡 TIP: Use './run.sh C major' for quick access (auto-activates venv)"
echo ""

# Install Ableton MIDI Remote Script if Ableton found
if [ "$(uname)" = "Darwin" ]; then
    REMOTE_SCRIPTS_DIR="$HOME/Music/Ableton/User Library/Remote Scripts"
    if [ -d "$(dirname "$REMOTE_SCRIPTS_DIR")" ]; then
        echo "📦 Installing Ableton MIDI Remote Script..."
        mkdir -p "$REMOTE_SCRIPTS_DIR"
        cp -r ableton_remote_script/LinnstrumentScale "$REMOTE_SCRIPTS_DIR/" 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "✅ MIDI Remote Script installed"
            echo "   ⚠️  Restart Ableton Live and enable it in Preferences → Link/Tempo/MIDI"
            echo "   ⚠️  Select 'LinnstrumentScale' as Control Surface"
        else
            echo "⚠️  Could not install MIDI Remote Script automatically"
            echo "   Manual copy: cp -r ableton_remote_script/LinnstrumentScale '$REMOTE_SCRIPTS_DIR/'"
        fi
    fi
fi
echo ""
