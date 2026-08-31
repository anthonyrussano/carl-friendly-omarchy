# Verification record

Last run: 2026-08-30 on Omarchy 4.0.1-1, 1920×1080.

## Automated checks passed

- Little O shell plugin validates with the installed Omarchy schema.
- The Omarchy post-boot hook summons the child home after login.
- Launcher scripts pass Bash syntax checks.
- The local HTML activity pack loads in Chromium headless mode.
- OmaBook builds against Qt 6.11.2 and has no unresolved dynamic libraries.
- OmaBook imports the starter EPUB into its owner-only SQLite library.
- The upstream OmaBook test suite passes 178 tests with zero failures and one fixture-dependent skip.
- GCompris exposes both selected activities: `click_on_letter` and `learn_digits`.
- End-to-end keyboard test: Enter on the selected tile dismissed the Home layer and mapped the Draw window; closing Draw summoned Home again.
- Hermes Desktop packages successfully for Linux.
- Hermes can see the system microphone through PipeWire.
- Local Faster Whisper transcribed a synthesized test phrase exactly.
- Edge TTS synthesized an MP3 using the configured voice.
- Speech Dispatcher is installed and the packaged Hermes sandbox has the required root ownership and setuid mode.
- PipeWire detected `onn USB Microphone Mono` and selected it as the default input.
- The home surface now uses Wayland `Top`, leaving the higher Omarchy audio overlay as the exclusive pointer target.
- The launcher waits for the Hermes window, focuses it, and sends its documented `Ctrl+B` voice shortcut.

Run `bin/doctor` for the current machine state.

## Manual checks still required

- Confirm OmaBook's **Read page** control produces audio through the desired output.
- Renew Anthropic authentication, then use **Talk to Helper** and confirm one complete spoken turn without clicking Hermes's voice control.
- Open the audio panel, change between built-in and USB inputs, and confirm no click activates a Home control behind the panel.
- Observe Carl launching and returning from each activity with his actual input device.
- Check saved drawing location and preferred music-file selection flow with Carl.
- Repeat after reboot and after an Omarchy upgrade.

## Acceptance rule

Do not call the helper fully operational merely because its window launches. A live voice turn requires all four stages to pass: microphone capture, transcription, Claude response, and spoken playback.
