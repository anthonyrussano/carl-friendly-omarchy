# Project State

Last updated: 2026-10-26

## Stage

Functional, offline-first beta installed. The AI helper is intentionally out of child mode; supervised child usability testing is next.

## Machine baseline

- Omarchy: `4.0.6-1`
- Hyprland: `0.56.2`
- Active theme: `Little O`
- Font: `JetBrainsMono Nerd Font`
- Activity runtimes: Chromium, Python 3, and GCompris 26.1.
- Stories reader: OmaBook non-AI `v0.1.1`, pinned as a Git submodule at `d03520444e8a03a4063183908c22816ce00f0d04`.
- User-installed Omarchy shell plugin: `little-o.home`.
- Live Hyprland session confirmed at 1920×1080.
- Child bar contains Home, clock, Bluetooth, and audio. Screensaver is 900 seconds; lock remains effectively disabled until separate parent/child accounts are designed.
- The default pointer uses the existing cursor theme at 64 px (up from 24 px) for improved visibility.
- A Bose Color II SoundLink is paired, trusted, connected, and configured as the default audio output.
- The private OmaBook library contains 13 public-domain children's books with extracted covers.
- Hardware: Intel Core i3-1115G4 (2 cores/4 threads), 7.5 GiB RAM and 14 GiB swap.

## Work completed

- Inspected the current user Omarchy and Hyprland configuration read-only.
- Inventoried 37 first-party shell plugins and current enablement.
- Reviewed official shell plugin and theme mechanisms plus current community registries.
- Defined version 1 scope, architecture, milestones, validation gates, and release approach.
- Created this project folder without changing live configuration during the initial discovery pass.

## Implementation update — 2026-08-30

- Selected the bold Playroom Shelf visual direction after the generated options were not visible in the user's client.
- Created and activated the user-owned `Little O` Omarchy theme.
- Created, validated, installed, and enabled the `little-o.home` shell plugin.
- Added six original activity assets, a responsive two-by-three home grid, keyboard navigation, a large Hermes helper action, audio access, and a grown-up exit to the stock Omarchy menu.
- Simplified the child bar to Home, time, and audio. Backup: `~/.config/omarchy/shell.json.bak.little-o-20260830`.
- Added `~/.local/bin/little-o-launch` with fixed activity routing. Tux Paint/GCompris launch automatically when installed; unfinished activities show a gentle notification.
- Captured and visually compared the live 1920×1080 implementation. See `design-qa.md`; final result passed.
- Verified Hermes Agent `0.20.6`; at the time, its xAI OAuth credential was active. This prototype was later retired from child mode.

## Production-hardening update — 2026-08-30

- Built the OmaBook `main-with-ai-features` branch locally with foliate-js and imported a public-domain *Tale of Peter Rabbit* EPUB into its owner-only library database.
- Ran the full OmaBook suite: 178 passed, zero failed, one optional fixture skipped.
- Installed GCompris and configured Letters to open `click_on_letter` and Numbers to open `learn_digits`, fullscreen with difficulty 1–2, sound enabled, kiosk disabled, and network downloads disabled.
- Added an offline local drawing canvas and music player. Drawing downloads default to `~/Pictures/Carl`; content folders exist under `~/Books/Carl`, `~/Music/Carl`, and `~/Pictures/Carl`.
- Fixed activity lifecycle: the child overlay dismisses before launching, and the launcher summons Home when an activity exits.
- Built Hermes Desktop. Installed and verified Faster Whisper with its local `tiny` model, microphone access, and Edge TTS; the synthesized phrase “Hi Carl. Your helper voice is ready.” round-tripped through speech recognition exactly.
- Added a Carl-aware Hermes persona: short spoken guidance for Carl, adult-level responses for Anthony, and explicit confirmation for purchases, disclosure, deletion, external contact, or security changes.
- Added idempotent install, OmaBook update, consolidated privileged setup, diagnostic, and recoverable uninstall commands plus dependency/testing documentation and an MIT license.
- Verified the complete shell lifecycle with synthetic keyboard input: launch dismisses the overlay, the activity maps, and closing it automatically restores Home. A post-boot Omarchy hook summons Home after login.
- Completed `bin/finish-system-setup`: Speech Dispatcher is installed and Hermes Electron sandbox ownership/mode are correct (`root:root`, `4755`).
- Diagnosed the USB microphone: PipeWire sees `onn USB Microphone Mono` and has it selected as the default input. Omarchy's stock audio plugin already supports input switching.
- Fixed pointer click-through by moving the full-screen child home from the Wayland `Overlay` layer to `Top`; Omarchy overlay panels such as audio now own input while open.
- Changed Talk to Helper into a one-action flow: it waits for the Hermes window, focuses it, sends Hermes's `Ctrl+B` voice shortcut, and returns Home when Hermes closes.
- Extended `bin/doctor` to report the default microphone, required one-tap voice tooling, active Grok model, and xAI OAuth state without exposing secrets.

## Accessibility and Bluetooth update — 2026-09-20

- Increased the default pointer from 24 px to 64 px without changing its theme. Persistent `XCURSOR_SIZE` and `HYPRCURSOR_SIZE` overrides were added to `~/.config/hypr/hyprland.lua`, and the GTK cursor-size setting was changed to 64.
- Applied the pointer size immediately to Hyprland and the current D-Bus/systemd user environment. `hyprctl reload` completed successfully and `hyprctl configerrors` returned no errors.
- Added the built-in `omarchy.bluetooth` widget beside `omarchy.audio` on the child bar so Bluetooth devices can be managed without a terminal.
- Paired, bonded, trusted, and connected the Bose Color II SoundLink. The speaker reported a full battery during setup.
- Set the Bose speaker as the default PipeWire/PulseAudio output and confirmed the running GCompris audio streams were routed to it.
- Created recoverable configuration backups at `~/.config/hypr/hyprland.lua.bak.cursor-size-24` and `~/.config/omarchy/shell.json.bak.bluetooth-menu`.

## Children's library expansion — 2026-09-20

- Downloaded 12 image-inclusive EPUB3 editions from Project Gutenberg into the private `~/Books/Carl` content folder: *A Little Princess*, *Alice's Adventures in Wonderland*, *Just So Stories*, *Peter Pan*, *The Adventures of Pinocchio*, *The Jungle Book*, *The Railway Children*, *The Secret Garden*, *The Velveteen Rabbit*, *The Wind in the Willows*, *The Wonderful Wizard of Oz*, and *Winnie-the-Pooh*.
- Verified on each Project Gutenberg catalog page that the selected edition is public domain in the United States. Exact provenance is recorded in `docs/DEPENDENCIES.md`; the EPUB files remain outside this repository.
- Validated every downloaded EPUB as a readable ZIP archive before moving it into the content folder.
- Backed up the reader database to `~/.local/share/omabook/omabook.db.bak.books-20260920`, then imported the folder through OmaBook's own import pipeline.
- Verified a healthy SQLite database with 13 books, 13 unique file hashes, 13 extracted covers, and no EPUB files left unimported.

## UX, media, and offline-reader update — 2026-10-26

- Moved the approved six-tile catalog into validated `activities.json`; pointer hover, keyboard selection, focus rings, and accessible names now agree.
- Replaced the one-click adult exit with a visible 1.8-second hold while retaining Escape and terminal recovery for adults.
- Routed child activities to workspace 10 so a terminal or maintenance window cannot tile beside an activity.
- Replaced the file-manager and manual music-picker flows with large local Music and read-only My Things surfaces restricted to `~/Music/Carl` and `~/Pictures/Carl`.
- Added a repeatable project test command, non-mutating installer dry run, persistent first-install recovery baseline, installed-source drift checks, and shell restart/recovery hardening.
- Added a CC0 starter library of three original EPUB stories, three original instrumental WAV files, and three original AI-assisted illustrations. Installation seeds missing content without overwriting family files.
- Added OmaBook as a Git submodule pinned to its tagged, offline, explicitly non-AI `v0.1.1` release. The reader vendors its reviewed foliate-js engine.
- Removed **Talk to Helper** from Home and removed Hermes from installation and health requirements after supervised use found the interaction laggy and unreliable. The old bridge is retained only as inactive research with measurable criteria for any future experiment.
- Captured a fresh live 1920×1080 product audit covering Home, Draw, Music, and My Things. Private media names and conversation captures remain ignored outside Git.

## Next recommended session

Run the first supervised usability pass:

1. After the next login or reboot, verify that the 64 px pointer, Bluetooth bar widget, and Bose default output are retained.
2. Ask Carl to launch all six tiles and return Home; note misses, hesitations, accidental launches, and whether he recognizes the pictures.
3. Confirm that the starter songs and pictures make Music and My Things immediately understandable without coaching.
4. Open each starter EPUB in the pinned OmaBook reader and observe page-turn and return-to-library behavior.
5. Confirm inactivity behavior and plan the `anthony` administrator account migration.

## Guardrails for future agents

- Read the current Omarchy customization instructions before touching config.
- Never modify `/usr/share/omarchy/`; it is reference material only.
- Do not install or enable third-party plugin code without source review and parent approval.
- Use new/namespaced user-owned plugin and theme directories.
- Back up targeted files before modifying them and keep uninstall behavior current.
- After Hyprland Lua edits, run `hyprctl reload` and `hyprctl configerrors` in the live session.
- Run `omarchy plugin validate` on plugin folders before enablement.
- Keep child observations anonymous in anything published.
- Update this file at the end of every implementation session.

## Definition of done for the whole project

The acceptance checkpoints in all six phases pass, the parent can recover or uninstall without specialist knowledge, no child data is exposed, and the reusable pieces are documented under a clear open-source license.
