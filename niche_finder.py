import json
from .llm_client import query_llm

class NicheFinderAgent:
    """Nick: Niche Finder - Finds profitable faceless YouTube niches."""
    def __init__(self):
        self.name = "Nick (Niche Finder)"
        self.role = "Tell you WHERE to start"

    def run(self, category_hint: str = "technology, finance, productivity, mysteries"):
        prompt = f"""
Find 5 highly profitable, high-RPM faceless YouTube channel niches related to: {category_hint}.
For each niche, specify:
1. Niche Name
2. Target Audience & Search Demand
3. Estimated RPM / CPM ($ range)
4. Why it works as a 100% faceless channel
5. Proof/Examples of channels making millions of views
6. Recommended monetization (AdSense, Affiliate, SaaS, Digital Products)

Return formatted as clean markdown with a concise summary.
"""
        response = query_llm(
            prompt=prompt,
            system_prompt="You are Nick, an expert YouTube algorithm strategist specializing in high-margin faceless channels."
        )
        if not response:
            response = self._get_fallback_niche()
        return response

    def _get_fallback_niche(self):
        return """# 🎯 Nick's Niche Analysis: Top Faceless High-CPM Niches

### 1. Autonomous AI Workflows & Solopreneur Tech (Recommended)
- **Estimated RPM:** $15.00 - $35.00
- **Audience:** Tech enthusiasts, freelancers, corporate workers automating repetitive tasks.
- **Why Faceless Works:** Screen recordings, slick motion UI graphics, code snippets, visual workflow nodes (Make, n8n, Python).
- **Proof Models:** 100x Growth, AI Advantage, Matt Wolfe (high view velocity with B-roll).
- **Monetization:** Software affiliate links ($50-200/sale), GitHub sponsorships, custom prompt/template packs.

### 2. Geopolitical Mystery & Infrastructure Megaprojects
- **Estimated RPM:** $8.00 - $18.00
- **Audience:** Broad intellectual audience, global viewers interested in modern history & economics.
- **Why Faceless Works:** Archival 4K footage, 3D animated maps, satellite tracking, engaging documentary narration.
- **Proof Models:** RealLifeLore, Fern, Wendover Productions.

### 3. Cyber Warfare & Dark Web Case Studies
- **Estimated RPM:** $12.00 - $22.00
- **Audience:** Tech, cybersecurity professionals, true crime / mystery cross-traffic.
- **Why Faceless Works:** Terminal text, redacted documents, schematic graphics, ominous voiceover.
- **Proof Models:** Barely Sociable, Disrupt, MagnatesMedia.
"""
