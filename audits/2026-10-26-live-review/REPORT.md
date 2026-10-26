# Little O live product audit — 2026-10-26

## Scope and target

This audit reviewed the installed 1920×1080 child journey from Home into all six approved activities and back, plus the adult escape and the retired voice-helper path. The goal is independent preschool use with large targets, stable navigation, forgiving recovery, offline content, and no destructive or open-ended system surface. Accessibility was assessed for keyboard reachability, visible focus, semantic names in source, readable sizing, reduced-motion handling, and non-color cues; this is not a WCAG conformance claim.

Evidence combines current-session screen captures, source inspection, Hyprland window/workspace state, restricted-server probes, headless Chromium startup, the project suite, the OmaBook upstream suite, and the installed-system diagnostic. No child observation, assistive-technology tree capture, touch-device pass, 100–200% scale matrix, sleep/wake cycle, or reboot was completed in this run.

## Outcome

No release-blocking problem remains in the six-tile shell. The highest-risk child flow—the laggy Hermes voice helper—was removed from the installed experience. Home is calmer, the adult exit resists accidental taps, activities no longer tile beside maintenance windows, Music and My Things expose only their approved folders, and clean installs start with useful media.

The main remaining product risk is Stories: pinned non-AI OmaBook is healthy and offline, but its full library interface is denser than the other child surfaces and includes adult-oriented search, taxonomy, import, and confirmed-remove controls.

## Journey health

1. **Enter Home — healthy.** Six large, consistently labeled tiles fit without scrolling. Pointer hover and keyboard selection now agree, focus is visible, and Home/sound have semantic names. Compare [before](01-home-before.png) with the [current Home](02-home-after.png).
2. **Draw and return — healthy.** Draw opens alone on workspace 10, uses large labeled controls, saves to `~/Pictures/Carl`, and returns Home when closed. See [Draw](05-draw.png).
3. **Letters and Numbers — healthy with evidence limits.** Both fixed routes exist in GCompris at difficulty 1–2 and launch checks pass. Their full child comprehension was not observed in this run.
4. **Stories — usable, child simplification recommended.** The pinned non-AI OmaBook `v0.1.1` passed 114 tests, launched offline, and retained the 13-book library. The screen is visually dense and offers controls beyond a preschooler's primary task; consider a read-only child shelf or direct-book launcher in a later iteration. See [Stories](06-stories-offline.png).
5. **Music — healthy.** The restricted localhost player found all 10 current tracks, supports range requests, and provides large play/pause and track controls. The live capture is kept private because it displays family media names.
6. **My Things — healthy.** The gallery is read-only, recursively constrained to `~/Pictures/Carl`, keyboard reachable, and now opens with three original starter pictures. See the [empty-state evidence](04-my-things-empty.png) and [seeded gallery](04-my-things-starter.png).
7. **Return and adult escape — healthy for the stated boundary.** Closing an activity returns Home. The visible adult action now requires a 1.8-second hold with progress; Escape and terminal recovery remain available. This is intentional friction, not a security boundary.
8. **AI helper — removed.** Hermes is no longer shown, installed, or required. The previous bridge is archived only as research, with a measurable latency/reliability bar before any adult-launched future experiment.

## Improvements implemented from the audit

- Declarative, validated `activities.json` catalog with safe fallback and duplicate-id rejection.
- Pointer/keyboard state alignment, focus rings, larger adult label, accessible button names, and keyboard activation.
- Dedicated child workspace and automatic return Home lifecycle.
- Large read-only picture gallery and local music library restricted to approved folders.
- Improved Draw controls, focus styles, status feedback, download location, and reduced-motion behavior.
- Persistent recovery baseline, recoverable legacy-helper retirement, installer dry run, source/runtime tests, drift checks, and shell-restart hardening.
- Pinned offline non-AI OmaBook submodule and CC0 starter library: three EPUBs, three songs, and three pictures.

## Next evidence to collect

The next release decision should be based on a supervised session in which Carl launches every tile, returns after a wrong choice, chooses a starter song/picture, opens a book, and uses the adult control accidentally or intentionally. Record only anonymous task outcomes: misses, hesitations, recoveries, and coaching needed.
