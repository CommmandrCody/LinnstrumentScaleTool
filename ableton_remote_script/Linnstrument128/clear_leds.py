"""
Simple script to clear all Linnstrument LEDs
"""

def clear_all_leds(c_instance):
    """
    Turn off all LEDs on the Linnstrument
    """
    c_instance.log_message("Clearing all Linnstrument LEDs...")

    status = 0xB0  # Control Change on channel 0

    # Turn off all pads (columns 1-16 for playable surface on Linnstrument 128)
    for row in range(8):
        for col in range(1, 17):  # Columns 1-16 (playable pads)
            c_instance.send_midi((status, 20, col))
            c_instance.send_midi((status, 21, row))
            c_instance.send_midi((status, 22, 7))  # Color 7 = OFF
