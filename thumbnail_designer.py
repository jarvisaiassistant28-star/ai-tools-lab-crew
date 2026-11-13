import json
import urllib.parse
from .llm_client import query_llm

class ThumbnailDesignerAgent:
    """Alex: Thumbnail Designer - Analyzes viral thumbnails and creates high-CTR visual concepts."""
    def __init__(self):
        self.name = "Alex (Thumbnail Designer)"
        self.role = "Make people CLICK"

    def run(self, video_title: str):
        prompt = f"""
Act as Alex, YouTube Thumbnail Designer & CTR Specialist.
For the video title: '{video_title}', generate 3 distinct high-CTR thumbnail concepts.

For each thumbnail concept:
1. Concept Name & Emotional Hook
2. Visual Composition (Background, Main Subject, Lighting, Color Palette)
3. Text Overlay (Strictly 2 to 4 high-impact words only)
4. AI Image Prompt (Detailed prompt for Midjourney / DALL-E / Pollinations)
5. Why this drives clicks over competitors
"""
        response = query_llm(
            prompt=prompt,
            system_prompt="You are Alex, elite YouTube thumbnail packaging director."
        )
        if not response:
            response = self._get_fallback_thumbnails(video_title)

        # Attach free image preview URLs using Pollinations.ai (100% free image generation)
        pollinations_prompt = "cinematic photorealistic 3D render, glowing neon red computer monitors showing autonomous AI code, dark cyberpunk studio, high contrast, 8k resolution"
        encoded_prompt = urllib.parse.quote(pollinations_prompt)
        image_preview_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true"

        preview_section = f"""

---
### 🖼️ Instant Free Preview Generator (Alex's Visual Concept)
- **Free Live Thumbnail URL:** {image_preview_url}
*(Powered by zero-dollar Pollinations engine - no API key required)*
"""
        return response + preview_section

    def _get_fallback_thumbnails(self, title: str):
        return f"""# 🎨 Alex's High-CTR Thumbnail Concepts for: "{title}"

### Concept 1: The "Impossible Zero" (Recommended)
- **Visual Composition:** Split screen. Left side: Frustrated developer staring at a massive red invoice "$1,840/mo". Right side: Glowing sleek neon computer desk with phone showing "$0" balance and WhatsApp alert.
- **Lighting:** Moody cinematic teal and energetic orange neon backlight.
- **Text Overlay (3 Words):** "IT'S 100% FREE!" (Bright yellow text with thick black outline).
- **AI Prompt:** `cinematic high contrast split screen, frustrated young man at dark computer desk with glowing red bill on left, relaxed programmer with glowing green screens and smartphone notification on right, hyper-detailed 8k octane render`

---

### Concept 2: The "Secret Army"
- **Visual Composition:** Center frame: 6 glowing holographic voxel avatars working simultaneously around a single holographic floating laptop.
- **Lighting:** Deep red studio lighting with aggressive rim light.
- **Text Overlay (2 Words):** "THEY WORKED?"
- **AI Prompt:** `6 miniature glowing cybernetic humanoid robots typing furiously around a holographic laptop in a dark aesthetic studio, volumetric neon red and blue lighting, 3d render`

---

### Concept 3: The "Forbidden Workflow"
- **Visual Composition:** Extreme close-up of a phone screen showing incoming WhatsApp messages with automated scripts, held in hands in front of glowing dual curved monitors.
- **Text Overlay (4 Words):** "WHILE I SLEPT..."
- **AI Prompt:** `first-person POV holding modern smartphone glowing with notification message, blurred background of multi-monitor trading desk with green status indicators, photorealistic cinematic lighting`
"""
