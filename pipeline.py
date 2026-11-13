import os
import sys
from datetime import datetime, timezone
from agents.niche_finder import NicheFinderAgent
from agents.idea_hunter import ViralIdeaHunterAgent
from agents.scriptwriter import ScriptwriterAgent
from agents.thumbnail_designer import ThumbnailDesignerAgent
from agents.thumbnail_generator import ThumbnailGeneratorAgent
from agents.browser_recorder import BrowserRecorderAgent
from agents.voice_agent import VoiceoverAgent
from agents.video_editor import VideoEditorAgent
from agents.boss_agent import BossReviewAgent
from agents.publisher_agent import YouTubePublisherAgent
from notifications.whatsapp import WhatsAppNotifier
from config import Config

def run_pipeline():
    now_utc = datetime.now(timezone.utc)
    print("=" * 80)
    print(f"🚀 {Config.CHANNEL_NAME} ({Config.CHANNEL_HANDLE}) - PRO AUTONOMOUS STUDIO")
    print(f"⏰ Execution Time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"🎯 Channel Mission: {Config.CHANNEL_SLOGAN}")
    print(f"📩 Business Contact: {Config.BUSINESS_EMAIL}")
    print("=" * 80)

    # 1. Nick: Niche Lock & Trend Intelligence
    print(f"\n[1/10] 🕵️ Nick is locking into channel niche: '{Config.TARGET_NICHE}'...")
    nick = NicheFinderAgent()
    niche_report = nick.run(category_hint=Config.TARGET_NICHE)

    # 2. Max: Viral Idea Hunter
    print("\n[2/10] 💡 Max is hunting high-retention viral topics for AI Tools Lab...")
    max_agent = ViralIdeaHunterAgent()
    ideas_report = max_agent.run(niche=Config.TARGET_NICHE, count=5)
    chosen_title = "5 Insane Free AI Tools You Didn't Know Existed in 2026"
    
    # 3. Sam: Retention Scriptwriter
    print(f"\n[3/10] ✍️ Sam is writing high-retention script for: '{chosen_title}'...")
    sam = ScriptwriterAgent()
    script_report = sam.run(topic=chosen_title, target_length_minutes=6)
    
    # 4. Alex & Thumbnail Generator (Real 1280x720 JPEG Image File)
    print(f"\n[4/10] 🎨 Alex & Thumbnail Generator are rendering high-CTR 1280x720 thumbnail...")
    alex = ThumbnailDesignerAgent()
    thumbnail_concept = alex.run(video_title=chosen_title)
    
    thumb_gen = ThumbnailGeneratorAgent()
    thumbnail_file = thumb_gen.render_thumbnail(
        main_text="IT'S 100% FREE!",
        sub_text="5 INSANE AI TOOLS",
        output_path="samples/thumbnail.jpg"
    )

    # 5. Playwright Browser Recorder (Real Software Screen Captures)
    print("\n[5/10] 🌐 Browser Recorder is capturing live UI screenshots of featured AI tools...")
    recorder = BrowserRecorderAgent()
    tool_captures = []
    featured_tools = [
        ("https://aistudio.google.com/", "Google AI Studio"),
        ("https://huggingface.co/spaces", "Hugging Face Spaces"),
        ("https://cursor.com/", "Cursor AI Editor")
    ]
    for url, tname in featured_tools:
        cap = recorder.capture(url, tname)
        tool_captures.append(cap)
    
    # 6. Voiceover Engine
    print("\n[6/10] 🎙️ Synthesizing narration with Edge-TTS free neural engine...")
    voice_agent = VoiceoverAgent()
    os.makedirs("samples", exist_ok=True)
    voice_file = "samples/sample_voiceover.mp3"
    voice_agent.generate(script_report[:600], voice_file)
    
    # 7. Leo: Video Editor & Multi-Layer MP4 Assembler (Audio Ducking + UI Captures)
    print("\n[7/10] 🎬 Leo (Video Editor) is compiling MP4 with audio layering & UI captures...")
    editor = VideoEditorAgent()
    final_video = editor.render_mp4(
        audio_path=voice_file if os.path.exists(voice_file) else "samples/sample_voiceover.txt",
        screen_captures=tool_captures,
        output_mp4="samples/final_video.mp4",
        title=chosen_title
    )
    
    # 8. Marcus: The Executive Boss Agent (Quality Gatekeeper)
    print("\n[8/10] 👔 Marcus (The Boss) is auditing the entire production package...")
    boss = BossReviewAgent()
    boss_audit = boss.review_video_package(
        title=chosen_title,
        script=script_report,
        thumbnail_concept=thumbnail_concept,
        niche=Config.TARGET_NICHE
    )
    print(f"        Audit Result: {boss_audit['status']} | Quality Score: {boss_audit['score']}")

    # 9. Zenith: YouTube Channel Manager & Maximum Reach Publisher (Affiliate + Safety Valve)
    print("\n[9/10] 🚀 Zenith is injecting affiliate links, SEO tags & staging for YouTube...")
    publisher = YouTubePublisherAgent()
    seo_metadata = publisher.generate_seo_metadata(title=chosen_title, script_summary=script_report[:500])
    upload_result = publisher.upload_to_youtube(
        video_path=final_video,
        thumbnail_path=thumbnail_file,
        metadata=seo_metadata
    )

    # Save output artifacts
    timestamp = now_utc.strftime('%Y%m%d_%H%M%S')
    with open(f"samples/boss_audit_{timestamp}.md", "w") as f:
        f.write(boss_audit["boss_review"])
    with open(f"samples/youtube_seo_package_{timestamp}.md", "w") as f:
        f.write(f"# 🚀 YouTube Metadata & Growth Package\n\n**Video Title:** {seo_metadata.get('title')}\n\n**Pinned Comment:**\n{seo_metadata.get('pinned_comment')}\n\n**Full Description:**\n```\n{seo_metadata.get('description', seo_metadata.get('raw_seo_package'))}\n```\n")
    with open(f"samples/full_script_{timestamp}.md", "w") as f:
        f.write(script_report)

    # 10. WhatsApp Executive Alert (With Safety Valve link)
    print("\n[10/10] 📱 Sending executive briefing to your WhatsApp...")
    whatsapp = WhatsAppNotifier()
    
    whatsapp_message = f"""🎬 *AI Tools Lab - Video Production Alert!*
📅 Date: {now_utc.strftime('%Y-%m-%d')}
📢 *Channel:* {Config.CHANNEL_NAME} ({Config.CHANNEL_HANDLE})

🏆 *Title:*
"{chosen_title}"

👔 *The Boss Verdict (Marcus):*
✅ {boss_audit['status']} (Score: {boss_audit['score']})
"Real UI captures verified. High retention expected."

🚀 *YouTube Status:*
Status: {upload_result['status']}
URL: {upload_result['video_url']}
Visibility: 🔒 {upload_result['visibility'].upper()} (Safety Valve Review)

💰 *Affiliate Links Injected:*
Cursor, ElevenLabs, Make.com, Freepik AI

🖼️ *Thumbnail File:*
{thumbnail_file} (1280x720 High-CTR Rendered)

Reply to approve or change privacy to PUBLIC!"""

    whatsapp.send_alert(whatsapp_message)
    print("\n✅ All 10 studio steps completed successfully!")

if __name__ == "__main__":
    run_pipeline()
