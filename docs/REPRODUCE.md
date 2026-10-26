# Reproducing Little O

This guide recreates the reference implementation without copying personal data or credentials.

## Baseline and requirements

- Omarchy 4.0.6 or a compatible release with Omarchy Shell/Quickshell and Hyprland
- Arch packages/applications: Chromium, Python 3, GCompris Qt, PipeWire/WirePlumber, `jq`, Git, Make, a C/C++ toolchain, and the Qt 6/poppler libraries listed by `bin/finish-system-setup`
- Rough reference hardware: x86-64 Intel i3, 8 GiB RAM, integrated graphics.
- Network access during initial package installation and repository/submodule checkout; child activities and the reader work offline afterward.

## 1. Install the project shell

Clone this repository and its pinned reader submodule, then run:

```bash
git clone --recurse-submodules <repository-url> ~/Projects/carl-friendly-omarchy
cd ~/Projects/carl-friendly-omarchy
bin/install --dry-run
bin/finish-system-setup
bin/install
bin/install-omabook
```

The installer backs up targeted user configuration under `~/.local/state/little-o/backups/`, installs the user-owned theme and plugin, seeds missing starter content, configures the small child bar, and registers the login hook. It never edits `/usr/share/omarchy`.

## 2. Install educational applications and content

Install GCompris (`gcompris-qt`) and place child-owned content in:

- `~/Books/Carl` for DRM-free EPUB/PDF/MOBI/AZW3
- `~/Music/Carl` for audio
- `~/Pictures/Carl` for drawings and files

Letters uses GCompris `click_on_letter`; Numbers uses `learn_digits`, both at difficulty 1–2. Draw is a bundled local activity. Music and My Things use Python standard-library servers bound to localhost, with Chromium providing the large child interface; each server is restricted to its approved media folder.

For Stories, `bin/install-omabook` verifies, tests, builds, and locally installs the submodule's tagged non-AI `v0.1.1` release. Its foliate-js engine is already vendored at the revision recorded in `docs/DEPENDENCIES.md`.

## 3. Starter and family content

`bin/install` copies the repository's three CC0 books, three songs, and three pictures only when same-named files are absent. Re-running it never overwrites family content. Add more approved files directly to the three content folders; OmaBook requires the adult to import new book folders from its library screen.

No Hermes installation or AI/model credential is required. The retired experiment is documented under `research/hermes-prototype/` and is not installed.

## 4. Verify

```bash
cd ~/Projects/carl-friendly-omarchy
bin/install
bin/test
bin/doctor
```

Then perform a supervised manual pass:

1. Open the speaker panel, select each input, and verify the chosen source has `*` in `wpctl status`. Confirm no click reaches the home tiles behind the panel.
2. Launch and close all six activities; each should use workspace 10 and Home should return after it closes.
3. Confirm Music and My Things show the seeded starter media without allowing arbitrary file-system access.
4. Import `~/Books/Carl` in Stories, open a starter EPUB, turn pages, and return to the library.
5. Restart the session and confirm the child Home appears from the post-boot hook.

## 5. Update, recover, or share

- Redeploy safely with `bin/install`; each run creates a timestamped backup.
- Reinstall the repository-pinned OmaBook release with `bin/update-omabook`; changing the pin requires a reviewed main-repository commit.
- Recover with `bin/uninstall`; personal content and OmaBook data are preserved.
- Before publishing, exclude credentials, conversations, models, browser profiles, personal media, and child observations. Share source, reviewed dependency revisions, screenshots without personal data, test results, and reproducible issue reports.
