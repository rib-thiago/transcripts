"""
Este script permite extrair um segmento de um arquivo de áudio MP3.
Ele utiliza a biblioteca ffmpeg-python para a manipulação do áudio.

O usuário deve fornecer o caminho do arquivo de áudio e os tempos de início e fim do segmento.
Os tempos podem ser fornecidos em segundos, minutos (ex.: 30s, 5m) ou no formato HH:MM:SS.

Após segmentar um trecho, o script pergunta se o usuário deseja segmentar outro trecho. O arquivo de saída será salvo no mesmo diretório do arquivo de áudio original.

Requisitos:
- ffmpeg-python
- ffmpeg instalado no sistema

Uso:
python segment_mp3.py
"""

import ffmpeg
from pathlib import Path


def convert_time_to_seconds(time_str: str) -> int:
    """
    Converte o tempo em vários formatos para segundos.

    Args:
        time_str (str): Tempo no formato Ns, Nm ou HH:MM:SS.

    Returns:
        int: Tempo em segundos.
    """
    if time_str.endswith('s'):
        return int(time_str[:-1])
    elif time_str.endswith('m'):
        return int(time_str[:-1]) * 60
    else:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s


def get_audio_duration(audio_file_path: Path) -> tuple:
    """
    Retorna a duração do arquivo de áudio em segundos, minutos e formato HH:MM:SS.

    Args:
        audio_file_path (Path): Caminho para o arquivo de áudio.

    Returns:
        tuple: Duração em segundos, minutos e formato HH:MM:SS.
    """
    try:
        probe = ffmpeg.probe(str(audio_file_path))
        duration = float(probe['format']['duration'])
        duration_minutes = duration / 60
        duration_hms = f"{int(duration // 3600):02}:{int((duration % 3600) // 60):02}:{int(duration % 60):02}"
        return duration, duration_minutes, duration_hms
    except Exception as e:
        print(f"Erro ao obter a duração do áudio: {e}")
        return None, None, None


def extract_audio_segment(audio_file_path: Path) -> None:
    """
    Extrai um segmento do arquivo de áudio e salva em um novo arquivo MP3.

    Args:
        audio_file_path (Path): Caminho para o arquivo de áudio.
    """
    try:
        # Obtém a duração do áudio
        duration_sec, duration_min, duration_hms = get_audio_duration(audio_file_path)
        if duration_sec is None:
            return

        print(f"Duração do áudio: {duration_sec:.2f} segundos, {duration_min:.2f} minutos, {duration_hms}")

        start_time_str = input('Digite o tempo de início do trecho (Ns, Nm ou HH:MM:SS): ')
        end_time_str = input('Digite o tempo de final do trecho (Ns, Nm ou HH:MM:SS): ')

        start_time = convert_time_to_seconds(start_time_str)
        end_time = convert_time_to_seconds(end_time_str)

        # Verifica se o arquivo de áudio existe
        if not audio_file_path.exists():
            print("Arquivo de áudio não encontrado.")
            return

        # Pergunta o nome do arquivo de saída
        output_filename = input('Digite o nome do arquivo de saída (sem extensão): ')
        segment_file_path = audio_file_path.parent / f"{output_filename}.mp3"

        # Extrai o segmento usando ffmpeg
        (
            ffmpeg
            .input(str(audio_file_path), ss=start_time, to=end_time)
            .output(str(segment_file_path))
            .run(quiet=True, overwrite_output=True)
        )

        print(f"Trecho extraído e salvo em: {segment_file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao extrair o trecho: {e}")


if __name__ == "__main__":
    audio_file_path = Path(input('Digite o caminho do arquivo de áudio (MP3): '))
    while True:
        extract_audio_segment(audio_file_path)

        # Pergunta se o usuário deseja segmentar outro trecho
        another_segment = input('Deseja segmentar outro trecho? (s/n): ')
        if another_segment.lower() != 's':
            break
