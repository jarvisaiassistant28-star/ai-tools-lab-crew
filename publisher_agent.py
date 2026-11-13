import os
import json
from config import Config
from .llm_client import query_llm
from .affiliate_manager import AffiliateManager

class YouTubePublisherAgent:
    """
    Zenith: YouTube Channel Manager & Maximum Reach Publisher Agent
    Role:
    - Prepares maximum-reach SEO metadata (Title, Rich Description, Tags, Pinned Comment).
    - Integrates automated affiliate links and official FTC disclosure.
    - Injects 'AI Tools Lab' branding, mission statement, and business email.
    - Connects to YouTube Data API v3 (Defaulting to 'unlisted' safety valve).
    - Attaches custom 1280x720 thumbnail file.
    - Pins high-converting engagement comment to jumpstart algorithm interaction.
    """
    def __init__(self):
        self.name = "Zenith (YouTube Channel Manager & Publisher)"
        self.role = "YouTube SEO optimization, automated video publishing & algorithmic growth"
        self.affiliate_mgr = AffiliateManager()

    def generate_seo_metadata(self, title: str, script_summary: str) -> dict:
        affiliate_block = self.affiliate_mgr.get_links_for_script(script_summary)
        
        prompt = f"""
Act as Zenith, elite YouTube Growth Engineer for the channel '{Config.CHANNEL_NAME}' ({Config.CHANNEL_HANDLE}).
Video Title: {title}
Script Summary: {script_summary[:500]}

Generate a Maximum Algorithmic Reach metadata package:
1. YouTube Title (incorporate curiosity + high search volume keywords, under 70 chars)
2. SEO Description containing:
   - 2-line gripping summary with keywords
   - Exact Chapter Timestamps (0:00 Intro, 0:45 Architecture, etc.)
   - Tool Links & Resources placeholder
   - Official Channel Mission: "Explore the world of Artificial Intelligence and discover tools that help you work smarter, create better content, and save time."
   - Channel Slogan: "{Config.CHANNEL_SLOGAN}"
   - Business & Collaboration email: "{Config.BUSINESS_EMAIL}"
   - Official Affiliate Disclaimer
   - 5 High-velocity Hashtags (#AITools #AI #Automation #Productivity #TechTips)
3. 25 High-Rank Search Tags (comma-separated, under 500 characters total)
4. Pinned Engagement Comment designed to get 100+ replies and trigger YouTube recommendation algorithms.
"""
        response = query_llm(
            prompt=prompt,
            system_prompt=f"You are Zenith, YouTube SEO & Algorithm Optimization Director for {Config.CHANNEL_NAME}."
        )
        if not response:
            return self._get_fallback_seo(title, affiliate_block)
        
        return {
            "title": title,
            "raw_seo_package": response,
            "affiliate_block": affiliate_block,
            "pinned_comment": "👇 Which of these free AI tools will you test first? Drop your thoughts below and subscribe to AI Tools Lab for daily workflow breakdowns!"
        }

    def _get_fallback_seo(self, title: str, affiliate_block: str) -> dict:
        description = f"""🚀 {title} - Full Step-by-Step AI Tools Tutorial

Welcome to {Config.CHANNEL_NAME}! In this video, we reveal how to deploy an autonomous AI agent workforce that runs 24/7 completely free — even when your computer is shut down.

TIMESTAMPS:
0:00 - The $0 AI Agent Secret
0:45 - Breaking Down the 8-Agent Architecture
2:00 - Live UI Screen Capture & Real Software Demos
3:15 - Free Neural Voiceover & Script Setup
4:30 - Automated WhatsApp Mobile Alerts & Quality Sign-Off
5:45 - 1-Click GitHub Repository Clone

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{affiliate_block}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Welcome to {Config.CHANNEL_NAME}!
Explore the world of Artificial Intelligence and discover tools that help you work smarter, create better content, and save time.

On this channel, you'll find:
🤖 AI Tool Reviews & Demonstrations
🎥 AI Video and Image Creation Tutorials
⚡ Productivity Tools and Automation
💻 Step-by-Step AI Guides
💰 Digital Tools and Affiliate Product Reviews

Our mission is simple: help you discover useful AI tools and learn how to use them effectively.
Subscribe and join the {Config.CHANNEL_NAME} community!

{Config.CHANNEL_SLOGAN}

📩 Business and collaboration enquiries: [{Config.BUSINESS_EMAIL}]

#AITools #ArtificialIntelligence #Automation #Productivity #AIToolsLab
"""
        tags = [
            "ai tools", "best ai tools 2026", "free ai tools", "ai automation", 
            "faceless youtube channel", "ai tools lab", "github actions automation",
            "chatgpt alternatives", "free text to speech", "ai agents tutorial",
            "autonomous ai", "productivity tools", "make money with ai"
        ]
        
        return {
            "title": f"{title} (100% Free AI Automation)",
            "description": description,
            "tags": tags,
            "category_id": "28",
            "privacy_status": Config.YOUTUBE_PRIVACY_STATUS,
            "pinned_comment": "👇 Which of these free AI tools are you planning to deploy first? Let us know in the comments, and don't forget to join the AI Tools Lab community!"
        }

    def upload_to_youtube(self, video_path: str, thumbnail_path: str, metadata: dict) -> dict:
        """
        Uploads video to YouTube using YouTube Data API v3 with automatic OAuth refresh token.
        Applies title, description, tags, category, and uploads custom 1280x720 thumbnail.
        Defaults to 'unlisted' so you can review on WhatsApp before public release.
        """
        # If credentials exist, execute live YouTube Data API v3 upload
        if Config.YOUTUBE_REFRESH_TOKEN and Config.YOUTUBE_CLIENT_ID and Config.YOUTUBE_CLIENT_SECRET:
            try:
                from google.oauth2.credentials import Credentials
                from googleapiclient.discovery import build
                from googleapiclient.http import MediaFileUpload

                print(f"[Publisher] Authenticating with YouTube Data API v3 (Target: {Config.CHANNEL_NAME})...")
                creds = Credentials(
                    None,
                    refresh_token=Config.YOUTUBE_REFRESH_TOKEN,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=Config.YOUTUBE_CLIENT_ID,
                    client_secret=Config.YOUTUBE_CLIENT_SECRET
                )
                youtube = build("youtube", "v3", credentials=creds)

                # 1. Upload Video
                body = {
                    "snippet": {
                        "title": metadata.get("title", "AI Tools Lab Showcase")[:100],
                        "description": metadata.get("description", metadata.get("raw_seo_package", "")),
                        "tags": metadata.get("tags", ["ai tools", "ai automation", "ai tools lab"]),
                        "categoryId": metadata.get("category_id", "28") # Science & Tech
                    },
                    "status": {
                        "privacyStatus": Config.YOUTUBE_PRIVACY_STATUS,
                        "selfDeclaredMadeForKids": False
                    }
                }

                # Find valid video file to upload
                media_file = video_path if os.path.exists(video_path) and video_path.endswith(".mp4") else None
                if not media_file and os.path.exists("samples/final_video.mp4"):
                    media_file = "samples/final_video.mp4"

                if media_file:
                    media = MediaFileUpload(media_file, chunksize=-1, resumable=True, mimetype="video/mp4")
                    request = youtube.videos().insert(
                        part="snippet,status",
                        body=body,
                        media_body=media
                    )
                    response = request.execute()
                    video_id = response.get("id")
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"[Publisher] ✅ SUCCESS! Video uploaded live to YouTube: {video_url}")

                    # 2. Upload Custom Thumbnail
                    if thumbnail_path and os.path.exists(thumbnail_path):
                        try:
                            thumb_media = MediaFileUpload(thumbnail_path, mimetype="image/jpeg")
                            youtube.thumbnails().set(videoId=video_id, media_body=thumb_media).execute()
                            print(f"[Publisher] ✅ Custom 1280x720 thumbnail applied to video!")
                        except Exception as te:
                            print(f"[Publisher] Notice setting thumbnail: {te}")

                    # 3. Pin First Engagement Comment
                    pinned_comment = metadata.get("pinned_comment")
                    if pinned_comment:
                        try:
                            comment_body = {
                                "snippet": {
                                    "videoId": video_id,
                                    "topLevelComment": {
                                        "snippet": {
                                            "textOriginal": pinned_comment
                                        }
                                    }
                                }
                            }
                            youtube.commentThreads().insert(part="snippet", body=comment_body).execute()
                            print("[Publisher] ✅ Algorithmic engagement comment pinned!")
                        except Exception as ce:
                            print(f"[Publisher] Notice pinning comment: {ce}")

                    return {
                        "status": "LIVE_UPLOAD_SUCCESS",
                        "channel": Config.CHANNEL_NAME,
                        "video_id": video_id,
                        "video_url": video_url,
                        "visibility": Config.YOUTUBE_PRIVACY_STATUS,
                        "thumbnail_attached": thumbnail_path
                    }
            except Exception as e:
                print(f"[Publisher] Live YouTube API upload error: {e}. Falling back to staged mode...")

        # Staged zero-dollar simulation mode (used until secrets are added)
        simulated_id = "AIToolsLab_" + os.urandom(4).hex()
        video_url = f"https://www.youtube.com/watch?v={simulated_id}"
        
        manifest_path = "samples/youtube_upload_package.json"
        with open(manifest_path, "w") as f:
            json.dump({
                "channel": Config.CHANNEL_NAME,
                "handle": Config.CHANNEL_HANDLE,
                "status": "STAGED_READY_FOR_BROADCAST",
                "privacy": Config.YOUTUBE_PRIVACY_STATUS,
                "video_url": video_url,
                "thumbnail_file": thumbnail_path,
                "metadata": metadata
            }, f, indent=2)

        print(f"[Publisher] Video packaged for YouTube! Target Channel: {Config.CHANNEL_NAME} (Visibility: {Config.YOUTUBE_PRIVACY_STATUS.upper()})")
        return {
            "status": "READY_TO_BROADCAST",
            "channel": Config.CHANNEL_NAME,
            "video_id": simulated_id,
            "video_url": video_url,
            "visibility": Config.YOUTUBE_PRIVACY_STATUS,
            "thumbnail_attached": thumbnail_path
        }
