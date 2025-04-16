import ollama
import requests
from services.llm_service import call_llm

OLLAMA_URL = "http://localhost:11434/api/chat"


def summarize_with_ollama(text, model="mistral"):
    prompt =    f"""
                A continuación encontrarás la transcripción del audio de un video de YouTube. 
                Resume su contenido de forma clara y humana, explicando los puntos clave, el propósito del video y cualquier conclusión o reflexión final que se haya mencionado.
                Transcripción
                \n\n{text}
                """
    
    system_prompt = """
                    Eres un asistente español experto en resumir videos de YouTube a partir de transcripciones generadas automáticamente. Tu objetivo es ofrecer un resumen claro, humano y comprensible del contenido del video, como si lo estuvieras explicando a otra persona. 
                    Debes tener en cuenta que la transcripción puede contener errores menores, palabras mal interpretadas o frases sin puntuación. Aun así, intenta captar el mensaje global del video. Si detectas ambigüedades, infiere con sentido común.
                    No repitas frases exactas del texto si no es necesario. Resume el contenido como lo haría una persona: comentando, explicando y destacando las ideas más relevantes.
                    Evita tecnicismos innecesarios y usa un lenguaje natural, empático y sencillo. No incluyas notas como "según la transcripción" ni te disculpes por posibles errores. Haz como si hubieras visto el video.
                    Responde siempre en español.
                    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        return call_llm(messages)
    except:
        print("No se pudo generar el resumen.")
