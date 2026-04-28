# 🎙️ InterScriber

![Python](https://img.shields.io/badge/python-3.11+-blue?style=flat-square)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey?style=flat-square)
![Built with Streamlit](https://img.shields.io/badge/built%20with-Streamlit-FF4B4B?style=flat-square&logo=streamlit)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)

**Low-cost, privacy-first transcription for journalists and qualitative researchers.**

Drop in your interview recording. Get back a clean, timestamped transcript in minutes — for pennies on the dollar compared to subscription services, or completely free using your own machine.

Built for professionals who transcribe regularly and are tired of paying Otter.ai $8–$20/month whether they use it or not.

---

## Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Transcription Engines](#-transcription-engines)
- [Cost Comparison](#-cost-comparison)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Privacy](#-privacy)
- [Built With](#-built-with)
- [AI Collaboration](#-ai-collaboration)
- [License](#-license)

---

## ✨ Features

- **Two engines** — run entirely offline (free) or use Groq Cloud for near-instant results
- **Timestamped phrases** — every line tagged with `[MM:SS–MM:SS]` so you can find any quote in the original recording
- **Multi-speaker support** — phrases are labelled by speaker when multiple voices are detected
- **No subscription** — pay only for what you transcribe, or nothing at all
- **Privacy by default** — local mode never sends audio to any server
- **Works with any format** — `.mp4`, `.mov`, `.wav`, `.m4a`, `.mp3`
- **One-click setup** — launcher script handles environment, dependencies, and launch automatically

---

## 🚀 Quick Start

**Prerequisites:** [Python 3.11+](https://python.org) and [ffmpeg](https://ffmpeg.org)

```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg

# Windows — download from https://ffmpeg.org/download.html and add to PATH
```

**Then run:**

```bash
# macOS / Linux
./run.sh

# Windows
run.bat
```

The launcher creates a virtual environment, installs all dependencies, and opens the web UI in your browser. No manual setup required.

---

## ⚡ Transcription Engines

### Local — Free & Private (Default)

Uses OpenAI Whisper `small` running on your CPU. No data ever leaves your machine. Ideal for sensitive interviews, source protection, or fieldwork without reliable internet.

| | |
|---|---|
| Cost | **$0.00** |
| Speed | 1–4× real-time (depends on hardware) |
| Privacy | Complete — audio stays on your machine |

### Groq Cloud — Fast & Low-Cost

Uses Whisper Large-V3 Turbo via the [Groq API](https://console.groq.com/keys), running at up to **164× real-time**. A 1-hour interview transcribes in under a minute.

| | |
|---|---|
| Cost | **~$0.04/hr** (Turbo) or **~$0.111/hr** (Large-V3) |
| Speed | Near-instant |
| Privacy | Audio processed on Groq's servers |

**To enable Groq:** rename `.env.example` → `.env`, paste your API key, and restart the app.

---

## 💰 Cost Comparison (2026)

For a typical project with **10 hours of interview audio**:

| Service | Engine | 10 hrs cost | Model |
|---|---|---|---|
| **InterScriber Local** | Whisper Small | **$0.00** | On-device |
| **InterScriber + Groq Turbo** | Whisper Large-V3 Turbo | **~$0.40** | Pay-per-use |
| **InterScriber + Groq** | Whisper Large-V3 | **~$1.11** | Pay-per-use |
| Rev.ai | AI | ~$1.80 | API, no subscription |
| OpenAI Whisper API | Whisper | ~$3.60 | Pay-per-use |
| **Otter.ai Pro** | Proprietary | **$8.33/mo minimum** | Subscription, 20 hr cap |
| **Otter.ai Business** | Proprietary | **$19.99/user/mo** | Subscription, 100 hr cap |
| **Trint** | Proprietary | **~$175** | ~$17.50/hr pay-as-you-go |

> Otter.ai and Trint charge subscription fees whether you transcribe one file or a hundred. InterScriber via Groq is strictly pay-per-use — no monthly commitment, no wasted spend.

---

## 🛠️ How It Works

1. **Upload** your audio or video file in the web UI
2. **Choose** your engine — local (free) or Groq Cloud (fast)
3. **Wait** — transcription runs in the background with a live progress indicator
4. **Read & download** — phrases are grouped by silence gaps and speaker changes, each tagged with a precise timestamp

The transcript is saved as a Markdown file you can open in any text editor, paste into your notes app, or attach to a story file.

---

## 📂 Project Structure

```
interscriber/
├── app.py                      # Streamlit web UI
├── tools/
│   ├── transcribe_groq.py      # Groq Cloud transcription
│   ├── transcribe_whisper.py   # Local Whisper transcription
│   └── pack_transcripts.py     # Converts JSON → readable Markdown
├── transcripts/                # Word-level JSON (the durable archive)
├── raw/                        # Temp staging — files deleted after transcription
├── takes_packed.md             # Final human-readable transcript
├── .env.example                # API key template
├── requirements.txt
├── run.sh                      # macOS/Linux launcher
└── run.bat                     # Windows launcher
```

---

## 🔒 Privacy

**Local mode is fully private.** Your audio never touches a server.

This matters for:
- **Journalists** protecting sources and unpublished material
- **Researchers** handling sensitive interviews, vulnerable participants, or IRB data requirements

When using Groq Cloud, audio is sent to Groq's servers for processing. Review [Groq's privacy policy](https://groq.com/privacy-policy/) before processing confidential material.

---

## 🔧 Built With

- [Streamlit](https://streamlit.io) — web UI
- [OpenAI Whisper](https://github.com/openai/whisper) — local speech recognition
- [Groq API](https://groq.com) — cloud inference (Whisper Large-V3 Turbo)
- [ffmpeg](https://ffmpeg.org) — audio extraction and conversion

---

## 🤝 AI Collaboration

This project was built collaboratively with AI coding assistants:

- **[Anthropic Claude Code](https://claude.ai/code)** — architecture, debugging, feature implementation, and code review throughout the project
- **[Google Gemini CLI](https://github.com/google-gemini/gemini-cli)** — research, ideation, and development support

InterScriber is an example of what's possible when human domain expertise (journalism, qualitative research) is paired with AI-assisted development.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Sources: [Otter.ai pricing](https://tldv.io/blog/otter-pricing/) · [Trint pricing](https://brasstranscripts.com/blog/trint-pricing-2025-premium-journalism-media-costs) · [Groq Whisper pricing](https://groq.com/blog/whisper-large-v3-turbo-now-available-on-groq-combining-speed-quality-for-speech-recognition) · [Whisper API comparison](https://tokenmix.ai/blog/whisper-api-pricing)*
