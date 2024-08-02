"""
Este script permite baixar o áudio de um vídeo do YouTube e convertê-lo para o formato MP3.
Ele utiliza a biblioteca pytube para baixar o vídeo e ffmpeg-python para a conversão do áudio.

O usuário deve fornecer a URL do vídeo e o diretório onde deseja salvar o download. 
O nome do arquivo de saída será solicitado ao usuário.

Requisitos:
- pytube
- ffmpeg-python
- ffmpeg instalado no sistema

Uso:
python youtube-to-mp3.py
"""

from pytubefix import YouTube
from pytubefix.cli import on_progress
import ffmpeg
from pathlib import Path
import re


def download_and_convert_video() -> None:
    """
    Baixa o áudio de um vídeo do YouTube e converte para MP3.

    Solicita ao usuário a URL do vídeo, o diretório de salvamento e o nome do arquivo de saída.
    """
    try:
        video_url = input('Digite a URL do vídeo: ')
        save_path = Path(input('Digite o diretório para salvar o download: '))

        if not save_path.exists():
            print("Diretório não existe. Criando...")
            save_path.mkdir(parents=True)

        yt = YouTube(video_url, on_progress_callback=on_progress)
        print(f"Baixando: {yt.title} do canal {yt.author}")

        # Normalizando o nome do arquivo temporário .aac
        temp_filename = re.sub(r'[^\w\s-]', '', yt.title).strip().replace(' ', '_')
        audio_file_path = save_path / f"{temp_filename}.aac"

        mp3_file_name = input('Digite o nome do arquivo de saída (sem extensão): ')
        mp3_file_path = save_path / f"{mp3_file_name}.mp3"

        ys = yt.streams.get_audio_only()
        ys.download(output_path=save_path, filename=audio_file_path.name)

        print(f"Convertendo para MP3: {mp3_file_path}")
        ffmpeg.input(str(audio_file_path)).output(str(mp3_file_path)).run(quiet=True, overwrite_output=True)

        audio_file_path.unlink()  # Remove o arquivo original AAC

        print(f"Download e conversão concluídos e salvo em: {mp3_file_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    while True:
        download_and_convert_video()

        # Pergunta se o usuário deseja baixar outro vídeo
        another_video = input('Deseja baixar outro vídeo? (s/n): ')
        if another_video.lower() != 's':
            break