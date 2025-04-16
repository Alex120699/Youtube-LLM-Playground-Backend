from services.llm_service import call_llm
import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")  # Valor por defecto


def build_chatbot_prompt(transcript: str, history: list, user_input: str) -> list:
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente experto en explicar el contenido de un video de YouTube. "
                "Usa la transcripción como contexto y responde como si hubieras visto el video.\n\n"
                "La transcripcion del video puede ser parcialmente incorrecta. Ten en cuenta alucinaciones en palabras. "
                "Si el usuario te pide mostrar la transcripción, recuerda añadir los signos de puntuacion y limpiar el texto.\n\n"
                f"Transcripción del video:\n{transcript}"
            )
        }
    ] + history + [{"role": "user", "content": user_input}]
    return messages

def chat_about_video(transcript: str, history: list, user_input: str, model=MODEL_NAME):
    messages = build_chatbot_prompt(transcript, history, user_input)
    return call_llm(messages, model=model, stream=True)  # stream=True aquí
