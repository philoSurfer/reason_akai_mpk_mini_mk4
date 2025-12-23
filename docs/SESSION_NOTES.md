# MPK Mini IV - Kong Mapping Session Notes

## Objective

Configure the AKAI MPK Mini IV pads to send Kong/Redrum-compatible MIDI notes (36-51) for use with Reason Studios Reason DAW.

## Key Findings

### MIDI Port Architecture

The MPK Mini IV exposes 3 usable MIDI ports:

| Port | Purpose |
|------|---------|
| MPK mini IV MIDI Port | Standard MIDI I/O (notes, CC, etc.) |
| MPK mini IV DAW Port | DAW integration |
| MPK mini IV Software Port | **SysEx communication** - use this for preset read/write |

### SysEx Protocol

#### Read Preset
```
Request:  F0 47 00 5D 66 00 01 [preset_num] F7
Response: F0 47 00 5D 67 [len_hi] [len_lo] [preset_data...] F7
```
- `preset_num`: 1-8 (stored presets)
- Send/receive via **Software Port**

#### Write Preset
```
F0 47 00 5D 67 [len_hi] [len_lo] [preset_data...] F7
```
- Same format as read response
- Send via **Software Port**
- Length is 7-bit encoded: `len_hi << 7 | len_lo`

### Preset Data Structure (321 bytes inner data)

| Offset | Field | Notes |
|--------|-------|-------|
| 0-5 | Header | `47 00 5D 67 len_hi len_lo` |
| 6 | Preset number | 1-8 |
| 7-23 | Preset name | 17 bytes, null-terminated ASCII |
| 24 | Pad MIDI channel | 0-15 (displayed as 1-16) |
| 25 | Key MIDI channel | 0-15 |
| 81, 86, 91... | Pad notes | **Every 5 bytes starting at 81** |

### Pad Note Offsets (Critical Discovery)

Pad notes are stored at indices `81 + (i * 5)` for pads 0-15:

```
Pad 1:  offset 81
Pad 2:  offset 86
Pad 3:  offset 91
Pad 4:  offset 96
Pad 5:  offset 101
Pad 6:  offset 106
Pad 7:  offset 111
Pad 8:  offset 116
Pad 9:  offset 121
Pad 10: offset 126
Pad 11: offset 131
Pad 12: offset 136
Pad 13: offset 141
Pad 14: offset 146
Pad 15: offset 151
Pad 16: offset 156
```

Each pad occupies 5 bytes: `[note, ?, cc, ?, ?]`

### Kong-Compatible Mapping

Kong/Redrum expects notes 36-51 (C1-D#2) for pads 1-16:

| Pad | Note | Note Name |
|-----|------|-----------|
| 1 | 36 | C1 |
| 2 | 37 | C#1 |
| 3 | 38 | D1 |
| ... | ... | ... |
| 16 | 51 | D#2 |

### Preset Slot Behavior

- **Slot 1 (DAW)**: Appears to be protected/hardcoded - writes may not persist
- **Slot 2-8 (USER1-7)**: Writable via SysEx
- **Slot 0 (RAM)**: Attempted but doesn't apply immediately

### Limitations Discovered

**No Remote Preset Switching**: The MPK Mini IV does not respond to any MIDI command to switch between presets. Tested:
- Function codes 0x60-0x7F
- Program Change on all channels/ports
- Various SysEx formats

User must manually select presets using: **PROG SELECT + Pad [1-8]**

## Final Solution

### Preset Configuration

- **Slot 2** renamed to "Reason" with Kong-compatible notes 36-51
- Reason Remote codec sends SysEx to write/refresh this preset on connection

### User Workflow

1. Open Reason (codec writes preset to slot 2)
2. On controller: Press **PROG SELECT**, tap **Pad 2**
3. Pads now trigger Kong/Redrum pads 1-16 correctly

### Files Modified

- `reason_remote/MPK mini IV.lua` - Updated SysEx in `remote_prepare_for_use()`
- `generate_reason_preset.py` - Fixed pad note offsets
- `reason_preset_sysex.txt` - Correct SysEx for preset 2

## Code Snippets

### Python: Write Kong Preset to Slot 2

```python
import mido
import json

with open('presets_raw.json', 'r') as f:
    presets = json.load(f)

base = presets['1'].copy()

# Set Kong notes at correct offsets
PAD_NOTE_OFFSETS = [81 + (i * 5) for i in range(16)]
for i, note in enumerate(range(36, 52)):
    base[PAD_NOTE_OFFSETS[i]] = note

# Set name to "Reason"
for i, c in enumerate("Reason"):
    base[7 + i] = ord(c)
for i in range(len("Reason"), 17):
    base[7 + i] = 0

# Set preset slot 2
base[6] = 2

# Build SysEx
preset_payload = base[6:]
len_hi = (len(preset_payload) >> 7) & 0x7F
len_lo = len(preset_payload) & 0x7F
sysex_data = [0x47, 0x00, 0x5D, 0x67, len_hi, len_lo] + preset_payload

# Send via Software Port
with mido.open_output('MPK mini IV Software Port') as port:
    port.send(mido.Message('sysex', data=sysex_data))
```

### Python: Read Preset from Controller

```python
import mido

request = [0x47, 0x00, 0x5D, 0x66, 0x00, 0x01, 0x02]  # Request preset 2

with mido.open_input('MPK mini IV Software Port') as inport:
    with mido.open_output('MPK mini IV Software Port') as outport:
        outport.send(mido.Message('sysex', data=request))
        for msg in inport:
            if msg.type == 'sysex':
                data = list(msg.data)
                name = bytes(data[7:24]).split(b'\x00')[0].decode()
                print(f"Preset name: {name}")
                print(f"Pad 1 note: {data[81]}")
                break
```

## Warnings

- **Update Mode**: Sending certain SysEx function codes can trigger firmware update mode. Avoid sending untested function codes in bulk.
- **Port Conflicts**: Reason takes exclusive access to MIDI ports. Close Reason before running Python MIDI scripts.

## Date

2024-12-22
