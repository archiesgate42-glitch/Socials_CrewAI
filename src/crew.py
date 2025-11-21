# src/crew.py

from crewai import Crew, Task
from langchain_ollama import ChatOllama
from pathlib import Path
import os

from src.agents.orchestrator import create_orchestrator_agent
from src.agents.writers.linkedin_writer import create_linkedin_writer
from src.agents.writers.x_writer import create_x_writer
from src.agents.writers.facebook_writer import create_facebook_writer
from src.agents.writers.instagram_writer import create_instagram_writer

from src.tools.obsidian_reader import ObsidianVaultReader
from src.tools.ip_filter import PresenceBasedIPFilter
from src.tools.content_classifier import classify_content

class SocialCrewAI:
    """
    Main orchestration class for social media content generation
    """
    
    def __init__(self, vault_path: str, ollama_model: str = "llama3:latest"):
        self.vault_path = Path(vault_path)
        self.vault_reader = ObsidianVaultReader(str(self.vault_path))
        self.ip_filter = PresenceBasedIPFilter(str(self.vault_path))
        
        # Initialize Ollama LLM
        self.llm = ChatOllama(
            model=ollama_model,
            base_url="http://localhost:11434"
        )
        
        # Create agents
        self.orchestrator = create_orchestrator_agent(self.llm)
        self.linkedin_writer = create_linkedin_writer(self.llm)
        self.x_writer = create_x_writer(self.llm)
        self.facebook_writer = create_facebook_writer(self.llm)
        self.instagram_writer = create_instagram_writer(self.llm)
    
    def process_staging_content(self):
        """
        Main pipeline: Read staging notes → Filter → Route → Generate
        """
        
        print("🔍 Scanning staging folder...")
        notes = self.vault_reader.read_staging_notes()
        
        if not notes:
            print("⚠️ No ready notes found in staging folder")
            return
        
        print(f"📝 Found {len(notes)} note(s) ready for processing\n")
        
        for note in notes:
            print(f"Processing: {note['title']}")
            
            # IP Filter check
            is_safe = self.ip_filter.is_safe_to_share(
                note['content'],
                note['metadata']
            )
            
            if not is_safe:
                print(f"⚠️ BLOCKED: {note['title']} contains sensitive content")
                continue
            
            # Classify content
            classification = classify_content(note['content'], note['metadata'])
            print(f"📊 Platforms: {', '.join(classification['platforms'])}")
            
            # Generate content for each platform
            for platform in classification['platforms']:
                self.generate_platform_content(note, platform)
    
    def generate_platform_content(self, note: dict, platform: str):
        """
        Generate platform-specific content using appropriate writer
        """
        
        # Select writer based on platform
        writer_map = {
            'linkedin': self.linkedin_writer,
            'x': self.x_writer,
            'facebook': self.facebook_writer,
            'instagram': self.instagram_writer
        }
        
        writer = writer_map.get(platform)
        if not writer:
            print(f"⚠️ No writer found for platform: {platform}")
            return
        
        # Create task
        task = Task(
            description=f"Create {platform} post from this content:\n\n{note['content']}",
            expected_output=f"Platform-optimized {platform} post",
            agent=writer
        )
        
        # Create crew and execute
        crew = Crew(
            agents=[writer],
            tasks=[task],
            verbose=True
        )
        
        result = crew.kickoff()
        
        # Save output
        self.save_output(note['title'], platform, result)
    
    def save_output(self, title: str, platform: str, content):
        """
        Save generated content to output folder
        """
        output_dir = Path("output") / title.replace(" ", "_")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"{platform}_post.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(content))
        
        print(f"✅ Saved: {output_file}\n")
