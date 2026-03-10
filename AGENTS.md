# AGENTS.md - DaPao Space Mouse

## Every Session
1. Read `SOUL.md`
2. Check `memory/` for recent context
3. Review current project state

## Memory
- Daily notes: `memory/YYYY-MM-DD.md`

## Project Structure
```
hardware/       — KiCad PCB project
case/           — 3D models (OpenSCAD/STL/STEP)
firmware/       — Mouse firmware (PlatformIO)
docs/           — BOM, assembly guide, wiring
```

## Workflow
- Feature branches, never push to main directly
- Version control all design files
- Keep a BOM (bill of materials) updated

## Safety
- No destructive commands without asking
- No ordering/purchasing without approval
- `trash` > `rm`
