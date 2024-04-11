import sounddevice as sd
import websocket
import wave
import numpy as np
import io
import threading
import time

# Audio recording parameters
RATE = 16000  # Sample rate (16kHz)
CHANNELS = 1  # Number of audio channels (mono)
RECORD_SECONDS = 10  # Duration of recording

# WebSocket parameters
WS_URL = 'ws://localhost:5003/transcribe'

def record_audio(duration, samplerate, channels):
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype='int16', blocking=True)
    return recording

def audio_to_wav_bytes(audio, samplerate, channels):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # Assuming 16-bit audio
        wf.setframerate(samplerate)
        wf.writeframes(audio)
    buffer.seek(0)
    return buffer.read()

def continuously_send_audio(ws):
    while True:
        audio = record_audio(RECORD_SECONDS, RATE, CHANNELS)
        wav_bytes = audio_to_wav_bytes(audio, RATE, CHANNELS)
        ws.send(wav_bytes, opcode=websocket.ABNF.OPCODE_BINARY)
        time.sleep(RECORD_SECONDS)  # Wait for the duration of the recording before starting the next one

def on_open(ws):
    print("WebSocket connection opened.")
    thread = threading.Thread(target=continuously_send_audio, args=(ws,))
    thread.start()

def on_message(ws, message):
    print("Received message from server: ", message)

def on_error(ws, error):
    print("Error: ", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed.")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws_app = websocket.WebSocketApp(WS_URL,
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    ws_app.run_forever()
