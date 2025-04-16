from flask import Blueprint, request, jsonify, Response, stream_with_context
from services.youtube_service import download_audio
from services.whisper_service import transcribe_audio
from services.chatbot import chat_about_video
import os
import time  # Importa time para medir duración

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    transcript = data.get("transcript")
    user_input = data.get("message")
    history = data.get("history", [])

    if not transcript or not user_input:
        return jsonify({'error': 'Faltan datos: transcript o mensaje del usuario'}), 400

    def generate():
        try:
            for chunk in chat_about_video(transcript, history, user_input):
                yield chunk
        except Exception as e:
            yield f"[ERROR]: {str(e)}"

    return Response(stream_with_context(generate()), content_type='text/plain')