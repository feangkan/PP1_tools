# Stigmergy toolkit — version archive (V1, V2, V3…)

**Never overwrite an old folder.** Each push that changes the generator adds the next `Vn/` snapshot. The live working copy stays in the parent folder (`../stigmergy-generator.py` etc.).

| Folder | Generator label | What changed |
|---|---|---|
| **V1** | v0.5 radial ring | Clock layout, fan spokes, thick pipes + text seats |
| **V2** | v0.6 nerve layout | Horizontal hubs, no galaxy ring, organic tips |
| **V3** | v0.7 mycelial mesh | Cross-links, junctions, capillaries |
| **V4** | v0.8 fast + animated | Fast centerlines, batched animation, deferred pipes |
| **V5** | v0.8.1 scrollable UI | Scroll settings; Generate always visible |
| **V6** | v0.9 nerve sub-links | Branches grow toward other groups; organic sub-links |
| **V7** | v1.0 clean + Futura | pic-2 defaults; catalog text; text legend (Gold / Green words) |
| **V8** | v1.1 pathway + circles | Victoria flowchart on gold trunk; colour-circle legend |
| **V9** | v1.2 own graphic language | stages only where they exist; cycle / loop / instrument / fork / split / contest / overlap |
| **V10** | v1.3 dense line linkages | highway bundles are stigmergy curves, not pipe polysurfaces |
| **V11** | v1.4 text on nodes | Futura labels middle-centered on each disc |
| **V12** | v1.5 text colour + mm | Legend black; colour chip per type; millimetre default (print-pt option still in the GUI) |
| **V13** | v1.6 millimetres only | **Latest** — GUI numbers are mm; print-pt option removed |

See [`VERSION-MANIFEST.md`](VERSION-MANIFEST.md) for git commits and dates.

## Local copy on Windows (`D:\Claude code`)

Run from PowerShell (once per machine):

```powershell
cd "D:\Claude code"
git clone https://github.com/feangkan/PP1_tools.git
.\PP1_tools\scripts\sync-claude-code-local.ps1
```

After each `git pull`, run the script again — it copies **only new** `Vn` folders into `D:\Claude code\PP1_stigmergy\Vn\` without touching older versions.

**Use a version:** open `D:\Claude code\PP1_stigmergy\V5\stigmergy-generator-V5.py` in Rhino (each folder has `stigmergy-generator-Vn.py`).

## For agents (next push)

1. Bump `LATEST.txt` (e.g. `13` → `14`).
2. Copy the four stigmergy files into `versions/V14/`.
3. Add a row to `VERSION-MANIFEST.md`.
4. Commit, push, remind user to run `sync-claude-code-local.ps1` locally.
