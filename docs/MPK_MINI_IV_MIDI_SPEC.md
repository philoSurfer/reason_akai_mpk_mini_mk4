# AKAI MPK Mini IV - Complete MIDI Specification

## Device Identification

| Property | Value |
|----------|-------|
| Manufacturer ID | `0x47` (71) - AKAI |
| Device Family | `0x5D` (93) |
| Device Member | `0x19` (25) |
| Firmware Version | 1.0.4.0 |
| USB Product Name | "MPK mini IV" |

## MIDI Ports

The MPK Mini IV exposes **5 MIDI ports**:

| Port Name | Direction | Purpose |
|-----------|-----------|---------|
| MPK mini IV MIDI Port | In/Out | Standard MIDI (notes, CC, pitch, etc.) |
| MPK mini IV DAW Port | In/Out | DAW integration/control |
| MPK mini IV Software Port | In/Out | SysEx communication with editor software |
| MPK mini IV Din Port | Out only | 5-pin DIN MIDI output |

## SysEx Protocol

### Message Format

```
F0 47 [channel] 5D [function] [length_hi] [length_lo] [data...] F7
```

- `F0` - SysEx start
- `47` - AKAI manufacturer ID
- `channel` - MIDI channel (usually `00`)
- `5D` - MPK Mini IV device ID
- `function` - Command/response code
- `length` - 7-bit encoded length (hi << 7 | lo)
- `F7` - SysEx end

### Function Codes

| Code | Hex | Direction | Description |
|------|-----|-----------|-------------|
| 102 | 0x66 | Request | Get preset from device |
| 103 | 0x67 | Response | Preset data from device |

### Get Preset Request

```
F0 47 00 5D 66 00 01 [preset_num] F7
```

- `preset_num`: 1-8

### Preset Data Response (321 bytes payload)

```
F0 47 00 5D 67 02 3B [preset_data...] F7
```

## Preset Data Structure (315 bytes)

| Offset | Length | Field | Description |
|--------|--------|-------|-------------|
| 0 | 1 | preset_number | Preset slot (1-8) |
| 1-17 | 17 | preset_name | Null-terminated ASCII name |
| 18 | 1 | pad_channel | Pad MIDI channel (0-15) |
| 19 | 1 | key_channel | Keys/Knobs MIDI channel (0-15) |
| 20 | 1 | octave | Octave offset (0-8, center=4) |
| 21 | 1 | transpose | Transpose (-12 to +12, stored as 0-24) |
| 22 | 1 | arp_tempo | Arpeggiator tempo (BPM) |
| 23-34 | 12 | arp_settings | Arpeggiator configuration |
| 35-78 | 44 | global_settings | Various global parameters |
| 79-158 | 80 | pad_config | 16 pads × 5 bytes each |
| 159-318 | 160 | knob_config | 8 knobs × 20 bytes each |

### Knob Configuration (20 bytes per knob)

| Offset | Field | Description |
|--------|-------|-------------|
| 0 | cc | MIDI CC number (0-127) |
| 1 | min | Minimum value (0-127) |
| 2 | max | Maximum value (0-127) |
| 3 | mode | Control mode (0=absolute) |
| 4-19 | name | 16-byte null-terminated name |

## Default MIDI Mapping (DAW Preset)

### MIDI Channels

| Control | Channel |
|---------|---------|
| Pads | 10 (drum channel) |
| Keys | 1 |
| Knobs | 1 |
| Joystick | 1 |
| Pitch Bend | 1 |

### Knobs (CC Numbers)

| Knob | CC | Default Range | Name |
|------|-----|---------------|------|
| 1 | 24 | 0-127 | Knob1 |
| 2 | 25 | 0-127 | Knob2 |
| 3 | 26 | 0-127 | Knob3 |
| 4 | 27 | 0-127 | Knob4 |
| 5 | 28 | 0-127 | Knob5 |
| 6 | 29 | 0-127 | Knob6 |
| 7 | 30 | 0-127 | Knob7 |
| 8 | 31 | 0-127 | Knob8 |

### Pads (Bank A - Notes)

| Pad | Note | Note Name | Velocity |
|-----|------|-----------|----------|
| 1 | 48 | C3 | Velocity sensitive |
| 2 | 50 | D3 | Velocity sensitive |
| 3 | 52 | E3 | Velocity sensitive |
| 4 | 53 | F3 | Velocity sensitive |
| 5 | 55 | G3 | Velocity sensitive |
| 6 | 57 | A3 | Velocity sensitive |
| 7 | 59 | B3 | Velocity sensitive |
| 8 | 60 | C4 | Velocity sensitive |

### Pads (Bank B - Notes)

| Pad | Note | Note Name | Velocity |
|-----|------|-----------|----------|
| 9 | 62 | D4 | Velocity sensitive |
| 10 | 64 | E4 | Velocity sensitive |
| 11 | 65 | F4 | Velocity sensitive |
| 12 | 67 | G4 | Velocity sensitive |
| 13 | 69 | A4 | Velocity sensitive |
| 14 | 71 | B4 | Velocity sensitive |
| 15 | 72 | C5 | Velocity sensitive |
| 16 | 74 | D5 | Velocity sensitive |

### Joystick

| Axis | CC | Range | Description |
|------|-----|-------|-------------|
| Y+ (up) | 1 | 0-127 | Modulation wheel |
| Y- (down) | 1 | 0-127 | Modulation wheel |
| X (left/right) | - | Pitch bend | 14-bit pitch bend |

### Pitch Bend

- **Range**: -8192 to +8191 (full 14-bit resolution)
- **Center**: 0
- **Channel**: 1

## Transport Controls

Transport buttons send CC messages on **Channel 1** to both MIDI Port and DAW Port.

| Button | CC | Behavior | Value |
|--------|-----|----------|-------|
| **PLAY/STOP** | 76 | Toggle | 127 (single button toggles play/stop) |
| LOOP | 74 | Toggle | 127 |
| RECORD | 77 | Toggle | 127 |
| FAST FORWARD (>>) | 78 | Toggle | 127 |
| UNDO | 73 | Toggle | 127 |
| TAP TEMPO | 11 | Momentary | 127 (press), 0 (release) |
| SHIFT (hold) | 17 | Momentary | 127 (press), 0 (release) |
| BANK - | 15 | Momentary | 127 (press), 0 (release) |
| BANK + | 16 | Momentary | 127 (press), 0 (release) |

### Shifted Functions

Hold **SHIFT** (CC 17) and press another button for secondary functions:

| Combo | Primary CC | Function |
|-------|-----------|----------|
| SHIFT + RECORD | 17 + 77 | **Quantize On/Off** toggle |
| SHIFT + TAP TEMPO | 17 + 11 | **Click On/Off** toggle |
| SHIFT + UNDO | 17 + 73 | **Redo** |

**Note**:
- The Play and Stop functions share a single toggle button (CC 74)
- Toggle buttons only send value 127 on press (no release message)
- SHIFT is momentary (127 on press, 0 on release)
- Shifted functions send the same CC as the primary button; software must track SHIFT state

### Reason DAW Mapping

For Reason Remote integration:

```lua
-- Transport buttons
{ name="Play/Stop", pattern="b0 4a xx" },  -- CC 74 (toggle play/stop)
{ name="Forward",   pattern="b0 4e xx" },  -- CC 78

-- CC 77 (Record) and CC 17 (SHIFT) handled in remote_process_midi()
-- to support: Record (alone) vs Quantize (SHIFT + Record)
```

The Lua codec tracks SHIFT state to route CC 77 to either:
- **Record** → when pressed alone
- **Quantize On/Off** → when SHIFT is held

## Pad Modes

Pads can operate in three modes, switchable via buttons on the device:

### Note Mode (Default)
- Sends Note On/Off messages
- Channel: 10 (drum channel)
- See "Pads (Bank A/B - Notes)" above

### CC Mode
Pads send CC messages with velocity as value:

| Pad | Bank A CC | Bank B CC | Channel |
|-----|-----------|-----------|---------|
| 1 | 16 | 24 | 10 |
| 2 | 17 | 25 | 10 |
| 3 | 18 | 26 | 10 |
| 4 | 19 | 27 | 10 |
| 5 | 20 | 28 | 10 |
| 6 | 21 | 29 | 10 |
| 7 | 22 | 30 | 10 |
| 8 | 23 | 31 | 10 |

- Value on press: Velocity (1-127)
- Value on release: 0

### Program Change Mode
Pads send Program Change messages:

| Pad | Bank A Program | Bank B Program | Channel |
|-----|----------------|----------------|---------|
| 1-8 | 0-7 | 8-15 | 10 |

### Keyboard

- **25 keys** (2 octaves + 1 note)
- **Base note**: Depends on octave setting
- **Velocity sensitive**: Yes
- **Aftertouch**: Channel pressure (configurable)
- **Channel**: 1 (configurable)

## Presets

The device stores **8 presets**:

| Slot | Default Name |
|------|--------------|
| 1 | DAW |
| 2 | USER1 |
| 3 | USER2 |
| 4 | USER3 |
| 5 | USER4 |
| 6 | USER5 |
| 7 | USER6 |
| 8 | USER7 |

## Arpeggiator

| Parameter | Values |
|-----------|--------|
| Enable | On/Off |
| Mode | Up, Down, Inclusive, Exclusive, Random, Order |
| Time Division | 1/4, 1/4T, 1/8, 1/8T, 1/16, 1/16T, 1/32, 1/32T |
| Clock | Internal, External |
| Latch | On/Off |
| Swing | 50-64% |
| Tempo | 30-240 BPM |
| Octave Range | 1-4 |

### Arpeggiator Preset Data Offsets

| Offset | Field | Values |
|--------|-------|--------|
| 28 | arp_tempo | BPM (30-240) |
| 29 | arp_mode | 0-5 (Up, Down, Inclusive, Exclusive, Random, Order) |
| 30 | arp_time_div | 0-7 (1/4, 1/4T, 1/8, 1/8T, 1/16, 1/16T, 1/32, 1/32T) |
| 31 | arp_clock | 0=Internal, 1=External |
| 32 | arp_latch | 0=Off, 1=On |
| 33 | arp_swing | 0-14 (50-64%) |
| 34 | arp_octave | 0-3 (1-4 octaves) |

**Note**: Offsets are relative to the SysEx payload (after F0), not including the F0 byte itself.

## Universal Identity Response

Request: `F0 7E 7F 06 01 F7`

Response:
```
F0 7E 7F 06 02 47 5D 00 19 00 01 00 04 00 00 00 00 00 [serial...] F7
```

- Bytes 5-6: Manufacturer ID (0x47 = AKAI)
- Bytes 7-8: Device Family (0x5D 0x00)
- Bytes 9-10: Device Member (0x19 0x00)
- Bytes 11-14: Firmware version
- Remaining: Serial number (ASCII)

## Python Example - Read Preset

```python
import mido

def get_preset(preset_num):
    with mido.open_input('MPK mini IV Software Port') as inport:
        with mido.open_output('MPK mini IV Software Port') as outport:
            # Request preset
            msg = mido.Message('sysex', data=[0x47, 0x00, 0x5D, 0x66, 0x00, 0x01, preset_num])
            outport.send(msg)

            # Wait for response
            for msg in inport:
                if msg.type == 'sysex' and msg.data[3] == 0x67:
                    return list(msg.data)
    return None

preset = get_preset(1)
print(f"Preset name: {bytes(preset[7:24]).split(b'\\x00')[0].decode()}")
```

## Files Generated

- `presets_raw.json` - Raw SysEx data for all 8 presets
- `presets_decoded.json` - Decoded preset data
- `poll_mk4.py` - MIDI polling script
- `decode_preset.py` - Preset decoder script
