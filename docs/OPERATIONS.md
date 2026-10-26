# Parent operations

## Daily use

The Home icon in the left bar summons Carl's activity screen. Closing an activity returns there automatically. Hold **Hold for grown-ups** for 1.8 seconds to open the stock Omarchy menu; Escape remains the documented emergency keyboard path.

The speaker icon opens Omarchy's audio panel. Choose an item under **Input** to change microphones; `wpctl status` shows the selected source with `*`. The Little O home intentionally uses the Wayland `Top` layer so the audio overlay receives all clicks while open.

There is no AI helper in child mode. The previous Hermes prototype was retired after supervised use found it too slow and unreliable.

## Add content

- Copy DRM-free EPUB/PDF/MOBI/AZW3 files to `~/Books/Carl`, open **Stories**, choose Import, and select that folder. Re-importing is safe and does not duplicate unchanged books.
- Copy supported audio files to `~/Music/Carl`; **Music** scans that folder automatically.
- Saved drawings and pictures belong in `~/Pictures/Carl`; **My Things** shows them without rename, move, or delete controls.

## Health check

```bash
cd ~/Projects/carl-friendly-omarchy
bin/doctor
```

The diagnostic checks the deployed source, pinned offline reader, starter media, local activities, content folders, and active audio/theme state.

Before deploying source changes, run the non-mutating checks:

```bash
bin/test
bin/install --dry-run
```

## System completion

```bash
cd ~/Projects/carl-friendly-omarchy
bin/finish-system-setup
bin/install-omabook
```

The first command needs Anthony's administrator password to install host packages. The second tests and locally installs the exact OmaBook release pinned by the main repository; it needs no model, account, or credential.

## Update

`bin/update-omabook` intentionally reinstalls the current submodule pin. To adopt a later release, update `vendor/omabook` in a dedicated review, run its tests, verify that the selected branch is still non-AI/offline, commit the new gitlink in this repository, then run `bin/install-omabook` and `bin/doctor`. Little O itself can be redeployed repeatably with `bin/install`.

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

The uninstaller moves installed shell files into `~/.local/state/little-o/removed/` and preserves books, music, pictures, and OmaBook data.
