# YouTube Video Analysis Tool

A powerful full-stack application that combines React and Python to analyze YouTube videos using AI. The application provides multiple features for processing and interacting with video content.

## Features

- **Video Transcription**: Transcribe YouTube videos using OpenAI's Whisper model
- **Video Summarization**: Generate concise summaries of video content using Ollama
- **Top Words Analysis**: Identify and display the most frequently used words in videos
- **Text Completion Exercise**: Create interactive exercises by hiding words from the transcript
- **Interactive Chat**: Ask questions about the video content with AI-powered responses

## Tech Stack

### Frontend
- React
- React Bootstrap
- React Router
- Axios for API calls

### Backend
- Flask
- OpenAI Whisper for transcription
- Ollama for LLM capabilities
- PyTubeFix for YouTube video processing

## Getting Started

### Frontend Setup
1. Navigate to the `frontend` directory
2. Install dependencies:
```bash
npm install
```
3. Start the development server:
```bash
npm start
```

### Backend Setup
1. Navigate to the `backend` directory
2. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate.bat
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Start the Flask server:
```bash
python app.py
```

## Environment Requirements
### Frontend

- Node.js
- npm

### Backend
- Python 3.x
- CUDA-compatible GPU (recommended for Whisper)
- FFmpeg
- Ollama server running locally

## Environment Variables
### Backend

Create a `.env` file in the backend directory:
```bash
MODEL_NAME=llama3.1
```

## License
MIT License