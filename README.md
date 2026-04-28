# 🎙️ InterScriber

A free, open-source transcription tool built for journalists and qualitative researchers who need accurate, quotable transcripts without paying subscription fees.

Drop in your interview recording. Get back a clean, timestamped transcript in minutes — for pennies, or for free.

## 🚀 Quick Start (1-2-3)

1. **Clone this repo** to your machine.
2. **Install ffmpeg** (required for audio processing):
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
   - **Windows:** [Download ffmpeg](https://ffmpeg.org/download.html) and add it to your PATH.
3. **Run the launcher:**
   - **macOS/Linux:** `./run.sh`
   - **Windows:** Double-click `run.bat`

The launcher creates a private Python environment, installs all dependencies, and opens the web UI in your browser automatically.

## 🛠️ How It Works

1. **Drop** your audio or video file into the web UI (`.mp4`, `.mov`, `.wav`, `.m4a`, `.mp3`).
2. **Transcribe** using either your local machine (free, private) or Groq Cloud (fast, low-cost).
3. **Download** a clean Markdown transcript with `[MM:SS–MM:SS]` timestamps on every phrase — ready to quote.

Transcripts are grouped into phrases by silence gaps and speaker changes, so you can instantly locate any quote in the original recording by its timestamp — whether you're filing a story on deadline or coding interview data for a research paper.

## ⚡ Transcription Engines

### Local (Free, Private — Default)

Uses OpenAI Whisper `small` running entirely on your CPU. No data ever leaves your machine. Best for sensitive interview data or fieldwork without reliable internet.

- **Cost:** $0.00
- **Speed:** Slower (roughly 1–4× real-time depending on your hardware)
- **Privacy:** Complete — audio never leaves your computer

### Groq Cloud (Fast, Low-Cost)

Uses Whisper Large-V3 Turbo via the [Groq API](https://console.groq.com/keys) — the same model quality as OpenAI's Whisper, at a fraction of the price, running at up to **164× real-time** speed.

- **Cost:** ~$0.04/hour of audio (Whisper Large-V3 Turbo)
- **Speed:** Near-instant — a 1-hour interview transcribes in under a minute
- **Privacy:** Audio is sent to Groq's servers for processing

To enable: rename `.env.example` → `.env`, add your Groq API key, and restart the app.

## 💰 Cost Comparison (2026)

For a typical qualitative project with **10 hours of interview audio**:

| Tool | Model | Cost for 10 hrs | Notes |
|---|---|---|---|
| **InterScriber (Local)** | Whisper Small | **$0.00** | Free, runs on your CPU |
| **InterScriber (Groq Turbo)** | Whisper Large-V3 Turbo | **~$0.40** | Pay only for what you use |
| **InterScriber (Groq)** | Whisper Large-V3 | **~$1.11** | Higher accuracy option |
| Rev.ai | AI transcription | ~$1.80 | API pricing, no subscription needed |
| OpenAI Whisper API | Whisper | ~$3.60 | $0.36/hr |
| Otter.ai Pro | Proprietary | **$8.33/mo minimum** | 1,200 min/mo cap (~20 hrs); subscription even if you transcribe one file |
| Otter.ai Business | Proprietary | **$19.99/user/mo** | 6,000 min/mo cap |
| Trint | Proprietary | ~$175 | ~$17.50/hr pay-as-you-go; subscription plans start ~$80/mo for 7 files |

Otter.ai and Trint charge subscription fees regardless of how much you transcribe. InterScriber via Groq is pay-as-you-go — you pay only for the audio you actually process, with no monthly commitment.

## 🔒 Privacy

**Local by default.** Unless you add a Groq API key and select "Groq Cloud" in the UI, your audio never leaves your computer. This matters for journalists protecting sources, and for researchers handling sensitive interviews, vulnerable participants, or IRB data requirements.

When using Groq Cloud, audio is transmitted to and processed on Groq's servers. Review [Groq's privacy policy](https://groq.com/privacy-policy/) before processing confidential material.

## 📂 Project Structure

- `app.py` — Streamlit web UI
- `tools/transcribe_groq.py` — Groq Cloud transcription
- `tools/transcribe_whisper.py` — Local Whisper transcription
- `tools/pack_transcripts.py` — Converts raw JSON to readable Markdown
- `transcripts/` — Word-level JSON transcripts (the durable archive)
- `takes_packed.md` — Final human-readable transcript with timestamps
