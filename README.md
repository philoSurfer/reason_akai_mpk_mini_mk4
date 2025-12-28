# AKAI MPK Mini IV - Reason Remote Integration

Reason Studios Remote control surface integration for the AKAI MPK Mini IV MIDI controller.

## Features

- **Transport Controls**: Play/Stop, Record, Loop, Fast Forward, Undo/Redo
- **SHIFT Modifiers**: Quantize (SHIFT+Record), Click (SHIFT+Tap Tempo), Redo (SHIFT+Undo)
- **8 Knobs**: Mapped to CCs 24-31 for parameter control
- **Kong/Redrum Pads**: Preset 2 maps pads 1-16 to notes 36-51
- **Keyboard**: Full pass-through with pitch bend and mod wheel
- **Bank +/- Patch Navigation**: Browse patches on focused instruments
- **Serum 2 Macro Control**: Knobs 1-8 map to Serum 2 Macros 1-8

## Installation

### macOS

**Option 1: Script (Recommended)**
```bash
./deploy.sh
```

**Option 2: Manual**

Copy these files:
```
reason_remote/MPK mini IV.lua        → ~/Library/Application Support/Propellerhead Software/Remote/Codecs/Lua Codecs/Akai/
reason_remote/MPK mini IV.luacodec   → ~/Library/Application Support/Propellerhead Software/Remote/Codecs/Lua Codecs/Akai/
reason_remote/MPK_mini_IV.remotemap  → ~/Library/Application Support/Propellerhead Software/Remote/Maps/Akai/MPK mini IV.remotemap
```

### Windows

**Option 1: Script (Recommended)**

Double-click `deploy.bat` or run from Command Prompt:
```cmd
deploy.bat
```

**Option 2: Manual**

Copy these files to your `%APPDATA%` folder:
```
reason_remote\MPK mini IV.lua        → %APPDATA%\Propellerhead Software\Remote\Codecs\Lua Codecs\Akai\
reason_remote\MPK mini IV.luacodec   → %APPDATA%\Propellerhead Software\Remote\Codecs\Lua Codecs\Akai\
reason_remote\MPK_mini_IV.remotemap  → %APPDATA%\Propellerhead Software\Remote\Maps\Akai\MPK mini IV.remotemap
```

To find your `%APPDATA%` folder: Press `Win+R`, type `%APPDATA%`, and press Enter.

Full path example: `C:\Users\YourName\AppData\Roaming\Propellerhead Software\Remote\`

## Setup in Reason

1. Open Reason
2. Go to **Preferences → Control Surfaces**
3. Click **Add** and select **Akai MPK mini IV**
4. Set MIDI In/Out to "MPK mini IV MIDI Port"

## Using Kong/Redrum Pad Mapping

The default controller preset uses chromatic notes (48-74). For Kong/Redrum compatibility:

1. On the MPK Mini IV, press **PROG SELECT**
2. Tap **Pad 2** to select the "Reason" preset
3. Pads now send notes 36-51, matching Kong/Redrum pads 1-16

The Reason preset is automatically saved to slot 2 when Reason connects.

## Arpeggiator External Clock Sync

To sync the MPK Mini IV arpeggiator with Reason's tempo:

1. Hold **SHIFT** + **ARP** to open Arp Config menu
2. Scroll to **Clock** setting
3. Change from **INT** to **EXT**

**Note**: This must be set manually each session. The arpeggiator clock setting cannot be automated via SysEx (firmware limitation).

### Troubleshooting 3x Tempo Display

If the arpeggiator shows 3x the actual tempo (e.g., 65 BPM shows as 195 BPM):

1. Open **Reason Preferences → Advanced MIDI**
2. In the **Sync** section, ensure MIDI clock is only sent on ONE MPK Mini IV port
3. Disable clock output on DAW Port and Software Port (keep only MIDI Port)

## Control Mapping

### Transport Controls

| Control | Function | MIDI |
|---------|----------|------|
| Play/Stop | Toggle playback | CC 76 |
| Record | Record / Quantize (SHIFT) | CC 77 |
| Loop | Loop on/off | CC 74 |
| Fast Forward | Forward | CC 78 |
| Undo | Undo / Redo (SHIFT) | CC 73 |
| Tap Tempo | Tap tempo / Click (SHIFT) | CC 11 |
| SHIFT | Modifier | CC 17 |
| Bank - | Previous patch | CC 15 |
| Bank + | Next patch | CC 16 |

### Knobs

| Knob | CC | Serum 2 Mapping |
|------|-----|-----------------|
| Knob 1 | CC 24 | Macro 1 |
| Knob 2 | CC 25 | Macro 2 |
| Knob 3 | CC 26 | Macro 3 |
| Knob 4 | CC 27 | Macro 4 |
| Knob 5 | CC 28 | Macro 5 |
| Knob 6 | CC 29 | Macro 6 |
| Knob 7 | CC 30 | Macro 7 |
| Knob 8 | CC 31 | Macro 8 |

### Pads (Preset 2 - "Reason")

| Pads | Notes | Channel |
|------|-------|---------|
| 1-8 (Bank A) | 36-43 (C1-G1) | 10 |
| 9-16 (Bank B) | 44-51 (G#1-D#2) | 10 |

## Project Structure

```
mk4/
├── reason_remote/          # Reason Remote files (deployed)
│   ├── MPK mini IV.lua         # Lua codec with MIDI processing
│   ├── MPK mini IV.luacodec    # Codec metadata
│   └── MPK_mini_IV.remotemap   # Control mappings
├── tools/                  # Development utilities
│   ├── midi_listener.py        # Monitor MIDI input
│   ├── decode_preset.py        # Decode SysEx presets
│   ├── generate_reason_preset.py
│   ├── read_preset_clock.py    # Check arpeggiator settings
│   └── poll_mk4.py             # Poll device for data
├── docs/                   # Documentation
│   ├── MPK_MINI_IV_MIDI_SPEC.md    # Complete MIDI protocol
│   └── SESSION_NOTES.md
├── openspec/               # Change management & specs
├── deploy.sh               # macOS installation script
├── deploy.bat              # Windows installation script
└── README.md
```

## Development

### Requirements

- Python 3.x with `mido` and `python-rtmidi` packages
- Close Reason before running MIDI scripts (port conflicts)

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mido python-rtmidi
```

### Testing MIDI

```bash
source .venv/bin/activate
python tools/midi_listener.py
```

### Reading Preset Data

```bash
python tools/decode_preset.py      # Decode all presets
python tools/read_preset_clock.py  # Check arp clock setting
```

### Regenerating Preset SysEx

```bash
python tools/generate_reason_preset.py
```

## Adding VST Plugin Mappings

To map knobs to a VST plugin (like Serum 2):

1. Load the VST in Reason's rack
2. Select the device
3. Go to **File → Export Device Remote Info**
4. Open the exported text file to find the scope line
5. Add a new scope section to `MPK_mini_IV.remotemap`

Example scope format:
```
Scope	Xfer Records	vst3.56534558667350736572756D20320000.Serum 2
```

## MIDI Ports

The MPK Mini IV exposes multiple MIDI ports:

| Port | Purpose |
|------|---------|
| MPK mini IV MIDI Port | Standard MIDI (notes, CC, pitch) |
| MPK mini IV DAW Port | DAW integration/transport |
| MPK mini IV Software Port | SysEx communication |
| MPK mini IV Din Port | 5-pin DIN MIDI output |

## Known Limitations

- **Arpeggiator clock**: Cannot be set via SysEx; must be configured manually each session
- **Preset 1 (DAW)**: Read-only; cannot be modified
- **Preset selection**: User must manually select preset 2 on the controller

## License

MIT
