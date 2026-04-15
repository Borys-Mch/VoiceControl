from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import Response
import requests
import tempfile
import shutil
import os

app = FastAPI()

WHISPER_URL = "http://whisper:10300/inference"
PIPER_URL = "http://piper:5000/"
REQUEST_TIMEOUT_SECONDS = 30

def transcribe(audio_path):
    with open(audio_path, "rb") as f:
        r = requests.post(
            WHISPER_URL,
            files={"file": f},
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
    r.raise_for_status()
    return r.json().get("text", "")

def synthesize(text):
    r = requests.post(
        PIPER_URL,
        data=text.encode("utf-8"),
        headers={"Content-Type": "text/plain; charset=utf-8"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    r.raise_for_status()
    return r.content



def handle_command(text):
    text = text.lower()

    if "світло" in text:
        return "Вмикаю світло"
    elif "температура" in text:
        return "Зараз 22 градуси"
    else:
        return "Я не зрозумів команду"

@app.post("/voice")
async def voice(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        text = transcribe(tmp_path)
        print("TEXT:", text)

        response_text = handle_command(text)

        audio = synthesize(response_text)
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Upstream voice service error: {exc}") from exc
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    return Response(content=audio, media_type="audio/wav")
