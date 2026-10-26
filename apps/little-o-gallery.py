#!/usr/bin/env python3
"""Read-only local picture gallery for Little O."""

from __future__ import annotations

import argparse
import html
import mimetypes
import os
from pathlib import Path
import subprocess
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse


IMAGE_SUFFIXES = {".avif", ".gif", ".jpeg", ".jpg", ".png", ".webp"}


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My Things</title>
  <style>
    :root { color-scheme: light; font-family: "Noto Sans", "DejaVu Sans", sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; color: #082859; background: #f5e7d0; }
    header { position: sticky; top: 0; z-index: 2; min-height: 96px; display: flex;
      align-items: center; justify-content: space-between; gap: 24px; padding: 16px 28px;
      background: #fff9eeed; border-bottom: 4px solid #d8b98b; }
    h1 { margin: 0; font-size: clamp(34px, 5vw, 58px); }
    button { min-width: 120px; min-height: 64px; border: 3px solid #c4a879;
      border-radius: 22px; padding: 10px 22px; color: #082859; background: #fff9ee;
      font: 800 24px/1 "Noto Sans", sans-serif; cursor: pointer; }
    button:hover { background: #f0e1ca; }
    button:focus-visible, .picture:focus-visible { outline: 7px solid #082859; outline-offset: 4px; }
    main { padding: 28px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 26px; }
    .picture { min-height: 250px; overflow: hidden; border: 6px solid #fff9ee; border-radius: 26px;
      background: #308ed1; box-shadow: 0 8px 0 #c4a879; cursor: pointer; }
    .picture img { display: block; width: 100%; height: 260px; object-fit: cover; }
    .picture span { display: block; overflow: hidden; padding: 14px; color: #fff;
      font-size: 22px; font-weight: 800; text-align: center; text-overflow: ellipsis; white-space: nowrap; }
    .empty { max-width: 720px; margin: 12vh auto; padding: 52px; border: 5px solid #d8b98b;
      border-radius: 30px; background: #fff9ee; text-align: center; }
    .empty h2 { margin: 0 0 18px; font-size: clamp(34px, 5vw, 52px); }
    .empty p { margin: 0; font-size: clamp(22px, 3vw, 32px); line-height: 1.4; }
    dialog { width: min(96vw, 1500px); height: 92vh; padding: 0; border: 0; border-radius: 28px;
      background: #151515; box-shadow: 0 24px 80px #0009; }
    dialog::backdrop { background: #082859d9; }
    .viewer { width: 100%; height: 100%; display: grid; grid-template-columns: 110px 1fr 110px;
      grid-template-rows: 86px 1fr; align-items: center; gap: 14px; padding: 16px; }
    .viewer .close { grid-column: 3; justify-self: end; min-width: 86px; }
    .viewer .previous { grid-column: 1; grid-row: 2; }
    .viewer img { grid-column: 2; grid-row: 2; width: 100%; height: 100%; object-fit: contain; }
    .viewer .next { grid-column: 3; grid-row: 2; }
    @media (max-width: 720px) {
      main { padding: 18px; }
      .grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
      .picture { min-height: 180px; }
      .picture img { height: 180px; }
      .viewer { grid-template-columns: 82px 1fr 82px; }
    }
  </style>
</head>
<body>
  <header><button type="button" onclick="window.close()">Home</button><h1>My Things</h1><span aria-label="__COUNT__ pictures">__COUNT__ pictures</span></header>
  <main>__CONTENT__</main>
  <dialog id="viewer" aria-label="Picture viewer">
    <div class="viewer">
      <button class="close" type="button" aria-label="Close picture">Close</button>
      <button class="previous" type="button" aria-label="Previous picture">Back</button>
      <img alt="">
      <button class="next" type="button" aria-label="Next picture">Next</button>
    </div>
  </dialog>
  <script>
    const pictures = [...document.querySelectorAll('.picture')];
    const viewer = document.querySelector('#viewer');
    const large = viewer.querySelector('img');
    let current = 0;
    function show(index) {
      if (!pictures.length) return;
      current = (index + pictures.length) % pictures.length;
      const picture = pictures[current];
      large.src = picture.dataset.src;
      large.alt = picture.dataset.name;
      if (!viewer.open) viewer.showModal();
    }
    pictures.forEach((picture, index) => {
      picture.addEventListener('click', () => show(index));
      picture.addEventListener('keydown', event => {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); show(index); }
      });
    });
    viewer.querySelector('.close').addEventListener('click', () => viewer.close());
    viewer.querySelector('.previous').addEventListener('click', () => show(current - 1));
    viewer.querySelector('.next').addEventListener('click', () => show(current + 1));
    document.addEventListener('keydown', event => {
      if (!viewer.open) return;
      if (event.key === 'ArrowLeft') show(current - 1);
      if (event.key === 'ArrowRight') show(current + 1);
    });
  </script>
</body>
</html>
"""


def pictures_in(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        return []

    pictures: list[Path] = []
    for candidate in root.rglob("*"):
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved.is_file() and resolved.suffix.lower() in IMAGE_SUFFIXES:
            pictures.append(resolved)
    return sorted(pictures, key=lambda path: path.name.casefold())


def render_page(pictures: list[Path]) -> bytes:
    if pictures:
        cards = []
        for index, picture in enumerate(pictures):
            display_name = picture.stem.replace("_", " ").replace("-", " ").strip()
            name = html.escape((display_name or "Picture").title())
            cards.append(
                f'<div class="picture" role="button" tabindex="0" '
                f'data-src="/picture/{index}" data-name="{name}">'
                f'<img src="/picture/{index}" alt="{name}" loading="lazy">'
                f'<span>{name}</span></div>'
            )
        content = '<section class="grid" aria-label="Saved pictures">' + "".join(cards) + "</section>"
    else:
        content = (
            '<section class="empty"><h2>No pictures yet</h2>'
            '<p>Make a drawing, save it, then come back to see it here.</p></section>'
        )
    return (
        PAGE.replace("__COUNT__", str(len(pictures))).replace("__CONTENT__", content).encode("utf-8")
    )


def handler_for(pictures: list[Path]) -> type[BaseHTTPRequestHandler]:
    page = render_page(pictures)

    class GalleryHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            route = unquote(urlparse(self.path).path)
            if route == "/":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(page)))
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'self'; img-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'",
                )
                self.end_headers()
                self.wfile.write(page)
                return

            parts = route.strip("/").split("/")
            if len(parts) == 2 and parts[0] == "picture" and parts[1].isdigit():
                index = int(parts[1])
                if 0 <= index < len(pictures):
                    picture = pictures[index]
                    try:
                        size = picture.stat().st_size
                        self.send_response(HTTPStatus.OK)
                        self.send_header("Content-Type", mimetypes.guess_type(picture.name)[0] or "application/octet-stream")
                        self.send_header("Content-Length", str(size))
                        self.send_header("Cache-Control", "no-store")
                        self.end_headers()
                        with picture.open("rb") as source:
                            while chunk := source.read(1024 * 1024):
                                self.wfile.write(chunk)
                        return
                    except (BrokenPipeError, FileNotFoundError, OSError):
                        return

            self.send_error(HTTPStatus.NOT_FOUND)

        def log_message(self, _format: str, *_args: object) -> None:
            return

    return GalleryHandler


def launch_gallery(root: Path, profile: Path) -> int:
    pictures = pictures_in(root)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(pictures))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    profile.mkdir(parents=True, exist_ok=True)
    url = f"http://127.0.0.1:{server.server_port}/"
    command = [
        "chromium",
        f"--user-data-dir={profile}",
        f"--app={url}",
        "--start-maximized",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        "--disable-extensions",
        "--disable-vulkan",
        "--disable-features=Translate,MediaRouter",
    ]
    try:
        return subprocess.run(command, check=False).returncode
    finally:
        server.shutdown()
        server.server_close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pictures", type=Path)
    parser.add_argument("--profile", type=Path, default=Path.home() / ".local/share/little-o/gallery-profile")
    parser.add_argument("--check", action="store_true", help="validate and report the picture count without opening a window")
    args = parser.parse_args()

    if args.check:
        found = pictures_in(args.pictures)
        render_page(found)
        print(f"Little O gallery ready: {len(found)} picture(s)")
        return 0

    if not shutil_which("chromium"):
        print("Little O gallery needs Chromium.", file=sys.stderr)
        return 1
    return launch_gallery(args.pictures, args.profile.expanduser())


def shutil_which(command: str) -> str | None:
    """Small PATH lookup kept local so the gallery has no non-stdlib dependency."""
    for directory in os.environ.get("PATH", "").split(os.pathsep):
        candidate = Path(directory) / command
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
