# MPK Mini IV Reason Remote

AKAI MPK Mini IV control surface integration for Reason Studios Reason DAW.

## Quick Reference

| Task | Command |
|------|---------|
| Deploy to Reason | `./deploy.sh` |
| Test MIDI input | `python tools/midi_listener.py` |
| Generate preset | `python tools/generate_reason_preset.py` |

## Key Files

- `reason_remote/MPK mini IV.lua` - Main Lua codec
- `docs/MPK_MINI_IV_MIDI_SPEC.md` - MIDI protocol documentation
- `docs/SESSION_NOTES.md` - Development session notes

## MIDI Testing

Always close Reason before running Python MIDI scripts (port conflicts).

```bash
source .venv/bin/activate
python tools/midi_listener.py
```

## SysEx Communication

Use **Software Port** for SysEx read/write operations:
- Read preset: `F0 47 00 5D 66 00 01 [preset] F7`
- Write preset: `F0 47 00 5D 67 [len_hi] [len_lo] [data] F7`

Pad notes are at offsets `81 + (i * 5)` in preset data.

<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->