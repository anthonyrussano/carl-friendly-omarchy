# Build Plan

## Outcome

Carl can log in and independently choose a small set of safe activities from a large, visual home screen. An adult can quickly switch to parent mode, maintain the machine, change the approved activity set, and restore stock Omarchy behavior.

## Scope for version 1

### Child mode

- Six large home tiles: **Draw**, **Letters**, **Numbers**, **Stories**, **Music**, and **My Things**.
- Persistent picture-based Home and Back actions with generous click/touch targets.
- One activity per workspace; suppress distracting system/developer widgets.
- Calm theme with high contrast, large type, consistent icons, and Carl-selected imagery.
- No terminal, package/update controls, power actions, arbitrary web browsing, or destructive file operations.
- Inactivity returns to the child home screen before the display sleeps.

### Parent mode

- Full Omarchy tools remain available after an adult-only gesture or credential-backed action.
- Approved activity/content list is data-driven rather than hard-coded into QML.
- Visible status for network, audio, battery, and updates only where the adult needs it.
- One-command backup/restore and an uninstall path.

### Learning layer

- Begin with four offline-first activity types: letter/sound matching, counting 1–10, shape/color matching, and free drawing.
- Sessions should take roughly 3–8 minutes and never punish exploratory input.
- Progress is local, minimal, exportable, and parent-readable. Track exposure and completion, not a score ranking.
- Content must be age-appropriate and usable without advertising, accounts, chat, or in-app purchases.

## Explicit non-goals for version 1

- A locked-down security boundary against a determined user.
- Replacing Hyprland, Omarchy Shell, or the whole login/session stack.
- Social features, surveillance, or detailed behavioral analytics. The parent-approved, supervised Hermes voice helper is an explicit exception to the original cloud/generative-chat non-goal.
- Installing a large collection of unreviewed themes/plugins.
- Building a full educational curriculum before navigation is validated with Carl.

## Delivery phases

### Phase 0 — Baseline and reversible scaffold

- [ ] Confirm display size, input devices, touch capability, audio, and whether Carl has a separate Linux account.
- [ ] Capture screenshots/video of the current flow and record Carl's successful and failed navigation attempts.
- [x] Add an installer that backs up only files it owns or patches.
- [x] Add `doctor`, install, update, and recoverable `uninstall` commands. (`install --dry-run` remains a release-hardening item.)
- [x] Record current Omarchy version and validate the live plugin on install.

Checkpoint: dry-run reports exact proposed changes; uninstall restores the captured baseline.

### Phase 1 — Paper prototype and interaction test

- [x] Create three visual directions; Anthony selected the visible Playroom Shelf direction when client options were unavailable.
- [x] Test a six-tile home screen as a static prototype and live 1920×1080 implementation.
- [ ] Observe whether Carl can launch, return Home, and recover from a wrong choice without coaching.
- [ ] Decide mouse/touch target minimums based on the actual display and input device.

Checkpoint: Carl completes 4 of 5 launch-and-return attempts without verbal navigation instructions on two occasions.

### Phase 2 — Minimal desktop shell

- [x] Create a namespaced plugin, `little-o.home`, with a valid `manifest.json`.
- [x] Keep the built-in Omarchy menu intact for parent mode.
- [ ] Build tiles from a declarative `activities.json` schema.
- [x] Simplify the bar for child mode and provide an obvious Home control.
- [ ] Add only necessary Hyprland overrides, preserving an emergency parent shortcut.
- [x] Validate the plugin with `omarchy plugin validate`; no Hyprland configuration override was needed.
- [x] Place Home on Wayland `Top` so Omarchy overlay panels receive pointer input without click-through.

Checkpoint: child and parent modes switch reliably; a broken plugin cannot strand the adult outside the normal desktop.

### Phase 3 — Theme and sensory polish

- [x] Create a new theme directory rather than modifying a stock theme.
- [x] Use semantic Omarchy colors for the theme and a consistent high-contrast QML palette.
- [x] Add original generated background and tile artwork.
- [ ] Test text/icon contrast, color-blind distinguishability, reduced motion, audio mute, and 100–200% display scaling.
- [ ] Ask Carl to choose between a small number of theme variants.

Checkpoint: all essential meaning survives without color or sound; labels remain legible at the machine's active scale.

### Phase 4 — Educational activities

- [x] Evaluate GCompris and purpose-built local activities against privacy, input, exit behavior, startup speed, and age fit.
- [x] Install GCompris and bundle the small Draw/Music fallback activity pack.
- [ ] Add optional spoken instructions recorded by a trusted adult or sourced under a compatible license.
- [ ] Store local progress in a documented, deletable format.

Checkpoint: every activity works offline after installation, exits back Home, and has no ads/purchases/chat.

### Phase 5 — Reliability and child testing

- [ ] Test reboot/login, sleep/wake, offline mode, audio failure, app crash, update, and low battery.
- [ ] Observe several short sessions; revise based on behavior rather than preference alone.
- [ ] Run a parent escape/recovery drill.
- [x] Record privacy, dependency, license, provenance, and third-party revision details for the current stack.
- [x] Add one-action Hermes voice startup and automated checks for microphone selection, STT dependencies, and provider authentication.

Checkpoint: five consecutive child sessions without adult recovery; parent recovery works after forced activity and shell crashes.

### Phase 6 — Community release

- [ ] Split reusable components if useful: shell plugin, theme, sample activity pack, and installer.
- [ ] Add screenshots, a short demo, supported Omarchy versions, license, security notes, and accessibility notes.
- [ ] Tag a release with checksums and a tested compatibility matrix.
- [ ] Submit the plugin to an active community registry and the theme to Omarchy's theme listing.
- [ ] Open upstream issues/PRs only for generally useful Omarchy improvements.

Checkpoint: a clean Omarchy test account can install, validate, use, and uninstall solely from the README.

## Backlog priorities

### Must

- Visual child home, reliable Home action, parent escape, approved activities, reversible install, offline operation.

### Should

- Spoken tile labels, on-screen keyboard where needed, usage time window, local progress summary, reduced-motion mode.

### Could

- Theme packs, printable activity cards, multiple child profiles, caregiver-recorded prompts, controller support.

### Won't yet

- Open-ended browser, online multiplayer, AI tutor, cloud sync, competitive leaderboards.

## Decisions still needed from the parent

1. Does Carl use a mouse, touchscreen, trackpad, keyboard, controller, or a combination?
2. Is `carl` a dedicated child account or also the administrator's account?
3. Which characters, animals, colors, songs, and current learning interests does Carl enjoy?
4. Should web content be completely absent, parent-launched only, or allowlisted in child mode?
5. What should happen after inactivity: return Home, dim, lock, or sleep?
