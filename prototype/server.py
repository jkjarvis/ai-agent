from flask import Flask
from flask_sockets import Sockets, Rule
import traceback
import base64
import requests
from speechToText import speechToText
# Import the BankingBot class
from askBot import BankingBot
from textToSpeech import textToSpeech

app = Flask(__name__, static_folder='static')
sockets = Sockets(app)

# If you want to maintain state across multiple connections, instantiate here
# bot = BankingBot()

def transcribe_socket(ws):
    # Instantiate BankingBot here if you want a fresh state for each connection
    bot = BankingBot()
    allowSpeech=True
    
    while not ws.closed:
        message = ws.receive()
        if message:
            print('message received', len(message), type(message))
            try:
                if isinstance(message, str):
                    message = base64.b64decode(message)
                print("received client message, transcribing...\n")
                text = speechToText(message)

                if len(text) <= 0 or not allowSpeech:
                    continue
                print("message transcribed, asking bot...\n")

                requests.post("http://localhost:5000/send-message", json={"user": text})
                print("post req sent")

                # Use the BankingBot's ask_bot method
                botAnswer = bot.ask_bot(text)
                requests.post("http://localhost:5000/send-message", json={"customer executive": botAnswer})
                print("got bot answer, converting to speech...")
                textToSpeech(botAnswer)
                ws.send("done")
    
            except Exception as e:
                traceback.print_exc()

sockets.url_map.add(Rule('/transcribe', endpoint=transcribe_socket, websocket=True))

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    print("starting server...")

    server = pywsgi.WSGIServer(('', 5003), app, handler_class=WebSocketHandler)
    server.serve_forever()
