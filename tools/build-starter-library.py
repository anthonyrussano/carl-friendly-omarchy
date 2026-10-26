#!/usr/bin/env python3
"""Build Little O's original starter EPUBs and WAV melodies."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
import struct
import wave
import zipfile


ROOT = Path(__file__).resolve().parents[1]
BOOKS = ROOT / "starter-library/books"
MUSIC = ROOT / "starter-library/music"
PICTURES = ROOT / "starter-library/pictures"

STORIES = [
    {
        "slug": "fox-and-bird-build-together",
        "title": "Fox and Bird Build Together",
        "color": "#f25b3f",
        "accent": "#f7c928",
        "pages": [
            "Fox found a box of blocks. Bird found a big idea.",
            "“Let’s build a little house,” chirped Bird.",
            "Fox placed one square block. Bird added one triangle roof.",
            "The tower leaned left. Wobble, wobble, wobble!",
            "They slowed down. Fox held the bottom. Bird moved the roof.",
            "The house stood tall. There was room for both friends inside.",
            "“We made it together,” said Fox. Bird gave a happy peep.",
        ],
    },
    {
        "slug": "turtle-counts-the-pond",
        "title": "Turtle Counts the Pond",
        "color": "#25b9b7",
        "accent": "#86bd35",
        "pages": [
            "Turtle took a slow swim around the bright blue pond.",
            "One pink flower opened to the sun.",
            "Two yellow ducks paddled side by side.",
            "Three green lily pads floated near the reeds.",
            "Four dragonflies danced above the water.",
            "Five smooth pebbles waited on the warm bank.",
            "One, two, three, four, five. Turtle smiled and counted again.",
        ],
    },
    {
        "slug": "bear-says-goodnight",
        "title": "Bear Says Goodnight",
        "color": "#308ed1",
        "accent": "#8c65bd",
        "pages": [
            "The sky grew dark blue. Bear put on soft striped pajamas.",
            "“Goodnight, red blocks,” Bear whispered. The blocks stayed still.",
            "“Goodnight, yellow moon.” The moon glowed gently.",
            "“Goodnight, green plant.” One leaf waved in the night breeze.",
            "Bear chose one last little book and turned each page slowly.",
            "The room was quiet. The blankets were warm.",
            "“Goodnight, everyone.” Bear closed both eyes and dreamed in colors.",
        ],
    },
]

MELODIES = [
    ("sunny-steps.wav", 132, [60, 64, 67, 72, 67, 64, 62, 65, 69, 74, 69, 65, 60, 64, 67, 72]),
    ("pond-parade.wav", 112, [55, 59, 62, 59, 57, 60, 64, 60, 55, 57, 59, 62, 59, 57, 55, 55]),
    ("quiet-stars.wav", 84, [60, 67, 64, 67, 59, 65, 62, 65, 57, 64, 60, 64, 55, 62, 59, 55]),
]

PICTURE_FILES = {
    "friends-build-together.webp",
    "pond-friends.webp",
    "bedtime-book.webp",
}


def zip_entry(archive: zipfile.ZipFile, name: str, data: str | bytes, *, stored: bool = False) -> None:
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_STORED if stored else zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data.encode("utf-8") if isinstance(data, str) else data)


def build_epub(story: dict[str, object]) -> Path:
    title = str(story["title"])
    slug = str(story["slug"])
    color = str(story["color"])
    accent = str(story["accent"])
    pages = list(story["pages"])
    output = BOOKS / f"{title}.epub"
    chapters = []
    manifest = []
    spine = []
    nav = []

    for index, text in enumerate(pages, start=1):
        filename = f"page-{index}.xhtml"
        chapters.append(
            (
                filename,
                f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head><title>{title} — page {index}</title><link rel="stylesheet" href="style.css" type="text/css"/></head>
<body><main><div class="shape shape-{(index % 4) + 1}" aria-hidden="true"></div><p>{text}</p><small>{index}</small></main></body>
</html>''',
            )
        )
        manifest.append(f'<item id="p{index}" href="{filename}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="p{index}"/>')
        nav.append(f'<li><a href="{filename}">Page {index}</a></li>')

    cover = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="1600" viewBox="0 0 1200 1600">
<rect width="1200" height="1600" rx="70" fill="#fff9ee"/><rect x="55" y="55" width="1090" height="1490" rx="60" fill="{color}"/>
<circle cx="600" cy="560" r="330" fill="{accent}"/><path d="M310 940 Q600 720 890 940 L890 1160 Q600 1360 310 1160Z" fill="#fff9ee"/>
<text x="600" y="230" text-anchor="middle" fill="#082859" font-family="sans-serif" font-size="86" font-weight="700">{title}</text>
<text x="600" y="1460" text-anchor="middle" fill="#082859" font-family="sans-serif" font-size="46">A Little O story</text></svg>'''
    css = f'''body {{ margin: 0; color: #082859; background: #fff9ee; font-family: sans-serif; }}
main {{ min-height: 90vh; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 8%; text-align: center; }}
p {{ max-width: 24em; font-size: 2.2rem; line-height: 1.5; }} small {{ font-size: 1rem; }}
.shape {{ width: 11rem; height: 11rem; margin-bottom: 2rem; background: {color}; border: 1.1rem solid {accent}; }}
.shape-1 {{ border-radius: 50%; }} .shape-2 {{ border-radius: 2rem; transform: rotate(10deg); }}
.shape-3 {{ border-radius: 50% 50% 20% 20%; }} .shape-4 {{ border-radius: 35% 65% 45% 55%; }}'''
    container = '''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'''
    package = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">urn:little-o:{slug}</dc:identifier><dc:title>{title}</dc:title><dc:creator>Little O Project</dc:creator><dc:language>en</dc:language><dc:rights>CC0-1.0</dc:rights><meta property="dcterms:modified">2026-10-26T00:00:00Z</meta><meta name="cover" content="cover"/></metadata>
<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="cover" href="cover.svg" media-type="image/svg+xml" properties="cover-image"/><item id="css" href="style.css" media-type="text/css"/>{''.join(manifest)}</manifest>
<spine>{''.join(spine)}</spine></package>'''
    navigation = f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="en"><head><title>{title}</title></head><body><nav epub:type="toc"><h1>{title}</h1><ol>{''.join(nav)}</ol></nav></body></html>'''

    with zipfile.ZipFile(output, "w") as archive:
        zip_entry(archive, "mimetype", "application/epub+zip", stored=True)
        zip_entry(archive, "META-INF/container.xml", container)
        zip_entry(archive, "OEBPS/package.opf", package)
        zip_entry(archive, "OEBPS/nav.xhtml", navigation)
        zip_entry(archive, "OEBPS/style.css", css)
        zip_entry(archive, "OEBPS/cover.svg", cover)
        for filename, chapter in chapters:
            zip_entry(archive, f"OEBPS/{filename}", chapter)
    return output


def note_frequency(note: int) -> float:
    return 440.0 * (2.0 ** ((note - 69) / 12.0))


def build_melody(filename: str, bpm: int, notes: list[int]) -> Path:
    output = MUSIC / filename
    sample_rate = 22050
    beat = 60.0 / bpm
    note_length = beat * 0.92
    rest = beat * 0.08
    frames: list[int] = []
    for note in notes:
        count = int(sample_rate * note_length)
        frequency = note_frequency(note)
        for sample in range(count):
            time = sample / sample_rate
            fade = min(1.0, sample / (sample_rate * 0.025), (count - sample) / (sample_rate * 0.08))
            tone = math.sin(2 * math.pi * frequency * time) + 0.22 * math.sin(4 * math.pi * frequency * time)
            frames.append(int(9500 * max(0.0, fade) * tone / 1.22))
        frames.extend([0] * int(sample_rate * rest))
    with wave.open(str(output), "wb") as audio:
        audio.setnchannels(1)
        audio.setsampwidth(2)
        audio.setframerate(sample_rate)
        audio.writeframes(b"".join(struct.pack("<h", frame) for frame in frames))
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate committed output instead of rebuilding it")
    args = parser.parse_args()
    BOOKS.mkdir(parents=True, exist_ok=True)
    MUSIC.mkdir(parents=True, exist_ok=True)

    if not args.check:
        for story in STORIES:
            build_epub(story)
        for filename, bpm, notes in MELODIES:
            build_melody(filename, bpm, notes)

    expected_books = {f"{story['title']}.epub" for story in STORIES}
    expected_music = {item[0] for item in MELODIES}
    assert expected_books <= {path.name for path in BOOKS.glob("*.epub")}
    assert expected_music <= {path.name for path in MUSIC.glob("*.wav")}
    assert PICTURE_FILES <= {path.name for path in PICTURES.glob("*.webp")}
    for book in BOOKS.glob("*.epub"):
        with zipfile.ZipFile(book) as archive:
            assert archive.testzip() is None
            assert archive.read("mimetype") == b"application/epub+zip"
    for track in MUSIC.glob("*.wav"):
        with wave.open(str(track), "rb") as audio:
            assert audio.getnchannels() == 1 and audio.getframerate() == 22050
            assert audio.getnframes() > 22050
    print(
        f"Starter library ready: {len(expected_books)} books, "
        f"{len(expected_music)} songs, and {len(PICTURE_FILES)} pictures"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
