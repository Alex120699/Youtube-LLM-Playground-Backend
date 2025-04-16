import whisper
import torch
from collections import Counter
import re

# Cargar el modelo de Whisper (se hace una sola vez al iniciar el servicio)
model = whisper.load_model("tiny", device="cuda" if torch.cuda.is_available() else "cpu")

def transcribe_audio(audio_path):
    try:
        # Transcribir el audio
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        raise Exception(f"Error al transcribir el audio: {str(e)}")

def analyze_audio(audio_path):
    try:
        # Transcribir el audio
        text = transcribe_audio(audio_path).lower()
        
        # Extraer palabras (excluyendo palabras muy cortas)
        words = re.findall(r'\b\w{3,}\b', text)
        
        # Contar frecuencia de palabras
        word_counts = Counter(words)
        
        # Obtener las 10 palabras más comunes
        top_words = word_counts.most_common(10)
        
        return top_words
    except Exception as e:
        raise Exception(f"Error al analizar el audio: {str(e)}") 