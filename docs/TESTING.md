# Verification record

Last run: 2026-10-26 on Omarchy 4.0.6-1, Hyprland 0.56.2, 1920×1080.

## Automated checks passed

- Little O shell plugin validates with the installed Omarchy schema.
- The Omarchy post-boot hook summons the child home after login.
- Launcher scripts pass Bash syntax checks.
- The local HTML activity pack loads in Chromium headless mode.
- Pinned non-AI OmaBook `v0.1.1` builds against the installed Qt and has no unresolved dynamic libraries.
- OmaBook imported all 13 local EPUBs into its owner-only SQLite library with 13 unique file hashes and 13 extracted covers.
- Every downloaded EPUB passed an archive integrity test, every source file appears in the library, and SQLite reports `integrity_check: ok`.
- The pinned upstream OmaBook test suite passes 114 tests with zero failures and one optional local-fixture skip.
- GCompris exposes both selected activities: `click_on_letter` and `learn_digits`.
- End-to-end keyboard test: Enter on the selected tile dismissed the Home layer and mapped the Draw window; closing Draw summoned Home again.
- PipeWire detected `onn USB Microphone Mono` and selected it as the default input.
- The home surface now uses Wayland `Top`, leaving the higher Omarchy audio overlay as the exclusive pointer target.
- All six child routes use the dedicated workspace; Music and My Things start from their restricted localhost servers.
- The project test validates the data-driven activity catalog, source syntax, plugin schema, local web activities, starter EPUB/WAV integrity, non-AI reader pin, and installer dry run.
- The starter collection installs without overwriting same-named content.
- The Hermes helper action and bridge are absent from the installed child experience.

Run `bin/doctor` for the current machine state.

## Manual checks still required

- Import the three starter EPUBs into the newly pinned reader and verify page turns and the return-to-library flow.
- Open the audio panel, change between built-in and USB inputs, and confirm no click activates a Home control behind the panel.
- Observe Carl launching and returning from each activity with his actual input device.
- Check the saved drawing location and the automatic starter music/picture flow with Carl.
- Repeat after reboot and after an Omarchy upgrade.

## Acceptance rule

Do not call a flow child-ready merely because it launches. It must return Home reliably, expose no unintended files or controls, and work in repeated supervised use without adult recovery. Any future AI assistant remains out of child mode until it meets the separate acceptance bar in `research/hermes-prototype/README.md`.
