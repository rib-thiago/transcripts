from pytubefix import YouTube
from pytubefix.cli import on_progress
import ffmpeg
import os
import re

def normalize_filename(filename):
    filename = re.sub(r'[^\w\s-]', '', filename)  # Remove caracteres especiais
    filename = filename.strip().replace(' ', '_')  # Substitui espaços por sublinhados
    return filename

def download_and_convert_video():
    try:
        video_url = input('Digite a URL do vídeo: ')
        save_path = input('Digite o diretório para salvar o download: ')

        if not os.path.exists(save_path):
            print("Diretório não existe. Criando...")
            os.makedirs(save_path)

        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f"Baixando: {yt.title}")

        normalized_title = normalize_filename(yt.title)
        audio_file_path = os.path.join(save_path, f"{normalized_title}.aac")
        mp3_file_path = os.path.join(save_path, f"{normalized_title}.mp3")

        ys = yt.streams.get_audio_only()
        ys.download(output_path=save_path, filename=f"{normalized_title}.aac")

        print(f"Convertendo para MP3: {mp3_file_path}")
        ffmpeg.input(audio_file_path).output(mp3_file_path).run(quiet=True, overwrite_output=True)

        os.remove(audio_file_path)  # Remove o arquivo original AAC

        print(f"Download e conversão concluídos e salvo em: {mp3_file_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    download_and_convert_video()
