import os
import streamlit as st
from core.downloader import download_video
from pipeline.processor import extract_audio
from database.mongo_client import VideoDatabase

st.set_page_config(
    page_title="Video Processing Hub", 
    page_icon="🎬", 
    layout="wide", 
    initial_sidebar_state="collapsed" 
)

@st.cache_resource
def init_db():
    db = VideoDatabase()
    db.connect()
    return db

db = init_db()

st.title("🎬 Video Processing Hub")
st.markdown("""
Welcome to the Video Processing Hub, a comprehensive local data ingestion engine designed to streamline the foundational stages of artificial intelligence development. In the modern machine learning landscape, acquiring and preprocessing high-quality datasets is often the most significant bottleneck. 

This platform solves that challenge by providing an automated, network-resilient pipeline that effortlessly extracts media from major platforms, separates clean audio tracks, and prepares structured data ready for advanced natural language processing or computer vision tasks. Whether you are building custom transcription models, analyzing sentiment, or compiling large-scale media archives, this hub ensures your data is standardized, accessible, and securely managed on your local system.
""")
st.divider()

with st.expander("📖 Comprehensive Usage Guide", expanded=False):
    st.markdown("""
    ### Step-by-Step Execution:
    
    1. **Source Identification:** Begin by locating your target media on supported platforms such as YouTube, TikTok, or Twitter. Copy the full, direct URL from your browser's address bar.
    
    2. **Pipeline Configuration:** Paste the copied URL into the 'Media URL' input field located in the dashboard. Determine your specific data requirements for this run; if your downstream AI models require speech-to-text processing or audio analysis, ensure the 'Extract Audio (MP3)' toggle remains active.
    
    3. **Execution & Resilience:** Initialize the pipeline by clicking the 'Process Video' button. The underlying system utilizes a fault-tolerant engine that automatically handles network instability, intelligently bypasses common platform rate limits, and secures the highest available quality format without requiring manual intervention.
    
    4. **Local Data Retrieval:** Upon successful execution, the system will verify file integrity. You can instantly access your newly ingested `.mp4` video files and `.mp3` audio tracks directly within the designated `downloads` and `downloads/audio` directories in your local workspace.
    """)

with st.container():
    st.subheader("Start a New Download")
    video_url = st.text_input("Media URL", placeholder="https://www.youtube.com/shorts/...", key="url_input")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<br>", unsafe_allow_html=True)
        extract_audio_toggle = st.toggle("🎵 Extract Audio (MP3)", value=True)
        
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        process_btn = st.button("Process Video", type="primary", use_container_width=True)

if process_btn:
    if not video_url:
        st.warning("⚠️ Please provide a valid URL.")
    else:
        with st.status("Processing your request...", expanded=True) as status:
            try:
                st.write("📥 Downloading video file...")
                saved_video_path = download_video(video_url)
                
                if saved_video_path and os.path.exists(saved_video_path):
                    st.write(f"✅ Video saved: `{os.path.basename(saved_video_path)}`")
                    
                    saved_audio_path = None
                    if extract_audio_toggle:
                        st.write("🎵 Extracting audio track...")
                        saved_audio_path = extract_audio(saved_video_path)
                        if saved_audio_path and os.path.exists(saved_audio_path):
                            st.write(f"✅ Audio extracted: `{os.path.basename(saved_audio_path)}`")
                    
                    if db.collection is not None:
                        st.write("☁️ Syncing to MongoDB...")
                        title = os.path.splitext(os.path.basename(saved_video_path))[0]
                        db.log_video(video_url, title, saved_video_path, saved_audio_path)
                        status.update(label="Processing & Sync Complete!", state="complete", expanded=False)
                        st.success("Files ready and synced to the cloud!")
                    else:
                        status.update(label="Processing Complete", state="complete", expanded=False)
                        st.success("Files successfully saved to your local directory!")
                        
                else:
                    status.update(label="Download Failed", state="error", expanded=True)
                    st.error("Failed to download the media. Please verify the URL and your network connection.")
            
            except Exception as e:
                status.update(label="System Error", state="error", expanded=True)
                st.error(f"An unexpected error occurred: {e}")