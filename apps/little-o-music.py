#!/usr/bin/env python3
"""Child-friendly local music library for Little O."""

from __future__ import annotations

import argparse
import html
import mimetypes
from pathlib import Path
from shutil import which
import subprocess
import sys
import threading
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse


AUDIO_SUFFIXES = {".flac", ".m4a", ".mp3", ".oga", ".ogg", ".opus", ".wav"}


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Music</title>
  <style>
    :root { color-scheme: light; font-family: "Noto Sans", "DejaVu Sans", sans-serif; }
    * { box-sizing: border-box; }
    body { margin: 0; min-height: 100vh; overflow: hidden; color: #082859;
      background: linear-gradient(135deg, #8c65bd, #5d3d91); }
    header { height: 96px; display: flex; align-items: center; justify-content: space-between;
      gap: 24px; padding: 16px 28px; background: #fff9eeed; border-bottom: 4px solid #d8b98b; }
    h1 { margin: 0; font-size: clamp(34px, 5vw, 58px); }
    button { min-width: 110px; min-height: 64px; border: 3px solid #c4a879;
      border-radius: 22px; padding: 10px 22px; color: #082859; background: #fff9ee;
      font: 800 23px/1.2 "Noto Sans", sans-serif; cursor: pointer; }
    button:hover { background: #fff; }
    button:focus-visible, audio:focus-visible { outline: 7px solid #082859; outline-offset: 4px; }
    main { height: calc(100vh - 96px); display: grid; grid-template-columns: minmax(300px, 34%) 1fr;
      gap: 24px; padding: 24px; }
    .songs { overflow: auto; padding: 16px; border: 5px solid #d8b98b; border-radius: 28px;
      background: #fff9ee; }
    .songs h2 { margin: 0 0 14px; font-size: 28px; }
    .song { width: 100%; min-height: 72px; margin: 8px 0; border-width: 3px; box-shadow: none;
      overflow: hidden; text-align: left; text-overflow: ellipsis; white-space: nowrap; }
    .song[aria-current="true"] { border-width: 6px; border-color: #082859; background: #e8d9f8; }
    .player { display: grid; place-items: center; min-width: 0; padding: 32px;
      border: 5px solid #d8b98b; border-radius: 28px; background: #fff9ee; text-align: center; }
    .player-inner { width: min(850px, 100%); }
    .album { width: min(260px, 40vh); aspect-ratio: 1; display: grid; place-items: center;
      margin: 0 auto 30px; border-radius: 38px; color: #fff; background: #8c65bd;
      box-shadow: 0 12px 0 #5d3d91; font-size: clamp(42px, 8vw, 86px); font-weight: 900; }
    #now-playing { min-height: 72px; margin: 18px 0 28px; overflow-wrap: anywhere;
      font-size: clamp(28px, 4vw, 46px); font-weight: 900; }
    .controls { display: flex; flex-wrap: wrap; justify-content: center; gap: 18px; }
    #play { min-width: 190px; background: #f7c928; font-size: 30px; }
    audio { width: min(680px, 100%); height: 70px; margin-top: 28px; }
    .status { min-height: 34px; margin-top: 14px; font-size: 22px; font-weight: 700; }
    @media (max-width: 860px) {
      main { grid-template-columns: 1fr; grid-template-rows: 34% 1fr; }
      .songs { display: flex; gap: 10px; align-items: center; overflow-x: auto; }
      .songs h2 { display: none; }
      .song { min-width: 240px; margin: 0; }
      .album { display: none; }
    }
  </style>
</head>
<body>
  <header><button type="button" onclick="window.close()">Home</button><h1>Music</h1><span>__COUNT__ songs</span></header>
  <main>
    <section class="songs" aria-label="Songs"><h2>Choose a song</h2>__SONGS__</section>
    <section class="player" aria-label="Music player"><div class="player-inner">
      <div class="album" aria-hidden="true">Music</div>
      <div id="now-playing">Choose a song</div>
      <div class="controls">
        <button id="previous" type="button">Previous</button>
        <button id="play" type="button">Play</button>
        <button id="next" type="button">Next</button>
      </div>
      <audio controls preload="metadata"></audio>
      <div class="status" role="status" aria-live="polite">Ready to play.</div>
    </div></section>
  </main>
  <script>
    const buttons = [...document.querySelectorAll('.song')];
    const audio = document.querySelector('audio');
    const play = document.querySelector('#play');
    const title = document.querySelector('#now-playing');
    const status = document.querySelector('.status');
    let current = 0;
    function select(index, start = true) {
      if (!buttons.length) return;
      current = (index + buttons.length) % buttons.length;
      buttons.forEach((button, position) => button.setAttribute('aria-current', String(position === current)));
      const selected = buttons[current];
      audio.src = selected.dataset.src;
      title.textContent = selected.dataset.name;
      status.textContent = start ? 'Playing.' : 'Ready to play.';
      if (start) audio.play().catch(() => { status.textContent = 'Press Play to begin.'; });
    }
    buttons.forEach((button, index) => button.addEventListener('click', () => select(index)));
    document.querySelector('#previous').addEventListener('click', () => select(current - 1));
    document.querySelector('#next').addEventListener('click', () => select(current + 1));
    play.addEventListener('click', () => audio.paused ? audio.play() : audio.pause());
    audio.addEventListener('play', () => { play.textContent = 'Pause'; status.textContent = 'Playing.'; });
    audio.addEventListener('pause', () => { play.textContent = 'Play'; status.textContent = 'Paused.'; });
    audio.addEventListener('ended', () => select(current + 1));
    audio.addEventListener('error', () => { status.textContent = 'This song could not be played. Try another one.'; });
    if (buttons.length) select(0, false);
  </script>
</body>
</html>
"""


def tracks_in(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.is_dir():
        return []
    tracks: list[Path] = []
    for candidate in root.rglob("*"):
        try:
            resolved = candidate.resolve()
            resolved.relative_to(root)
        except (OSError, ValueError):
            continue
        if resolved.is_file() and resolved.suffix.lower() in AUDIO_SUFFIXES:
            tracks.append(resolved)
    return sorted(tracks, key=lambda path: path.name.casefold())


def render_page(tracks: list[Path]) -> bytes:
    songs = []
    for index, track in enumerate(tracks):
        display_name = track.stem.replace("_", " ").replace("-", " ").strip()
        name = html.escape((display_name or "Song").title())
        songs.append(
            f'<button class="song" type="button" data-src="/track/{index}" '
            f'data-name="{name}" aria-current="false">{name}</button>'
        )
    return PAGE.replace("__COUNT__", str(len(tracks))).replace("__SONGS__", "".join(songs)).encode("utf-8")


def byte_range(header: str | None, size: int) -> tuple[int, int] | None:
    if not header or not header.startswith("bytes="):
        return None
    value = header.removeprefix("bytes=").split(",", 1)[0]
    start_text, _, end_text = value.partition("-")
    try:
        if start_text:
            start = int(start_text)
            end = int(end_text) if end_text else size - 1
        else:
            length = int(end_text)
            start = max(0, size - length)
            end = size - 1
    except ValueError:
        return None
    if start < 0 or start >= size or end < start:
        return None
    return start, min(end, size - 1)


def handler_for(tracks: list[Path]) -> type[BaseHTTPRequestHandler]:
    page = render_page(tracks)

    class MusicHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            route = unquote(urlparse(self.path).path)
            if route == "/":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(page)))
                self.send_header(
                    "Content-Security-Policy",
                    "default-src 'self'; media-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'",
                )
                self.end_headers()
                self.wfile.write(page)
                return

            parts = route.strip("/").split("/")
            if len(parts) == 2 and parts[0] == "track" and parts[1].isdigit():
                index = int(parts[1])
                if 0 <= index < len(tracks):
                    self.send_track(tracks[index])
                    return
            self.send_error(HTTPStatus.NOT_FOUND)

        def send_track(self, track: Path) -> None:
            try:
                size = track.stat().st_size
                requested = byte_range(self.headers.get("Range"), size)
                start, end = requested or (0, size - 1)
                self.send_response(HTTPStatus.PARTIAL_CONTENT if requested else HTTPStatus.OK)
                self.send_header("Content-Type", mimetypes.guess_type(track.name)[0] or "application/octet-stream")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(end - start + 1))
                if requested:
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                with track.open("rb") as source:
                    source.seek(start)
                    remaining = end - start + 1
                    while remaining:
                        chunk = source.read(min(1024 * 1024, remaining))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
            except (BrokenPipeError, FileNotFoundError, OSError):
                return

        def log_message(self, _format: str, *_args: object) -> None:
            return

    return MusicHandler


def launch_music(root: Path, profile: Path) -> int:
    tracks = tracks_in(root)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler_for(tracks))
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    profile.mkdir(parents=True, exist_ok=True)
    command = [
        "chromium",
        f"--user-data-dir={profile}",
        f"--app=http://127.0.0.1:{server.server_port}/",
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
    parser.add_argument("music", type=Path)
    parser.add_argument("--profile", type=Path, default=Path.home() / ".local/share/little-o/music-profile")
    parser.add_argument("--check", action="store_true", help="validate and report the track count without opening a window")
    args = parser.parse_args()

    tracks = tracks_in(args.music)
    if args.check:
        render_page(tracks)
        print(f"Little O music ready: {len(tracks)} track(s)")
        return 0
    if not tracks:
        print("Little O music folder is empty.", file=sys.stderr)
        return 1
    if not which("chromium"):
        print("Little O music needs Chromium.", file=sys.stderr)
        return 1
    return launch_music(args.music, args.profile.expanduser())


if __name__ == "__main__":
    raise SystemExit(main())
