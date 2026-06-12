import os
import argparse
from core.downloader import download_video
from pipeline.processor import extract_audio
from database.mongo_client import VideoDatabase

def process_video(url, db, db_connected, extract_audio_flag=False):
    """Handles the full pipeline for a single video URL."""
    try:
        print(f"\n--- Processing: {url} ---")
        saved_video_path = download_video(url)
        print(f"Success! Video saved to: {saved_video_path}")
        
        saved_audio_path = None
        if extract_audio_flag:
            saved_audio_path = extract_audio(saved_video_path)
            if saved_audio_path:
                print(f"Success! Audio extracted to: {saved_audio_path}")
                
        if db_connected:
            video_title = os.path.splitext(os.path.basename(saved_video_path))[0]
            print("Logging to database...")
            db.log_video(
                url=url, 
                title=video_title, 
                video_path=saved_video_path, 
                audio_path=saved_audio_path
            )
    except Exception as e:
        print(f"Failed to process {url}. Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Video Downloader Pipeline")
    parser.add_argument("--batch", type=str, help="Path to a text file containing video URLs (one per line)")
    parser.add_argument("--audio", action="store_true", help="Automatically extract audio for all videos")
    args = parser.parse_args()

    print("=== AI Video Downloader & Processor ===")
    db = VideoDatabase()
    db_connected = db.connect()

    if args.batch:
        if not os.path.exists(args.batch):
            print(f"Batch file not found: {args.batch}")
        else:
            with open(args.batch, 'r') as file:

                urls = [line.strip() for line in file if line.strip()]
                
            print(f"Found {len(urls)} URLs in batch file. Starting batch run...")
            for url in urls:
                process_video(url, db, db_connected, args.audio)

    else:
        video_url = input("\nEnter video URL: ")
        user_choice = input("Do you want to extract audio for AI processing? (y/n): ").lower()
        extract_flag = (user_choice == 'y')
        process_video(video_url, db, db_connected, extract_flag)