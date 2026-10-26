# Retired Hermes child-helper prototype

This code records the voice-toggle bridge tested on the reference laptop. It is research material only: `bin/install` does not install it, the child home does not expose an AI action, and the system check does not require Hermes.

The prototype was retired on 2026-10-26 after supervised use found the end-to-end experience too laggy and unreliable for independent preschool use. Provider login expiry, desktop/HUD timing, speech capture, model response latency, and spoken playback created too many failure points in one child-facing action.

Any future assistant experiment should begin as a separate, adult-launched prototype and earn its way back through observed child testing. The minimum bar is:

- one obvious push-to-talk control with visible listening/thinking/speaking states;
- local interruption and a hard timeout that always returns control;
- median first response under three seconds on the reference laptop;
- 9 of 10 successful turns in representative noise without adult recovery;
- a provider-independent adapter and an offline, non-AI fallback for activity help;
- no purchasing, messaging, deletion, or system mutation from child mode.

Do not choose a replacement model provider until the interaction loop meets those requirements with a fake/local response backend. Provider comparison is downstream of fixing the UX and reliability boundary.
