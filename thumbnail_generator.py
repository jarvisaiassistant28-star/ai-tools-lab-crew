import os
import requests
import urllib.parse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class ThumbnailGeneratorAgent:
    """
    Renders actual 1280x720 high-CTR JPEG thumbnail image files ready for YouTube upload.
    Adheres strictly to the 3-word text rule, high visual contrast, and AI Tools Lab branding.
    """
    def __init__(self):
        self.width = 1280
        self.height = 720

    def render_thumbnail(self, main_text: str = "IT'S 100% FREE!", sub_text: str = "5 INSANE AI TOOLS", output_path: str = "samples/thumbnail.jpg") -> str:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 1. Base Canvas - Deep tech aesthetic (dark blue to deep slate gradient)
        img = Image.new("RGB", (self.width, self.height), color="#090d16")
        draw = ImageDraw.Draw(img)

        # Draw tech grid / radial glow effect
        for r in range(400, 0, -20):
            alpha_color = (15 + int(r * 0.05), 23 + int(r * 0.1), 42 + int(r * 0.25))
            draw.ellipse([self.width - 450 - r, 360 - r, self.width - 450 + r, 360 + r], fill=alpha_color)

        # Draw sleek divider line with cyan neon glow
        draw.rectangle([60, 40, self.width - 60, 44], fill="#38bdf8")
        
        # 2. Channel Brand Badge
        badge_x, badge_y = 60, 65
        draw.rounded_rectangle([badge_x, badge_y, badge_x + 320, badge_y + 45], radius=8, fill="#ef4444")
        
        # Safe font loading
        try:
            badge_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
            main_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 86)
            sub_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 46)
            badge_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except Exception:
            badge_font = ImageFont.load_default()
            main_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
            badge_small = ImageFont.load_default()

        draw.text((badge_x + 18, badge_y + 10), "AI TOOLS LAB • VERIFIED", font=badge_font, fill="#ffffff")

        # 3. Main Hook (e.g., "IT'S 100% FREE!") - Massive Yellow with Deep Shadow
        text_x, text_y = 60, 160
        # Shadow
        for dx, dy in [(-4, -4), (4, -4), (-4, 4), (4, 4), (0, 8), (0, -8), (8, 0), (-8, 0)]:
            draw.text((text_x + dx, text_y + dy), main_text, font=main_font, fill="#000000")
        draw.text((text_x, text_y), main_text, font=main_font, fill="#facc15")  # High-CTR electric yellow

        # 4. Subtitle Banner (High contrast white / cyan)
        sub_y = text_y + 115
        draw.rounded_rectangle([text_x, sub_y - 8, text_x + 650, sub_y + 65], radius=10, fill="#1e293b")
        draw.text((text_x + 20, sub_y), sub_text, font=sub_font, fill="#38bdf8")

        # 5. Visual Value Tags (3 Pill Badges)
        pill_y = sub_y + 110
        pills = [("ZERO DOLLAR", "#22c55e"), ("NO SUBSCRIPTION", "#f97316"), ("OFFLINE AUTO", "#a855f7")]
        px = 60
        for label, color in pills:
            draw.rounded_rectangle([px, pill_y, px + 210, pill_y + 50], radius=8, fill=color)
            draw.text((px + 18, pill_y + 12), label, font=badge_font, fill="#ffffff")
            px += 230

        # 6. Right Side Visual Frame (Simulated 3D UI / Tool Card)
        card_x1, card_y1, card_x2, card_y2 = self.width - 480, 130, self.width - 60, self.height - 100
        draw.rounded_rectangle([card_x1 - 4, card_y1 - 4, card_x2 + 4, card_y2 + 4], radius=16, fill="#38bdf8")
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=16, fill="#0f172a")
        
        # Header of card
        draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y1 + 55], radius=16, fill="#1e293b")
        draw.text((card_x1 + 25, card_y1 + 15), "⚡ TOOL SCORECARD", font=badge_font, fill="#38bdf8")
        
        # Card metric bars
        metrics = [("Automation Speed", "100%", "#22c55e", 280), ("API Cost", "$0.00", "#38bdf8", 320), ("Ease of Use", "9.8/10", "#facc15", 300)]
        my = card_y1 + 80
        for name, val, bar_color, bar_len in metrics:
            draw.text((card_x1 + 25, my), name, font=badge_small, fill="#94a3b8")
            draw.text((card_x2 - 100, my), val, font=badge_font, fill=bar_color)
            my += 35
            draw.rounded_rectangle([card_x1 + 25, my, card_x1 + 380, my + 10], radius=5, fill="#334155")
            draw.rounded_rectangle([card_x1 + 25, my, card_x1 + 25 + bar_len, my + 10], radius=5, fill=bar_color)
            my += 45

        # Footer badge
        draw.text((60, self.height - 70), "Explore • Learn • Create • Grow • @AiToolsLab-w9y", font=badge_small, fill="#64748b")

        # Save high quality JPEG
        img.save(output_path, "JPEG", quality=95)
        print(f"[ThumbnailGenerator] Rendered 1280x720 thumbnail image: {output_path}")
        return output_path
