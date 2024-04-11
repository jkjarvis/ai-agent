from flask import Flask, render_template
from flask_sockets import Sockets, Rule
import whisper
import traceback
import tempfile
import base64
from output_stream import get_tts

app = Flask(__name__)
sockets = Sockets(app)

print(whisper.available_models())
model = whisper.load_model('base')

def process_wav_bytes(webm_bytes: bytes, sample_rate: int = 16000):
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as temp_file:
        temp_file.write(webm_bytes)
        temp_file.flush()
        waveform = whisper.audio.load_audio(temp_file.name)
        print("wv: ",type(waveform))
        return waveform

def transcribe_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message:
            print('message received', len(message), type(message))
            try:
                if isinstance(message, str):
                    message = base64.b64decode(message)
                audio = process_wav_bytes(bytes(message))

                print("here 1")
          
                audio = whisper.pad_or_trim(audio)
                print("here 3")
                transcription = model.transcribe(
                    audio
                )
                print(transcription)
                response = get_tts(transcription["text"])
                
            except Exception as e:
                traceback.print_exc()

sockets.url_map.add(Rule('/transcribe', endpoint=transcribe_socket, websocket=True))


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print("starting server...")

    server = pywsgi.WSGIServer(('', 5003), app, handler_class=WebSocketHandler)
    server.serve_forever()