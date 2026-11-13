import json
from .llm_client import query_llm

class ScriptwriterAgent:
    """Sam: YouTube Scriptwriter - Writes hooks, retention resets, and full ready-to-record scripts."""
    def __init__(self):
        self.name = "Sam (YouTube Scriptwriter)"
        self.role = "Tell you WHAT to say"

    def run(self, topic: str, target_length_minutes: int = 5):
        prompt = f"""
Act as Sam, master YouTube retention scriptwriter.
Write a full, high-retention video script for the topic: '{topic}'.
Estimated length: {target_length_minutes} minutes (~750-1,000 spoken words).

Script Requirements:
1. THE 10-SECOND HOOK (No filler, start right in the action with a pattern interrupt).
2. TENSION & VALUE PROMISE
3. SECTION-BY-SECTION SCRIPT with:
   - Spoken Narration
   - Visual Cues: [VISUAL: ...]
   - Sound Effects: [SFX: ...]
   - Retention Reset Points (every 60 seconds)
4. STRONG CALL TO ACTION & SEAMLESS OUTRO
"""
        response = query_llm(
            prompt=prompt,
            system_prompt="You are Sam, elite scriptwriter for top YouTube creators with average 65%+ retention rates."
        )
        if not response:
            response = self._get_fallback_script(topic)
        return response

    def _get_fallback_script(self, topic: str):
        return f"""# 🎬 Full Retention Script: {topic}
**Duration:** ~5-6 Minutes | **Target Retention:** >65%

---

### [0:00 - 0:15] THE 10-SECOND HOOK
**[VISUAL: Fast-paced dark room montage: computer terminal executing automated tasks, phone screen lighting up with WhatsApp alert, zero balance credit card alert.]**  
**[SFX: Digital whoosh + bass pulse]**  
**NARRATOR:**  
Right now, while you are watching this, thousands of developers are wasting hundreds of dollars every month on cloud servers and API subscriptions. But what if I told you that a single open-source GitHub workflow can run a 6-agent autonomous workforce for literally zero dollars... forever?

---

### [0:15 - 0:45] THE SETUP & REVEAL
**[VISUAL: Split screen showing $200 AWS bill vs. $0 GitHub Actions bill. Green checkmarks animating on screen.]**  
**[SFX: Subtle error beep transitioning into clean notification chime]**  
**NARRATOR:**  
Most people think running AI agents 24/7 requires expensive virtual private servers, paid OpenAI credits, and complex DevOps pipelines. That’s a myth. Today, you are getting the complete blueprint: how to chain intelligent agents that find viral trends, write scripts, generate voiceovers, and alert your personal WhatsApp number the second new content is ready.

---

### [0:45 - 2:00] AGENT 1 & 2: THE BRAIN TRUST
**[VISUAL: Graphic of "Nick: Niche Finder" and "Max: Idea Hunter" scanning YouTube search queries.]**  
**[SFX: Fast typing SFX + data stream sound]**  
**NARRATOR:**  
Step one is killing guesswork. The first agent, Nick, scrapes high-CPM search demand. It doesn’t guess what’s trending; it tracks view velocity. Once Nick spots an unsaturated pocket, Max kicks in to extract thirty psychological angles that force viewers to click.

---

### [2:00 - 3:30] AGENT 3 & 4: SCRIPT & VOICE ENGINE
**[VISUAL: Flowchart showing automated script hand-off to Edge-TTS neural engine.]**  
**[SFX: Smooth whoosh transition]**  
**NARRATOR:**  
Next comes Sam and the voice synthesizer. Sam breaks the script into 60-second retention loops. Then, instead of paid voice APIs that charge per character, we plug into Microsoft's free neural engine. The result? Studio-grade audio without spending a cent.

---

### [3:30 - 4:45] AGENT 5 & 6: THE OFFLINE CLOUD DISPATCH
**[VISUAL: Close-up mockup of incoming WhatsApp message with full video package summary.]**  
**[SFX: WhatsApp notification 'ding']**  
**NARRATOR:**  
Here’s the best part: you don't even need your laptop open. We host the pipeline on GitHub Actions scheduled cron runners. When the pipeline finishes, Agent 6 sends the title, script, and thumbnail package straight to your WhatsApp.

---

### [4:45 - 5:15] CALL TO ACTION
**[VISUAL: Repository link highlighted on screen with 1-click clone instruction.]**  
**[SFX: Mouse click + rising synth outro]**  
**NARRATOR:**  
The full code and step-by-step setup are completely free in the repository linked in the description. Star the repo, drop your thoughts in the comments, and subscribe for the next open-source release.
"""
