import os
import pandas as pd
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
    """Connects to MongoDB once and caches the connection for app speed."""
    db = VideoDatabase()
    try:
        db.connect()
    except Exception as e:
        st.toast("⚠️ Network blocking database. Running in Offline Mode.")
        print(f"Database connection failed: {e}")
    return db

db = init_db()

st.title("🎬 Video Processing Hub")
st.markdown("Download media, extract audio tracks, and manage your AI-ready datasets.")
st.divider()

tab_process, tab_database = st.tabs(["📥 Process New Media", "🗄️ Database Archive"])

with tab_process:
    with st.expander("📖 Quick Start Guide", expanded=False):
        st.markdown("""
        ### How it works:
        1. **Get your link:** Copy a video URL from your source platform.
        2. **Choose settings:** Paste the URL below and select if you need the audio track extracted.
        3. **Process:** Click **Process Video**. 
        4. **Access files:** Find your processed files in the local `/downloads` folder.
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
                            st.write("☁️ Logging to database...")
                            title = os.path.splitext(os.path.basename(saved_video_path))[0]
                            db.log_video(video_url, title, saved_video_path, saved_audio_path)
                                
                        status.update(label="Processing Complete!", state="complete", expanded=False)
                        st.success("Your files are ready and logged to the database!")
                    else:
                        status.update(label="Download Failed", state="error", expanded=True)
                        st.error("Failed to download the media. Please verify the URL and your network connection.")
                
                except Exception as e:
                    status.update(label="System Error", state="error", expanded=True)
                    st.error(f"An unexpected error occurred: {e}")

with tab_database:
    st.subheader("Cloud Data Archive")
    st.markdown("View and manage all media records synced to MongoDB Atlas.")
    
    col_refresh, col_empty = st.columns([1, 5])
    with col_refresh:
        refresh = st.button("🔄 Refresh Data")
    
    videos_data = db.get_all_videos()
    
    if not videos_data:
        st.info("No records found in the database. Process a video to start building your dataset.")
    else:
        df = pd.DataFrame(videos_data)
    
        if "_id" in df.columns:
            df = df.drop(columns=["_id"]) 

        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "original_url": st.column_config.LinkColumn("Source URL"),
                "title": "Media Title",
                "status": "Pipeline Status",
                "video_file_path": "Local Video Path",
                "audio_file_path": "Local Audio Path",
                "transcript": "AI Transcript"
            },
            hide_index=True
        )