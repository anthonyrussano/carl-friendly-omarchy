# Carl-Friendly Omarchy

A parent-managed, child-friendly Omarchy desktop for Carl (age 3½), designed to make independent navigation easier while adding calm, playful learning experiences.

This repository is the project record and, later, the shareable implementation. It deliberately does **not** contain secrets, personal data, browser profiles, or a copy of the entire home configuration.

## Current status

The first usable system is installed. The active `Little O` theme and `little-o.home` plugin provide a full-screen six-tile child home, simplified bar, large Hermes helper action, and a grown-up path back to stock Omarchy. Every activity tile now has a working launch target.

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
- Escape or **Grown-ups**: leave child home and open the stock Omarchy menu.
- **Talk to Helper**: open Hermes Desktop and automatically start a voice conversation.

The activity launcher is intentionally fixed-command routing rather than arbitrary menu shell strings:

- **Draw** opens the bundled touch/mouse drawing activity and saves PNG pictures locally.
- **Letters** opens GCompris's spoken letter-finding activity at preschool difficulty.
- **Numbers** opens GCompris's learn-digits activity at preschool difficulty.
- **Stories** opens the locally built OmaBook AI branch. `~/Books/Carl` contains a public-domain starter EPUB.
- **Music** opens the bundled music picker/player for files in `~/Music/Carl`.
- **My Things** opens `~/Pictures/Carl` in Nautilus.
- **Talk to Helper** opens the built Hermes Desktop, focuses it, and automatically invokes its `Ctrl+B` voice-conversation action. Local speech recognition, xAI Grok OAuth, and Edge speech output keep the laptop workflow simple.

Closing an activity summons the Little O home again.

## Install and verify

From this repository:

```bash
bin/install
bin/doctor
```

`bin/install` is repeatable and creates timestamped backups under `~/.local/state/little-o/backups/`. `bin/doctor` is read-only and reports missing components without printing credentials.

The system-level setup uses one visible administrator prompt:

```bash
bin/finish-system-setup
```

That installs the offline speech backend for OmaBook and gives Electron's sandbox helper its required root-owned permissions. It has been completed on the reference laptop; Talk to Helper retains an automatic `--no-sandbox` compatibility fallback for incomplete installations.

To refresh the experimental OmaBook branch and rebuild it:

```bash
bin/update-omabook
```

To remove Little O while preserving personal content and AI data:

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

The included *Tale of Peter Rabbit* test book comes from [Project Gutenberg](https://www.gutenberg.org/ebooks/14838), which marks it public domain in the United States. It is test content, not part of the distributable project source.

## AI provider

Hermes is configured for `xai-oauth` with `grok-4.6`; OAuth and local microphone/speech components pass the system check. Provider credentials live only under Hermes's private configuration and are never copied into this repository. Claude consumer credentials were deliberately not chosen for the third-party harness because Anthropic documents consumer-plan access and API/application access as separate products.

## Proposed name for the public project

Working title: **Little O**. Keep the repository name descriptive until the name and artwork are chosen.
