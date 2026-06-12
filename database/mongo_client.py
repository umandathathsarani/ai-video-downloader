import os
import certifi
from pymongo import MongoClient
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
            self.client = MongoClient(
                self.uri, 
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=5000
            )
            self.db = self.client.ai_video_dataset
            self.collection = self.db.videos

            self.client.admin.command('ping')
            print("Successfully connected to MongoDB Atlas!")
            return True
        except Exception as e:
            print(f"Network block detected. Running in Offline Mode. Error: {e}")
            self.collection = None 
            return False

    def log_video(self, url, title, video_path, audio_path=None, transcript=None):
        if self.collection is not None:
            try:
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
            except Exception as e:
                print(f"Failed to log to database (Network Error): {e}")
        return None

    def get_all_videos(self):
        """Fetches all video records from MongoDB, sorted by newest first."""
        if self.collection is not None:
            try:
                videos = list(self.collection.find().sort("_id", -1))

                for video in videos:
                    video["_id"] = str(video["_id"])
                return videos
            except Exception as e:
                print(f"Failed to fetch archive (Network Error): {e}")
                return []
        return []