#!/usr/bin/env python3
"""
MPK Mini MK4 MIDI Discovery Script
Polls the device to discover its SysEx protocol and MIDI capabilities.
"""

import mido
import time
from collections import defaultdict

def hex_str(data):
    """Format bytes as hex string."""
    return " ".join(f"{b:02X}" for b in data)

def send_and_receive(outport, inport, sysex_data, description, timeout=0.5):
    """Send a SysEx message and capture any response."""
    print(f"\n>>> Sending: {description}")
    print(f"    TX: F0 {hex_str(sysex_data)} F7")

    # Clear any pending messages
    while inport.poll():
        pass

    # Send the message
    msg = mido.Message('sysex', data=list(sysex_data))
    outport.send(msg)

    # Wait for response
    responses = []
    start = time.time()
    while time.time() - start < timeout:
        msg = inport.poll()
        if msg:
            if msg.type == 'sysex':
                responses.append(msg.data)
                print(f"    RX: F0 {hex_str(msg.data)} F7")
            else:
                print(f"    RX (other): {msg}")
        time.sleep(0.01)

    if not responses:
        print("    (no response)")

    return responses

def main():
    print("=" * 70)
    print("MPK Mini MK4 MIDI Discovery")
    print("=" * 70)

    # List all ports
    in_ports = mido.get_input_names()
    out_ports = mido.get_output_names()

    mpk_in_ports = [p for p in in_ports if 'MPK mini IV' in p]
    mpk_out_ports = [p for p in out_ports if 'MPK mini IV' in p]

    print(f"\nMPK Mini IV Input Ports: {mpk_in_ports}")
    print(f"MPK Mini IV Output Ports: {mpk_out_ports}")

    # Focus on Software Port for SysEx
    software_in = next((p for p in mpk_in_ports if 'Software' in p), None)
    software_out = next((p for p in mpk_out_ports if 'Software' in p), None)

    if not software_in or not software_out:
        print("ERROR: Software Port not found!")
        return

    print(f"\nUsing Software Port for SysEx communication...")

    inport = mido.open_input(software_in)
    outport = mido.open_output(software_out)

    # 1. Universal MIDI Identity Request
    responses = send_and_receive(
        outport, inport,
        [0x7E, 0x7F, 0x06, 0x01],
        "Universal Identity Request"
    )

    if responses:
        for resp in responses:
            if len(resp) >= 6:
                print(f"\n    === IDENTITY RESPONSE DECODED ===")
                print(f"    Manufacturer ID: {hex_str(resp[1:4]) if resp[1] == 0 else hex_str([resp[1]])}")
                if len(resp) >= 8:
                    print(f"    Device Family: {hex_str(resp[4:6])}")
                    print(f"    Device Member: {hex_str(resp[6:8])}")
                if len(resp) >= 12:
                    print(f"    Software Rev: {hex_str(resp[8:12])}")

    # 2. Try AKAI-specific queries - trying many device IDs
    print("\n" + "=" * 70)
    print("Trying AKAI SysEx Queries")
    print("=" * 70)

    # Device IDs to try (AKAI uses 0x47 as manufacturer)
    device_ids_to_try = [
        0x4A, 0x4B, 0x4C, 0x4D,  # Likely MK4 candidates
        0x49,  # MK3
        0x44,  # MPK Mini Play
        0x26,  # MK2
        0x7C,  # MK1
        0x7F,  # Broadcast
        0x00,  # Sometimes used
    ]

    found_device_id = None

    for dev_id in device_ids_to_try:
        # Try request preset format: F0 47 [ch] [dev_id] [func] [len_hi] [len_lo] [preset] F7
        # Function 0x63 = Get preset (older), 0x66 = Get preset (newer)

        for func in [0x63, 0x66, 0x67]:
            responses = send_and_receive(
                outport, inport,
                [0x47, 0x00, dev_id, func, 0x00, 0x01, 0x01],
                f"AKAI Preset Request (dev=0x{dev_id:02X}, func=0x{func:02X})",
                timeout=0.3
            )
            if responses:
                found_device_id = dev_id
                print(f"\n    !!! FOUND WORKING DEVICE ID: 0x{dev_id:02X} !!!")
                break

        if found_device_id:
            break

    # 3. Try knob position request
    print("\n" + "=" * 70)
    print("Trying Knob Position Requests")
    print("=" * 70)

    for dev_id in ([found_device_id] if found_device_id else device_ids_to_try[:5]):
        send_and_receive(
            outport, inport,
            [0x47, 0x00, dev_id, 0x60, 0x00, 0x00],
            f"Request Knob Positions (dev=0x{dev_id:02X})"
        )

    inport.close()
    outport.close()

    # 4. Monitor MIDI Port for real-time data
    print("\n" + "=" * 70)
    print("Monitoring MIDI Port - INTERACT WITH DEVICE NOW!")
    print("(Press pads, turn knobs, play keys for 15 seconds)")
    print("=" * 70)

    midi_port_in = next((p for p in mpk_in_ports if 'MIDI Port' in p and 'DAW' not in p), None)
    if midi_port_in:
        with mido.open_input(midi_port_in) as inport:
            messages = defaultdict(list)
            start = time.time()

            while time.time() - start < 15:
                msg = inport.poll()
                if msg:
                    print(f"  {msg}")
                    messages[msg.type].append(msg)
                time.sleep(0.001)

            # Summary
            print("\n" + "=" * 70)
            print("MIDI CAPABILITY SUMMARY")
            print("=" * 70)

            if messages:
                for msg_type, msgs in sorted(messages.items()):
                    print(f"\n{msg_type}: {len(msgs)} messages")
                    if msg_type == 'control_change':
                        ccs = {}
                        for m in msgs:
                            if m.control not in ccs:
                                ccs[m.control] = {'channel': m.channel, 'min': m.value, 'max': m.value}
                            else:
                                ccs[m.control]['min'] = min(ccs[m.control]['min'], m.value)
                                ccs[m.control]['max'] = max(ccs[m.control]['max'], m.value)
                        print(f"  CC Assignments:")
                        for cc, info in sorted(ccs.items()):
                            print(f"    CC {cc:3d} (ch {info['channel']+1}): range {info['min']}-{info['max']}")
                    elif msg_type == 'note_on':
                        notes = {}
                        for m in msgs:
                            if m.note not in notes:
                                notes[m.note] = {'channel': m.channel, 'velocities': [m.velocity]}
                            else:
                                notes[m.note]['velocities'].append(m.velocity)
                        print(f"  Note Assignments:")
                        for note, info in sorted(notes.items()):
                            vel_range = f"{min(info['velocities'])}-{max(info['velocities'])}"
                            print(f"    Note {note:3d} (ch {info['channel']+1}): velocity range {vel_range}")
                    elif msg_type == 'program_change':
                        progs = set((m.channel, m.program) for m in msgs)
                        print(f"  Program Changes: {sorted(progs)}")
                    elif msg_type == 'pitchwheel':
                        pitches = [m.pitch for m in msgs]
                        print(f"  Pitch range: {min(pitches)} to {max(pitches)}")
            else:
                print("\nNo MIDI messages captured. Make sure to interact with the device!")

    print("\nDone!")

if __name__ == "__main__":
    main()
