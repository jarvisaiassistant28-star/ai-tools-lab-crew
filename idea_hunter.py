import json
from .llm_client import query_llm

class ViralIdeaHunterAgent:
    """Max: Viral Idea Hunter - Studies viral videos in your niche and finds high-demand topics."""
    def __init__(self):
        self.name = "Max (Viral Idea Hunter)"
        self.role = "Tell you WHAT to create"

    def run(self, niche: str, count: int = 5):
        prompt = f"""
Act as Max, the YouTube Viral Idea Hunter.
For the niche: '{niche}', generate {count} ultra-clickable, curiosity-driven YouTube video ideas designed to get 500k+ views.

For EACH idea, provide:
1. High-CTR Title (A/B Test options)
2. The Core Curiosity Gap / Psychological Hook
3. Target Viewer Emotion
4. Estimated 30-Day View Potential
5. Key Competitor Angle

Select the #1 single best video idea to proceed with for immediate scriptwriting.
"""
        response = query_llm(
            prompt=prompt,
            system_prompt="You are Max, master of YouTube click psychology, title formatting, and viral packaging."
        )
        if not response:
            response = self._get_fallback_ideas(niche)
        return response

    def _get_fallback_ideas(self, niche: str):
        return f"""# 💡 Max's Viral Idea Blueprint ({niche})

### 🏆 WINNING PICK (Proceeding to Script):
**"They Made a $0 AI Agent That Works While You Sleep (Step-by-Step)"**
- **Alternative Title:** "I Let 6 AI Agents Run My Life for 7 Days (Zero Dollar Setup)"
- **Curiosity Gap:** Everyone thinks autonomous AI agents cost thousands in API fees or need dedicated servers. Showing how GitHub Actions + Free LLMs run forever offline breaks expectations.
- **Viewer Emotion:** Intense Curiosity & Relief (FOMO on zero-budget automation).
- **View Potential:** 750,000+ views (mass appeal to coders, students, and entrepreneurs).

---

### Additional High-Potential Concepts:
2. **"Why Big Tech Hates This 100% Free Python Automation"** (Angle: Anti-subscription sentiment)
3. **"How a 19-Year-Old Built a $10,000/mo Faceless Media House with Free Tools"** (Angle: Case study breakdown)
4. **"The Secret WhatsApp Automation No One Is Talking About"** (Angle: Instant utility, high retention)
5. **"Stop Paying for ChatGPT: 5 Zero-Dollar AI Tools Hidden on GitHub"** (Angle: Direct value, high shareability)
"""
