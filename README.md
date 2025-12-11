# TikTok Audio Downloader (yt-dlp)

A command-line tool for downloading audio-only tracks (MP3 or other codecs) from public TikTok videos using yt-dlp and ffmpeg.

It is designed for:

- Research workflows
- Large-scale data collection
- Team use
- Reproducible pipelines

This repository contains only code, not any TikTok media.

## Features

- Downloads audio-only from TikTok videos (default MP3, 64 kbps)
- Supports short URLs and full URLs
- Batch processing through urls.txt
- Consistent filenames (uploader_videoid.mp3)
- Generates a metadata CSV
- Requires no TikTok authentication or API keys

## Requirements

- Python 3.10+
- ffmpeg installed

### Mac (Homebrew)

```
brew install ffmpeg
```

Verify:

```
ffmpeg -version
ffprobe -version
```

## Install Python dependencies

```
pip install -r requirements.txt
```

## Prepare URLs

Create a text file:

```
https://vt.tiktok.com/example/
https://www.tiktok.com/@user/video/1234567890123456789
```

Save as urls.txt.

## Usage

```
python tiktok_audio_downloader.py     --urls-file urls.txt     --output-dir "./Downloaded_Audio"     --ffmpeg-location "/opt/homebrew/bin"
```

## Arguments

| Argument | Description |
|---------|-------------|
| --urls-file | Text file with TikTok URLs |
| --output-dir | Folder for audio files |
| --metadata | Path to metadata CSV |
| --ffmpeg-location | Directory containing ffmpeg |
| --codec | Output codec (default mp3) |
| --quality | Audio quality (default 64) |

## Ethical Use

Use only with public content you are allowed to download.  
Do not redistribute downloaded media.

## License

MIT License.
