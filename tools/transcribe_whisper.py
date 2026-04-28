#!/usr/bin/env python3
"""Transcribe a video with Whisper and write video-use-compatible JSON."""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

_GAP_THRESHOLD_S = 0.1  # gaps wider than this become spacing tokens in video-use schema


def extract_audio(video_path: Path, audio_path: Path) -> None:
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path),
             "-ac", "1", "-ar", "16000", "-vn", str(audio_path)],
            check=True, capture_output=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg failed: {e.stderr.decode()}") from e


def whisper_to_video_use_schema(result: dict) -> dict:
    """Convert Whisper word-timestamp output to video-use words schema."""
    words = []
    prev_end = 0.0

    for segment in result.get("segments", []):
        for w in segment.get("words", []):
            start_val = w.get("start")
            end_val = w.get("end")
            word_val = w.get("word")
            if start_val is None or end_val is None or word_val is None:
                continue
            start = round(start_val, 3)
            end = round(end_val, 3)
            text = word_val.strip()

            if not text:
                continue

            if start - prev_end >= _GAP_THRESHOLD_S:
                words.append({
                    "type": "spacing",
                    "text": " ",
                    "start": round(prev_end, 3),
                    "end": start,
                })

            words.append({
                "type": "word",
                "text": text,
                "start": start,
                "end": end,
                "speaker_id": "speaker_0",
            })
            prev_end = end

    return {"words": words}


def transcribe(video_path: Path, output_path: Path) -> None:
    import whisper

    audio_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio_path = Path(tmp.name)
        extract_audio(video_path, audio_path)
        model = whisper.load_model("small")
        result = model.transcribe(str(audio_path), word_timestamps=True, fp16=False)
        schema = whisper_to_video_use_schema(result)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")
        print(f"words: {len(schema['words'])}")
        print(f"Saved → {output_path}")
    finally:
        if audio_path:
            audio_path.unlink(missing_ok=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/transcribe_whisper.py <video_file>")
        sys.exit(1)

    video = Path(sys.argv[1])
    if not video.exists():
        print(f"Error: file not found: {video}")
        sys.exit(1)
    out = Path("transcripts") / (video.stem + ".json")
    transcribe(video, out)
