# src/tools/obsidian_reader.py
from pathlib import Path
import frontmatter
import json
from datetime import datetime

class ObsidianVaultReader:
    """
    Direct file system access to vault
    Watches for new/updated notes in staging folder
    """
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.staging_folder = self.vault_path / "Social_Crew_Staging"
        self.presence_file = self.vault_path / "Presence.md"
    
    def read_staging_notes(self) -> list:
        """
        Check staging folder for new content
        Returns list of ready-to-post notes
        """
        staging_notes = []
        
        if not self.staging_folder.exists():
            self.staging_folder.mkdir(parents=True)
            return staging_notes
        
        for note_file in self.staging_folder.glob("*.md"):
            note_data = self.parse_note(note_file)
            if note_data.get('ready_to_process'):
                staging_notes.append(note_data)
        
        return staging_notes
    
    def parse_note(self, file_path: Path) -> dict:
        """
        Parse markdown with frontmatter
        Extract metadata + content
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
        
        return {
            'filename': file_path.name,
            'title': post.metadata.get('title', file_path.stem),
            'content': post.content,
            'tags': post.metadata.get('tags', []),
            'platforms': post.metadata.get('platforms', ['linkedin']),
            'ready_to_process': post.metadata.get('ready', False),
            'metadata': post.metadata,
            'date_created': file_path.stat().st_ctime
        }
    
    def get_presence_context(self) -> str:
        """
        Read Presence.md as context for Orchestrator
        """
        with open(self.presence_file, 'r', encoding='utf-8') as f:
            post = frontmatter.load(f)
            return post.content
