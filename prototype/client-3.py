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

# Define a threading event for signaling
ready_to_record = threading.Event()

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
    ready_to_record.wait()  # Wait until the event is set before starting the first recording
    while True:
        audio = record_audio(RECORD_SECONDS, RATE, CHANNELS)
        wav_bytes = audio_to_wav_bytes(audio, RATE, CHANNELS)
        ws.send(wav_bytes, opcode=websocket.ABNF.OPCODE_BINARY)
        ready_to_record.clear()  # Clear the event after sending audio
        ready_to_record.wait()  # Wait for the next server response before recording again

def on_open(ws):
    print("WebSocket connection opened.")
    # Initially set the event to start the first recording immediately
    ready_to_record.set()
    thread = threading.Thread(target=continuously_send_audio, args=(ws,))
    thread.start()

def on_message(ws, message):
    print("Received message from server: ", message)
    # Set the event when a message is received to signal ready for the next recording
    ready_to_record.set()

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
