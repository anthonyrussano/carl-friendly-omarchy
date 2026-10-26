# Child-Centered Design Direction

## Navigation model

Use a shallow hub-and-spoke design. The child home screen is the hub; every activity returns there through the same visible action. Avoid nested menus in child mode.

Suggested screen structure:

```text
┌─────────────────────────────────────────────────────────┐
│  Carl's Computer                         🔊      🏠      │
│                                                         │
│   🎨 Draw       🔤 Letters       🔢 Numbers             │
│                                                         │
│   📚 Stories    🎵 Music         ⭐ My Things           │
│                                                         │
│                 grown-up corner                         │
└─────────────────────────────────────────────────────────┘
```

Icons in the sketch are placeholders. Final tiles should use consistent original or properly licensed artwork, not a mixture of emoji styles.

## Interaction rules

- Make the entire tile interactive, with generous spacing and no tiny adjacent controls.
- Pair image, stable color, and a one- or two-word label; optionally speak the label on focus or first click.
- Prefer single click/tap. Avoid double-click, drag, hover-only controls, right-click, chords, and time-limited input.
- Provide immediate gentle feedback, but delay launching just enough to prevent accidental repeated opens.
- Make mistakes cheap: wrong choices should be reversible through a constant Home action.
- Use short transitions and provide a reduced-motion setting.
- Never encode success/failure through color or sound alone.

## Adult boundary

A hidden corner alone is discoverability friction, not security. Parent mode should combine an adult gesture with actual OS authentication for consequential settings. If `carl` is the administrator account, access controls will remain weak; a separate child account is the preferred architecture if meaningful restrictions are required.

The adult must always retain a documented keyboard escape and a recovery path from another TTY/session.

## Learning design

- Follow Carl's interests and rotate a small activity set rather than exposing a catalog.
- Use concrete matching and manipulation before abstract drills.
- Repeat concepts with varied examples; accept approximate motor input.
- Celebrate effort briefly, then return attention to the task.
- Let the parent see recently explored concepts without ranking Carl or creating streak anxiety.
- Favor co-play prompts that encourage talking with a caregiver.

## Candidate technical shape

`activities.json` describes each approved tile by stable id, short label, prompt, artwork, color, and fixed launcher action. QML validates and renders the catalog, so content changes do not require layout edits.

All child activities open on the same dedicated workspace, preventing terminals or maintenance windows from appearing beside them. The local Music and My Things surfaces expose only approved media folders, and My Things deliberately omits destructive file operations.

The visible adult affordance uses a 1.8-second hold with progress feedback. It reduces accidental exits but is not a security boundary; Escape and the documented terminal recovery path remain available to the adult.

Child mode deliberately has no open-ended AI action. The voice-agent prototype added too much latency and too many recoverable failure states for a preschool interaction. Stories use the pinned offline, non-AI OmaBook release, while a bundled starter library ensures Stories, Music, and My Things have understandable content on first use.

Child mode should hide unnecessary bar widgets rather than disabling essential background services. Parent mode should reuse stock Omarchy surfaces wherever possible so upgrades remain supportable.
