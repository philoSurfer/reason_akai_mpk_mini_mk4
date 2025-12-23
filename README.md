# AKAI MPK Mini IV - Reason Remote Integration

Reason Studios Remote control surface integration for the AKAI MPK Mini IV MIDI controller.

## Features

- **Transport Controls**: Play/Stop, Record, Loop, Fast Forward, Undo/Redo
- **SHIFT Modifiers**: Quantize (SHIFT+Record), Click (SHIFT+Tap Tempo), Redo (SHIFT+Undo)
- **8 Knobs**: Mapped to CCs 24-31 for parameter control
- **Kong/Redrum Pads**: Preset 2 maps pads 1-16 to notes 36-51
- **Keyboard**: Full pass-through with pitch bend and mod wheel

## Installation

```bash
./deploy.sh
```

This copies the Remote files to:
- `~/Library/Application Support/Propellerhead Software/Remote/Codecs/Lua Codecs/Akai/`
- `~/Library/Application Support/Propellerhead Software/Remote/Maps/Akai/`

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

## Project Structure

```
mk4/
├── reason_remote/      # Reason Remote files (deployed)
│   ├── MPK mini IV.lua
│   ├── MPK mini IV.luacodec
│   └── MPK_mini_IV.remotemap
├── tools/              # Development utilities
│   ├── midi_listener.py
│   ├── generate_reason_preset.py
│   └── ...
├── docs/               # Documentation
│   ├── MPK_MINI_IV_MIDI_SPEC.md
│   └── SESSION_NOTES.md
├── openspec/           # Change management
├── deploy.sh           # Installation script
└── README.md
```

## Development

### Requirements

- Python 3.x with `mido` package
- Close Reason before running MIDI scripts (port conflicts)

### Testing MIDI

```bash
source .venv/bin/activate
python tools/midi_listener.py
```

### Regenerating Preset SysEx

```bash
python tools/generate_reason_preset.py
```

## Control Mapping

| Control | Function | MIDI |
|---------|----------|------|
| Play/Stop | Toggle playback | CC 76 |
| Record | Record / Quantize (SHIFT) | CC 77 |
| Loop | Loop on/off | CC 74 |
| Fast Forward | Forward | CC 78 |
| Undo | Undo / Redo (SHIFT) | CC 73 |
| Tap Tempo | Tap tempo / Click (SHIFT) | CC 11 |
| SHIFT | Modifier | CC 17 |
| Knobs 1-8 | Parameters | CC 24-31 |
| Pads 1-16 | Notes 36-51 (Preset 2) | Ch 10 |

## License

MIT
