#!/usr/bin/env python3
"""
TikTok Audio Downloader using yt-dlp.
Downloads audio-only tracks (e.g., MP3) from TikTok URLs supplied via a text file.

Usage:
    python tiktok_audio_downloader.py \
        --urls-file urls.txt \
        --output-dir "./Downloaded_Audio" \
        --ffmpeg-location "/opt/homebrew/bin"
"""

import argparse
import csv
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

import yt_dlp
import shutil


def download_tiktok_audio(
    url: str,
    download_dir: Path,
    ffmpeg_location: Optional[str] = None,
    audio_codec: str = "mp3",
    audio_quality: str = "64",
) -> Dict[str, Any]:
    download_dir.mkdir(parents=True, exist_ok=True)
    outtmpl = str(download_dir / "%(uploader)s_%(id)s.%(ext)s")

    if ffmpeg_location is None:
        ffmpeg_bin = shutil.which("ffmpeg")
        ffprobe_bin = shutil.which("ffprobe")
        if ffmpeg_bin and ffprobe_bin:
            ffmpeg_location = str(Path(ffmpeg_bin).parent)

    ydl_opts: Dict[str, Any] = {
        "outtmpl": outtmpl,
        "format": "bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": audio_codec,
            "preferredquality": audio_quality,
        }],
    }

    if ffmpeg_location:
        ydl_opts["ffmpeg_location"] = ffmpeg_location

    info: Dict[str, Any] = {
        "input_url": url,
        "status": "unknown",
        "filepath": None,
        "title": None,
        "uploader": None,
        "id": None,
        "duration": None,
        "webpage_url": None,
        "error": None,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)

            if isinstance(result, dict) and "entries" in result:
                entries = result.get("entries") or []
                if entries:
                    result = entries[0]

            base_path = ydl.prepare_filename(result)
            if "." in base_path:
                base_path = base_path.rsplit(".", 1)[0]

            final_path = base_path + f".{audio_codec}"
            info["filepath"] = final_path

    except Exception as e:
        info["status"] = "error"
        info["error"] = str(e)
        return info

    info["status"] = "ok"
    info["title"] = result.get("title")
    info["uploader"] = result.get("uploader")
    info["id"] = result.get("id")
    info["duration"] = result.get("duration")
    info["webpage_url"] = result.get("webpage_url") or result.get("original_url")

    return info


def read_urls_from_file(urls_file: Path) -> List[str]:
    urls: List[str] = []
    with urls_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                urls.append(line)
    return urls


def write_metadata_csv(metadata_file: Path, records: List[Dict[str, Any]]) -> None:
    fieldnames = [
        "input_url", "status", "filepath", "title", "uploader",
        "id", "duration", "webpage_url", "error"
    ]

    metadata_file.parent.mkdir(parents=True, exist_ok=True)

    with metadata_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in records:
            writer.writerow({k: rec.get(k, "") for k in fieldnames})


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download TikTok audio (mp3) from a list of URLs using yt-dlp."
    )

    parser.add_argument("--urls-file", required=True,
                        help="Text file containing TikTok URLs (one per line).")
    parser.add_argument("--output-dir", required=True,
                        help="Directory to save MP3 files.")
    parser.add_argument("--metadata", default="tiktok_audio_metadata.csv",
                        help="Metadata CSV path. Relative paths are created inside output-dir.")
    parser.add_argument("--ffmpeg-location", default=None,
                        help="Directory containing ffmpeg and ffprobe.")
    parser.add_argument("--codec", default="mp3",
                        help="Audio codec (default mp3).")
    parser.add_argument("--quality", default="64",
                        help="Audio quality (default 64).")

    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)

    urls_file = Path(args.urls_file)
    output_dir = Path(args.output_dir)
    metadata_path = Path(args.metadata)

    if not metadata_path.is_absolute():
        metadata_path = output_dir / metadata_path

    if not urls_file.exists():
        print(f"ERROR: URLs file not found: {urls_file}")
        sys.exit(1)

    urls = read_urls_from_file(urls_file)
    if not urls:
        print(f"No URLs found in {urls_file}")
        sys.exit(0)

    print(f"Found {len(urls)} URLs.")
    print(f"Saving audio to: {output_dir}")
    print(f"Metadata CSV: {metadata_path}")

    results: List[Dict[str, Any]] = []

    for i, url in enumerate(urls, start=1):
        print(f"[{i}/{len(urls)}] {url}")
        info = download_tiktok_audio(
            url=url,
            download_dir=output_dir,
            ffmpeg_location=args.ffmpeg_location,
            audio_codec=args.codec,
            audio_quality=args.quality,
        )
        print("   →", info["status"])
        if info["error"]:
            print("   error:", info["error"])
        results.append(info)

    write_metadata_csv(metadata_path, results)
    print("Done.")


if __name__ == "__main__":
    main()
