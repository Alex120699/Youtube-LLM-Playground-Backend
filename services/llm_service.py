import requests
import json
import os
from dotenv import load_dotenv

OLLAMA_URL = "http://localhost:11434/api/chat"

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1")  # Valor por defecto


def call_llm(messages, model=MODEL_NAME, stream=False):
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=stream)
        response.raise_for_status()

        if stream:
            def stream_generator():
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            data = json.loads(line)
                            content = data.get("message", {}).get("content", "")
                            if content:
                                yield content
                        except Exception as parse_error:
                            yield f"[Error al parsear]: {parse_error}"
            return stream_generator()
        else:
            result = response.json()
            return result.get("message", {}).get("content", "").strip()

    except Exception as e:
        print(f"[ERROR] Llamada a Ollama fallida: {e}")
        if stream:
            def error_generator():
                yield f"[Error]: {e}"
            return error_generator()
        return f"[Error]: {e}"
