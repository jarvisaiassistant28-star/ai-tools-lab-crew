import os
import json

class AffiliateManager:
    """
    Scans video topics and scripts to automatically inject verified affiliate links,
    promotional discounts, and FTC disclosure into the YouTube video description.
    """
    def __init__(self, config_path: str = "affiliates.json"):
        self.config_path = config_path
        self.affiliates = self._load_affiliates()

    def _load_affiliates(self) -> dict:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[AffiliateManager] Error reading {self.config_path}: {e}")
        return {"tools": {}, "default_disclaimer": ""}

    def get_links_for_script(self, script_text: str) -> str:
        """
        Matches tools found in the script and returns clean Markdown / YouTube description links.
        """
        tools = self.affiliates.get("tools", {})
        matched_links = []
        script_lower = script_text.lower()

        for key, tool in tools.items():
            if key in script_lower or tool["name"].lower() in script_lower or len(matched_links) < 3:
                link_entry = f"🔹 {tool['name']}: {tool['affiliate_url']}\n   ↳ {tool['tagline']}"
                if link_entry not in matched_links:
                    matched_links.append(link_entry)
            if len(matched_links) >= 4:
                break

        links_block = "🔗 FEATURED AI TOOLS & EXCLUSIVE DISCOUNTS:\n"
        links_block += "\n".join(matched_links)
        links_block += "\n\n" + self.affiliates.get("default_disclaimer", "")
        return links_block
