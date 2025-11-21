# src/tools/obsidian_scanner.py (UPDATED with image handling)

from pathlib import Path
from typing import List, Dict
import frontmatter
import re
import yaml


class ObsidianScanner:
    """Recursive Obsidian vault scanner with metadata extraction + image detection"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        
        # Folders to skip
        self.skip_folders = [
            '.obsidian',
            'Social_Crew_Staging',
            '.trash',
            '.git',
        ]
        
        # Allowed image extensions
        self.image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']
    
    def scan_vault(self, include_subpages: bool = True) -> List[Dict]:
        """
        Recursively scan vault for all .md files + images
        
        Returns:
            List of dicts with file data
        """
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault not found: {self.vault_path}")
        
        pages = []
        
        for md_file in self.vault_path.rglob("*.md"):
            # Skip excluded folders
            if any(skip_folder in md_file.parts for skip_folder in self.skip_folders):
                print(f"⏭️  Skipping (excluded folder): {md_file.name}")
                continue
            
            try:
                page_data = self._parse_page(md_file)
                pages.append(page_data)
            except Exception as e:
                print(f"⚠️ Error parsing {md_file.name}: {e}")
                continue
        
        return pages
    
    def _parse_page(self, file_path: Path) -> Dict:
        """Parse single markdown file with frontmatter + image detection"""
        # Try to parse with frontmatter
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
        except yaml.YAMLError as yaml_error:
            # Fallback: parse as plain markdown without frontmatter
            print(f"   ⚠️ YAML error in {file_path.name}, parsing as plain markdown")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            # Create empty frontmatter
            post = type('obj', (object,), {
                'metadata': {},
                'content': content
            })()
        
        # Extract metadata
        metadata = post.metadata if hasattr(post, 'metadata') else {}
        content = post.content if hasattr(post, 'content') else ""
        
        # Find links and images
        internal_links = re.findall(r'\[\[(.*?)\]\]', content)
        
        # Find image references (both Obsidian and markdown formats)
        image_refs = re.findall(r'!\[\[?(.*?\.(?:png|jpg|jpeg|gif|svg|webp))\]?\]', content, re.IGNORECASE)
        
        # Also find markdown image syntax
        md_images = re.findall(r'!\[.*?\]\((.*?\.(?:png|jpg|jpeg|gif|svg|webp))\)', content, re.IGNORECASE)
        
        # Combine and deduplicate
        all_images = list(set(image_refs + md_images))
        
        # Resolve image paths (find actual files in vault)
        resolved_images = self._resolve_images(file_path, all_images)
        
        tags = re.findall(r'#(\w+)', content)
        
        return {
            "file_path": str(file_path),
            "file_name": file_path.stem,
            "title": metadata.get("title", file_path.stem),
            "metadata": metadata,
            "content": content,
            "word_count": len(content.split()),
            "internal_links": internal_links,
            "image_refs": all_images,  # Raw references from markdown
            "images": resolved_images,  # Resolved file paths
            "image_count": len(resolved_images),
            "tags": tags,
            "has_subpages": len(internal_links) > 0,
            # Analysis placeholders
            "topic": metadata.get("topic", "unknown"),
            "audience": metadata.get("audience", "general"),
            "platforms": metadata.get("platforms", ["linkedin", "x", "facebook", "instagram"])
        }
    
    def _resolve_images(self, md_file: Path, image_refs: List[str]) -> List[Dict]:
        """
        Resolve image references to actual files in vault
        
        Returns:
            List of dicts with image info: {name, path, exists, safe}
        """
        resolved = []
        
        for img_ref in image_refs:
            img_ref = img_ref.strip()
            
            # Try multiple strategies to find the image
            candidates = [
                md_file.parent / img_ref,  # Same folder
                self.vault_path / img_ref,  # Root of vault
                self.vault_path / "attachments" / img_ref,  # Common attachments folder
                self.vault_path / "Images" / img_ref,
                self.vault_path / "Attachments" / img_ref,
            ]
            
            found_image = None
            for candidate in candidates:
                if candidate.exists():
                    found_image = candidate
                    break
            
            # Check if it's safe (not in excluded folders)
            is_safe = True
            if found_image:
                if any(skip_folder in found_image.parts for skip_folder in self.skip_folders):
                    is_safe = False
            
            resolved.append({
                "name": img_ref,
                "found": found_image is not None,
                "path": str(found_image) if found_image else None,
                "safe": is_safe
            })
        
        # Filter to only safe, found images
        safe_images = [img for img in resolved if img["found"] and img["safe"]]
        return safe_images
