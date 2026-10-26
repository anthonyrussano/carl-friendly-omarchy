# Carl-Friendly Omarchy

A parent-managed, child-friendly Omarchy desktop for Carl (age 3½), designed to make independent navigation easier while adding calm, playful learning experiences.

This repository is the project record and, later, the shareable implementation. It deliberately does **not** contain secrets, personal data, browser profiles, or a copy of the entire home configuration.

## Current status

The current beta is installed on the reference laptop. The active `Little O` theme and `little-o.home` plugin provide a full-screen six-tile child home, simplified bar, and a deliberate grown-up path back to stock Omarchy. Every activity opens full-screen on the dedicated child workspace and returns Home when it closes. The earlier Hermes voice-helper prototype has been removed from child mode after supervised use found it laggy and unreliable.

Start with:

- [`PLAN.md`](PLAN.md) — scope, phases, acceptance checks, and backlog
- [`PROJECT_STATE.md`](PROJECT_STATE.md) — the handoff point for future agent sessions
- [`docs/DESIGN.md`](docs/DESIGN.md) — child-centered interaction model
- [`docs/REPRODUCE.md`](docs/REPRODUCE.md) — complete clean-machine reproduction guide
- [`research/OMARCHY_ECOSYSTEM.md`](research/OMARCHY_ECOSYSTEM.md) — local inventory and community review
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to work safely and prepare this for community sharing

## Product principles

1. Carl sees a few large, recognizable choices; an adult can still reach the full desktop.
2. Favor pictures, color, and spoken feedback over reading, precision, or memorized shortcuts.
3. Never use shame, streak pressure, ads, purchases, or manipulative rewards.
4. Learning activities are short, forgiving, offline-first where practical, and easy to exit.
5. Parent controls, updates, terminal access, settings, deletion, and web access stay behind an adult gate.
6. All changes are reversible, versioned, and confined to user-owned paths.

## Intended architecture

The first release should be a thin, maintainable layer over Omarchy 4:

- a custom Quickshell menu/plugin for a six-tile child home screen;
- a custom theme under `~/.config/omarchy/themes/`;
- minimal overrides in `~/.config/omarchy/shell.json` and `~/.config/hypr/`;
- educational apps/content launched as ordinary applications;
- a parent mode that exposes maintenance and the normal Omarchy menu;
- an idempotent installer, backup, validator, and uninstaller in this repository.

Do not edit `/usr/share/omarchy/`. It is packaged, read-only project input and will be replaced by upgrades.

## Current controls

- Home bar button: reopen the child home.
- Arrow keys: move the selected activity.
- Enter or Space: open the selected activity.
- Escape: emergency keyboard path to the stock Omarchy menu.
- Hold **Hold for grown-ups** for 1.8 seconds: deliberate pointer/touch path to the stock menu.

The activity launcher is intentionally fixed-command routing rather than arbitrary menu shell strings:

- **Draw** opens the bundled touch/mouse drawing activity and saves PNG pictures locally.
- **Letters** opens GCompris's spoken letter-finding activity at preschool difficulty.
- **Numbers** opens GCompris's learn-digits activity at preschool difficulty.
- **Stories** opens the pinned, fully offline, non-AI OmaBook `v0.1.1` release.
- **Music** automatically lists and plays supported files from `~/Music/Carl` in a large local player.
- **My Things** opens a read-only, child-sized picture gallery for `~/Pictures/Carl`.

Closing an activity summons the Little O home again.

## Install and verify

From this repository:

```bash
bin/install --dry-run
bin/install
bin/install-omabook
bin/test
bin/doctor
```

`bin/install --dry-run` validates the source and previews the owned paths without changing files. `bin/install` is repeatable, preserves a first-install recovery baseline, and creates timestamped backups under `~/.local/state/little-o/backups/`. `bin/test` checks the source and local web activities; `bin/doctor` is read-only and checks the installed system without printing credentials.

The system-level setup uses one visible administrator prompt:

```bash
bin/finish-system-setup
```

That installs the host packages used by the shell, activities, and pinned reader. It has been completed on the reference laptop.

OmaBook is a Git submodule pinned to reviewed tag `v0.1.1` and commit `d03520444e8a03a4063183908c22816ce00f0d04`. To restore and reinstall that exact reader:

```bash
git submodule update --init vendor/omabook
bin/install-omabook
```

To remove Little O while preserving personal content:

```bash
bin/uninstall
```

## Recovery

If the prototype needs to be disabled from a terminal:

```bash
omarchy plugin disable little-o.home
omarchy theme set "Tokyo Night"
cp ~/.config/omarchy/shell.json.bak.little-o-20260830 ~/.config/omarchy/shell.json
omarchy restart shell
```

Source stays in this repository; installed copies live only in user-owned paths under `~/.config/omarchy/` and `~/.local/bin/`.

## Content folders

- Books: `~/Books/Carl` (DRM-free EPUB is preferred; PDF, MOBI, and AZW3 are supported by OmaBook.)
- Music: `~/Music/Carl`
- Pictures and saved drawings: `~/Pictures/Carl` and the browser's configured download directory.

The repository includes a small CC0 starter library: three original EPUB stories, three original instrumental melodies, and three original AI-assisted illustrations. `bin/install` seeds only missing files and never overwrites family content. The reference machine also has a private collection of public-domain children's books downloaded separately from Project Gutenberg; exact provenance is recorded in [docs/DEPENDENCIES.md](docs/DEPENDENCIES.md).

## AI helper status

No AI agent or model provider is part of the child experience. The Hermes integration was retired because the full voice loop was too slow and failure-prone in real use. Its small bridge and the criteria for any future experiment remain under [`research/hermes-prototype/`](research/hermes-prototype/), but the installer actively retires an older installed bridge. Provider selection is intentionally deferred until a provider-neutral interaction prototype can meet the reliability and latency bar without exposing it to Carl.

## Proposed name for the public project

Working title: **Little O**. Keep the repository name descriptive until the name and artwork are chosen.
