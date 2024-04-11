from flask import Flask, jsonify, render_template, request
import os
import json

app = Flask(__name__, static_folder='static')
MESSAGES_FILE = 'messages.json'

@app.route('/')
def index():
    return render_template('conversationView.html')

@app.route('/get-messages')
def get_messages():
    # Read the messages file and return its contents
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as file:
            messages = json.load(file)
    else:
        messages = []
    return jsonify(messages=messages)

@app.route('/send-message', methods=['POST'])
def send_message():
    # Append a new message to the JSON file
    print("here 1")
    message = request.json
    print("received message: ",message)
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r+') as file:
            messages = json.load(file)
            messages.append(message)
            file.seek(0)
            json.dump(messages, file)
    else:
        with open(MESSAGES_FILE, 'w') as file:
            json.dump([message], file)
    print("here 2")
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)