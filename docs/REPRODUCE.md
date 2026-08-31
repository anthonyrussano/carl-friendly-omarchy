# Reproducing Little O

This guide recreates the reference implementation without copying personal data or credentials.

## Baseline and requirements

- Omarchy 4.0.1 or a compatible release with Omarchy Shell/Quickshell and Hyprland
- Arch packages/applications: Chromium, Nautilus, GCompris Qt, `speech-dispatcher`, PipeWire/WirePlumber, `wtype`, `jq`, Git, Make, a C/C++ toolchain, Qt 6 development/runtime libraries, and Node/npm for the Hermes desktop build
- Rough reference hardware: x86-64 Intel i3, 8 GiB RAM, integrated graphics. Allow swap and use Faster Whisper `tiny` on low-end hardware.
- Network access during installation for packages, source checkouts, model download, Edge TTS, and the configured AI provider
- An xAI account authorized through Hermes's device OAuth flow. Never commit credentials.

## 1. Install the project shell

Clone/copy this repository to `~/Projects/carl-friendly-omarchy`, then run:

```bash
cd ~/Projects/carl-friendly-omarchy
bin/install
bin/finish-system-setup
```

The installer backs up targeted user configuration under `~/.local/state/little-o/backups/`, installs the user-owned theme and plugin, configures the small child bar, and registers the login hook. It never edits `/usr/share/omarchy`.

## 2. Install educational applications and content

Install GCompris (`gcompris-qt`) and place child-owned content in:

- `~/Books/Carl` for DRM-free EPUB/PDF/MOBI/AZW3
- `~/Music/Carl` for audio
- `~/Pictures/Carl` for drawings and files

Letters uses GCompris `click_on_letter`; Numbers uses `learn_digits`, both at difficulty 1–2. Draw and Music are bundled local Chromium activities.

For Stories, clone `https://github.com/newx/omabook` branch `main-with-ai-features` into `~/.local/share/little-o/omabook`, initialize/build its `foliate-js` dependency, then build OmaBook according to upstream instructions. The reviewed reference revisions are recorded in `docs/DEPENDENCIES.md`; `bin/update-omabook` performs the project's explicit update/build workflow.

## 3. Install and configure Hermes

Install Hermes Agent separately so `hermes` is on `PATH`, build/install its desktop application, then configure:

```text
model.provider = xai-oauth
model.default = grok-4.6
stt.enabled = true
stt.provider = local
stt.model = tiny
stt.language = en
tts.provider = edge
tts.voice = en-US-AriaNeural
voice.record_key = ctrl+b
voice.submit_mode = direct
voice.auto_tts = true
voice.client_direct = true
```

Install `faster-whisper` and `sounddevice` in Hermes's own virtual environment and let it download/warm the `tiny` model. Authenticate interactively:

```bash
hermes auth add xai-oauth
hermes doctor
```

Confirm that `hermes doctor` reports xAI OAuth logged in. Authentication failures are independent of microphone, STT, and TTS health.

Run `bin/finish-system-setup` after the desktop build so Electron's `chrome-sandbox` is owned by root with mode 4755. The launcher uses a compatibility fallback until that is true.

## 4. Verify

```bash
cd ~/Projects/carl-friendly-omarchy
bin/install
bin/doctor
```

Then perform a supervised manual pass:

1. Open the speaker panel, select each input, and verify the chosen source has `*` in `wpctl status`. Confirm no click reaches the home tiles behind the panel.
2. Select **Talk to Helper**. Hermes should open/focus and voice conversation should start without another click.
3. Speak a short phrase and confirm transcription, a Grok response, and spoken output.
4. Launch and close all six activities; Home should return after each closes.
5. Restart the session and confirm the child Home appears from the post-boot hook.

## 5. Update, recover, or share

- Redeploy safely with `bin/install`; each run creates a timestamped backup.
- Update OmaBook explicitly with `bin/update-omabook`, rerun upstream tests, then `bin/doctor`.
- Recover with `bin/uninstall`; personal content, Hermes data, and OmaBook data are preserved.
- Before publishing, exclude credentials, conversations, models, browser profiles, personal media, and child observations. Share source, reviewed dependency revisions, screenshots without personal data, test results, and reproducible issue reports.
