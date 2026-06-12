import os
import whisper

def transcribe_audio(audio_path, model_size="base"):
    """
    Loads a local Whisper model and transcribes the given audio file.
    """
    if not audio_path or not os.path.exists(audio_path):
        print("Audio file not found for transcription.")
        return None

    print(f"\nLoading Whisper '{model_size}' model (this may take a moment)...")
    try:
        model = whisper.load_model(model_size)
        
        print("Transcribing audio...")
    
        result = model.transcribe(audio_path)
        
        text = result["text"].strip()
        return text
        
    except Exception as e:
        print(f"Transcription failed: {e}")
        return None