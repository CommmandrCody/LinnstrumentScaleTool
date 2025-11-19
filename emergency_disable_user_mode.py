#!/usr/bin/env python3
"""
EMERGENCY: Disable LinnStrument User Firmware Mode
Run this if your LinnStrument is stuck and you can't access Global Settings
"""

import mido
import sys
import time

def send_nrpn(port, nrpn_number, value):
    """Send complete NRPN message"""
    channel = 0  # Channel 1 (0-indexed)

    nrpn_msb = (nrpn_number >> 7) & 0x7F
    nrpn_lsb = nrpn_number & 0x7F
    value_msb = (value >> 7) & 0x7F
    value_lsb = value & 0x7F

    # Send 6-message NRPN sequence
    port.send(mido.Message('control_change', channel=channel, control=99, value=nrpn_msb))
    port.send(mido.Message('control_change', channel=channel, control=98, value=nrpn_lsb))
    port.send(mido.Message('control_change', channel=channel, control=6, value=value_msb))
    port.send(mido.Message('control_change', channel=channel, control=38, value=value_lsb))
    port.send(mido.Message('control_change', channel=channel, control=101, value=127))
    port.send(mido.Message('control_change', channel=channel, control=100, value=127))

def main():
    print("=" * 60)
    print("EMERGENCY: LinnStrument User Firmware Mode Disable")
    print("=" * 60)

    # Find LinnStrument
    print("\nSearching for LinnStrument...")

    linnstrument_port = None
    for name in mido.get_output_names():
        if 'LinnStrument' in name or 'LINN' in name.upper():
            linnstrument_port = name
            break

    if not linnstrument_port:
        print("\nERROR: LinnStrument not found!")
        print("\nAvailable MIDI outputs:")
        for name in mido.get_output_names():
            print(f"  - {name}")
        sys.exit(1)

    print(f"Found: {linnstrument_port}")

    # Open port and send disable message
    print("\nDisabling User Firmware Mode...")

    try:
        with mido.open_output(linnstrument_port) as port:
            # Disable User Firmware Mode (NRPN 245 = 0)
            send_nrpn(port, 245, 0)
            time.sleep(0.1)

            # Restore row offset to 5 (default)
            send_nrpn(port, 227, 5)
            time.sleep(0.1)

            print("✓ User Firmware Mode DISABLED")
            print("✓ Row offset restored to 5 (default)")
            print("\nYour LinnStrument should be back to normal!")
            print("Try accessing Global Settings now.")

    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
