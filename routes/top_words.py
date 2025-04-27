from flask import Blueprint, request, jsonify
from services.youtube_service import download_audio
from services.whisper_service import analyze_audio
import os
import torch

top_words_bp = Blueprint('top_words', __name__)

@top_words_bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        youtube_url = data.get('url')
        
        if not youtube_url:
            return jsonify({'error': 'URL de YouTube no proporcionada'}), 400
        
        # Descargar el audio
        audio_path = download_audio(youtube_url)
        
        try:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Analizar el audio
            top_words = analyze_audio(audio_path,device=device)
            
            # Limpiar el archivo temporal
            os.remove(audio_path)
            os.rmdir(os.path.dirname(audio_path))
            
            return jsonify({
                'top_words': [{'word': word, 'count': count} for word, count in top_words]
            })
        except Exception as e:
            # Asegurarse de limpiar los archivos temporales incluso si hay un error
            if os.path.exists(audio_path):
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400 