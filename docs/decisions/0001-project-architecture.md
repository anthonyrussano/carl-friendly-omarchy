# ADR 0001: Thin User-Owned Layer over Omarchy

Status: proposed

## Context

The desktop needs a radically simpler child experience without creating an unmaintainable fork or losing the adult's normal Omarchy environment.

## Decision

Build a namespaced Quickshell child-home plugin, custom theme, declarative activity catalog, and minimal user configuration overrides. Preserve stock Omarchy components for parent mode. Put source, install logic, tests, and documentation in this repository; deploy generated or linked artifacts only into user-owned configuration paths.

## Consequences

- Omarchy updates can continue to improve core components.
- The public project can be installed and removed independently.
- Some deep visual changes may require a cloned first-party widget, but that is an exception requiring an additional decision record.
- Access restriction remains an OS/account-policy concern, not a property of the launcher.
