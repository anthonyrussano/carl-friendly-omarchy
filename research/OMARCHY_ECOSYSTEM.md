# Omarchy Ecosystem Review

Research date: 2026-08-30. Community registries change quickly; re-check them before selecting dependencies.

## Installed platform

This machine runs Omarchy `4.0.1-1` (Quattro generation). Its shell is a long-running Quickshell process. User plugins live under `~/.config/omarchy/plugins/`, menu extensions under `~/.config/omarchy/extensions/omarchy-menu.jsonc`, theme overrides under `~/.config/omarchy/themes/`, and shell layout in `~/.config/omarchy/shell.json`.

There are no user-installed shell plugins. The system currently discovers 37 first-party plugins. The child design can reuse the core bar/menu, audio, notifications, OSD, lock, idle, background, and media capabilities while hiding developer-oriented widgets in child mode.

## Community landscape reviewed

- The official [Shell Plugins manual](https://omarchy.org/manual/shell-plugins/) documents install, clone, validation, namespacing, plugin kinds, and publishing. It explicitly warns that third-party plugins are unsandboxed code.
- The official [Omarchy plugin marketplace](https://plugins.omarchy.org/) is the publication target named by current documentation, though its browse response was empty during this review and should be checked again.
- [Omahub](https://omahub.dev/) is an active third-party registry with current plugin metadata and source links.
- The official [theme gallery](https://omarchy.org/themes/) and the community [awesome-omarchy list](https://github.com/Wheel-Smith/awesome-omarchy) are the primary visual research sources reviewed.
- The official [theming documentation](https://github.com/omacom/omarchy/blob/quattro/docs/theming.md) describes semantic colors, activation, user overrides, template generation, and theme-aware QML surfaces.
- The upstream [Omarchy repository](https://github.com/omacom/omarchy) and its local packaged source are authoritative implementation references.

“Any and all” cannot be treated as a fixed exhaustive set: these registries and GitHub repositories update continuously. The practical best practice is a reproducible dated inventory plus per-dependency review, not bulk installation.

## Potentially relevant community work

| Candidate | Possible value | Decision now |
|---|---|---|
| On-Screen Keyboard (Omahub) | Touch-friendly text entry | Evaluate source and touch behavior later; do not install yet |
| Dictionary (Omahub) | Future word exploration | Too reading-heavy for the first release; revisit later |
| Lock Screen Explorer (Omahub) | Visual references and lock variants | Research only; parent boundary needs more than a cosmetic lock |
| NES / Super Game Bro themes | Child-friendly visual inspiration | Inspiration only; avoid copying licensed game artwork |
| GCompris | Broad, established educational activities | Evaluate package, age fit, offline behavior, and exit controls |
| Tux Paint | Simple creative drawing | Strong candidate pending package/input test |

The registries currently emphasize productivity, system status, media, networking, and cosmetics. That reinforces building a small child-focused plugin rather than composing many unrelated plugins.

## Implementation best practices

1. **Extend before forking.** Use menu JSONC for static adult/child entries. Create a new plugin for the visual child hub. Clone a first-party widget only when its behavior truly must change.
2. **Keep packaged files read-only.** Read `/usr/share/omarchy/` as the canonical example, but put every change in user-owned config.
3. **Namespace and validate.** Use an id such as `little-o.home`; keep `manifest.json` at repository root for a publishable plugin; run `omarchy plugin validate` before enablement.
4. **Audit third-party code.** Pin a reviewed tag/commit, inspect QML and executable calls, inventory dependencies/network use, verify the license, and update deliberately. Popularity is not a security review.
5. **Use semantic theme APIs.** Base QML colors, spacing, typography, and borders on Omarchy's theme primitives so the UI survives theme and platform changes.
6. **Make installation transactional.** Preflight version/dependencies, show a dry-run, back up targeted files, install atomically, validate, and roll back on failure.
7. **Separate policy from presentation.** A pretty launcher is not a sandbox. Use a separate non-admin child account, application allowlisting, browser policy, and file permissions if restrictions matter.
8. **Test upgrades.** Maintain a small compatibility matrix and smoke-test against supported Omarchy releases; never promise compatibility with untested versions.
9. **Design for escape and failure.** Retain an adult shortcut, TTY recovery instructions, and a simple uninstall path if Quickshell fails.
10. **Publish clean components.** Avoid personal paths/data, declare artwork/audio licenses, provide screenshots and accessibility notes, and keep configuration examples generic.

## Current-system implications

- The current bar exposes agents, updates, networking, display, power, workspaces, and other developer/system concepts. Child mode should present far fewer controls.
- The current top bar clock uses a text-heavy weekday/time format. A child view could use a simple day-part illustration while parent mode keeps the precise clock.
- The current 150-second screensaver may interrupt exploratory play; tune only after observing sessions. The extremely long lock timeout also needs a deliberate parent decision.
- Chromium and Nautilus are present. Neither should be unrestricted child-home tiles in version 1.
- No live monitor information was available because the inspection shell was outside the Hyprland session.
