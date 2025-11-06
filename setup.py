#!/usr/bin/env python3
"""
Setup script for Linnstrument Scale Tool
Helps with installation and configuration
"""

import sys
import subprocess
import shutil
from pathlib import Path
import platform

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_python_version():
    """Check if Python version is adequate"""
    print("Checking Python version...")
    version = sys.version_info
    if version < (3, 7):
        print(f"❌ Python 3.7+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def setup_venv():
    """Create and setup virtual environment"""
    print("\nChecking virtual environment...")
    venv_path = Path(__file__).parent / "venv"

    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True

    print("Creating virtual environment...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    requirements = Path(__file__).parent / "requirements.txt"
    venv_path = Path(__file__).parent / "venv"

    # Determine the pip executable
    if venv_path.exists():
        # Use venv pip if available
        if platform.system() == "Windows":
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            pip_exe = venv_path / "bin" / "pip"

        if pip_exe.exists():
            print("Using virtual environment pip...")
            pip_cmd = str(pip_exe)
        else:
            pip_cmd = sys.executable
            pip_args = ["-m", "pip"]
    else:
        pip_cmd = sys.executable
        pip_args = ["-m", "pip"]

    try:
        if 'pip_args' in locals():
            subprocess.check_call([pip_cmd] + pip_args + ["install", "-r", str(requirements)])
        else:
            subprocess.check_call([pip_cmd, "install", "-r", str(requirements)])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("\n⚠️  Hint: If you see 'externally-managed-environment' error:")
        print("   Run: ./install.sh (creates a virtual environment automatically)")
        return False

def test_midi_ports():
    """Test if MIDI ports are available"""
    print("\nChecking MIDI ports...")
    try:
        import mido
        output_ports = mido.get_output_names()
        input_ports = mido.get_input_names()

        print(f"✅ Found {len(output_ports)} output port(s)")
        print(f"✅ Found {len(input_ports)} input port(s)")

        # Check for Linnstrument
        linnstrument_found = any('linnstrument' in p.lower() for p in output_ports)
        if linnstrument_found:
            print("✅ Linnstrument detected!")
        else:
            print("⚠️  No Linnstrument detected (make sure it's connected)")

        return True
    except Exception as e:
        print(f"❌ Error checking MIDI: {e}")
        return False

def setup_max_for_live():
    """Guide user through Max for Live setup"""
    print("\nMax for Live Setup")
    print("-" * 60)

    system = platform.system()

    if system == "Darwin":  # macOS
        target = Path.home() / "Music" / "Ableton" / "User Library" / "Presets" / "MIDI Effects" / "Max MIDI Effect"
    elif system == "Windows":
        target = Path.home() / "Documents" / "Ableton" / "User Library" / "Presets" / "MIDI Effects" / "Max MIDI Effect"
    else:
        print("⚠️  Unknown operating system")
        return False

    source = Path(__file__).parent / "max_for_live" / "LinnstrumentScaleLight.maxpat"

    print(f"Source: {source}")
    print(f"Target: {target}")

    if not source.exists():
        print("❌ Max for Live device not found")
        return False

    if not target.parent.exists():
        print("⚠️  Ableton User Library not found")
        print(f"   Expected location: {target.parent}")
        print("   You'll need to manually copy max_for_live/LinnstrumentScaleLight.maxpat")
        return False

    # Automatically install the device
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source, target)
        print(f"✅ Copied to {target}")
        print("   ⚠️  IMPORTANT: Restart Ableton Live to see the device!")
        return True
    except Exception as e:
        print(f"❌ Copy failed: {e}")
        print(f"   Manual copy: cp {source} {target}")
        return False

def setup_virtual_midi():
    """Guide user through virtual MIDI setup"""
    print("\nVirtual MIDI Bus Setup (for MIDI Effect Plugin)")
    print("-" * 60)

    system = platform.system()

    if system == "Darwin":  # macOS
        print("""
To set up IAC Driver on macOS:

1. Open 'Audio MIDI Setup' (in Applications/Utilities)
2. Go to Window > Show MIDI Studio
3. Double-click 'IAC Driver'
4. Check 'Device is online'
5. You should see 'IAC Driver Bus 1' in the Ports list
6. Click Apply
        """)
    elif system == "Windows":
        print("""
To set up virtual MIDI on Windows:

1. Download loopMIDI from:
   https://www.tobias-erichsen.de/software/loopmidi.html
2. Install and run loopMIDI
3. Click the + button to add a new port
4. Name it 'Linnstrument Bridge'
        """)
    else:
        print("⚠️  Unknown operating system")

    input("\nPress Enter when done (or to skip)...")
    return True

def run_test():
    """Run a test of the basic functionality"""
    print("\nTesting basic functionality...")

    try:
        from scales import get_scale_notes, get_available_scales
        scales = get_available_scales()
        print(f"✅ Loaded {len(scales)} scales")

        scale_notes = get_scale_notes('C', 'major')
        print(f"✅ Generated C major scale ({len(scale_notes)} notes)")

        from linnstrument import Linnstrument
        print("✅ Linnstrument module loaded")

        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print_header("Installation Complete!")

    print("""
🎉 Your Linnstrument Scale Tool is ready!

NEXT STEPS:

1. Command Line Tool (easiest to start):
   python scale_tool.py C major

2. Max for Live (if using Ableton):
   - Restart Ableton Live
   - Find 'LinnstrumentScaleLight' in Max MIDI Effect
   - Drag it onto a MIDI track

3. MIDI Effect Plugin (advanced):
   - Set up virtual MIDI bus (see above)
   - Run: python vst_plugin/midi_effect_plugin.py --list-ports
   - Follow the guide in vst_plugin/README.md

HELPFUL COMMANDS:

  python scale_tool.py --list-scales    # See all available scales
  python scale_tool.py --list-colors    # See all available colors
  python scale_tool.py --help           # Get help
  python examples.py                    # Run interactive examples

DOCUMENTATION:

  README.md           - Full documentation
  QUICK_START.md      - Quick start guide
  max_for_live/       - Max for Live device
  vst_plugin/         - MIDI effect plugin

Enjoy your illuminated Linnstrument! 🎹✨
    """)

def main():
    """Main setup routine"""
    print_header("Linnstrument Scale Tool - Setup")

    steps = [
        ("Python Version", check_python_version),
        ("Virtual Environment", setup_venv),
        ("Dependencies", install_dependencies),
        ("MIDI Ports", test_midi_ports),
        ("Basic Test", run_test),
    ]

    results = []
    for name, func in steps:
        print_header(name)
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((name, False))

    # Optional steps
    print_header("Max for Live Setup")

    # Automatically attempt Max for Live setup
    m4l_result = setup_max_for_live()

    if not m4l_result:
        print("\n💡 Tip: You can manually copy the Max for Live device later:")
        print("   max_for_live/LinnstrumentScaleLight.maxpat")
        print("   → ~/Music/Ableton/User Library/Presets/MIDI Effects/Max MIDI Effect/")

    # Summary
    print_header("Setup Summary")
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")

    if all(result for _, result in results):
        print_next_steps()
    else:
        print("\n⚠️  Some steps failed. Please check the errors above.")
        print("   You may need to install dependencies manually:")
        print("   pip install -r requirements.txt")

if __name__ == '__main__':
    main()
