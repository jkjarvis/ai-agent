import sounddevice as sd
import numpy as np
import wave
import io
import websocket
import threading
from websocket import WebSocketConnectionClosedException

# Audio recording parameters
RATE = 16000  # Sample rate (16kHz)
CHANNELS = 1  # Mono audio
CHUNK_SIZE = 1024  # Frames per buffer
FORMAT = np.int16  # Data type for recording
THRESHOLD = 0.01  # Minimum amplitude to consider as significant sound
SILENCE_DURATION = 1  # Seconds of silence before stopping

# WebSocket parameters
WS_URL = 'ws://localhost:5003/transcribe'

# Initialize variables
silence_counter = 0  # To track silence duration
recording_buffer = []  # To store recorded audio chunks

# Create a WebSocket connection
def create_ws_connection():
    ws = None
    try:
        ws = websocket.create_connection(WS_URL)
        print("WebSocket connection established.")
    except Exception as e:
        print("Failed to establish WebSocket connection:", str(e))
    return ws

def save_audio_to_buffer(audio_data):
    # Save the audio buffer to a BytesIO object
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(np.dtype(FORMAT).itemsize)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(audio_data))
    buffer.seek(0)
    return buffer.read()

def send_audio_via_ws(ws, audio_data):
    if ws:
        try:
            ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
            print("Audio data sent via WebSocket.")
        except WebSocketConnectionClosedException:
            print("WebSocket connection was closed. Attempting to reconnect...")
            ws = create_ws_connection()
            if ws:
                ws.send(audio_data, opcode=websocket.ABNF.OPCODE_BINARY)
                print("Audio data sent via WebSocket after reconnection.")
        except Exception as e:
            print("Failed to send audio via WebSocket:", str(e))

def audio_callback(indata, frames, time, status):
    global silence_counter, recording_buffer
    if status:
        print(status)
    recording_buffer.append(indata.copy())
    indata_normalized = indata.astype(np.float32) / np.iinfo(indata.dtype).max  # Normalize if 'indata' is in integer format

    amplitude = np.sqrt(np.mean(indata_normalized**2))
    print("amp: ",amplitude)
    if amplitude > THRESHOLD:
        silence_counter = 0
    else:
        silence_counter += frames
    silence_seconds = silence_counter / RATE
    if silence_seconds >= SILENCE_DURATION:
        audio_data = save_audio_to_buffer(recording_buffer)
        send_audio_via_ws(ws, audio_data)
        recording_buffer = []
        silence_counter = 0

if __name__ == "__main__":
    ws = create_ws_connection()
    try:
        with sd.InputStream(callback=audio_callback, samplerate=RATE, channels=CHANNELS, blocksize=CHUNK_SIZE, dtype=FORMAT):
            print("Listening... Speak into the microphone.")
            while True:
                sd.sleep(1000)
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        if ws:
            ws.close()
            print("WebSocket connection closed.")
