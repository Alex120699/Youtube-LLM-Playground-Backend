from flask import Blueprint, request, jsonify
from services.youtube_service import download_audio
from services.whisper_service import transcribe_audio
from services.summarizer import summarize_with_ollama
import os
import time  # Importa time para medir duración

summarize_bp = Blueprint('summarize', __name__)

@summarize_bp.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        youtube_url = data.get('url')
        
        if not youtube_url:
            return jsonify({'error': 'URL de YouTube no proporcionada'}), 400
        
        # ⏱ Inicio del proceso
        total_start = time.time()

        # Descargar el audio
        print("Downloading Audio...")
        start_download = time.time()
        audio_path = download_audio(youtube_url)
        end_download = time.time()
        print(f"✅ Audio descargado en {end_download - start_download:.2f} segundos")

        try:
            print("Transcribing audio...")
            start_transcription = time.time()
            text = transcribe_audio(audio_path)
            end_transcription = time.time()
            print(f"✅ Transcripción completada en {end_transcription - start_transcription:.2f} segundos")
            
            # Limpiar el archivo temporal
            os.remove(audio_path)
            os.rmdir(os.path.dirname(audio_path))
            
            print("Writing the summary...")
            start_summary = time.time()
            summarized_text = summarize_with_ollama(text)
            end_summary = time.time()
            print(f"✅ Resumen generado en {end_summary - start_summary:.2f} segundos")

            return jsonify({
                'summary': summarized_text
            })
        except Exception as e:
            # Asegurarse de limpiar los archivos temporales incluso si hay un error
            if os.path.exists(audio_path):
                os.remove(audio_path)
                os.rmdir(os.path.dirname(audio_path))
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400 