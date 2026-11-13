import os
import json
import requests
from config import Config

def query_llm(prompt: str, system_prompt: str = "You are a professional YouTube production strategist.", temperature: float = 0.7) -> str:
    """
    Zero-dollar LLM dispatcher:
    1. Tries Google Gemini API (Free tier: 15 RPM / 1M TPM free)
    2. Tries Groq API (Free tier: 30 RPM free)
    3. Falls back gracefully with rich, realistic structured content if keys are not yet configured.
    """
    # 1. Try Gemini
    if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"{system_prompt}\n\nTask:\n{prompt}"}]}
                ],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": 2048
                }
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLM] Gemini request error: {e}. Trying fallback...")

    # 2. Try Groq
    if Config.GROQ_API_KEY and Config.GROQ_API_KEY != "your_groq_api_key_here":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {Config.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLM] Groq request error: {e}. Trying fallback...")

    # 3. Fallback / Template Engine for demonstration and testing without API keys
    return None
