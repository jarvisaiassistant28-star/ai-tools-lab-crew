import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Engine API Keys (100% Free Tiers)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Alert Configuration (Telegram & WhatsApp - 100% Free)
    TELEGRAM_USER = os.getenv("TELEGRAM_USER", "@Manuhcruz")
    WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "")
    CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_FROM_WHATSAPP = os.getenv("TWILIO_FROM_WHATSAPP", "whatsapp:+14155238886")
    TWILIO_TO_WHATSAPP = os.getenv("TWILIO_TO_WHATSAPP", "")

    # YouTube API Configuration (Google Cloud YouTube Data API v3 - Free Tier)
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
    YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "unlisted")  # unlisted, private, or public

    # Pexels Free API Key (for HD B-roll footage)
    PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")

    # EXACT CHANNEL BRANDING & NICHE LOCK
    CHANNEL_NAME = "AI Tools Lab"
    CHANNEL_HANDLE = "@AiToolsLab-w9y"
    CHANNEL_SLOGAN = "Explore • Learn • Create • Grow"
    BUSINESS_EMAIL = "jarvisaiassistant28@gmail.com"
    TARGET_NICHE = "AI Tools, Video & Image Creation Tutorials, Automation & Productivity"
    VOICE_MODEL = os.getenv("VOICE_MODEL", "en-US-ChristopherNeural")
