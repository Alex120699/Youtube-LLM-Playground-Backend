from flask import Blueprint, request, jsonify
from services.youtube_service import download_audio
from services.whisper_service import transcribe_audio
from services.summarizer import summarize_with_ollama
import os
import time  # Importa time para medir duración
import torch

transcribe_bp = Blueprint('transcribe', __name__)

@transcribe_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        ip = request.remote_addr
        print(f"Conexión desde: {ip}")
        data = request.get_json()
        youtube_url = data.get('url')

        if not youtube_url:
            return jsonify({'error': 'URL de YouTube no proporcionada'}), 400

        print("Downloading Audio...")
        audio_path = download_audio(youtube_url)

        try:
            print("Transcribing audio...")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            transcript = transcribe_audio(audio_path,device=device)

            os.remove(audio_path)
            os.rmdir(os.path.dirname(audio_path))

            return jsonify({'text': transcript})

        except Exception as e:
            if os.path.exists(audio_path):
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            raise e

    except Exception as e:
        return jsonify({'error': str(e)}), 400
