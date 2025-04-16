from pytubefix import YouTube
import tempfile
import os

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