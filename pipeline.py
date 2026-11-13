import os
import sys
import json
import time
import asyncio
import urllib.parse
import subprocess
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. GLOBAL CONFIGURATION & CHANNEL BRANDING
# ==============================================================================
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Alert Configuration (Telegram & WhatsApp - 100% Free)
    TELEGRAM_USER = os.getenv("TELEGRAM_USER", "@Manuhcruz")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8486769140")
    WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "")
    CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")

    # YouTube API Configuration
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
    YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "unlisted")
    PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

    # Channel Brand Lock
    CHANNEL_NAME = "AI Tools Lab"
    CHANNEL_HANDLE = "@AiToolsLab-w9y"
    CHANNEL_SLOGAN = "Explore • Learn • Create • Grow"
    BUSINESS_EMAIL = "jarvisaiassistant28@gmail.com"
    TARGET_NICHE = os.getenv("TARGET_NICHE", "AI Tools, Video & Image Creation Tutorials, Automation & Productivity")
    VOICE_MODEL = os.getenv("VOICE_MODEL", "en-US-ChristopherNeural")


# ==============================================================================
# 2. ZERO-DOLLAR LLM DISPATCHER
# ==============================================================================
def query_llm(prompt: str, system_prompt: str = "You are an expert YouTube growth strategist.") -> str:
    if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": f"{system_prompt}\n\nTask:\n{prompt}"}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLM] Gemini request notice: {e}. Checking backup...")

    if Config.GROQ_API_KEY and Config.GROQ_API_KEY != "your_groq_api_key_here":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {Config.GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLM] Groq request notice: {e}")

    return None


# ==============================================================================
# 3. AGENT 1 & 2: NICK & MAX (TEAM STRATEGY & ASPECT RATIO DECISION)
# ==============================================================================
class StrategyAgent:
    def __init__(self):
        self.name = "Nick & Max (Strategy Team)"

    def plan_video(self, niche: str) -> dict:
        """
        Communicates and decides:
        1. Winning Topic
        2. Format: 'SHORTS' (9:16 vertical, 45-60s) or 'LONG' (16:9 landscape, 4-6m)
        3. Pacing & visual requirements
        """
        prompt = f"""
Act as Nick and Max, YouTube Strategists for {Config.CHANNEL_NAME}.
Target niche: {niche}

Decide:
1. One viral video concept.
2. Best aspect ratio: 'SHORTS' (9:16 vertical) OR 'LONG' (16:9 landscape).
3. The core psychological hook.

Format your response as strict JSON:
{{
  "title": "5 Insane Free AI Tools You Didn't Know Existed",
  "format": "SHORTS",
  "width": 1080,
  "height": 1920,
  "estimated_duration_sec": 50,
  "hook": "Stop paying $20 a month for AI! These 5 tools are 100% free."
}}
"""
        res = query_llm(prompt, "You are Nick and Max. Return valid JSON only.")
        if res:
            try:
                clean_json = res.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                data = json.loads(clean_json)
                if data.get("format") not in ["SHORTS", "LONG"]:
                    data["format"] = "SHORTS"
                data["width"] = 1080 if data["format"] == "SHORTS" else 1920
                data["height"] = 1920 if data["format"] == "SHORTS" else 1080
                return data
            except Exception as e:
                print(f"[Strategy] JSON parse notice: {e}")

        # Default smart strategy: Fast, high-retention 9:16 YouTube Short
        return {
            "title": "5 Insane Free AI Tools You Didn't Know Existed",
            "format": "SHORTS",
            "width": 1080,
            "height": 1920,
            "estimated_duration_sec": 50,
            "hook": "Stop paying for AI! These 5 hidden tools are 100% free forever."
        }


# ==============================================================================
# 4. AGENT 3: SAM (DYNAMIC RETENTION SCRIPTWRITER)
# ==============================================================================
class ScriptwriterAgent:
    def __init__(self):
        self.name = "Sam (Retention Scriptwriter)"

    def write_script(self, plan: dict) -> dict:
        is_shorts = (plan.get("format") == "SHORTS")
        length_guide = "45-55 seconds (around 120-140 words, rapid fire, punchy)" if is_shorts else "4-5 minutes (600 words)"

        prompt = f"""
Act as Sam, master retention scriptwriter for {Config.CHANNEL_NAME}.
Topic: {plan.get('title')}
Format: {plan.get('format')} ({length_guide})
Hook: {plan.get('hook')}

Break this script into 6 to 8 fast-paced micro-scenes (each 3 to 5 seconds max).
For each scene, give:
1. Spoken words (narrator)
2. Tool name / visual angle to show

Return clean text formatted by scenes.
"""
        res = query_llm(prompt, "You are Sam, elite YouTube scriptwriter. Zero fluff.")
        if not res:
            if is_shorts:
                res = """[SCENE 1: THE HOOK]
Stop paying for ChatGPT and expensive AI tools! Here are 3 hidden gems that are 100% free right now.

[SCENE 2: GOOGLE AI STUDIO]
First is Google AI Studio. You get direct access to Gemini with a million token context window without paying a dime.

[SCENE 3: HUGGING FACE SPACES]
Second is Hugging Face Spaces. It gives you thousands of open-source video, image, and voice models running live for zero dollars.

[SCENE 4: CURSOR AI EDITOR]
Third is Cursor. It's an AI-native coding environment that builds full automations directly from plain English prompts.

[SCENE 5: OUTRO & CTA]
All links are pinned in the comments below. Subscribe to AI Tools Lab for daily free workflow tutorials!
"""
            else:
                res = """[SCENE 1]
Right now, creators are wasting hundreds of dollars on paid AI subscriptions. Here is how to run an entire studio for zero dollars.
[SCENE 2]
Tool number one is Google AI Studio. It gives you million-token context access completely free.
[SCENE 3]
Tool number two is Hugging Face Spaces for free open-source image and video generation.
[SCENE 4]
Tool number three is Cursor for autonomous coding and workflow execution.
[SCENE 5]
Subscribe to AI Tools Lab for daily free tools breakdowns!
"""

        return {
            "full_script": res,
            "is_shorts": is_shorts
        }


# ==============================================================================
# 5. MULTI-ANGLE VISUAL ENGINE (BROWSER & HIGH-RES UI CARDS)
# ==============================================================================

# ==============================================================================
# 5. REAL MOTION B-ROLL ENGINE (PIXABAY 1080p HD VIDEO FETCHER)
# ==============================================================================
class RealVideoBrollEngine:
    """
    Downloads real 1080p HD motion video clips from Pixabay API.
    Kills static image slides permanently.
    """
    def __init__(self, output_dir: str = "samples/broll"):
        self.output_dir = output_dir
        self.api_key = Config.PIXABAY_API_KEY
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_video_clips(self, keywords: list, is_portrait: bool = True, count: int = 5) -> list:
        downloaded = []
        if not self.api_key:
            print("[BrollEngine] Notice: PIXABAY_API_KEY not configured. Falling back to dynamic visual cards.")
            return []

        print(f"[BrollEngine] 🎥 Searching Pixabay for {len(keywords)} real motion video clips...")
        for kw in keywords[:count]:
            try:
                # Orientation filter
                encoded_q = urllib.parse.quote(kw)
                url = f"https://pixabay.com/api/videos/?key={self.api_key}&q={encoded_q}&video_type=film&per_page=5"
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    hits = data.get("hits", [])
                    if hits:
                        # pick best resolution
                        video_entry = hits[0]
                        v_files = video_entry.get("videos", {})
                        # Try medium or large
                        target_file = v_files.get("medium", v_files.get("small", v_files.get("large", {})))
                        download_url = target_file.get("url")
                        if download_url:
                            out_clip = os.path.join(self.output_dir, f"clip_{len(downloaded)+1}.mp4")
                            print(f"[BrollEngine] Downloading real HD clip for '{kw}'...")
                            v_resp = requests.get(download_url, stream=True, timeout=30)
                            with open(out_clip, "wb") as f:
                                for chunk in v_resp.iter_content(chunk_size=1024 * 1024):
                                    if chunk:
                                        f.write(chunk)
                            if os.path.exists(out_clip) and os.path.getsize(out_clip) > 50000:
                                downloaded.append(out_clip)
                                print(f"[BrollEngine] ✅ Saved real video clip: {out_clip} ({os.path.getsize(out_clip)/1024:.0f} KB)")
            except Exception as e:
                print(f"[BrollEngine] Notice downloading '{kw}': {e}")

        return downloaded

class VisualDirectorAgent:
    """
    Kills the frozen single-screenshot slop.
    Generates 6-10 distinct visual scenes tailored to the exact aspect ratio (9:16 or 16:9).
    """
    def __init__(self, output_dir: str = "samples/scenes"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def create_scene_visuals(self, width: int = 1080, height: int = 1920) -> list:
        from PIL import Image, ImageDraw, ImageFont

        scenes_data = [
            ("⚡ THE $0 AI REVOLUTION", "Stop Paying For Subscriptions", "#090d16", "#ef4444", "ZERO DOLLARS"),
            ("🤖 GOOGLE AI STUDIO", "Gemini 1.5 • 1M Token Context", "#0f172a", "#38bdf8", "FREE DEVELOPER TIER"),
            ("🎨 HUGGING FACE SPACES", "Open-Source Video & Image AI", "#1e1b4b", "#a855f7", "COMMUNITY ZEROGPU"),
            ("💻 CURSOR AI COMPOSER", "Build Full Apps in Plain English", "#022c22", "#22c55e", "NO CODING NEEDED"),
            ("⚡ WORKFLOW SCORECARD", "Speed: 10/10 • Cost: $0.00", "#18181b", "#facc15", "100% VERIFIED"),
            ("🚀 AI TOOLS LAB", "Explore • Learn • Create • Grow", "#0c4a6e", "#38bdf8", "SUBSCRIBE FOR DAILY TIPS")
        ]

        generated_paths = []
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(width * 0.055))
            f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(width * 0.035))
            f_badge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(width * 0.028))
        except Exception:
            f_title = f_sub = f_badge = ImageFont.load_default()

        for idx, (title, sub, bg_color, accent, badge_text) in enumerate(scenes_data):
            img = Image.new("RGB", (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Modern Tech Grid & Glow
            draw.rectangle([0, 0, width, int(height * 0.01)], fill=accent)
            draw.rectangle([0, height - int(height * 0.01), width, height], fill=accent)

            # Center Card Container
            card_w = int(width * 0.88)
            card_h = int(height * 0.55) if height > width else int(height * 0.7)
            card_x = (width - card_w) // 2
            card_y = (height - card_h) // 2

            # Outer glow frame
            draw.rounded_rectangle([card_x - 3, card_y - 3, card_x + card_w + 3, card_y + card_h + 3], radius=24, fill=accent)
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill="#0f172a")

            # Card Header Bar
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + int(card_h * 0.16)], radius=24, fill="#1e293b")
            draw.text((card_x + 30, card_y + int(card_h * 0.04)), f"AI TOOLS LAB • SCENE {idx+1}", font=f_badge, fill=accent)

            # Main Title
            draw.text((card_x + 30, card_y + int(card_h * 0.25)), title, font=f_title, fill="#ffffff")
            draw.text((card_x + 30, card_y + int(card_h * 0.40)), sub, font=f_sub, fill="#94a3b8")

            # Status Badge Pill
            pill_y = card_y + int(card_h * 0.58)
            draw.rounded_rectangle([card_x + 30, pill_y, card_x + 30 + int(card_w * 0.65), pill_y + int(card_h * 0.12)], radius=12, fill=accent)
            draw.text((card_x + 50, pill_y + int(card_h * 0.025)), badge_text, font=f_badge, fill="#000000" if accent == "#facc15" else "#ffffff")

            # Metric Bar
            bar_y = card_y + int(card_h * 0.78)
            draw.text((card_x + 30, bar_y), "Performance Verified", font=f_sub, fill="#64748b")
            draw.rounded_rectangle([card_x + 30, bar_y + 35, card_x + card_w - 30, bar_y + 50], radius=8, fill="#334155")
            draw.rounded_rectangle([card_x + 30, bar_y + 35, card_x + int(card_w * 0.82), bar_y + 50], radius=8, fill=accent)

            # Footer
            draw.text(((width - int(width * 0.7)) // 2, height - int(height * 0.08)), f"{Config.CHANNEL_SLOGAN}", font=f_sub, fill="#64748b")

            out_path = os.path.join(self.output_dir, f"scene_{idx+1}.png")
            img.save(out_path, "PNG")
            generated_paths.append(out_path)

        print(f"[VisualDirector] ✅ Generated {len(generated_paths)} multi-angle scene visuals for {width}x{height}!")
        return generated_paths


# ==============================================================================
# 6. VOICEOVER ENGINE (EDGE-TTS WITH DYNAMIC PACING)
# ==============================================================================
class VoiceoverAgent:
    def __init__(self, voice: str = Config.VOICE_MODEL):
        self.voice = voice

    async def generate_speech_async(self, text: str, output_path: str):
        try:
            import edge_tts
            import re
            clean_text = re.sub(r'\[.*?\]', '', text)
            clean_text = re.sub(r'#+\s.*', '', clean_text)
            clean_text = re.sub(r'\*\*.*?\*\*', '', clean_text).strip()
            communicate = edge_tts.Communicate(clean_text, self.voice)
            await communicate.save(output_path)
            print(f"[Voiceover] ✅ Studio narration synthesized: {output_path}")
            return True, output_path
        except Exception as e:
            print(f"[Voiceover] Notice: {e}")
            with open(output_path.replace(".mp3", ".txt"), "w") as f:
                f.write(text)
            return False, str(e)

    def generate(self, text: str, output_path: str = "samples/sample_voiceover.mp3"):
        return asyncio.run(self.generate_speech_async(text, output_path))


# ==============================================================================
# 7. KINETIC SUBTITLE GENERATOR (.ASS FORMAT WITH WORD HIGHLIGHTS)
# ==============================================================================
class KineticSubtitleGenerator:
    """
    Creates Alex Hormozi / CapCut-style kinetic bouncing subtitles.
    Highlights current spoken words in electric yellow with thick black stroke.
    """
    @staticmethod
    def generate_ass(text: str, total_duration_sec: float, width: int, height: int, output_path: str = "samples/subtitles.ass") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        import re
        words = re.sub(r'\[.*?\]', '', text).replace('\n', ' ').split()
        words = [w.strip() for w in words if len(w.strip()) > 0]

        if not words:
            words = ["AI", "TOOLS", "LAB", "EXPLORE", "LEARN", "CREATE", "GROW"]

        font_size = int(width * 0.065) if height > width else int(width * 0.038)
        margin_v = int(height * 0.35) if height > width else int(height * 0.12)

        ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,30,30,{margin_v},1
Style: Highlight,DejaVu Sans,{int(font_size * 1.08)},&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,105,105,0,0,1,8,4,2,30,30,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        # Distribute words evenly across timeline
        sec_per_word = max(0.28, total_duration_sec / len(words))
        events = []
        chunk_size = 4 if height > width else 6

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            start_t = i * sec_per_word
            end_t = min(total_duration_sec, (i + len(chunk)) * sec_per_word)

            def fmt_time(s):
                h = int(s // 3600)
                m = int((s % 3600) // 60)
                sec = s % 60
                return f"{h:01d}:{m:02d}:{sec:05.2f}"

            t_start_str = fmt_time(start_t)
            t_end_str = fmt_time(end_t)
            sentence = " ".join(chunk).upper()

            events.append(f"Dialogue: 0,{t_start_str},{t_end_str},Highlight,,0,0,0,,{{\\c&H00FFFF&}}{sentence}")

        with open(output_path, "w") as f:
            f.write(ass_header + "\n".join(events) + "\n")

        print(f"[SubtitleGenerator] ✅ Created kinetic word-by-word subtitles: {output_path}")
        return output_path


# ==============================================================================
# 8. LEO: THE MULTI-SCENE COMPILER & CONCAT TIMELINE ENGINE
# ===============================================================import os
import sys
import json
import time
import asyncio
import urllib.parse
import subprocess
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# 1. GLOBAL CONFIGURATION & CHANNEL BRANDING
# ==============================================================================
class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    # Alert Configuration (Telegram & WhatsApp - 100% Free)
    TELEGRAM_USER = os.getenv("TELEGRAM_USER", "@Manuhcruz")
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "8486769140")
    WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "")
    CALLMEBOT_API_KEY = os.getenv("CALLMEBOT_API_KEY", "")

    # YouTube API Configuration
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID", "")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET", "")
    YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN", "")
    YOUTUBE_PRIVACY_STATUS = os.getenv("YOUTUBE_PRIVACY_STATUS", "unlisted")
    PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")

    # Channel Brand Lock
    CHANNEL_NAME = "AI Tools Lab"
    CHANNEL_HANDLE = "@AiToolsLab-w9y"
    CHANNEL_SLOGAN = "Explore • Learn • Create • Grow"
    BUSINESS_EMAIL = "jarvisaiassistant28@gmail.com"
    TARGET_NICHE = os.getenv("TARGET_NICHE", "AI Tools, Video & Image Creation Tutorials, Automation & Productivity")
    VOICE_MODEL = os.getenv("VOICE_MODEL", "en-US-ChristopherNeural")


# ==============================================================================
# 2. ZERO-DOLLAR LLM DISPATCHER
# ==============================================================================
def query_llm(prompt: str, system_prompt: str = "You are an expert YouTube growth strategist.") -> str:
    if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != "your_gemini_api_key_here":
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
            payload = {
                "contents": [{"role": "user", "parts": [{"text": f"{system_prompt}\n\nTask:\n{prompt}"}]}],
                "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print(f"[LLM] Gemini request notice: {e}. Checking backup...")

    if Config.GROQ_API_KEY and Config.GROQ_API_KEY != "your_groq_api_key_here":
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {Config.GROQ_API_KEY}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[LLM] Groq request notice: {e}")

    return None


# ==============================================================================
# 3. AGENT 1 & 2: NICK & MAX (TEAM STRATEGY & ASPECT RATIO DECISION)
# ==============================================================================
class StrategyAgent:
    def __init__(self):
        self.name = "Nick & Max (Strategy Team)"

    def plan_video(self, niche: str) -> dict:
        """
        Communicates and decides:
        1. Winning Topic
        2. Format: 'SHORTS' (9:16 vertical, 45-60s) or 'LONG' (16:9 landscape, 4-6m)
        3. Pacing & visual requirements
        """
        prompt = f"""
Act as Nick and Max, YouTube Strategists for {Config.CHANNEL_NAME}.
Target niche: {niche}

Decide:
1. One viral video concept.
2. Best aspect ratio: 'SHORTS' (9:16 vertical) OR 'LONG' (16:9 landscape).
3. The core psychological hook.

Format your response as strict JSON:
{{
  "title": "5 Insane Free AI Tools You Didn't Know Existed",
  "format": "SHORTS",
  "width": 1080,
  "height": 1920,
  "estimated_duration_sec": 50,
  "hook": "Stop paying $20 a month for AI! These 5 tools are 100% free."
}}
"""
        res = query_llm(prompt, "You are Nick and Max. Return valid JSON only.")
        if res:
            try:
                clean_json = res.strip()
                if "```json" in clean_json:
                    clean_json = clean_json.split("```json")[1].split("```")[0].strip()
                elif "```" in clean_json:
                    clean_json = clean_json.split("```")[1].split("```")[0].strip()
                data = json.loads(clean_json)
                if data.get("format") not in ["SHORTS", "LONG"]:
                    data["format"] = "SHORTS"
                data["width"] = 1080 if data["format"] == "SHORTS" else 1920
                data["height"] = 1920 if data["format"] == "SHORTS" else 1080
                return data
            except Exception as e:
                print(f"[Strategy] JSON parse notice: {e}")

        # Default smart strategy: Fast, high-retention 9:16 YouTube Short
        return {
            "title": "5 Insane Free AI Tools You Didn't Know Existed",
            "format": "SHORTS",
            "width": 1080,
            "height": 1920,
            "estimated_duration_sec": 50,
            "hook": "Stop paying for AI! These 5 hidden tools are 100% free forever."
        }


# ==============================================================================
# 4. AGENT 3: SAM (DYNAMIC RETENTION SCRIPTWRITER)
# ==============================================================================
class ScriptwriterAgent:
    def __init__(self):
        self.name = "Sam (Retention Scriptwriter)"

    def write_script(self, plan: dict) -> dict:
        is_shorts = (plan.get("format") == "SHORTS")
        length_guide = "45-55 seconds (around 120-140 words, rapid fire, punchy)" if is_shorts else "4-5 minutes (600 words)"

        prompt = f"""
Act as Sam, master retention scriptwriter for {Config.CHANNEL_NAME}.
Topic: {plan.get('title')}
Format: {plan.get('format')} ({length_guide})
Hook: {plan.get('hook')}

Break this script into 6 to 8 fast-paced micro-scenes (each 3 to 5 seconds max).
For each scene, give:
1. Spoken words (narrator)
2. Tool name / visual angle to show

Return clean text formatted by scenes.
"""
        res = query_llm(prompt, "You are Sam, elite YouTube scriptwriter. Zero fluff.")
        if not res:
            if is_shorts:
                res = """[SCENE 1: THE HOOK]
Stop paying for ChatGPT and expensive AI tools! Here are 3 hidden gems that are 100% free right now.

[SCENE 2: GOOGLE AI STUDIO]
First is Google AI Studio. You get direct access to Gemini with a million token context window without paying a dime.

[SCENE 3: HUGGING FACE SPACES]
Second is Hugging Face Spaces. It gives you thousands of open-source video, image, and voice models running live for zero dollars.

[SCENE 4: CURSOR AI EDITOR]
Third is Cursor. It's an AI-native coding environment that builds full automations directly from plain English prompts.

[SCENE 5: OUTRO & CTA]
All links are pinned in the comments below. Subscribe to AI Tools Lab for daily free workflow tutorials!
"""
            else:
                res = """[SCENE 1]
Right now, creators are wasting hundreds of dollars on paid AI subscriptions. Here is how to run an entire studio for zero dollars.
[SCENE 2]
Tool number one is Google AI Studio. It gives you million-token context access completely free.
[SCENE 3]
Tool number two is Hugging Face Spaces for free open-source image and video generation.
[SCENE 4]
Tool number three is Cursor for autonomous coding and workflow execution.
[SCENE 5]
Subscribe to AI Tools Lab for daily free tools breakdowns!
"""

        return {
            "full_script": res,
            "is_shorts": is_shorts
        }


# ==============================================================================
# 5. MULTI-ANGLE VISUAL ENGINE (BROWSER & HIGH-RES UI CARDS)
# ==============================================================================

# ==============================================================================
# 5. REAL MOTION B-ROLL ENGINE (PIXABAY 1080p HD VIDEO FETCHER)
# ==============================================================================
class RealVideoBrollEngine:
    """
    Downloads real 1080p HD motion video clips from Pixabay API.
    Kills static image slides permanently.
    """
    def __init__(self, output_dir: str = "samples/broll"):
        self.output_dir = output_dir
        self.api_key = Config.PIXABAY_API_KEY
        os.makedirs(self.output_dir, exist_ok=True)

    def fetch_video_clips(self, keywords: list, is_portrait: bool = True, count: int = 5) -> list:
        downloaded = []
        if not self.api_key:
            print("[BrollEngine] Notice: PIXABAY_API_KEY not configured. Falling back to dynamic visual cards.")
            return []

        print(f"[BrollEngine] 🎥 Searching Pixabay for {len(keywords)} real motion video clips...")
        for kw in keywords[:count]:
            try:
                # Orientation filter
                encoded_q = urllib.parse.quote(kw)
                url = f"https://pixabay.com/api/videos/?key={self.api_key}&q={encoded_q}&video_type=film&per_page=5"
                r = requests.get(url, timeout=15)
                if r.status_code == 200:
                    data = r.json()
                    hits = data.get("hits", [])
                    if hits:
                        # pick best resolution
                        video_entry = hits[0]
                        v_files = video_entry.get("videos", {})
                        # Try medium or large
                        target_file = v_files.get("medium", v_files.get("small", v_files.get("large", {})))
                        download_url = target_file.get("url")
                        if download_url:
                            out_clip = os.path.join(self.output_dir, f"clip_{len(downloaded)+1}.mp4")
                            print(f"[BrollEngine] Downloading real HD clip for '{kw}'...")
                            v_resp = requests.get(download_url, stream=True, timeout=30)
                            with open(out_clip, "wb") as f:
                                for chunk in v_resp.iter_content(chunk_size=1024 * 1024):
                                    if chunk:
                                        f.write(chunk)
                            if os.path.exists(out_clip) and os.path.getsize(out_clip) > 50000:
                                downloaded.append(out_clip)
                                print(f"[BrollEngine] ✅ Saved real video clip: {out_clip} ({os.path.getsize(out_clip)/1024:.0f} KB)")
            except Exception as e:
                print(f"[BrollEngine] Notice downloading '{kw}': {e}")

        return downloaded

class VisualDirectorAgent:
    """
    Kills the frozen single-screenshot slop.
    Generates 6-10 distinct visual scenes tailored to the exact aspect ratio (9:16 or 16:9).
    """
    def __init__(self, output_dir: str = "samples/scenes"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def create_scene_visuals(self, width: int = 1080, height: int = 1920) -> list:
        from PIL import Image, ImageDraw, ImageFont

        scenes_data = [
            ("⚡ THE $0 AI REVOLUTION", "Stop Paying For Subscriptions", "#090d16", "#ef4444", "ZERO DOLLARS"),
            ("🤖 GOOGLE AI STUDIO", "Gemini 1.5 • 1M Token Context", "#0f172a", "#38bdf8", "FREE DEVELOPER TIER"),
            ("🎨 HUGGING FACE SPACES", "Open-Source Video & Image AI", "#1e1b4b", "#a855f7", "COMMUNITY ZEROGPU"),
            ("💻 CURSOR AI COMPOSER", "Build Full Apps in Plain English", "#022c22", "#22c55e", "NO CODING NEEDED"),
            ("⚡ WORKFLOW SCORECARD", "Speed: 10/10 • Cost: $0.00", "#18181b", "#facc15", "100% VERIFIED"),
            ("🚀 AI TOOLS LAB", "Explore • Learn • Create • Grow", "#0c4a6e", "#38bdf8", "SUBSCRIBE FOR DAILY TIPS")
        ]

        generated_paths = []
        try:
            f_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(width * 0.055))
            f_sub = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", int(width * 0.035))
            f_badge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(width * 0.028))
        except Exception:
            f_title = f_sub = f_badge = ImageFont.load_default()

        for idx, (title, sub, bg_color, accent, badge_text) in enumerate(scenes_data):
            img = Image.new("RGB", (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Modern Tech Grid & Glow
            draw.rectangle([0, 0, width, int(height * 0.01)], fill=accent)
            draw.rectangle([0, height - int(height * 0.01), width, height], fill=accent)

            # Center Card Container
            card_w = int(width * 0.88)
            card_h = int(height * 0.55) if height > width else int(height * 0.7)
            card_x = (width - card_w) // 2
            card_y = (height - card_h) // 2

            # Outer glow frame
            draw.rounded_rectangle([card_x - 3, card_y - 3, card_x + card_w + 3, card_y + card_h + 3], radius=24, fill=accent)
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill="#0f172a")

            # Card Header Bar
            draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + int(card_h * 0.16)], radius=24, fill="#1e293b")
            draw.text((card_x + 30, card_y + int(card_h * 0.04)), f"AI TOOLS LAB • SCENE {idx+1}", font=f_badge, fill=accent)

            # Main Title
            draw.text((card_x + 30, card_y + int(card_h * 0.25)), title, font=f_title, fill="#ffffff")
            draw.text((card_x + 30, card_y + int(card_h * 0.40)), sub, font=f_sub, fill="#94a3b8")

            # Status Badge Pill
            pill_y = card_y + int(card_h * 0.58)
            draw.rounded_rectangle([card_x + 30, pill_y, card_x + 30 + int(card_w * 0.65), pill_y + int(card_h * 0.12)], radius=12, fill=accent)
            draw.text((card_x + 50, pill_y + int(card_h * 0.025)), badge_text, font=f_badge, fill="#000000" if accent == "#facc15" else "#ffffff")

            # Metric Bar
            bar_y = card_y + int(card_h * 0.78)
            draw.text((card_x + 30, bar_y), "Performance Verified", font=f_sub, fill="#64748b")
            draw.rounded_rectangle([card_x + 30, bar_y + 35, card_x + card_w - 30, bar_y + 50], radius=8, fill="#334155")
            draw.rounded_rectangle([card_x + 30, bar_y + 35, card_x + int(card_w * 0.82), bar_y + 50], radius=8, fill=accent)

            # Footer
            draw.text(((width - int(width * 0.7)) // 2, height - int(height * 0.08)), f"{Config.CHANNEL_SLOGAN}", font=f_sub, fill="#64748b")

            out_path = os.path.join(self.output_dir, f"scene_{idx+1}.png")
            img.save(out_path, "PNG")
            generated_paths.append(out_path)

        print(f"[VisualDirector] ✅ Generated {len(generated_paths)} multi-angle scene visuals for {width}x{height}!")
        return generated_paths


# ==============================================================================
# 6. VOICEOVER ENGINE (EDGE-TTS WITH DYNAMIC PACING)
# ==============================================================================
class VoiceoverAgent:
    def __init__(self, voice: str = Config.VOICE_MODEL):
        self.voice = voice

    async def generate_speech_async(self, text: str, output_path: str):
        try:
            import edge_tts
            import re
            clean_text = re.sub(r'\[.*?\]', '', text)
            clean_text = re.sub(r'#+\s.*', '', clean_text)
            clean_text = re.sub(r'\*\*.*?\*\*', '', clean_text).strip()
            communicate = edge_tts.Communicate(clean_text, self.voice)
            await communicate.save(output_path)
            print(f"[Voiceover] ✅ Studio narration synthesized: {output_path}")
            return True, output_path
        except Exception as e:
            print(f"[Voiceover] Notice: {e}")
            with open(output_path.replace(".mp3", ".txt"), "w") as f:
                f.write(text)
            return False, str(e)

    def generate(self, text: str, output_path: str = "samples/sample_voiceover.mp3"):
        return asyncio.run(self.generate_speech_async(text, output_path))


# ==============================================================================
# 7. KINETIC SUBTITLE GENERATOR (.ASS FORMAT WITH WORD HIGHLIGHTS)
# ==============================================================================
class KineticSubtitleGenerator:
    """
    Creates Alex Hormozi / CapCut-style kinetic bouncing subtitles.
    Highlights current spoken words in electric yellow with thick black stroke.
    """
    @staticmethod
    def generate_ass(text: str, total_duration_sec: float, width: int, height: int, output_path: str = "samples/subtitles.ass") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        import re
        words = re.sub(r'\[.*?\]', '', text).replace('\n', ' ').split()
        words = [w.strip() for w in words if len(w.strip()) > 0]

        if not words:
            words = ["AI", "TOOLS", "LAB", "EXPLORE", "LEARN", "CREATE", "GROW"]

        font_size = int(width * 0.065) if height > width else int(width * 0.038)
        margin_v = int(height * 0.35) if height > width else int(height * 0.12)

        ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,DejaVu Sans,{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,30,30,{margin_v},1
Style: Highlight,DejaVu Sans,{int(font_size * 1.08)},&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,105,105,0,0,1,8,4,2,30,30,{margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
        # Distribute words evenly across timeline
        sec_per_word = max(0.28, total_duration_sec / len(words))
        events = []
        chunk_size = 4 if height > width else 6

        for i in range(0, len(words), chunk_size):
            chunk = words[i:i + chunk_size]
            start_t = i * sec_per_word
            end_t = min(total_duration_sec, (i + len(chunk)) * sec_per_word)

            def fmt_time(s):
                h = int(s // 3600)
                m = int((s % 3600) // 60)
                sec = s % 60
                return f"{h:01d}:{m:02d}:{sec:05.2f}"

            t_start_str = fmt_time(start_t)
            t_end_str = fmt_time(end_t)
            sentence = " ".join(chunk).upper()

            events.append(f"Dialogue: 0,{t_start_str},{t_end_str},Highlight,,0,0,0,,{{\\c&H00FFFF&}}{sentence}")

        with open(output_path, "w") as f:
            f.write(ass_header + "\n".join(events) + "\n")

        print(f"[SubtitleGenerator] ✅ Created kinetic word-by-word subtitles: {output_path}")
        return output_path


# ==============================================================================
# 8. LEO: THE MULTI-SCENE COMPILER & CONCAT TIMELINE ENGINE
# ===============================================================
