import os, json, requests, subprocess, uuid

API_KEY = "9ba9ff258c72493ca88e4aa80eaed6fc"
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech"
VOICE_ID="Lhkfd0eq2F87bgx4Aozc" #ruchika
def get_tts(text, voice_id=VOICE_ID):
   url = f"{BASE_URL}/{voice_id}"
   headers = {
       "Accept": "audio/mpeg",
       "Content-Type": "application/json",
       "xi-api-key": API_KEY,
   }
   data = {
       "text": text,
       #   "model_id": "eleven_monolingual_v1",
       "voice_settings": {"stability": 0, "similarity_boost": 0},
   }

   response = requests.post(url, json=data, headers=headers)
   print(response)
   audio_data = response.content
   file_path = f"{str(uuid.uuid4())}.mp3"
   with open(file_path, "wb") as f:
       f.write(audio_data)
   return file_path

