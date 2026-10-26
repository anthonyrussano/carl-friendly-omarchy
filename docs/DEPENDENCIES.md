# Dependencies and provenance

## Required runtime

| Component | Purpose | Source/license notes |
|---|---|---|
| Omarchy Shell / Quickshell | Child home and status bar | Provided by the host Omarchy system |
| Chromium | Local Draw, Music, and My Things interfaces | Host package; local content only, no arbitrary browsing |
| Python 3 standard library | Read-only localhost Music and My Things servers | Host package; servers bind only to `127.0.0.1` and expose approved media roots |
| GCompris 26.1 | Letters and Numbers | Arch `extra/gcompris-qt`; GPL educational suite |
| PipeWire/WirePlumber (`wpctl`) | Audio routing and input selection | Host Omarchy audio stack |
| `hyprctl` | Dedicated child workspace routing | Host Omarchy/Wayland tool |

## Stories

OmaBook is included as `vendor/omabook`, a Git submodule of `newx/omabook` pinned to tagged release `v0.1.1` and reviewed revision `d03520444e8a03a4063183908c22816ce00f0d04`. That release's main branch explicitly contains no AI, network model, summaries, questions, or speech service. It is MIT-licensed and installs locally through `bin/install-omabook`.

The reader engine is vendored inside the pinned submodule from `johnfactotum/foliate-js` revision `78914aef4466eb960965702401634c2cb348e9b1`. This makes the complete reader source reproducible without an additional nested checkout. Upgrading the reader means reviewing and committing a new main-repository submodule pointer; `bin/update-omabook` intentionally installs the current pin instead of tracking a branch.

## Included starter content

`starter-library/` contains three original EPUB stories, three original synthesized instrumental WAV tracks, and three original AI-assisted illustrations. They are dedicated under CC0-1.0 to the extent rights exist. The image prompts and file list are recorded in `starter-library/manifest.json`; no third-party reference images, logos, or characters were used. `tools/build-starter-library.py` reproducibly builds and validates the EPUB and WAV files.

The reference machine's private library contains the following Project Gutenberg editions:

| Book | Project Gutenberg ebook |
|---|---|
| *A Little Princess* | [146](https://www.gutenberg.org/ebooks/146) |
| *Alice's Adventures in Wonderland* | [11](https://www.gutenberg.org/ebooks/11) |
| *Just So Stories* | [2781](https://www.gutenberg.org/ebooks/2781) |
| *Peter Pan* | [16](https://www.gutenberg.org/ebooks/16) |
| *The Adventures of Pinocchio* | [500](https://www.gutenberg.org/ebooks/500) |
| *The Jungle Book* | [236](https://www.gutenberg.org/ebooks/236) |
| *The Railway Children* | [1874](https://www.gutenberg.org/ebooks/1874) |
| *The Secret Garden* | [17396](https://www.gutenberg.org/ebooks/17396) |
| *The Tale of Peter Rabbit* | [14838](https://www.gutenberg.org/ebooks/14838) |
| *The Velveteen Rabbit* | [11757](https://www.gutenberg.org/ebooks/11757) |
| *The Wind in the Willows* | [289](https://www.gutenberg.org/ebooks/289) |
| *The Wonderful Wizard of Oz* | [55](https://www.gutenberg.org/ebooks/55) |
| *Winnie-the-Pooh* | [67098](https://www.gutenberg.org/ebooks/67098) |

Project Gutenberg identifies each listed edition as public domain in the United States. The local copies are downloaded separately into `~/Books/Carl`; they are neither committed nor redistributed by this repository. Users outside the United States should check the copyright laws that apply where they live.

## Retired helper prototype

Hermes is not a runtime dependency and no AI provider is selected for the product. The retired bridge remains only under `research/hermes-prototype/` with the observed failure modes and the acceptance bar for a future, adult-launched experiment. `bin/install` removes an older installed Little O bridge from Hermes and stores it in that run's recoverable backup.
