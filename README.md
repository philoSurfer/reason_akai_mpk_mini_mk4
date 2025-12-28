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

## Please consider Donating if you find this useful
I have a family, and every little bit helps. Aloha.

Venmo: @philosurfer

## Installation

### Step 1: Download

1. Click the green **Code** button at the top of this page
2. Select **Download ZIP**
3. Extract the ZIP file to a location you can find (like your Desktop or Downloads folder)

### Step 2: Install the Files

#### macOS

**Easy Method (Recommended):**
1. Open the extracted folder
2. Double-click `deploy.sh`
3. If prompted, click "Open" to allow the script to run
4. Done! The files are now installed.

**Manual Method:**
1. Open Finder
2. Press `Cmd + Shift + G` (Go to Folder)
3. Paste: `~/Library/Application Support/Propellerhead Software/Remote/`
4. Create these folders if they don't exist:
   - `Codecs/Lua Codecs/Akai/`
   - `Maps/Akai/`
5. Copy from the `reason_remote/` folder you downloaded:
   - `MPK mini IV.lua` → into `Codecs/Lua Codecs/Akai/`
   - `MPK mini IV.luacodec` → into `Codecs/Lua Codecs/Akai/`
   - `MPK_mini_IV.remotemap` → into `Maps/Akai/` (rename to `MPK mini IV.remotemap`)

#### Windows

**Easy Method (Recommended):**
1. Open the extracted folder
2. Double-click `deploy.bat`
3. A window will appear showing the installation progress
4. Press any key to close when done

**Manual Method:**
1. Press `Win + R` to open Run dialog
2. Type `%APPDATA%` and press Enter
3. Navigate to `Propellerhead Software\Remote\`
4. Create these folders if they don't exist:
   - `Codecs\Lua Codecs\Akai\`
   - `Maps\Akai\`
5. Copy from the `reason_remote\` folder you downloaded:
   - `MPK mini IV.lua` → into `Codecs\Lua Codecs\Akai\`
   - `MPK mini IV.luacodec` → into `Codecs\Lua Codecs\Akai\`
   - `MPK_mini_IV.remotemap` → into `Maps\Akai\` (rename to `MPK mini IV.remotemap`)

### Step 3: Setup in Reason

1. Open Reason (or restart if already open)
2. Go to **Preferences → Control Surfaces**
3. Click **Add** and select **Akai MPK mini IV**
4. Configure the MIDI ports:
   - **Input 1**: MPK mini IV DAW Port (transport controls)
   - **Input 2**: MPK mini IV MIDI Port (keyboard, knobs, pads)
5. Click **OK** to save

## Using Kong/Redrum Pad Mapping

The default controller preset uses chromatic notes (48-74). For Kong/Redrum compatibility:

1. On the MPK Mini IV, hold **SHIFT** and press **USER PRESETS**
2. Turn the knob to select **Prg2:Reason**
3. Press the knob to confirm
4. Pads now send notes 36-51, matching Kong/Redrum pads 1-16

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
├── device_data/            # Exported device remote info
│   └── Serum 2 Remote Info.txt # VST scope reference
├── docs/                   # Documentation
│   ├── MPK_MINI_IV_MIDI_SPEC.md    # Complete MIDI protocol
│   └── SESSION_NOTES.md
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
- **Preset selection**: User must manually select Prg2:Reason on the controller (SHIFT + USER PRESETS)

## License

MIT
