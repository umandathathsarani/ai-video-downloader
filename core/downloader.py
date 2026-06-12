import os
import yt_dlp

def download_video(url, output_dir="downloads"):
    """
    Downloads a video from a given URL using yt-dlp.
    Includes network resilience to bypass throttling and drops.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'quiet': False,

        'retries': 10, 
        'fragment_retries': 10, 
        'extractor_retries': 3,  
        'nocheckcertificate': True, 
    }
    
    try:
        print(f"Starting download for: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
            
    except Exception as e:
        print(f"yt-dlp encountered an error: {e}")
        return None