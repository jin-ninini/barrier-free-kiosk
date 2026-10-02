import os
import re
import tempfile

import openai
import pyttsx3
import scipy.io.wavfile as wav
import sounddevice as sd
from dotenv import load_dotenv

# OpenAI API
load_dotenv()  # .env의 OPENAI_API_KEY 불러오기
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def find_korean_voice(voices):
    """한국어 음성이 있으면 선택, 없으면 첫 번째 음성 사용"""
    for voice in voices:
        if re.search(r"ko[_-]kr", f"{voice.id} {voice.languages}", re.IGNORECASE):
            return voice
    return voices[0]


# TTS
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)
engine.setProperty("voice", find_korean_voice(engine.getProperty("voices")).id)

# 음성 녹음
SAMPLERATE = 16000
DURATION = 5


def speak(text):
    print(f"🗣️ {text}")
    engine.say(text)
    engine.runAndWait()


def record_audio():
    print("🎙️ 녹음 중...")
    audio = sd.rec(int(SAMPLERATE * DURATION), samplerate=SAMPLERATE, channels=1, dtype='int16')
    sd.wait()
    return audio


def transcribe(audio_data):
    """Whisper API로 음성을 텍스트로 변환"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
        wav.write(temp_file.name, SAMPLERATE, audio_data)
    try:
        with open(temp_file.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ko"
            )
    finally:
        os.unlink(temp_file.name)  # API 오류가 나도 임시 파일 삭제
    return transcript.text.strip()
