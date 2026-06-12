# Video Processing Hub 🎬

## Overview

The **Video Processing Hub** is a robust, local data ingestion engine designed to streamline the foundational stages of artificial intelligence development. It provides an automated, network-resilient pipeline that extracts media from major platforms (YouTube, TikTok, etc.), separates clean audio tracks, and prepares structured datasets ready for downstream Natural Language Processing (NLP) or Computer Vision tasks.

Built with a focus on fault tolerance, the hub intelligently bypasses common network throttles and features a graceful **Offline Mode** to ensure continuous operation even when deployed on restrictive corporate or university networks.

---

## Key Features

### 🚀 Automated Media Ingestion

Seamlessly download high-quality video content using a custom-configured **yt-dlp** engine.

### 🎧 AI-Ready Audio Extraction

Automatically strip and format MP3 audio tracks using **moviepy**, optimizing files for Speech-to-Text models like **OpenAI Whisper**.

### 🌐 Network Resilience & Offline Mode

Built-in retry logic catches dropped connections and throttled chunks. If cloud database ports are blocked by strict firewalls, the system automatically falls back to a local-only **Offline Mode** without crashing.

### ☁️ Cloud Database Synchronization

When online, automatically logs video metadata, local file paths, and processing status to a **MongoDB Atlas** cluster.

### 🖥️ Interactive UI

A clean, responsive single-page web dashboard built with **Streamlit** for easy pipeline management.

---

## Tech Stack

| Component        | Technology                       |
| ---------------- | -------------------------------- |
| Frontend         | Streamlit                        |
| Backend          | Python 3                         |
| Media Processing | yt-dlp, moviepy, FFmpeg          |
| AI Integration   | OpenAI Whisper (Local Execution) |
| Database         | MongoDB Atlas, pymongo, certifi  |

---

## Prerequisites

Before running the application, ensure you have the following installed on your system:

* Python 3.8+ (Tested on Python 3.11)
* FFmpeg (Required for audio extraction and Whisper transcription)
* MongoDB Atlas account and cluster

---

## Installation & Setup

### 1. Clone the Repository

Open your terminal and navigate to your desired workspace, then clone the project:

```bash
git clone https://github.com/umandathathsarani/ai-video-downloader.git
cd ai-video-downloader
```

### 2. Install Python Dependencies

Ensure your environment is set up with the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your secure MongoDB connection string:

```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```

---

## Usage

### Launching the Dashboard

To start the application, run the following command in your terminal:

```bash
streamlit run app.py
```

This will initialize the local server and open the web dashboard in your default browser.

### Using the Pipeline

1. Copy a valid video URL from a supported platform.
2. Paste the URL into the **Media URL** input field on the dashboard.
3. Toggle **Extract Audio (MP3)** depending on your dataset requirements.
4. Click **Process Video**.
5. The system will securely download the highest quality format, extract the requested files, and save them to the local `/downloads` directory while syncing metadata to the cloud.

---

## System Architecture Notes

### Strict Network Environments

If you are running this tool on a restricted network (e.g., a university campus), the system may fail the initial SSL handshake with MongoDB. The application will detect this `ServerSelectionTimeoutError` and automatically boot into **Offline Mode**.

In Offline Mode:

* ✅ Videos are downloaded successfully.
* ✅ Audio extraction continues normally.
* ✅ Local file storage remains fully functional.
* ⚠️ Cloud synchronization is temporarily paused until connectivity is restored.

This ensures uninterrupted dataset collection and preprocessing regardless of network restrictions.

---

## Project Structure

```text
ai-video-downloader/
│
├── app.py
├── requirements.txt
├── .env
├── downloads/
│   ├── videos/
│   └── audio/
│
├── services/
│   ├── downloader.py
│   ├── audio_extractor.py
│   ├── database.py
│   └── whisper_processor.py
│
└── README.md
```

---

## License

This project is intended for educational, research, and AI dataset preparation purposes. Ensure compliance with the terms of service of the platforms from which content is downloaded.
