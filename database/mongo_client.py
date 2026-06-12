import os
import certifi
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

class VideoDatabase:
    def __init__(self):
        self.uri = os.getenv("MONGO_URI")
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        try:
            self.client = MongoClient(self.uri, tlsCAFile=certifi.where())
            self.db = self.client.ai_video_dataset
            self.collection = self.db.videos
            print("Successfully connected to MongoDB Atlas!")
            return True
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            return False

    def log_video(self, url, title, video_path, audio_path=None, transcript=None):
        if not self.collection is None:
            if transcript:
                status = "Transcribed"
            elif audio_path:
                status = "Audio Extracted"
            else:
                status = "Downloaded"

            video_document = {
                "original_url": url,
                "title": title,
                "video_file_path": video_path,
                "audio_file_path": audio_path,
                "transcript": transcript,
                "status": status
            }
            result = self.collection.insert_one(video_document)
            print(f"Video logged to database with ID: {result.inserted_id}")
            return result.inserted_id
        return None
    
def get_all_videos(self):
        """Fetches all video records from MongoDB, sorted by newest first."""
        if self.collection is not None:
            videos = list(self.collection.find().sort("_id", -1))
            
            for video in videos:
                video["_id"] = str(video["_id"])
            return videos
        return []