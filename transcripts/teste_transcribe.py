import ffmpeg
import tempfile
from pathlib import Path
import speech_recognition as sr
import os

def convert_to_wav(audio_file_path: Path, output_path: Path) -> None:
    """
    Converte um arquivo de áudio para o formato WAV, se necessário.

    Args:
        audio_file_path (Path): Caminho para o arquivo de áudio original.
        output_path (Path): Caminho para o arquivo WAV convertido.
    """
    try:
        ffmpeg.input(str(audio_file_path)).output(str(output_path)).run(quiet=True, overwrite_output=True)
        print(f"Arquivo convertido para WAV e salvo em: {output_path}")
    except ffmpeg.Error as e:
        print(f"Erro ao converter o arquivo de áudio: {e}")


def segment_audio(audio_file_path: Path) -> list[Path]:
    """
    Segmenta um arquivo de áudio em intervalos de 50 segundos e salva os segmentos em um diretório temporário.

    Args:
        audio_file_path (Path): Caminho para o arquivo de áudio original.

    Returns:
        list[Path]: Lista de caminhos para os arquivos de áudio segmentados.
    """
    temp_dir = tempfile.mkdtemp()
    audio_file_path = Path(audio_file_path)
    
    # Obtém a duração do áudio usando ffmpeg
    probe = ffmpeg.probe(str(audio_file_path), select_streams='a', show_entries='format=duration', of='json')
    duration = float(probe['format']['duration'])
    
    segment_duration = 50  # duração de cada segmento em segundos
    segments = []
    start_time = 0
    
    while start_time < duration:
        end_time = min(start_time + segment_duration, duration)
        segment_file = Path(temp_dir) / f"segment_{start_time}_{end_time}.wav"
        ffmpeg.input(str(audio_file_path), ss=start_time, to=end_time).output(str(segment_file)).run(quiet=True, overwrite_output=True)
        segments.append(segment_file)
        start_time += segment_duration
    
    return sorted(segments)


def transcribe_and_save(segments: list[Path], output_file: Path) -> None:
    """
    Transcreve o áudio de arquivos segmentados e salva o texto com timestamps em um arquivo.

    Args:
        segments (list[Path]): Lista de caminhos para os arquivos de áudio segmentados.
        output_file (Path): Caminho para o arquivo onde o texto será salvo.
    """
    recognizer = sr.Recognizer()
    
    with open(output_file, 'w') as file:
        for segment in segments:
            start_time = float(segment.stem.split('_')[1])
            end_time = float(segment.stem.split('_')[2])
            timestamp = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02} - {int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02}"
            
            try:
                # Passar o caminho do arquivo como string
                with sr.AudioFile(str(segment)) as source:
                    print(f"Transcrevendo segmento: {segment}")
                    audio_data = recognizer.record(source)
                    text = recognizer.recognize_google(audio_data, language="pt-BR")
                    file.write(f"{timestamp}\n{text}\n\n")
            except sr.UnknownValueError:
                file.write(f"{timestamp}\n[Áudio não reconhecido]\n\n")
            except sr.RequestError as e:
                file.write(f"{timestamp}\n[Erro de requisição: {e}]\n\n")
            finally:
                os.remove(segment)  # Remove o arquivo temporário após a transcrição


if __name__ == "__main__":
    input_audio_path = Path(input('Digite o caminho do arquivo de áudio: '))

    # Verifica a extensão do arquivo e converte para WAV se necessário
    if input_audio_path.suffix.lower() != '.wav':
        wav_path = input_audio_path.with_suffix('.wav')
        convert_to_wav(input_audio_path, wav_path)
        audio_path = wav_path
    else:
        audio_path = input_audio_path    
    
    segments = segment_audio(audio_path)
    transcribe_and_save(segments, Path("saida_transcricao.txt"))
