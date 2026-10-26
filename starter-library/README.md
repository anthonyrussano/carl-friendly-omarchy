# Little O starter library

This small offline collection prevents the child surfaces from opening empty on a clean install:

- three short original EPUB picture stories;
- three original synthesized instrumental melodies;
- three original, AI-assisted gouache illustrations.

`bin/install` copies a starter file only when a same-named file is absent. It never overwrites family content, and `bin/uninstall` deliberately preserves all books, music, and pictures.

The stories, melodies, and pictures are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/), to the extent any copyright or related rights exist. The pictures were generated for this project with OpenAI's image-generation tool from prompts recorded in `manifest.json`; they contain no third-party logos, characters, or source images.

Rebuild the deterministic EPUB and WAV outputs with:

```bash
python3 tools/build-starter-library.py
```
