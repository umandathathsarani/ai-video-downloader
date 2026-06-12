import os
from moviepy.editor import VideoFileClip

def extract_audio(video_path, output_dir="downloads/audio", format="mp3"):
    """
    Extracts the audio track from a video file.
    Whisper and other NLP models typically work best with .mp3 or .wav.
    """
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.basename(video_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    audio_filename = f"{file_name_without_ext}.{format}"
    audio_path = os.path.join(output_dir, audio_filename)

    print(f"Extracting audio to: {audio_path}...")
    
    try:
        video = VideoFileClip(video_path)
        audio = video.audio

        audio.write_audiofile(audio_path, logger=None)
        
        audio.close()
        video.close()
        
        return audio_path
        
    except Exception as e:
        print(f"Failed to extract audio: {e}")
        return None