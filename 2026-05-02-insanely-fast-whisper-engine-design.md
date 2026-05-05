# Local Turbo Engine — Design Spec

**Date:** 2026-05-02
**Feature:** Add `insanely-fast-whisper` as a third transcription engine to InterScriber
**Reference:** https://github.com/Vaibhavs10/insanely-fast-whisper

---

## Goal

Fill the gap between the two existing engines by adding a **fast, local, high-quality** option:

| Engine | Speed | Accuracy | Privacy | Cost |
|---|---|---|---|---|
| Local Small (existing) | Slow (1–2× RT) | Lower | Local | Free |
| **Local Turbo (NEW)** | **Fast (3–5× RT on M1, 50×+ on NVIDIA)** | **High** | **Local** | **Free** |
| Groq Cloud (existing) | Fastest (100×+ RT) | Highest | Off-device | Paid |

The new engine uses Whisper Large-V3 Turbo via the `insanely-fast-whisper` CLI, which leverages MPS on Apple Silicon and CUDA on NVIDIA hardware.

---

## Architecture

A new transcription script `tools/transcribe_ifw.py` joins the existing two. `app.py` detects whether `insanely-fast-whisper` is on PATH at startup and conditionally adds the engine to the radio. Selection routes to the new script via `subprocess.run`, identical to the existing engines.

```
app.py (Streamlit UI)
  ├── detects engines at startup:
  │     - Local Small (always)
  │     - Local Turbo (if shutil.which("insanely-fast-whisper"))
  │     - Groq Cloud  (if GROQ_API_KEY set)
  └── subprocess.run(["python3", <script>, <file>])
        ├── tools/transcribe_whisper.py  (existing)
        ├── tools/transcribe_groq.py     (existing)
        └── tools/transcribe_ifw.py      (NEW)
              ├── ffmpeg → mono 16kHz WAV (tempfile)
              ├── insanely-fast-whisper CLI:
              │     --file-name <wav>
              │     --model openai/whisper-large-v3-turbo
              │     --device-id <mps|0>   # mps on Darwin, 0 on Linux/Windows
              │     --timestamp word
              │     --transcript-path <tmp.json>
              ├── load CLI output JSON
              ├── reshape → video-use schema
              └── write transcripts/<stem>.json
```

### Key decisions

- **Same output contract** — writes `transcripts/<stem>.json` in the existing video-use schema (`{type, text, start, end, speaker_id}` words plus `spacing` tokens). No changes needed to `pack_transcripts.py`.
- **Word-level timestamps required** — pass `--timestamp word` to the CLI. This is slower than the default chunk-level mode but preserves the precise per-phrase `[MM:SS–MM:SS]` markers the project is built around.
- **Device selection** — the CLI requires explicit device choice via `--device-id`. We branch on `platform.system()`: `"mps"` on Darwin (Apple Silicon), `"0"` on Linux/Windows (CUDA GPU 0). One-liner, no torch import needed in our wrapper. Users on Intel Macs or CPU-only Linux boxes will see the engine fail with a clear MPS/CUDA-not-available error from the CLI — which is acceptable since the engine is gated to "GPU/Apple Silicon" hardware in its label.
- **Detection mirrors Groq** — `app.py` checks at startup; if the CLI isn't installed, the engine doesn't appear in the radio. Avoids forcing every user to install ~3GB of torch + transformers.
- **Install via `pipx`, not `requirements.txt`** — keeps the base venv lean. Users who want this engine run `pipx install insanely-fast-whisper` once, documented in the README.

---

## Components

### `tools/transcribe_ifw.py` (new)

Mirrors the shape of `tools/transcribe_whisper.py`. Estimated ~80 lines.

Functions:
- `extract_audio(video_path, audio_path)` — same ffmpeg invocation as `transcribe_whisper.py` (`-ac 1 -ar 16000 -vn`).
- `ifw_to_video_use_schema(ifw_result)` — converts the CLI's word-level output to the video-use schema. Inserts `spacing` tokens when gap between consecutive words exceeds `_GAP_THRESHOLD_S = 0.1`. Tags every word with `speaker_id: "speaker_0"` (matches the other engines — speaker diarization is out of scope).
- `transcribe(video_path, output_path)` — orchestrates: extract audio → run CLI → load JSON → reshape → write `transcripts/<stem>.json`.

CLI invocation:
```python
device = "mps" if platform.system() == "Darwin" else "0"
subprocess.run([
    "insanely-fast-whisper",
    "--file-name", str(audio_path),
    "--model", "openai/whisper-large-v3-turbo",
    "--device-id", device,
    "--timestamp", "word",
    "--transcript-path", str(ifw_json_path),
], check=True)
```

### `app.py` (small edit)

Changes (~5 lines):
- Import `shutil` if not already imported.
- Compute `has_ifw = shutil.which("insanely-fast-whisper") is not None`.
- Append `"Local Turbo (Fast, Requires GPU/Apple Silicon)"` to `engine_options` when `has_ifw`.
- Add a branch in the script selector: if `"Turbo" in engine` → `tools/transcribe_ifw.py`.
- Update the `engine_label` in the status text to display "Local Turbo" when selected.
- The trailing caption block (`if "Groq" in engine` vs else) already does the right thing for three engines — Local Turbo correctly falls into the "all processing is local" branch. No change needed there.

### `README.md` (doc update)

- Change "Two engines" → "Three engines" in the features list.
- Add a "Local Turbo" subsection between "Local" and "Groq Cloud" with the `pipx install insanely-fast-whisper` instruction and a brief perf note.
- Add a row to the cost-comparison table for Local Turbo (free, fast).
- Update the project-structure tree to include `transcribe_ifw.py`.

### `requirements.txt`

**Unchanged.** `insanely-fast-whisper` is installed via `pipx`, deliberately outside the project venv to avoid bloating users who only want Local Small or Groq.

---

## Data flow

1. User uploads file in Streamlit UI.
2. `app.py` saves to `raw/<filename>`.
3. `app.py` calls `python3 tools/transcribe_ifw.py raw/<filename>`.
4. Script extracts audio with ffmpeg → temp `.wav`.
5. Script invokes `insanely-fast-whisper` CLI → temp `.json` (word-level chunks).
6. Script reshapes to video-use schema → writes `transcripts/<stem>.json`.
7. Script cleans up both temp files in `finally`.
8. `app.py` deletes the raw upload (best-effort), packs the transcript via `pack_transcripts.py`, displays `takes_packed.md`.

---

## Error handling

| Failure | Detection | Response |
|---|---|---|
| CLI not on PATH at runtime | `FileNotFoundError` from `subprocess.run` | Catch, raise `RuntimeError` with: "insanely-fast-whisper CLI not found. Run: pipx install insanely-fast-whisper" |
| CLI exits non-zero (OOM, model download failure, audio decode error) | `subprocess.CalledProcessError` | Existing `app.py` `except` block catches this and surfaces return code. Script lets stderr pass through so terminal has detail. |
| Output JSON missing or malformed | `Path.exists()` check + `json.loads` parse | Raise `RuntimeError("insanely-fast-whisper produced no output")` |
| Tempfile cleanup | — | Both temp paths (audio WAV + CLI JSON) `.unlink(missing_ok=True)` in `finally` |

---

## Testing

Manual smoke test plan (project has no automated test suite; not adding one for this change):

1. Confirm engine does **not** appear in UI before `pipx install insanely-fast-whisper`.
2. Install it, restart app, confirm "Local Turbo (Fast, Requires GPU/Apple Silicon)" option appears in the radio.
3. Upload a short (~30s) audio clip, run with Local Turbo.
4. Verify `transcripts/<stem>.json` exists with word-level timestamps and video-use schema.
5. Verify `takes_packed.md` renders correctly with `[MM:SS–MM:SS]` markers.
6. Re-run on a 5-min clip — confirm meaningful speedup vs Local Small on the M1.
7. Failure path: rename the CLI binary temporarily, click Start, confirm the error message is helpful.

---

## Out of scope

- Speaker diarization (all engines tag everything as `speaker_0`).
- Model size selection in the UI (hardcoded to `large-v3-turbo`).
- Bundling `insanely-fast-whisper` in `requirements.txt` or a `[fast]` extras group.
- Automated test harness for any engine.
