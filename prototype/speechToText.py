import whisper
import tempfile

model = whisper.load_model('base')

def process_wav_bytes(webm_bytes: bytes, sample_rate: int = 16000):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.audio.load_audio(temp_file.name)
        return waveform

def speechToText(message: str):
    audio = process_wav_bytes(bytes(message))
    audio = whisper.pad_or_trim(audio)
    transcription = model.transcribe(
        audio
    )
    print("Transcription output: ",transcription)

    return transcription["text"]