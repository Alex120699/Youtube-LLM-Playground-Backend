import whisper
import torch
from collections import Counter
import re
import os
from dotenv import load_dotenv

load_dotenv()

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # Valor por defecto


def transcribe_audio(audio_path,device="cpu"):
    try:
        print(f"Usando dispositivo: {device}")
        print(f"Modelo de Whisper: {WHISPER_MODEL}")
        model = whisper.load_model(WHISPER_MODEL, device=device)
        # Transcribir el audio
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        raise Exception(f"Error al transcribir el audio: {str(e)}")

def analyze_audio(audio_path,device="cpu"):
    try:
        # Transcribir el audio
        text = transcribe_audio(audio_path,device).lower()
        
        # Extraer palabras (excluyendo palabras muy cortas)
        words = re.findall(r'\b\w{3,}\b', text)
        
        # Contar frecuencia de palabras
        word_counts = Counter(words)
        
        # Obtener las 10 palabras más comunes
        top_words = word_counts.most_common(10)
        
        return top_words
    except Exception as e:
        raise Exception(f"Error al analizar el audio: {str(e)}") 