# src/phase1_intelligence.py (UPDATED to show images)

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.obsidian_scanner import ObsidianScanner
from tools.content_analyzer import ContentAnalyzer
from tools.ip_filter import PresenceBasedIPFilter

from typing import List, Dict
import json
import os
from dotenv import load_dotenv


class ContentIntelligence:
    """Phase 1: Scan vault, analyze, filter, and extract images"""
    
    def __init__(self, vault_path: str):
        self.scanner = ObsidianScanner(vault_path)
        self.analyzer = ContentAnalyzer()
        self.ip_filter = PresenceBasedIPFilter(vault_path)
    
    def run(self, filter_unsafe: bool = True) -> tuple:
        """Execute Phase 1: Scan, analyze, filter + images
        
        Returns: (safe_pages, blocked_pages)
        """
        print("🔍 Phase 1: Content Intelligence + IP Protection + Images")
        print("=" * 60)
        
        # Scan vault
        print(f"📂 Scanning vault...")
        pages = self.scanner.scan_vault()
        print(f"✅ Found {len(pages)} pages\n")
        
        # Analyze + Filter each page
        safe_pages = []
        blocked_pages = []
        
        for page in pages:
            print(f"📄 Analyzing: {page['title']}")
            
            # IP FILTER CHECK
            is_safe = self.ip_filter.is_safe_to_share(
                page["content"], 
                page["metadata"]
            )
            
            if not is_safe:
                print(f"   🚨 BLOCKED: Private/vault-only/sensitive content")
                blocked_pages.append({
                    "title": page["title"],
                    "reason": "IP/Privacy protection"
                })
                continue
            
            # Add analysis
            page["tone"] = self.analyzer.analyze_tone(page["content"])
            page["suggested_platforms"] = self.analyzer.suggest_platforms(page)
            page["keywords"] = self.analyzer.extract_keywords(page["content"])
            page["is_safe"] = True
            
            safe_pages.append(page)
            
            # Show image info
            img_status = f"🖼️  {page['image_count']} images" if page["image_count"] > 0 else "📝 No images"
            print(f"   ✅ SAFE: {page['tone']} → {', '.join(page['suggested_platforms'])} | {img_status}")
        
        print(f"\n📊 Summary:")
        print(f"   Total scanned: {len(pages)}")
        print(f"   ✅ Safe to share: {len(safe_pages)}")
        print(f"   🚨 Blocked (private/IP): {len(blocked_pages)}")
        
        # Image stats
        total_images = sum(page.get("image_count", 0) for page in safe_pages)
        print(f"   🖼️  Total images found: {total_images}")
        
        return safe_pages, blocked_pages
    
    def save_analysis(self, safe_pages: List[Dict], blocked_pages: List[Dict]):
        """Save analysis + image info to JSON files"""
        output_path = Path(__file__).parent.parent
        
        # Clean + save safe pages with image info
        clean_safe = []
        for page in safe_pages:
            clean_page = {
                "title": page["title"],
                "file_name": page["file_name"],
                "tone": page["tone"],
                "platforms": page["suggested_platforms"],
                "keywords": page["keywords"],
                "word_count": page["word_count"],
                "images": page.get("images", []),  # ← Image paths!
                "image_count": page.get("image_count", 0),
            }
            clean_safe.append(clean_page)
        
        with open(output_path / "safe_content.json", 'w', encoding='utf-8') as f:
            json.dump(clean_safe, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Safe content saved to: safe_content.json ({len(clean_safe)} items)")
        
        # Save blocked pages for review
        with open(output_path / "blocked_content.json", 'w', encoding='utf-8') as f:
            json.dump(blocked_pages, f, indent=2, ensure_ascii=False)
        print(f"🚨 Blocked content saved to: blocked_content.json ({len(blocked_pages)} items)")


# Test runner
if __name__ == "__main__":
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    
    if not vault_path:
        print("❌ OBSIDIAN_VAULT_PATH not set in .env")
        exit(1)
    
    print(f"🔍 Vault path: {vault_path}\n")
    
    intelligence = ContentIntelligence(vault_path)
    safe_pages, blocked_pages = intelligence.run(filter_unsafe=True)
    intelligence.save_analysis(safe_pages, blocked_pages)
