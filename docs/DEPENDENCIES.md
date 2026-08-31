# Dependencies and provenance

## Required runtime

| Component | Purpose | Source/license notes |
|---|---|---|
| Omarchy Shell / Quickshell | Child home and status bar | Provided by the host Omarchy system |
| Chromium | Bundled local Draw and Music activities | Host package; local `file:` content, no application telemetry |
| GCompris 26.1 | Letters and Numbers | Arch `extra/gcompris-qt`; GPL educational suite |
| Nautilus | My Things | Host file manager |
| PipeWire/WirePlumber (`wpctl`) | Audio routing and input selection | Host Omarchy audio stack |
| `wtype` and `hyprctl` | Focus Hermes and invoke voice in one action | Host Omarchy/Wayland tools |
| `speech-dispatcher` | Lightweight offline story narration | Arch package |

## Stories

OmaBook is installed from `newx/omabook`, branch `main-with-ai-features`, at reviewed revision `2caba05140af22f0684e1b746e0d4a71079259fe`, and built under `~/.local/share/little-o/omabook`. It is MIT-licensed. Its reader engine is `johnfactotum/foliate-js`, revision `78914aef4466eb960965702401634c2cb348e9b1`. The branch is experimental; `bin/update-omabook` makes updates explicit rather than unattended.

Read-aloud prefers OmaBook's local Kokoro service when separately enabled. The lighter default is Qt Speech with the Arch `speech-dispatcher` package. OmaBook questions/summaries require a separately supported AI configuration; they do not inherit Hermes credentials automatically.

The local starter book, *The Tale of Peter Rabbit* by Beatrix Potter, is downloaded separately to the private content directory from Project Gutenberg ebook 14838. Project Gutenberg identifies that edition as public domain in the United States. It is not committed or redistributed by this repository.

## Helper

Hermes Agent 0.20.6 is installed separately under `~/.hermes`. Little O does not vendor it. The desktop build supplies voice conversation, and this machine uses:

- local `faster-whisper` 1.2.1 with the `tiny` model for speech recognition;
- Edge TTS with `en-US-AriaNeural` for spoken replies;
- xAI OAuth with `grok-4.6` for reasoning.

Hermes data, conversations, credentials, and models remain outside this repository. `bin/uninstall` deliberately preserves them.

Voxtype is not installed on the reference machine. It is useful for general desktop dictation, but not required for Hermes voice conversation; running a second always-on recognizer adds memory/CPU use and microphone contention on this 2-core/4-thread laptop. Revisit it only if system-wide dictation becomes a separate requirement.
