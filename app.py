from flask import Flask, request, jsonify
from flask_cors import CORS
from pytubefix import YouTube
import whisper
import os
import tempfile
from collections import Counter
import re
import torch
from routes.top_words import top_words_bp
from routes.complete_text import complete_text_bp
from routes.summarize import summarize_bp
from routes.transcribe import transcribe_bp
from routes.chat_about_video import chat_bp


app = Flask(__name__)
CORS(app)#, origins=["https://youtube-llm-playground-frontend.vercel.app"])

# Registrar los blueprints
app.register_blueprint(top_words_bp, url_prefix='/top-words')
app.register_blueprint(complete_text_bp, url_prefix='/complete-text')
app.register_blueprint(summarize_bp)
app.register_blueprint(transcribe_bp)
app.register_blueprint(chat_bp)

# Cargar el modelo de Whisper (se hace una sola vez al iniciar la aplicación)
model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())
def download_audio(url):
    try:
        yt = YouTube(url)
        # Obtener el stream de audio
        audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        
        if not audio_stream:
            raise Exception("No se encontró stream de audio disponible")
            
        # Crear un archivo temporal
        temp_dir = tempfile.mkdtemp()
        temp_file = os.path.join(temp_dir, "audio.mp4")
        
        # Descargar el audio
        audio_stream.download(output_path=temp_dir, filename="audio.mp4")
        return temp_file
    except Exception as e:
        raise Exception(f"Error al descargar el audio: {str(e)}")

def analyze_audio(audio_path):
    try:
        # Transcribir el audio
        result = model.transcribe(audio_path)
        text = result["text"].lower()
        
        # Extraer palabras (excluyendo palabras muy cortas)
        words = re.findall(r'\b\w{3,}\b', text)
        
        # Contar frecuencia de palabras
        word_counts = Counter(words)
        
        # Obtener las 10 palabras más comunes
        top_words = word_counts.most_common(10)
        
        return top_words
    except Exception as e:
        raise Exception(f"Error al analizar el audio: {str(e)}")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        youtube_url = data.get('url')
        
        if not youtube_url:
            return jsonify({'error': 'URL de YouTube no proporcionada'}), 400
        
        # Descargar el audio
        audio_path = download_audio(youtube_url)
        
        try:
            # Analizar el audio
            top_words = analyze_audio(audio_path)
            
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

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        num1 = float(data['num1'])
        num2 = float(data['num2'])
        operation = data['operation']
        
        result = 0
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                return jsonify({'error': 'No se puede dividir por cero'}), 400
            result = num1 / num2
        else:
            return jsonify({'error': 'Operación no válida'}), 400
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
 
@app.route('/saludo', methods=['POST'])
def saludar():
    data = request.get_json()
    nombre = data.get("nombre", "desconocido")
    return jsonify({"mensaje": f"Hola, {nombre}!"})

if __name__ == '__main__':
    app.run(debug=True) 