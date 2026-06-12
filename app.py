import os
import streamlit as st
from core.downloader import download_video
from pipeline.processor import extract_audio

st.set_page_config(
    page_title="AI Video Data Pipeline", 
    page_icon="🎬", 
    layout="centered"
)

st.title("🎬 AI Video Downloader & Pipeline")
st.markdown("Download videos, extract audio, and prepare data for AI processing.")
st.divider()

video_url = st.text_input("Enter Video URL (YouTube, TikTok, Twitter, etc.)", placeholder="https://www.youtube.com/...")
extract_audio_toggle = st.toggle("Extract Audio for Speech-to-Text (Whisper AI)")

if st.button("Process Video", type="primary"):
    if not video_url:
        st.warning("Please enter a valid URL.")
    else:
        with st.status("Initializing Pipeline...", expanded=True) as status:
            try:
                st.write("📥 Downloading video file...")
                saved_video_path = download_video(video_url)
                
                
                if saved_video_path and os.path.exists(saved_video_path):
                    st.write(f"✅ Video saved: `{saved_video_path}`")
                    
                    if extract_audio_toggle:
                        st.write("🎵 Extracting audio track...")
                        saved_audio_path = extract_audio(saved_video_path)
                        
                        if saved_audio_path and os.path.exists(saved_audio_path):
                            st.write(f"✅ Audio extracted: `{saved_audio_path}`")
                            
                    status.update(label="Pipeline Complete!", state="complete", expanded=False)
                    st.success("Successfully processed the video!")
                else:
                    status.update(label="Pipeline Failed", state="error", expanded=True)
                    st.error("Failed to download the video. Check the URL.")
            
            except Exception as e:
                status.update(label="Pipeline Failed", state="error", expanded=True)
                st.error(f"An error occurred: {e}")