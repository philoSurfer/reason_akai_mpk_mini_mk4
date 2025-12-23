#!/usr/bin/env python3
"""
Generate SysEx preset for MPK Mini IV with Kong-compatible pad notes.
Outputs hex string suitable for Reason Remote's remote.make_midi()
"""

import json
import os

# Get directory where this script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the DAW preset as base
with open(os.path.join(SCRIPT_DIR, 'presets_raw.json'), 'r') as f:
    presets = json.load(f)

# Use preset 1 (DAW) as base
base_preset = presets['1'].copy()

# Pad note offsets (verified from raw data analysis)
# In the raw SysEx data (including header), pad notes are at indices:
# 81, 86, 91, 96, 101, 106, 111, 116, 121, 126, 131, 136, 141, 146, 151, 156
# Each pad is 5 bytes: [note, ?, cc, ?, ?]
PAD_NOTE_OFFSETS = [81 + (i * 5) for i in range(16)]

# Kong-compatible pad notes (C1 = 36 through D#2 = 51)
# This maps pads 1-16 to sequential notes starting at C1
KONG_PAD_NOTES = list(range(36, 52))  # 36, 37, 38, ... 51

print("=" * 70)
print("MPK Mini IV - Reason Preset Generator")
print("=" * 70)

print("\nOriginal pad notes:")
for i, offset in enumerate(PAD_NOTE_OFFSETS):
    print(f"  Pad {i+1:2d}: Note {base_preset[offset]:3d} (offset {offset})")

print("\nNew Kong-compatible pad notes:")
for i, (offset, note) in enumerate(zip(PAD_NOTE_OFFSETS, KONG_PAD_NOTES)):
    base_preset[offset] = note
    print(f"  Pad {i+1:2d}: Note {note:3d} -> {['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][note % 12]}{note // 12 - 1}")

# Change preset name to "Reason" (bytes 7-23)
name = "Reason"
name_bytes = name.encode('ascii') + b'\x00' * (17 - len(name))
for i, b in enumerate(name_bytes):
    base_preset[7 + i] = b

# Ensure keyboard channel is 1 (index 0)
base_preset[25] = 0  # key_channel = 1

# Set preset slot to 2 (USER1 renamed to "Reason")
base_preset[6] = 2

# Generate the full SysEx message
# Format: F0 47 00 5D 67 [length_hi] [length_lo] [preset_data...] F7
# preset_data starts from byte 6 (preset_num) in the raw data

preset_data = base_preset[6:]  # Data from preset_num onwards
data_length = len(preset_data)
length_hi = (data_length >> 7) & 0x7F
length_lo = data_length & 0x7F

# Build SysEx for writing to preset slot 2
sysex = [0xF0, 0x47, 0x00, 0x5D, 0x67, length_hi, length_lo] + preset_data + [0xF7]

# Convert to hex string for Reason Remote
hex_string = ' '.join(f'{b:02X}' for b in sysex)

print("\n" + "=" * 70)
print("SysEx for Reason Remote (remote.make_midi):")
print("=" * 70)
print(f"\nLength: {len(sysex)} bytes")
print(f"\nHex string (for Lua codec):")
print(f'"{hex_string}"')

# Also save to file for reference
output_path = os.path.join(SCRIPT_DIR, 'reason_preset_sysex.txt')
with open(output_path, 'w') as f:
    f.write(hex_string)
print(f"\nSaved to {output_path}")

# Generate Lua code snippet
print("\n" + "=" * 70)
print("Lua code for codec (add to MPK mini IV.lua):")
print("=" * 70)
print('''
function remote_prepare_for_use()
    return {
        -- Send Kong-compatible preset to MPK Mini IV RAM
        remote.make_midi("''' + hex_string + '''"),
    }
end
''')
