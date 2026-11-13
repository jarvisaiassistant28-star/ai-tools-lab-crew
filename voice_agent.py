import asyncio
import os

class VoiceoverAgent:
    """Agent 5: Voiceover Engine using Microsoft Edge-TTS (100% Free, unlimited, natural neural voices)."""
    def __init__(self, voice: str = "en-US-ChristopherNeural"):
        self.voice = voice

    async def generate_speech_async(self, text: str, output_path: str):
        try:
            import edge_tts
            # Strip markdown cues from spoken text
            import re
            clean_text = re.sub(r'\[.*?\]', '', text)
            clean_text = re.sub(r'#+\s.*', '', clean_text)
            clean_text = re.sub(r'\*\*.*?\*\*', '', clean_text)
            clean_text = clean_text.strip()

            communicate = edge_tts.Communicate(clean_text, self.voice)
            await communicate.save(output_path)
            return True, output_path
        except Exception as e:
            with open(output_path.replace(".mp3", ".txt"), "w") as f:
                f.write(text)
            return False, str(e)

    def generate(self, text: str, output_path: str = "samples/sample_voiceover.mp3"):
        return asyncio.run(self.generate_speech_async(text, output_path))
