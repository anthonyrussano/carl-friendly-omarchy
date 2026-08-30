# Parent operations

## Daily use

The Home icon in the top bar summons Carl's activity screen. Closing an activity returns there automatically. **Grown-ups** opens the stock Omarchy menu.

Hermes voice chat starts from the microphone control in its composer or with `Ctrl+B`. Say “stop” to end a voice conversation.

## Add content

- Copy DRM-free EPUB/PDF/MOBI/AZW3 files to `~/Books/Carl`, open **Stories**, choose Import, and select that folder. Re-importing is safe and does not duplicate unchanged books.
- Copy audio files to `~/Music/Carl`. In **Music**, choose **Choose Songs** and select the desired files.
- Saved drawings and Carl's files belong in `~/Pictures/Carl`.

## Health check

```bash
cd ~/Projects/carl-friendly-omarchy
bin/doctor
```

The diagnostic does not print API keys. A healthy credential-independent installation reports zero failures. Provider connectivity is checked separately with `hermes doctor`.

## Credential and system completion

```bash
cd ~/Projects/carl-friendly-omarchy
bin/finish-system-setup
hermes model
```

The first command needs Anthony's administrator password. The second needs a valid Anthropic credential. Do not put either password or token in this repository.

## Update

Run `bin/update-omabook` only when ready to test upstream changes; the AI branch is experimental. Then run its upstream tests and `bin/doctor`. Little O itself can be redeployed repeatably with `bin/install`.

## Recovery

If only the home overlay is troublesome, open a terminal and run:

```bash
omarchy plugin disable little-o.home
omarchy restart shell
```

For a recoverable removal of the complete Little O shell/theme layer:

```bash
cd ~/Projects/carl-friendly-omarchy
bin/uninstall
```

The uninstaller moves installed files into `~/.local/state/little-o/removed/` and preserves books, music, pictures, OmaBook data, and Hermes data.
