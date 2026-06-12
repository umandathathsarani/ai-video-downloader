import os
from core.downloader import download_video
from pipeline.processor import extract_audio
from database.mongo_client import VideoDatabase

if __name__ == "__main__":
    print("=== AI Video Downloader & Processor ===")
    
    db = VideoDatabase()
    db_connected = db.connect()

    video_url = input("\nEnter video URL: ")
    
    try:
        saved_video_path = download_video(video_url)
        print(f"Success! Video saved to: {saved_video_path}")

        saved_audio_path = None
        user_choice = input("\nDo you want to extract audio for AI processing? (y/n): ").lower()
        if user_choice == 'y':
            saved_audio_path = extract_audio(saved_video_path)
            if saved_audio_path:
                print(f"Success! Audio extracted to: {saved_audio_path}")

        if db_connected:
            video_title = os.path.splitext(os.path.basename(saved_video_path))[0]
            
            print("\nLogging to database...")
            db.log_video(
                url=video_url, 
                title=video_title, 
                video_path=saved_video_path, 
                audio_path=saved_audio_path
            )
            
    except Exception as e:
        print(f"An error occurred: {e}")