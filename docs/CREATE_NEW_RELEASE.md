# Creating a New Release

A release is identified by its version **`<major>.<minor>.<patch>`** (e.g. `0.1.1`). There is
**no build number**. The single source of truth is `pyproject.toml` `[project] version`. It holds
the **last shipped** version.

Each release bumps the last segment (`0.1.0` -> `0.1.1`). To start a new minor or major line,
set the version by hand after a release (e.g. `0.2.0`). The next release then ships `0.2.1`.

Current line: `0.3.x` (set to `0.3.0`, so the first release with this system ships `0.3.1`).
Older GitHub releases used `v`-prefixed tags (`v0.1`, `v0.2`). From `0.3.1` on, tags are the
plain version (`0.3.1`).

**Normally you run the one-command release in section 6.** Sections 1-4 describe the steps it
runs, so you can also do them by hand.

## 1. Version

```bat
tools\version_get.bat         :: prints the current version, e.g. 0.1.0
tools\version_increment.bat   :: bumps the last segment (0.1.0 -> 0.1.1) and prints it
tools\version_decrement.bat   :: rolls the last segment back by one (use after a failed build)
```

All three call `tools\release\version_number.py` (`get` / `increment` / `decrement`) via
`uv run`. It edits only the `[project]` `version` line and keeps the file's line endings.
`tests\unit\test_version_number.py` covers it.

## 2. Release notes folder + `en.json`

- Folder: `release_notes\<version>\`, named exactly after the **new** version (the one after
  `tools\version_increment.bat`). Example: releasing `0.1.1` -> `release_notes\0.1.1\en.json`.
- No release folders exist yet (`release_notes\.gitkeep` only keeps the folder in git). The first
  release creates the first one.
- Changes since the last release: the anchor is the last `RELEASE (tapo): <version>` commit or
  plain version tag (e.g. `0.3.1`). If there is none, use the newest `release_notes\` folder. For
  the first release (`0.3.1`), the anchor is the old tag `v0.2`.

Schema of `en.json` (UTF-8). The actual release text goes into the **`notes`** array, one
user-facing bullet per entry:

```json
{
  "version": "0.1.1",
  "date": "YYYY-MM-DD",
  "title": "Short headline",
  "notes": [
    "First user-facing change",
    "Second user-facing change"
  ]
}
```

- `version` must equal the folder name.
- `date` is the release date (ISO `YYYY-MM-DD`).

## 3. Translation: NONE (English only)

**This project is English only. Create only `en.json`.** Do not create or hand-author any other
locale file. There is no translator bat (`english_only`). If a translation step is added later,
it goes here and becomes mandatory.

## 4. Build the release

```bat
tools\version_increment.bat   :: 1. bump the version (prints the new label)
                              :: 2. write release_notes\<new version>\en.json (section 2)
tools\build_release.bat       :: 3. build dist\tapo.exe
```

If the build fails, roll back with `tools\version_decrement.bat`.

`tools\build_release.bat` runs PyInstaller through `uv run --with pyinstaller` and passes its
exit code through. The artifact is the single file **`dist\tapo.exe`**. `release_notes\` is
**bundled into the exe** (`--add-data "release_notes;release_notes"`). The notes therefore ship
inside the binary, not beside it. The build works on a dirty working tree.

There is no installer and no code signing.

Commit the release as `RELEASE (tapo): <version>` (version bump + release notes + `uv.lock`,
which records the project version). Tag it with the plain version and push. Then publish
`dist\tapo.exe` as a GitHub Release with that tag. The release body comes from `en.json`.

## 5. In-app release notes view

**None, deliberately.** `tapo` is a command-line tool with no UI. The release notes are bundled
into `tapo.exe` (section 4) but no command displays them. If a view is wanted later, add a CLI
subcommand that reads the bundled `release_notes\` (`sys._MEIPASS` when frozen). It must sort the
releases by numeric version segments (`0.1.10` after `0.1.9`) and show the newest first, with a
way to page to older releases.

## 6. One-command release (`tools\release_create.bat`)

```bat
tools\release_create.bat              :: full release
tools\release_create.bat --internal   :: internal test build (INTERNAL commit, no notes in the GitHub body)
tools\release_create.bat --dry-run    :: preview only, changes nothing
```

It runs `release-tool create` with **`tools\release_create.ini`** (`versioning = semver`,
`english_only = true`). Steps:

1. It prints the next label (`tools\version_get.bat` + 1).
2. If `release_notes\<label>\en.json` is missing, Codex authors it. Codex follows section 2 and
   `tools\CREATE_RELEASE_NOTES.md`.
3. It bumps the version. **`release-tool create` owns the bump** through
   `tools\version_increment.bat`. `tools\build_release.bat` does not bump.
4. It runs `tools\build_release.bat`. On failure it rolls back with `tools\version_decrement.bat`.
5. It writes the previous version to `tools\previous_version.txt` (gitignored). No publish bat
   uses it, because there is no FTP or store publish.
6. It asks **"Commit, tag and push <label>?"**, then commits `RELEASE (tapo): <label>`, tags
   `<label>` and pushes.
7. It asks **"Create GitHub Release <label>?"**. Then `gh release create` uploads
   `dist\tapo.exe` to `BenjaminKobjolke/TAPO-P100-Control`, with the `en.json` notes as the body.
   This needs `gh auth login` once.

The completed artifact is `dist\tapo.exe`. Its version is the `pyproject.toml` version at build
time, and later the git tag. No separate version record is written: the GitHub step runs in the
same `create` run, right after the build.

**Retry publishing without rebuilding or bumping**, e.g. after declining or a failed `gh` call
(the tag is already pushed):

```bat
gh release create <label> dist\tapo.exe --title <label> --notes-file <notes.md> --repo BenjaminKobjolke/TAPO-P100-Control
```

This only works while `dist\tapo.exe` is still the build of `<label>`. After any later build,
check out the tag and run `tools\build_release.bat` first. Do not run `tools\version_increment.bat`.

Machine paths: `tools\config.bat` (gitignored) sets `RELEASE_TOOL_DIR`. On a fresh clone, copy
`tools\config_example.bat` to `tools\config.bat` and adjust it. Without it the launcher exits 1
before doing anything.
