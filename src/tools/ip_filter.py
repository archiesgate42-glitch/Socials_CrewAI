# src/tools/ip_filter.py

from pathlib import Path
import frontmatter


class PresenceBasedIPFilter:
    """
    Uses your Precence.md as single source of truth
    for what's shareable vs vault-only
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.presence_page = self.load_presence()
    
    def load_presence(self) -> dict:
        """
        Parse your Precence.md page to extract:
        - What happened today (public-ready content)
        - Tagged exclusions (vault-only)
        """
        # Try both spellings
        presence_files = [
            self.vault_path / "Precence.md",  # Your actual file
            self.vault_path / "Presence.md",
            self.vault_path / "Mobile_Vaulte" / "Precence.md",  # Subfolder
        ]
        
        presence_file = None
        for pf in presence_files:
            if pf.exists():
                presence_file = pf
                break
        
        if not presence_file:
            print(f"⚠️ Presence file not found, using permissive filtering")
            return {
                'daily_summary': '',
                'public_narrative': [],
                'timestamp': 'unknown'
            }
        
        try:
            with open(presence_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            return {
                'daily_summary': post.content,
                'public_narrative': self.extract_public_narrative(post.content),
                'timestamp': post.metadata.get('updated', 'unknown')
            }
        except Exception as e:
            print(f"⚠️ Error loading Presence file: {e}")
            return {
                'daily_summary': '',
                'public_narrative': [],
                'timestamp': 'unknown'
            }
    
    def is_safe_to_share(self, note_content: str, note_metadata: dict) -> bool:
        """
        Check against presence page + manual vault exclusions
        """
        
        # Hard block: vault-only tags (check both with and without #)
        vault_only_tags = ['vault-only', 'private', 'internal', 'confidential', 'secret']
        metadata_tags = note_metadata.get('tags', [])
        
        # Check if any vault-only tag is present
        for tag in metadata_tags:
            tag_clean = tag.lower().replace('#', '').strip()
            if tag_clean in vault_only_tags:
                return False
        
        # Hard block: sensitive patterns (STRICT - only truly dangerous stuff)
        dangerous_patterns = [
            'api_key',
            'secret_key',
            'password:',
            'token:',
            'private_key',
            'credential',
        ]
        
        content_lower = note_content.lower()
        if any(pattern in content_lower for pattern in dangerous_patterns):
            return False
        
        # Block: Personal/private markers in content
        private_markers = [
            '#vault-only',
            '#private',
            '#internal',
            '⚠️ vault only',
            '⚠️ private',
        ]
        
        if any(marker.lower() in content_lower for marker in private_markers):
            return False
        
        # PERMISSIVE: Allow by default if no red flags
        # (We're not blocking code snippets anymore - those can be shared!)
        return True
    
    def extract_public_narrative(self, presence_content: str) -> list:
        """
        Extract bullet points/sections marked as shareable
        from your daily Presence notes
        """
        if not presence_content:
            return []
        
        lines = presence_content.split('\n')
        # Filter out lines marked as private
        public_items = [
            line for line in lines 
            if not any(marker in line.lower() for marker in ['⚠️', 'vault-only', 'private'])
        ]
        return public_items
    
    def is_mentioned_in_presence(self, note_content: str) -> bool:
        """
        Check if content or keywords from note appear in Presence.md
        Simple matching for now (can be upgraded to semantic similarity)
        """
        if not self.presence_page['public_narrative']:
            return False
        
        presence_text = '\n'.join(self.presence_page['public_narrative']).lower()
        
        # Extract key keywords from note (first 20 words)
        words = note_content.split()[:20]
        significant_words = [w for w in words if len(w) > 4]
        
        # Check if any significant words appear in presence
        matches = sum(1 for word in significant_words if word.lower() in presence_text)
        
        # If 2+ words match, likely related to public narrative
        return matches >= 2
