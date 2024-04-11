import whisper

model = whisper.load_model("base")
result = model.transcribe("2024-02-17 00-21-13.mkv")
print(result["text"])