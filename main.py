from core.downloader import download_video

if __name__ == "__main__":
    video_url = input("Enter video URL: ")
    try:
        saved_path = download_video(video_url)
        print(f"Success! Video saved to: {saved_path}")
    except Exception as e:
        print(f"An error occurred: {e}")