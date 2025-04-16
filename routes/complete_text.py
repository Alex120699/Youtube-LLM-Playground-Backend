from flask import Blueprint, request, jsonify
from services.youtube_service import download_audio
from services.whisper_service import transcribe_audio
import os
import random

complete_text_bp = Blueprint('complete_text', __name__)

@complete_text_bp.route('/get-text', methods=['POST'])
def get_text():
    try:
        data = request.get_json()
        youtube_url = data.get('url')
        
        if not youtube_url:
            return jsonify({'error': 'URL de YouTube no proporcionada'}), 400
        
        # Descargar el audio
        audio_path = download_audio(youtube_url)
        
        try:
            # Transcribir el audio
            text = transcribe_audio(audio_path)
            words = text.split()
            
            # Seleccionar 10% de las palabras al azar para ocultar
            num_words_to_hide = max(1, int(len(words) * 0.05))
            hidden_indices = random.sample(range(len(words)), num_words_to_hide)
            
            # Crear la versión del texto con palabras ocultas y guardar las palabras originales
            hidden_words = {}
            for idx in hidden_indices:
                hidden_words[idx] = words[idx]
                words[idx] = '_____'
            
            # Limpiar el archivo temporal
            os.remove(audio_path)
            os.rmdir(os.path.dirname(audio_path))
            
            return jsonify({
                'text': ' '.join(words),
                'hidden_words': hidden_words
            })
        except Exception as e:
            # Asegurarse de limpiar los archivos temporales incluso si hay un error
            if os.path.exists(audio_path):
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@complete_text_bp.route('/validate', methods=['POST'])
def validate():
    try:
        data = request.get_json()
        user_answers = data.get('answers', {})
        correct_words = data.get('hidden_words', {})
        
        if not user_answers or not correct_words:
            return jsonify({'error': 'Respuestas o palabras correctas no proporcionadas'}), 400
        
        # Convertir índices de string a int para la comparación
        correct_words = {int(k): v.lower() for k, v in correct_words.items()}
        user_answers = {int(k): v.lower() for k, v in user_answers.items()}
        
        # Calcular aciertos
        correct_count = sum(1 for idx in correct_words if correct_words[idx] == user_answers.get(idx, ''))
        total_words = len(correct_words)
        
        # Calcular porcentaje y score
        percentage = (correct_count / total_words) * 100
        score = int(percentage * 10)  # Score de 0 a 1000
        
        return jsonify({
            'percentage': round(percentage, 2),
            'score': score,
            'correct_count': correct_count,
            'total_words': total_words,
            'correct_answers': correct_words
        })
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400 