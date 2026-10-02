from dotenv import load_dotenv
import openai
from openai import OpenAI
import sounddevice as sd
import scipy.io.wavfile as wav
import tempfile
import os
from playsound import playsound # mp3 재생용
import uuid # For generating unique filenames

# OpenAI API
load_dotenv()  # .env의 OPENAI_API_KEY 불러오기
client = OpenAI()

initial_prompt = """

"""


# 음성 녹음
SAMPLERATE = 16000
DURATION = 3


def ask(question, message_history=[], model="gpt-3.5-turbo"):
    """
    만들어 보세요!
    """
    return message_history


# TODO: 학습한 코드에서 speak와 record_audio, transcribe를 가져오세요.
if __name__ == "__main__":
    message_history = ask("안녕하세요?", message_history=[])
    speak(message_history[-1]["content"])

    while True:
        audio_data = record_audio()
        user_text = transcribe(audio_data)
        print(f"📝 인식된 말: {user_text}")
        message_history = ask(user_text, message_history=message_history)
        speak(message_history[-1]["content"])

        # 종료 코드
        if any(
            x in message_history[-1]["content"]
            for x in ["종료", "끝", "그만", "결제", "주문 끝", "주문 완료", "다 했어"]
        ):
            break
