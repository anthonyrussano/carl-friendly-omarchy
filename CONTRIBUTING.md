# Contributing

## Workflow

1. Read `PROJECT_STATE.md` and the relevant decision records.
2. Work on one checked phase item at a time.
3. Keep source and deployable templates in this repository; do not hand-edit packaged Omarchy files.
4. Record material choices in `docs/decisions/`.
5. Update the project state and acceptance evidence before ending a session.

## Required checks for implementation changes

- Shell plugin: `omarchy plugin validate <plugin-folder>`
- Hyprland Lua: `hyprctl reload` followed by `hyprctl configerrors`
- Installer: dry-run, clean install, repeated install, and uninstall/restore
- Theme: inspect child and parent modes at supported scales, with reduced motion and muted audio
- Activities: offline launch, Home/exit recovery, crash recovery, privacy and license review

## Privacy and safety

Do not commit Carl's surname, face, voice, birth date, location, usage logs, browser data, passwords, or unredacted system diagnostics. Publish anonymized observations only with parental approval. Do not add telemetry by default.

Third-party plugins execute unsandboxed. Every new external dependency needs its source URL, pinned revision/version, license, capabilities, network behavior, and review outcome recorded before installation.

## Community packaging

Use a standard open-source license after confirming the parent's preference. Keep code, theme, and optional content separable so licenses remain clear. A release should include:

- supported Omarchy versions;
- screenshots without personal data;
- installation, update, recovery, and uninstall instructions;
- dependency and permission explanations;
- accessibility and child-safety notes;
- artwork, font, sound, and content attributions;
- a changelog and signed/tagged version.

Submit the plugin to the currently active Omarchy registry and the theme to the official gallery following their current contribution instructions.
