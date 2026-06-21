# EMU source-folder index

Maps a short **repo/vehicle name** to its EMU Black source folder on disk, so that
naming a repo in chat resolves to a concrete path without re-discovering it.

## Base

```
BASE = C:\Users\WTCra\OneDrive\Documents
```

The canonical tree is `BASE\EMU_BLACK_V3\<reponame>`. A few vehicles also have an
older `BASE\EMU_BLACK\<reponame>` (V1) folder — listed where it exists.

Rule of thumb: **referring to a repo name = referring to `BASE\EMU_BLACK_V3\<reponame>`.**

## Index

| Name (say this in chat) | Vehicle / role | EMU_BLACK_V3 path | Older EMU_BLACK (V1) path |
|---|---|---|---|
| `supra` | MKIV Supra 2JZ-GTE (this repo: `emu-black-tuning-notes`) | `BASE\EMU_BLACK_V3\Supra` (+ `LogAutosave`) | `BASE\EMU_BLACK\Supra` |
| `bradley` | Bradley's 1JZ | `BASE\EMU_BLACK_V3\bradley` | `BASE\EMU_BLACK\bradley-1jz` |
| `land cruiser` / `fj80` | FJ80 Land Cruiser 1FZ-FE | `BASE\EMU_BLACK_V3\Land Cruiser` | — |
| `napier` / `gs300` | Napier GS300 | — | `BASE\EMU_BLACK\Napier_GS300` |
| `base maps` | ECUMaster base/reference maps | `BASE\EMU_BLACK_V3\Base maps` | — |
| `default` | EMU default project | `BASE\EMU_BLACK_V3\DEFAULT` | `BASE\EMU_BLACK\DEFAULT` |
| `firmware` | EMU firmware files | `BASE\EMU_BLACK_V3\FIRMWARE` | `BASE\EMU_BLACK\FIRMWARE` |
| `emub2` | EMU Black 2 projects | `BASE\EMU_BLACK_V3\EMUB2` | — |

## Notes

- Default to the **EMU_BLACK_V3** path; only use the V1 (`EMU_BLACK`) path when a file
  is missing from V3 or the user names the older project.
- For `supra`, canonical files are mirrored into this repo under `supra/tunes/` and
  `supra/exports/`; the OneDrive folder is the source for anything not already in-repo.
- Per global rules, OneDrive access is normal/local only for the `supra` folder
  (`EMU_BLACK_V3\Supra` + `LogAutosave`). For any other folder above, access only the
  specific file the user names — no broad traversal.
- `bradley` is a 1JZ: pull its files only from the two bradley folders above; do not
  load supra-specs for it.
