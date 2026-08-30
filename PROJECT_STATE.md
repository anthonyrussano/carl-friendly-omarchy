# Project State

Last updated: 2026-08-30

## Stage

Functional beta installed; parent credential completion and supervised child usability testing are next.

## Machine baseline

- Omarchy: `4.0.1-1`
- Active theme: `Little O`
- Font: `JetBrainsMono Nerd Font`
- Browser/file manager found: Chromium and Nautilus
- Educational applications installed: GCompris 26.1; Amberol is also available though the child Music tile uses the smaller bundled player.
- User-installed Omarchy shell plugin: `little-o.home`.
- Live Hyprland session confirmed at 1920×1080.
- Child bar contains only Home, clock, and audio. Screensaver is 900 seconds; lock remains effectively disabled until separate parent/child accounts are designed.

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
- Verified Hermes Agent `0.20.6`. It is configured for Anthropic `claude-sonnet-5`, but `hermes doctor` reports the stored Anthropic API credential as invalid. Re-authentication through `hermes model` is still required.

## Production-hardening update — 2026-08-30

- Built the OmaBook `main-with-ai-features` branch locally with foliate-js and imported a public-domain *Tale of Peter Rabbit* EPUB into its owner-only library database.
- Ran the full OmaBook suite: 178 passed, zero failed, one optional fixture skipped.
- Installed GCompris and configured Letters to open `click_on_letter` and Numbers to open `learn_digits`, fullscreen with difficulty 1–2, sound enabled, kiosk disabled, and network downloads disabled.
- Added an offline local drawing canvas and music player. Drawing downloads default to `~/Pictures/Carl`; content folders exist under `~/Books/Carl`, `~/Music/Carl`, and `~/Pictures/Carl`.
- Fixed activity lifecycle: the child overlay dismisses before launching, and the launcher summons Home when an activity exits.
- Built Hermes Desktop. Installed and verified Faster Whisper with its local `tiny` model, microphone access, and Edge TTS; the synthesized phrase “Hi Carl. Your helper voice is ready.” round-tripped through speech recognition exactly.
- Added a Carl-aware Hermes persona: short spoken guidance for Carl, adult-level responses for Anthony, and explicit confirmation for purchases, disclosure, deletion, external contact, or security changes.
- Added idempotent install, OmaBook update, consolidated privileged setup, diagnostic, and recoverable uninstall commands plus dependency/testing documentation and an MIT license.
- Current `bin/doctor` result: zero failures and one warning. The warning clears after `bin/finish-system-setup` installs Speech Dispatcher.

## Next recommended session

Run the first supervised usability pass:

1. Complete the already-open **Little O — Finish Setup** terminal password prompt, or later run `bin/finish-system-setup`.
2. Run `hermes model`, choose Anthropic, authenticate, and keep Claude Sonnet selected.
3. Ask Carl to launch all six tiles and return Home; note misses, hesitations, accidental launches, and whether he recognizes the pictures.
4. Add DRM-free books to `~/Books/Carl` and music to `~/Music/Carl`, then import the book folder in OmaBook.
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
