#!/usr/bin/env python3
"""
MPK Mini IV Preset Decoder
Decodes the SysEx preset data structure.
"""

import json

# Load preset data
with open('presets_raw.json', 'r') as f:
    presets = json.load(f)

def decode_preset(data):
    """Decode a single preset."""
    result = {}

    # Header (bytes 0-6)
    result['header'] = {
        'manufacturer': data[0],  # 0x47 = AKAI
        'channel': data[1],
        'device_id': data[2],     # 0x5D = MPK Mini IV
        'function': data[3],      # 0x67 = preset data
        'length': (data[4] << 7) | data[5],
        'preset_number': data[6],
    }

    # Preset name (bytes 7-23, 17 bytes, null-terminated)
    name_bytes = bytes(data[7:24])
    result['name'] = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace')

    # Global settings (bytes 24-54)
    result['global'] = {
        'pad_channel': data[24] + 1,      # MIDI channel 1-16
        'key_channel': data[25] + 1,      # MIDI channel 1-16
        'octave': data[26] - 4,           # -4 to +4
        'transpose': data[27] - 12,       # -12 to +12
        'arp_tempo': data[28],            # BPM
        'arp_mode': data[29],
        'arp_time_div': data[30],
        'arp_clock': data[31],
        'arp_latch': data[32],
        'arp_swing': data[33],
        'arp_octave': data[34],
    }

    # Joystick settings (bytes around 35-42)
    result['joystick'] = {
        'x_positive': data[35],
        'x_negative': data[36],
        'y_positive': data[37],
        'y_negative': data[38],
    }

    # Aftertouch settings (bytes 43-53)
    result['aftertouch'] = {
        'mode': data[43],  # 0=off, 1=channel, 2=poly
        'threshold': data[44],
        'curve': data[45],
    }

    # Pads section (bytes 85-160, 16 pads x ~5 bytes each)
    # Each pad: note, PC, CC, mode + extra
    result['pads'] = []
    pad_start = 85

    # Looking at the hex dump pattern, each pad seems to be 5 bytes
    # Pattern: [idx] [note] [01] [0E] [next_note]
    # Let me try a different interpretation - looking for note values
    for i in range(16):
        # Find notes in the data - they should be in a predictable pattern
        # Based on hex dump: notes at offsets 87, 91, 95, 99, ...
        offset = 87 + (i * 4)
        if offset < len(data):
            pad = {
                'pad_number': i + 1,
                'note': data[offset],
                'bank': 'A' if i < 8 else 'B',
            }
            result['pads'].append(pad)

    # Knobs section (bytes 161-320, 8 knobs x 20 bytes each)
    # Each knob: CC (1), min (1), max (1), mode (1), name (16)
    result['knobs'] = []
    knob_start = 161  # 0xA1

    for i in range(8):
        offset = knob_start + (i * 20)
        if offset + 19 < len(data):
            name_bytes = bytes(data[offset + 4:offset + 20])
            name = name_bytes.split(b'\x00')[0].decode('ascii', errors='replace')

            knob = {
                'knob_number': i + 1,
                'cc': data[offset],
                'min': data[offset + 1],
                'max': data[offset + 2],
                'mode': data[offset + 3],  # 0=absolute, 1=relative?
                'name': name,
            }
            result['knobs'].append(knob)

    return result

# Decode all presets
print("=" * 70)
print("MPK Mini IV Preset Decoder")
print("=" * 70)

for preset_num, data in sorted(presets.items(), key=lambda x: int(x[0])):
    decoded = decode_preset(data)

    print(f"\n{'='*70}")
    print(f"PRESET {decoded['header']['preset_number']}: {decoded['name']}")
    print(f"{'='*70}")

    print(f"\nGlobal Settings:")
    print(f"  Pad MIDI Channel: {decoded['global']['pad_channel']}")
    print(f"  Keys/Knobs MIDI Channel: {decoded['global']['key_channel']}")
    print(f"  Octave: {decoded['global']['octave']:+d}")
    print(f"  Transpose: {decoded['global']['transpose']:+d} semitones")
    print(f"  Arpeggiator Tempo: {decoded['global']['arp_tempo']} BPM")

    print(f"\nKnobs:")
    print(f"  {'#':<4} {'CC':<6} {'Min':<5} {'Max':<5} {'Name':<16}")
    print(f"  {'-'*4} {'-'*6} {'-'*5} {'-'*5} {'-'*16}")
    for knob in decoded['knobs']:
        print(f"  {knob['knob_number']:<4} {knob['cc']:<6} {knob['min']:<5} {knob['max']:<5} {knob['name']:<16}")

# Save decoded data
decoded_all = {}
for preset_num, data in presets.items():
    decoded_all[preset_num] = decode_preset(data)

with open('presets_decoded.json', 'w') as f:
    json.dump(decoded_all, f, indent=2)

print(f"\n\nSaved decoded presets to presets_decoded.json")

# Print raw analysis
print("\n" + "=" * 70)
print("RAW DATA ANALYSIS - Preset 1")
print("=" * 70)

data = presets['1']
print("\nLooking for pad note values in data:")
# Notes should be MIDI note numbers (0-127), looking for a sequence
for i in range(50, 160):
    if 30 <= data[i] <= 80:  # Reasonable note range
        print(f"  Offset {i:3d} (0x{i:02X}): {data[i]:3d} (note {data[i]})")
