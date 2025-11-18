"""
Test script to light a single pad and verify LED addressing
"""

def test_light_single_pad(c_instance):
    """
    Comprehensive LED addressing test with split mode detection
    """
    c_instance.log_message("=== LINNSTRUMENT LED DIAGNOSTIC START ===")
    c_instance.log_message("")
    c_instance.log_message("CRITICAL: Check Linnstrument settings BEFORE running this test:")
    c_instance.log_message("  1. Press 'Per-Split Settings' button (top right)")
    c_instance.log_message("  2. Look at Row 2, Column 1 (Split Mode)")
    c_instance.log_message("  3. If it shows 'Left' or 'Right', tap to toggle to 'Off'")
    c_instance.log_message("  4. Split mode MUST be OFF for LED control to work properly")
    c_instance.log_message("")
    c_instance.log_message("Proceeding with LED test...")
    c_instance.log_message("")

    # First, try to turn off ALL LEDs by sending commands across the grid
    c_instance.log_message("Step 1: Clearing all LEDs...")
    status = 0xB0  # Control Change on channel 0

    # Clear grid by setting all to OFF (color 7)
    for row in range(8):
        for col in range(16):
            c_instance.send_midi((status, 20, col))
            c_instance.send_midi((status, 21, row))
            c_instance.send_midi((status, 22, 7))  # OFF

    c_instance.log_message("Step 2: Testing corner positions with unique colors...")
    c_instance.log_message("")

    # Test 4 corners with different colors to identify coordinate system
    # Bottom-left (should be column 0, row 0) = RED
    c_instance.log_message("  Corner 1: column=0, row=0 => RED")
    c_instance.send_midi((status, 20, 0))
    c_instance.send_midi((status, 21, 0))
    c_instance.send_midi((status, 22, 1))  # RED

    # Bottom-right (should be column 15, row 0) = YELLOW
    c_instance.log_message("  Corner 2: column=15, row=0 => YELLOW")
    c_instance.send_midi((status, 20, 15))
    c_instance.send_midi((status, 21, 0))
    c_instance.send_midi((status, 22, 2))  # YELLOW

    # Top-left (should be column 0, row 7) = GREEN
    c_instance.log_message("  Corner 3: column=0, row=7 => GREEN")
    c_instance.send_midi((status, 20, 0))
    c_instance.send_midi((status, 21, 7))
    c_instance.send_midi((status, 22, 3))  # GREEN

    # Top-right (should be column 15, row 7) = CYAN
    c_instance.log_message("  Corner 4: column=15, row=7 => CYAN")
    c_instance.send_midi((status, 20, 15))
    c_instance.send_midi((status, 21, 7))
    c_instance.send_midi((status, 22, 4))  # CYAN

    c_instance.log_message("")
    c_instance.log_message("=== LINNSTRUMENT LED DIAGNOSTIC COMPLETE ===")
    c_instance.log_message("")
    c_instance.log_message("You should now see 4 colored pads at the corners:")
    c_instance.log_message("  - BOTTOM-LEFT should be RED (column=0, row=0)")
    c_instance.log_message("  - BOTTOM-RIGHT should be YELLOW (column=15, row=0)")
    c_instance.log_message("  - TOP-LEFT should be GREEN (column=0, row=7)")
    c_instance.log_message("  - TOP-RIGHT should be CYAN (column=15, row=7)")
    c_instance.log_message("")
    c_instance.log_message("If colors appear in WRONG positions, report:")
    c_instance.log_message("  1. Which corner has which color")
    c_instance.log_message("  2. What note each colored pad plays")
    c_instance.log_message("  3. Is split mode OFF on your Linnstrument?")
    c_instance.log_message("")
    c_instance.log_message("If NO lights appear or wrong colors:")
    c_instance.log_message("  - Check if split mode is enabled (turn it OFF)")
    c_instance.log_message("  - Check MIDI channel settings on Linnstrument")
    c_instance.log_message("  - Try pressing 'Global Settings' > 'Reset' > 'LED Settings'")
