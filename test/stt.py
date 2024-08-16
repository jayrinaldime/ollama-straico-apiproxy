import requests
import os

url = "http://127.0.0.1:3214/v1/audio/transcriptions"

params = {
    "model": "whisper-1",
}

files = {
    "file": (
        "audio.mp3",
        open(
            "./How can we even hear gravitational waves.mp3",
            "rb",
        ),
        "audio/mpeg",
    ),
}

response = requests.post(url, files=files, data=params)

print(response.json())
