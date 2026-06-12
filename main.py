from core.downloader import download_video
from pipeline.processor import extract_audio

if __name__ == "__main__":
    print("=== AI Video Downloader & Processor ===")
    video_url = input("Enter video URL: ")
    
    try:
        saved_video_path = download_video(video_url)
        print(f"Success! Video saved to: {saved_video_path}")
        
        user_choice = input("\nDo you want to extract audio for AI processing? (y/n): ").lower()
        if user_choice == 'y':
            saved_audio_path = extract_audio(saved_video_path)
            if saved_audio_path:
                print(f"Success! Audio extracted to: {saved_audio_path}")
                
    except Exception as e:
        print(f"An error occurred: {e}")