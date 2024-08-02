import ffmpeg
import os

def convert_time_to_seconds(time_str):
    """Converts time in various formats to seconds."""
    if time_str.endswith('s'):
        return int(time_str[:-1])
    elif time_str.endswith('m'):
        return int(time_str[:-1]) * 60
    else:
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s

def get_audio_duration(audio_file_path):
    """Returns the duration of the audio file in seconds, minutes and HH:MM:SS format."""
    try:
        probe = ffmpeg.probe(audio_file_path)
        duration = float(probe['format']['duration'])
        duration_minutes = duration / 60
        duration_hms = f"{int(duration // 3600):02}:{int((duration % 3600) // 60):02}:{int(duration % 60):02}"
        return duration, duration_minutes, duration_hms
    except Exception as e:
        print(f"Erro ao obter a duração do áudio: {e}")
        return None, None, None

def extract_audio_segment(audio_file_path):
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
        if not os.path.exists(audio_file_path):
            print("Arquivo de áudio não encontrado.")
            return

        # Pergunta o nome do arquivo de saída
        output_filename = input('Digite o nome do arquivo de saída (sem extensão): ')
        segment_file_path = f"{output_filename}.mp3"

        # Extrai o segmento usando ffmpeg
        (
            ffmpeg
            .input(audio_file_path, ss=start_time, to=end_time)
            .output(segment_file_path)
            .run(quiet=True, overwrite_output=True)
        )

        print(f"Trecho extraído e salvo em: {segment_file_path}")
    except Exception as e:
        print(f"Ocorreu um erro ao extrair o trecho: {e}")

if __name__ == "__main__":
    audio_file_path = input('Digite o caminho do arquivo de áudio (MP3): ')
    extract_audio_segment(audio_file_path)
