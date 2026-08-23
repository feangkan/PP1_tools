# Stigmergy toolkit — version archive (V1, V2, V3…)

**Never overwrite an old folder.** Each push that changes the generator adds the next `Vn/` snapshot. The live working copy stays in the parent folder (`../stigmergy-generator.py` etc.).

| Folder | Generator label | What changed |
|---|---|---|
| **V1** | v0.5 radial ring | Clock layout, fan spokes, thick pipes + text seats |
| **V2** | v0.6 nerve layout | Horizontal hubs, no galaxy ring, organic tips |
| **V3** | v0.7 mycelial mesh | Cross-links, junctions, capillaries |
| **V4** | v0.8 fast + animated | Fast centerlines, batched animation, deferred pipes |

See [`VERSION-MANIFEST.md`](VERSION-MANIFEST.md) for git commits and dates.

## Local copy on Windows (`D:\Claude code`)

Run from PowerShell (once per machine):

```powershell
cd "D:\Claude code"
git clone https://github.com/feangkan/PP1_tools.git
.\PP1_tools\scripts\sync-claude-code-local.ps1
```

After each `git pull`, run the script again — it copies **only new** `Vn` folders into `D:\Claude code\PP1_stigmergy\Vn\` without touching older versions.

**Use a version:** open `D:\Claude code\PP1_stigmergy\V4\stigmergy-generator.py` in Rhino (or whichever `Vn` you want).

## For agents (next push)

1. Bump `LATEST.txt` (e.g. `4` → `5`).
2. Copy the four stigmergy files into `versions/V5/`.
3. Add a row to `VERSION-MANIFEST.md`.
4. Commit, push, remind user to run `sync-claude-code-local.ps1` locally.
