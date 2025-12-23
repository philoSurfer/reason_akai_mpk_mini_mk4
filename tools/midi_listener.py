#!/usr/bin/env python3
"""
MPK Mini IV MIDI Listener Agent
Interactive tool for capturing and analyzing MIDI messages from the controller.
Outputs structured data that can be used to verify/create Remote codec mappings.
"""

import mido
import json
import sys
import argparse
from datetime import datetime
from collections import defaultdict

class MIDIListener:
    def __init__(self, port_name=None, output_format='human'):
        self.port_name = port_name
        self.output_format = output_format
        self.captured_messages = []
        self.message_summary = defaultdict(list)

    def find_mpk_ports(self):
        """Find all MPK Mini IV MIDI ports"""
        all_ports = mido.get_input_names()
        mpk_ports = [p for p in all_ports if 'MPK mini IV' in p]
        return mpk_ports, all_ports

    def format_message(self, msg):
        """Format a MIDI message for display"""
        raw_bytes = msg.bytes()
        hex_str = ' '.join(f'{b:02X}' for b in raw_bytes)

        if msg.type == 'note_on':
            return {
                'type': 'note_on',
                'channel': msg.channel + 1,
                'note': msg.note,
                'velocity': msg.velocity,
                'hex': hex_str,
                'reason_pattern': f"{raw_bytes[0]:02x} xx yy",
                'description': f"Note On: Ch {msg.channel+1}, Note {msg.note}, Vel {msg.velocity}"
            }
        elif msg.type == 'note_off':
            return {
                'type': 'note_off',
                'channel': msg.channel + 1,
                'note': msg.note,
                'velocity': msg.velocity,
                'hex': hex_str,
                'reason_pattern': f"{raw_bytes[0]:02x} xx yy",
                'description': f"Note Off: Ch {msg.channel+1}, Note {msg.note}, Vel {msg.velocity}"
            }
        elif msg.type == 'control_change':
            return {
                'type': 'control_change',
                'channel': msg.channel + 1,
                'cc': msg.control,
                'value': msg.value,
                'hex': hex_str,
                'reason_pattern': f"{raw_bytes[0]:02x} {raw_bytes[1]:02x} xx",
                'description': f"CC: Ch {msg.channel+1}, CC {msg.control}, Val {msg.value}"
            }
        elif msg.type == 'pitchwheel':
            return {
                'type': 'pitchwheel',
                'channel': msg.channel + 1,
                'pitch': msg.pitch,
                'hex': hex_str,
                'reason_pattern': f"{raw_bytes[0]:02x} xx yy",
                'description': f"Pitch Bend: Ch {msg.channel+1}, Value {msg.pitch}"
            }
        else:
            return {
                'type': msg.type,
                'hex': hex_str,
                'raw': str(msg),
                'description': str(msg)
            }

    def print_message(self, formatted):
        """Print a formatted message"""
        if self.output_format == 'json':
            print(json.dumps(formatted))
        else:
            desc = formatted['description']
            hex_str = formatted['hex']
            pattern = formatted.get('reason_pattern', 'N/A')
            print(f"{desc:50s} | {hex_str:15s} | Pattern: {pattern}")

    def listen(self, duration=None, max_messages=None):
        """Listen for MIDI messages"""
        mpk_ports, all_ports = self.find_mpk_ports()

        if not mpk_ports:
            print("ERROR: No MPK Mini IV found!", file=sys.stderr)
            print(f"Available ports: {all_ports}", file=sys.stderr)
            return False

        # Select port
        if self.port_name:
            port = next((p for p in mpk_ports if self.port_name in p), None)
            if not port:
                print(f"ERROR: Port '{self.port_name}' not found", file=sys.stderr)
                return False
        else:
            # Default to MIDI Port (not DAW or Software)
            port = next((p for p in mpk_ports if 'MIDI Port' in p), mpk_ports[0])

        print(f"=" * 70, file=sys.stderr)
        print(f"MPK Mini IV MIDI Listener", file=sys.stderr)
        print(f"=" * 70, file=sys.stderr)
        print(f"Listening on: {port}", file=sys.stderr)
        print(f"Press Ctrl+C to stop and see summary", file=sys.stderr)
        print(f"=" * 70, file=sys.stderr)
        print(file=sys.stderr)

        if self.output_format == 'human':
            print(f"{'Description':50s} | {'Hex':15s} | Reason Pattern")
            print("-" * 90)

        count = 0
        try:
            with mido.open_input(port) as inport:
                start_time = datetime.now()
                for msg in inport:
                    formatted = self.format_message(msg)
                    self.captured_messages.append(formatted)
                    self.print_message(formatted)

                    # Track for summary
                    key = (formatted['type'], formatted.get('channel'), formatted.get('cc'), formatted.get('note'))
                    self.message_summary[key].append(formatted)

                    count += 1
                    if max_messages and count >= max_messages:
                        break
                    if duration:
                        elapsed = (datetime.now() - start_time).total_seconds()
                        if elapsed >= duration:
                            break

        except KeyboardInterrupt:
            pass

        self.print_summary()
        return True

    def print_summary(self):
        """Print a summary of captured messages"""
        print(file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print("CAPTURE SUMMARY", file=sys.stderr)
        print("=" * 70, file=sys.stderr)
        print(f"Total messages captured: {len(self.captured_messages)}", file=sys.stderr)
        print(file=sys.stderr)

        if not self.captured_messages:
            print("No messages captured!", file=sys.stderr)
            return

        # Group by type
        by_type = defaultdict(list)
        for msg in self.captured_messages:
            by_type[msg['type']].append(msg)

        # Print CC summary
        if 'control_change' in by_type:
            print("Control Change (CC) Messages:", file=sys.stderr)
            cc_summary = defaultdict(set)
            for msg in by_type['control_change']:
                cc_summary[(msg['channel'], msg['cc'])].add(msg['value'])
            for (ch, cc), values in sorted(cc_summary.items()):
                pattern = f"b{ch-1:01x} {cc:02x} xx"
                print(f"  Ch {ch}, CC {cc:3d}: values {min(values)}-{max(values):3d}  | Pattern: {pattern}", file=sys.stderr)
            print(file=sys.stderr)

        # Print Note summary
        for note_type in ['note_on', 'note_off']:
            if note_type in by_type:
                print(f"{note_type.replace('_', ' ').title()} Messages:", file=sys.stderr)
                note_summary = defaultdict(set)
                for msg in by_type[note_type]:
                    note_summary[(msg['channel'], msg['note'])].add(msg.get('velocity', 0))
                for (ch, note), velocities in sorted(note_summary.items()):
                    status = 0x90 if note_type == 'note_on' else 0x80
                    status += (ch - 1)
                    pattern = f"{status:02x} {note:02x} xx"
                    print(f"  Ch {ch}, Note {note:3d}: velocities {min(velocities)}-{max(velocities):3d}  | Pattern: {pattern}", file=sys.stderr)
                print(file=sys.stderr)

        # Print Pitch Bend summary
        if 'pitchwheel' in by_type:
            print("Pitch Bend Messages:", file=sys.stderr)
            pb_summary = defaultdict(lambda: {'min': 8192, 'max': -8192})
            for msg in by_type['pitchwheel']:
                ch = msg['channel']
                pb_summary[ch]['min'] = min(pb_summary[ch]['min'], msg['pitch'])
                pb_summary[ch]['max'] = max(pb_summary[ch]['max'], msg['pitch'])
            for ch, vals in sorted(pb_summary.items()):
                pattern = f"e{ch-1:01x} xx yy"
                print(f"  Ch {ch}: range {vals['min']} to {vals['max']}  | Pattern: {pattern}", file=sys.stderr)
            print(file=sys.stderr)

        # Generate Reason codec snippet
        print("=" * 70, file=sys.stderr)
        print("SUGGESTED REASON REMOTE PATTERNS:", file=sys.stderr)
        print("=" * 70, file=sys.stderr)

        patterns_seen = set()
        for msg in self.captured_messages:
            pattern = msg.get('reason_pattern')
            if pattern and pattern not in patterns_seen:
                patterns_seen.add(pattern)
                print(f'{{ pattern="{pattern}", name="TODO" }},', file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description='MPK Mini IV MIDI Listener')
    parser.add_argument('--port', '-p', help='Specific port name to use')
    parser.add_argument('--format', '-f', choices=['human', 'json'], default='human',
                        help='Output format')
    parser.add_argument('--duration', '-d', type=float, help='Listen duration in seconds')
    parser.add_argument('--max', '-m', type=int, help='Maximum messages to capture')

    args = parser.parse_args()

    listener = MIDIListener(port_name=args.port, output_format=args.format)
    listener.listen(duration=args.duration, max_messages=args.max)


if __name__ == '__main__':
    main()
