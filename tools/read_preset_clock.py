#!/usr/bin/env python3
"""
Read preset 2 from MPK Mini IV and check the arp_clock setting.
"""

import mido
import time

def read_preset(preset_num=2):
    # Find the Software Port
    in_port_name = None
    out_port_name = None

    for name in mido.get_output_names():
        if 'MPK mini' in name and 'Software' in name:
            out_port_name = name

    for name in mido.get_input_names():
        if 'MPK mini' in name and 'Software' in name:
            in_port_name = name

    if not in_port_name or not out_port_name:
        print("ERROR: MPK mini IV Software Port not found!")
        return None

    print(f"Reading preset {preset_num} from device...")
    print(f"  Output: {out_port_name}")
    print(f"  Input: {in_port_name}")
    print()

    # Request preset: F0 47 00 5D 66 00 01 [preset_num] F7
    request = [0x47, 0x00, 0x5D, 0x66, 0x00, 0x01, preset_num]

    try:
        with mido.open_input(in_port_name) as inport:
            with mido.open_output(out_port_name) as outport:
                # Send request
                msg = mido.Message('sysex', data=request)
                outport.send(msg)

                # Wait for response
                start = time.time()
                while time.time() - start < 3.0:
                    for msg in inport.iter_pending():
                        if msg.type == 'sysex' and len(msg.data) > 10:
                            if msg.data[3] == 0x67:  # Preset response
                                return list(msg.data)
                    time.sleep(0.05)

                print("ERROR: No response from device (timeout)")
                return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def analyze_preset(data):
    if not data:
        return

    print(f"Received {len(data)} bytes")
    print()

    # Decode key fields
    preset_num = data[6]
    name_bytes = bytes(data[7:24])
    name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace')

    print(f"Preset Number: {preset_num}")
    print(f"Preset Name: '{name}'")
    print()

    print("Arpeggiator Settings:")
    print(f"  Offset 28 - arp_tempo:    {data[28]} BPM")
    print(f"  Offset 29 - arp_mode:     {data[29]}")
    print(f"  Offset 30 - arp_time_div: {data[30]}")
    print(f"  Offset 31 - arp_clock:    {data[31]} ({'EXTERNAL' if data[31] == 1 else 'INTERNAL'})")
    print(f"  Offset 32 - arp_latch:    {data[32]}")
    print(f"  Offset 33 - arp_swing:    {data[33]}")
    print(f"  Offset 34 - arp_octave:   {data[34]}")
    print()

    # Show raw bytes around arp_clock for debugging
    print("Raw bytes around arp settings (offsets 27-35):")
    for i in range(27, 36):
        print(f"  [{i:2d}] 0x{data[i]:02X} = {data[i]:3d}")

if __name__ == '__main__':
    print("=" * 50)
    print("MPK Mini IV Preset Reader")
    print("=" * 50)
    print()

    data = read_preset(2)
    if data:
        analyze_preset(data)
