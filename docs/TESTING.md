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
- Hermes Desktop packages successfully for Linux.
- Hermes can see the system microphone through PipeWire.
- Local Faster Whisper transcribed a synthesized test phrase exactly.
- Edge TTS synthesized an MP3 using the configured voice.

Run `bin/doctor` for the current machine state.

## Manual checks still required

- Enter the administrator password in `bin/finish-system-setup`, then confirm OmaBook's **Read page** control produces audio.
- Re-authenticate Anthropic with `hermes model`, then start voice chat with the microphone button or `Ctrl+B` and confirm one complete spoken turn.
- Observe Carl launching and returning from each activity with his actual input device.
- Check saved drawing location and preferred music-file selection flow with Carl.
- Repeat after reboot and after an Omarchy upgrade.

## Acceptance rule

Do not call the helper fully operational merely because its window launches. A live voice turn requires all four stages to pass: microphone capture, transcription, Claude response, and spoken playback.
