#!/usr/bin/env python3
"""
Linnstrument Scale Light - MIDI Effect Plugin (Standalone)

This runs as a standalone MIDI effect that sits between your DAW and Linnstrument:
DAW MIDI Out -> This Plugin -> Linnstrument MIDI In

It analyzes incoming MIDI notes and automatically lights up the Linnstrument
based on the detected scale or manually selected scale.
"""

import mido
import threading
import time
import sys
import argparse
from collections import Counter, deque
from pathlib import Path

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))
from scales import get_scale_notes, get_available_scales, SCALES
from linnstrument import Linnstrument

class ScaleDetector:
    """Detects the scale being played based on MIDI note input"""

    def __init__(self, history_size=50):
        self.note_history = deque(maxlen=history_size)
        self.current_scale = None
        self.current_root = None

    def add_note(self, note):
        """Add a played note to the history"""
        pitch_class = note % 12
        self.note_history.append(pitch_class)

    def detect_scale(self):
        """
        Analyze note history and detect the most likely scale

        Returns:
            tuple: (root_note, scale_name, confidence) or None
        """
        if len(self.note_history) < 5:
            return None

        # Get unique pitch classes
        pitch_classes = set(self.note_history)

        # Try to match against known scales
        best_match = None
        best_score = 0

        for root in range(12):
            for scale_name, intervals in SCALES.items():
                # Get expected pitch classes for this root + scale
                expected = set((root + interval) % 12 for interval in intervals)

                # Calculate match score
                matches = len(pitch_classes & expected)
                total = len(pitch_classes | expected)

                if total > 0:
                    score = matches / total

                    # Bonus for exact match
                    if pitch_classes == expected:
                        score += 0.2

                    if score > best_score:
                        best_score = score
                        best_match = (root, scale_name, score)

        return best_match if best_score > 0.6 else None

    def get_current_scale(self):
        """Get the currently detected scale"""
        return self.current_root, self.current_scale


class MIDIEffectPlugin:
    """
    MIDI Effect plugin that passes through MIDI while controlling Linnstrument lights
    """

    def __init__(self, input_port_name, output_port_name, linnstrument_port_name=None,
                 auto_detect=True, manual_scale=None, manual_root=None,
                 update_interval=2.0):
        """
        Initialize MIDI effect plugin

        Args:
            input_port_name: MIDI input port (from DAW)
            output_port_name: MIDI output port (to Linnstrument/synth)
            linnstrument_port_name: Linnstrument control port
            auto_detect: Automatically detect scale from played notes
            manual_scale: Manually specified scale name
            manual_root: Manually specified root note (0-11)
            update_interval: Seconds between scale updates
        """
        self.auto_detect = auto_detect
        self.manual_scale = manual_scale
        self.manual_root = manual_root
        self.update_interval = update_interval
        self.running = False

        # Open MIDI ports
        print(f"Opening input: {input_port_name}")
        self.midi_in = mido.open_input(input_port_name)

        print(f"Opening output: {output_port_name}")
        self.midi_out = mido.open_output(output_port_name)

        # Connect to Linnstrument
        print("Connecting to Linnstrument for light control...")
        self.linnstrument = Linnstrument(port_name=linnstrument_port_name)

        # Scale detection
        self.scale_detector = ScaleDetector()
        self.current_lit_scale = None

        print("MIDI Effect Plugin initialized!")

    def process_message(self, msg):
        """
        Process a MIDI message: pass it through and analyze for scale detection

        Args:
            msg: MIDI message
        """
        # Pass through the message
        self.midi_out.send(msg)

        # Analyze note-on messages for scale detection
        if self.auto_detect and msg.type == 'note_on' and msg.velocity > 0:
            self.scale_detector.add_note(msg.note)

    def update_lights(self):
        """Update Linnstrument lights based on current/detected scale"""
        if self.manual_scale and self.manual_root is not None:
            # Use manually specified scale
            scale_notes = get_scale_notes(self.manual_root, self.manual_scale)
            scale_id = (self.manual_root, self.manual_scale)

        elif self.auto_detect:
            # Try to detect scale
            detection = self.scale_detector.detect_scale()
            if detection:
                root, scale_name, confidence = detection
                print(f"Detected: {['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][root]} "
                      f"{scale_name} (confidence: {confidence:.2f})")
                scale_notes = get_scale_notes(root, scale_name)
                scale_id = (root, scale_name)
            else:
                return  # No confident detection yet

        else:
            return  # No scale to display

        # Only update if scale changed
        if scale_id != self.current_lit_scale:
            print(f"Updating Linnstrument lights...")
            self.linnstrument.light_scale_with_degrees(scale_notes)
            self.current_lit_scale = scale_id

    def run(self):
        """Main loop: process MIDI and update lights"""
        self.running = True

        # Start light update thread
        update_thread = threading.Thread(target=self._light_update_loop, daemon=True)
        update_thread.start()

        print("\nMIDI Effect Plugin running!")
        print("Press Ctrl+C to stop\n")

        try:
            # Process incoming MIDI messages
            for msg in self.midi_in:
                if not self.running:
                    break
                self.process_message(msg)

        except KeyboardInterrupt:
            print("\nStopping...")

        finally:
            self.stop()

    def _light_update_loop(self):
        """Background thread for updating lights"""
        while self.running:
            self.update_lights()
            time.sleep(self.update_interval)

    def stop(self):
        """Stop the plugin and cleanup"""
        self.running = False
        self.midi_in.close()
        self.midi_out.close()
        self.linnstrument.close()
        print("Plugin stopped.")

    @staticmethod
    def list_ports():
        """List available MIDI ports"""
        print("Available MIDI Input Ports:")
        for port in mido.get_input_names():
            print(f"  {port}")

        print("\nAvailable MIDI Output Ports:")
        for port in mido.get_output_names():
            print(f"  {port}")


def main():
    parser = argparse.ArgumentParser(
        description='Linnstrument Scale Light MIDI Effect Plugin',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Auto-detect scale from played notes
  %(prog)s --input "IAC Driver Bus 1" --output "Linnstrument MIDI 1"

  # Manual scale selection
  %(prog)s --input "IAC Driver Bus 1" --output "Linnstrument MIDI 1" \\
           --root C --scale major

  # List available ports
  %(prog)s --list-ports
        """
    )

    parser.add_argument('--input', '-i', type=str,
                       help='MIDI input port name (from your DAW)')
    parser.add_argument('--output', '-o', type=str,
                       help='MIDI output port name (to Linnstrument)')
    parser.add_argument('--linnstrument-port', type=str,
                       help='Linnstrument control port (auto-detected if not specified)')

    parser.add_argument('--auto-detect', action='store_true', default=True,
                       help='Auto-detect scale from played notes (default)')
    parser.add_argument('--no-auto-detect', action='store_false', dest='auto_detect',
                       help='Disable auto-detection')

    parser.add_argument('--root', type=str,
                       help='Manual root note (C, D, E, etc.)')
    parser.add_argument('--scale', type=str,
                       help='Manual scale name')

    parser.add_argument('--update-interval', type=float, default=2.0,
                       help='Seconds between light updates (default: 2.0)')

    parser.add_argument('--list-ports', action='store_true',
                       help='List available MIDI ports')
    parser.add_argument('--list-scales', action='store_true',
                       help='List available scales')

    args = parser.parse_args()

    if args.list_ports:
        MIDIEffectPlugin.list_ports()
        return 0

    if args.list_scales:
        print("Available scales:")
        for scale in get_available_scales():
            print(f"  {scale}")
        return 0

    # Validate required arguments
    if not args.input or not args.output:
        parser.error("--input and --output are required")

    # Parse manual scale if specified
    manual_root = None
    if args.root:
        from scales import note_name_to_number
        manual_root = note_name_to_number(args.root)

    # Create and run plugin
    plugin = MIDIEffectPlugin(
        input_port_name=args.input,
        output_port_name=args.output,
        linnstrument_port_name=args.linnstrument_port,
        auto_detect=args.auto_detect,
        manual_scale=args.scale,
        manual_root=manual_root,
        update_interval=args.update_interval
    )

    plugin.run()
    return 0


if __name__ == '__main__':
    sys.exit(main())
