#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

mkdir -p core agents data media reports samples cache

# Core files
for f in config.py llm_client.py pipeline.py; do
  if [ -f "$f" ]; then mv "$f" core/; fi
done

# Agent files
for f in \
  affiliate_manager.py \
  boss_agent.py \
  browser_recorder.py \
  idea_hunter.py \
  niche_finder.py \
  publisher_agent.py \
  scriptwriter.py \
  thumbnail_designer.py \
  thumbnail_generator.py \
  video_editor.py \
  voice_agent.py \
  whatsapp.py
 do
  if [ -f "$f" ]; then mv "$f" agents/; fi
done

# Data files
for f in affiliates.json final_video_manifest.json youtube_upload_package.json; do
  if [ -f "$f" ]; then mv "$f" data/; fi
done

# Media files
for f in thumbnail.jpg cursor_ai_editor_ui.png google_ai_studio_ui.png hugging_face_spaces_ui.png; do
  if [ -f "$f" ]; then mv "$f" media/; fi
done

# Reports
for f in \
  boss_audit_20261113_000514.md \
  boss_audit_20261113_000543.md \
  boss_audit_20261113_002201.md \
  full_script_20261112_235111.md \
  full_script_20261113_000514.md \
  full_script_20261113_000543.md \
  full_script_20261113_002201.md \
  niche_report_20261112_235111.md \
  thumbnails_20261112_235111.md \
  viral_ideas_20261112_235111.md \
  youtube_seo_package_20261113_000514.md \
  youtube_seo_package_20261113_000543.md \
  youtube_seo_package_20261113_002201.md
 do
  if [ -f "$f" ]; then mv "$f" reports/; fi
done

# Sample text
if [ -f "sample_voiceover.txt" ]; then mv "sample_voiceover.txt" samples/; fi

# Cache / pyc files
for f in \
  affiliate_manager.cpython-313.pyc \
  boss_agent.cpython-313.pyc \
  browser_recorder.cpython-313.pyc \
  config.cpython-313.pyc \
  idea_hunter.cpython-313.pyc \
  llm_client.cpython-313.pyc \
  niche_finder.cpython-313.pyc \
  publisher_agent.cpython-313.pyc \
  scriptwriter.cpython-313.pyc \
  thumbnail_designer.cpython-313.pyc \
  thumbnail_generator.cpython-313.pyc \
  video_editor.cpython-313.pyc \
  voice_agent.cpython-313.pyc \
  whatsapp.cpython-313.pyc
 do
  if [ -f "$f" ]; then mv "$f" cache/; fi
done

echo "Repository organized into folder structure."
