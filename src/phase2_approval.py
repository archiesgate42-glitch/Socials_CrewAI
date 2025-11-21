# src/phase2_approval.py (UPGRADED VERSION)

import sys
from pathlib import Path
from typing import List, Dict
import json

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class ProposalGenerator:
    """Phase 2: Generate social media proposals from safe content"""
    
    def generate_proposals(self, safe_pages: List[Dict]) -> List[Dict]:
        """
        Convert vault content → social media proposals
        Each proposal is a structured post idea with platform recommendations
        """
        proposals = []
        
        for page in safe_pages:
            # Only include pages with content
            if not page.get("word_count", 0) > 10:
                continue
            
            proposal = {
                "id": len(proposals) + 1,
                "source_page": page["title"],
                "source_file": page["file_name"],
                "content_preview": self._get_preview(page),
                "tone": page.get("tone", "neutral"),
                "suggested_platforms": page.get("platforms", ["linkedin"]),
                "images": page.get("images", []),
                "image_count": page.get("image_count", 0),
                "keywords": page.get("keywords", []),
                
                # Generate platform-specific angles
                "platform_angles": self._generate_angles(page),
                
                # Readiness for posting
                "ready_to_post": True,
                "status": "pending_approval",
                "notes": ""
            }
            proposals.append(proposal)
        
        return proposals
    
    def _get_preview(self, page: Dict) -> str:
        """Get clean content preview"""
        content = page.get("content", "")
        # Clean preview (remove extra whitespace, images, etc.)
        preview = " ".join(content.split())[:300]
        return preview + "..." if len(preview) == 300 else preview
    
    def _generate_angles(self, page: Dict) -> Dict:
        """Generate platform-specific content angles"""
        title = page["title"]
        tone = page.get("tone", "neutral")
        image_count = page.get("image_count", 0)
        keywords = page.get("keywords", [])[:3]
        
        angles = {
            "linkedin": {
                "angle": f"Professional insights: {title}",
                "tone": "thought-leadership",
                "length": "300-500 words",
                "cta": "Share your thoughts in the comments 💬",
                "hashtags": ["#AI", "#Tech", "#Innovation"] + keywords[:2],
                "visual": "Professional image/diagram" if image_count > 0 else "Text-only"
            },
            "x": {
                "angle": f"Hot take: {title}",
                "tone": "punchy, viral-focused",
                "length": "3 tweets (280 chars each)",
                "cta": "Retweet if you agree! 🔄",
                "hashtags": ["#Tech", "#AI", "#Development"],
                "visual": "Tweet images" if image_count > 0 else "Text-only"
            },
            "facebook": {
                "angle": f"Community post: {title}",
                "tone": "conversational, engaging",
                "length": "200-400 words",
                "cta": "What's your experience? Drop a comment! 💬",
                "hashtags": ["#Community", "#Tech", "#Learning"],
                "visual": "Engaging screenshot/diagram" if image_count > 0 else "Text-only"
            },
            "instagram": {
                "angle": f"Visual story: {title}",
                "tone": "creative, visual-first",
                "length": "50-100 word caption",
                "cta": "Save this for later 📌",
                "hashtags": ["#Tech", "#AI", "#Developer", "#Learning"] + keywords[:1],
                "visual": f"REQUIRED: {image_count} images available" if image_count > 0 else "❌ No images (IG needs visuals)"
            }
        }
        
        return angles
    
    def save_proposals(self, proposals: List[Dict], output_file: str = "proposals.json"):
        """Save proposals for human review"""
        output_path = Path(__file__).parent.parent / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(proposals, f, indent=2, ensure_ascii=False)
        
        print(f"\n📋 {len(proposals)} proposals generated!")
        print(f"💾 Saved to: {output_file}")
        
        return output_path


class HITLApproval:
    """Human-in-the-Loop approval workflow"""
    
    @staticmethod
    def present_options(proposals: List[Dict]) -> List[Dict]:
        """Interactive approval workflow"""
        
        approved = []
        
        print("\n" + "="*60)
        print("🎯 PROPOSAL REVIEW (Human-in-the-Loop)")
        print("="*60 + "\n")
        
        print(f"Total proposals: {len(proposals)}\n")
        print("Commands:")
        print("  y     = Approve")
        print("  n     = Skip")
        print("  quit  = Stop reviewing")
        print("  all   = Approve all remaining\n")
        
        for i, proposal in enumerate(proposals, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(proposals)}] {proposal['source_page']}")
            print(f"{'='*60}")
            print(f"Tone: {proposal['tone']} | Platforms: {', '.join(proposal['suggested_platforms'])}")
            print(f"Images: {proposal['image_count']} found")
            print(f"\nPreview:\n{proposal['content_preview']}")
            
            # Show platform angles
            print(f"\n📱 Platform Angles:")
            for platform, angle_info in proposal['platform_angles'].items():
                if platform in proposal['suggested_platforms']:
                    print(f"   {platform.upper()}: {angle_info['angle']}")
                    print(f"      CTA: {angle_info['cta']}")
            
            # User decision
            decision = input(f"\n➡️  Approve? (y/n/quit/all): ").strip().lower()
            
            if decision == 'y':
                proposal["status"] = "approved"
                approved.append(proposal)
                print("   ✅ Approved!")
            elif decision == 'n':
                print("   ⏭️  Skipped")
            elif decision == 'all':
                # Approve all remaining
                remaining = proposals[i-1:]
                for p in remaining:
                    p["status"] = "approved"
                    approved.append(p)
                print(f"   ✅ Approved {len(remaining)} remaining proposals!")
                break
            elif decision == 'quit':
                print("   🛑 Stopping review...")
                break
        
        return approved


# Main execution
if __name__ == "__main__":
    from dotenv import load_dotenv
    
    # Load safe content from Phase 1
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    safe_content_file = Path(__file__).parent.parent / "safe_content.json"
    
    if not safe_content_file.exists():
        print("❌ safe_content.json not found. Run Phase 1 first!")
        print(f"   python src/phase1_intelligence.py")
        exit(1)
    
    print("📂 Loading safe content from Phase 1...")
    with open(safe_content_file, 'r', encoding='utf-8') as f:
        safe_pages = json.load(f)
    
    print(f"✅ Loaded {len(safe_pages)} safe pages\n")
    
    # Generate proposals
    generator = ProposalGenerator()
    proposals = generator.generate_proposals(safe_pages)
    proposals_path = generator.save_proposals(proposals)
    
    # Interactive approval
    print("\n" + "="*60)
    mode = input("Review mode? (interactive/batch): ").strip().lower()
    
    if mode == "interactive":
        approval = HITLApproval()
        approved = approval.present_options(proposals)
        
        # Save approved proposals
        approved_path = Path(__file__).parent.parent / "approved_proposals.json"
        with open(approved_path, 'w', encoding='utf-8') as f:
            json.dump(approved, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ {len(approved)} proposals approved!")
        print(f"💾 Saved to: approved_proposals.json")
        print(f"\n🚀 Next step: Phase 3 (Content Generation)")
        print(f"   python src/phase3_content_generation.py")
    else:
        print("\n📦 Batch mode: All proposals saved to proposals.json")
        print("Next: python src/phase3_content_generation.py")
