import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_response(prompt):
    if not API_KEY:
        return "API key bulunamadı!"

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "deepseek/deepseek-r1:free",   # ücretsiz ve güçlü
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except:
        return "Üzgünüm, AI şu anda yanıt veremiyor."
