
from gtts import gTTS
from playsound import playsound
import tempfile
import threading
import os

voice_lock = threading.Lock()

def speak_alert(message, lang="en"):
    threading.Thread(
        target=_speak,
        args=(message, lang),
        daemon=True
    ).start()

def _speak(message, lang):
    with voice_lock:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                filename = fp.name

            tts = gTTS(text=message, lang=lang)
            tts.save(filename)

            playsound(filename)

            os.remove(filename)

        except Exception as e:
            print(e)