import os
import subprocess
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

RAW_DIR = Path("raw")
TRANSCRIPTS_DIR = Path("transcripts")
PACKED_FILE = Path("takes_packed.md")

RAW_DIR.mkdir(exist_ok=True)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="InterScriber", page_icon="🎙️")

st.title("🎙️ InterScriber")
st.markdown("""
Turn interview audio/video into precise, timestamped, quotable transcripts.
1. **Drop** your file below.
2. **Select** your transcription engine.
3. **Wait** for transcription.
4. **Download** your packed markdown transcript.
""")

has_groq_key = bool(os.environ.get("GROQ_API_KEY"))
engine_options = ["Local (Free, Slower)"]
if has_groq_key:
    engine_options.append("Groq Cloud (Fast, Requires API Key)")

engine = st.radio("Transcription Engine", options=engine_options)

uploaded_file = st.file_uploader("Choose an audio or video file", type=["mp4", "mov", "wav", "m4a", "mp3"])

if uploaded_file is not None:
    safe_name = os.path.basename(uploaded_file.name)
    file_path = RAW_DIR / safe_name
    transcript_path = TRANSCRIPTS_DIR / (Path(safe_name).stem + ".json")

    already_transcribed = transcript_path.exists()
    if already_transcribed:
        st.info(f"Transcript already exists for **{safe_name}**. Click below to use it, or force re-transcription.")
        force_retranscribe = st.checkbox("Re-transcribe (overwrites existing)", value=False)
    else:
        force_retranscribe = False

    if st.button("Start Transcription", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Stage 1: Save uploaded file to disk
            status_text.text("💾 Saving file...")
            progress_bar.progress(5)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            progress_bar.progress(10)

            # Stage 2: Transcribe (the slow stage)
            if not already_transcribed or force_retranscribe:
                engine_label = "Groq Cloud" if "Groq" in engine else "local Whisper"
                status_text.text(f"⏳ Transcribing with {engine_label} — this is the slow step, please wait...")
                progress_bar.progress(15)

                script = "tools/transcribe_groq.py" if "Groq" in engine else "tools/transcribe_whisper.py"
                subprocess.run(["python3", script, str(file_path)], check=True)
            else:
                status_text.text(f"⏭️ Skipping transcription — using existing transcript for {safe_name}.")

            progress_bar.progress(75)

            # Stage 3: Clean up the raw file — transcript JSON is the durable artifact
            try:
                file_path.unlink(missing_ok=True)
            except OSError:
                pass  # non-fatal; raw/ cleanup is best-effort

            progress_bar.progress(80)

            # Stage 4: Pack only this file's transcript — not everything in the folder
            status_text.text("📦 Packing transcript...")
            subprocess.run(
                ["python3", "tools/pack_transcripts.py",
                 "--edit-dir", ".",
                 "--files", str(transcript_path)],
                check=True,
            )

            progress_bar.progress(95)

            # Stage 5: Display result
            status_text.text("✅ Done!")
            progress_bar.progress(100)

            if PACKED_FILE.exists():
                st.divider()
                st.subheader("Final Transcript")
                content = PACKED_FILE.read_text()
                st.markdown(content)

                st.download_button(
                    label="Download Transcript (.md)",
                    data=content,
                    file_name=f"{Path(safe_name).stem}_transcript.md",
                    mime="text/markdown",
                )

        except subprocess.CalledProcessError as e:
            st.error(f"Subprocess failed (return code {e.returncode}). Check terminal output for details.")
            status_text.text("❌ Failed.")
        except Exception as e:
            st.error(f"Error: {e}")
            status_text.text("❌ Failed.")

st.divider()
if "Groq" in engine:
    st.caption("Audio is sent to Groq for ultra-fast transcription.")
else:
    st.caption("All processing is local. No data is sent to external servers.")
