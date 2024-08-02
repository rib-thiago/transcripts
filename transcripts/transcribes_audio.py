"""
Este script permite transcrever o áudio de um arquivo de áudio em português para texto.
Ele utiliza a biblioteca SpeechRecognition para realizar a transcrição e ffmpeg-python para converter o áudio para o formato WAV, se necessário.

O usuário deve fornecer o caminho do arquivo de áudio.

Requisitos:
- SpeechRecognition
- ffmpeg-python (para converter formatos de áudio para WAV, se necessário)

Uso:
python transcribe_audio.py
"""

import speech_recognition as sr
from pathlib import Path
import ffmpeg

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

def transcribe_audio(audio_file_path: str) -> None:
    """
    Transcreve o áudio do arquivo fornecido para texto em português e exibe o texto.

    Args:
        audio_file_path (Path): Caminho para o arquivo de áudio (deve estar em formato WAV).
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file_path) as source:
            print("Transcrevendo áudio...")
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="pt-BR")
            print(f"Texto transcrito: {text}")
    except sr.UnknownValueError:
        print("O reconhecimento de fala não conseguiu entender o áudio.")
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")

if __name__ == "__main__":
    input_audio_path = Path(input('Digite o caminho do arquivo de áudio: '))

    # Verifica a extensão do arquivo e converte para WAV se necessário
    if input_audio_path.suffix.lower() != '.wav':
        wav_path = input_audio_path.with_suffix('.wav')
        convert_to_wav(input_audio_path, wav_path)
        audio_path = wav_path
    else:
        audio_path = input_audio_path

    transcribe_audio(str(audio_path))  # Passa o caminho como string