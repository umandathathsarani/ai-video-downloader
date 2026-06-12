# Video Processing Hub 🎬

## Overview

The **Video Processing Hub** is a robust, local data ingestion engine designed to streamline the foundational stages of artificial intelligence development. It provides an automated, network-resilient pipeline that extracts media from major platforms (YouTube, TikTok, etc.), separates clean audio tracks, and prepares structured datasets ready for downstream Natural Language Processing (NLP) or Computer Vision tasks.

Built with a focus on fault tolerance, the hub intelligently bypasses common network throttles and features a graceful **Offline Mode** to ensure continuous operation even when deployed on restrictive corporate or university networks.

---

## Key Features

### 🚀 Automated Media Ingestion

Seamlessly download high-quality video content using a custom-configured **yt-dlp** engine.

### 🎵 AI-Ready Audio Extraction

Automatically strip and format MP3 audio tracks using **moviepy**, optimizing files for Speech-to-Text models like **OpenAI Whisper**.

### 🌐 Network Resilience & Offline Mode

Built-in retry logic catches dropped connections and throttled chunks. If cloud database ports are blocked by strict firewalls, the system automatically falls back to a local-only **Offline Mode** without crashing.

### ☁️ Cloud Database Synchronization

When online, automatically logs video metadata, local file paths, and processing status to a **MongoDB Atlas** cluster.

### 🖥️ Interactive UI

A clean, responsive single-page web dashboard built with **Streamlit** for easy pipeline management.

---

## Tech Stack

| Layer            | Technology                       |
| ---------------- | -------------------------------- |
| Frontend         | Streamlit                        |
| Backend          | Python 3                         |
| Media Processing | yt-dlp, moviepy, FFmpeg          |
| AI Integration   | OpenAI Whisper (Local Execution) |
| Database         | MongoDB Atlas, pymongo, certifi  |

---

## Project Structure

```plaintext
ai-video-downloader/
├── app.py             # Main Streamlit dashboard
├── core/              # Downloader logic
├── database/          # MongoDB client and schemas
├── pipeline/          # Audio processing modules
├── .env               # Environment variables
└── requirements.txt   # Project dependencies
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/umandathathsarani/ai-video-downloader.git
cd ai-video-downloader
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory and add your MongoDB connection string:

```env
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
```

---

## Usage

### Launch the Dashboard

```bash
streamlit run app.py
```

### Processing a Video

1. Copy a valid video URL from a supported platform.
2. Paste the URL into the **Media URL** field.
3. Toggle **Extract Audio (MP3)** if required.
4. Click **Process Video**.
5. The system will download, process, and store the media while syncing metadata to MongoDB Atlas when online.

---

## Troubleshooting

### SSL Handshake Errors

If running on a restricted network, ensure your `certifi` package is updated.

The system will automatically detect blocked MongoDB connections and enter **Offline Mode**, allowing local downloads and processing to continue without interruption.

### JavaScript Runtime Issues

If **yt-dlp** reports a missing JavaScript runtime, install **Deno** to ensure uninterrupted video extraction and metadata processing.

---

## Roadmap & Future Improvements

### Phase 2

Integrate **OpenAI Whisper** for automatic, high-accuracy transcript generation directly within the dashboard.

### Phase 3

Add batch processing support to allow users to ingest large lists of URLs in a single processing queue.

### Phase 4

Introduce Docker containerization to simplify deployment across Windows, Linux, and macOS environments.

---

## Credits & Acknowledgments

This project utilizes the power of open-source software. Special thanks to the maintainers of:

* **yt-dlp** for advanced video extraction.
* **Streamlit** for enabling rapid UI development.
* **moviepy** for robust media manipulation.
* **pymongo** for seamless cloud database integration.

---

## Copyright & Usage Notice

**© 2026 Mummullage Binuri Umanda Thathsarani. All rights reserved.**

This source code and the accompanying documentation are the intellectual property of the author. Unauthorized copying, distribution, modification, or reproduction of this content, in whole or in part, without explicit written permission from the owner is strictly prohibited.

For inquiries regarding licensing, collaboration, or usage permissions, please contact the author directly.

---

## Disclaimer

This tool is intended for educational, research, and AI dataset preparation purposes. Users are responsible for ensuring compliance with the Terms of Service, copyright regulations, and content usage policies of any platforms from which media is downloaded.
