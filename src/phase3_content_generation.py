# src/phase3_content_generation.py

import sys
from pathlib import Path
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from crewai import Crew, Task, Agent, LLM


class SocialContentGenerator:
    """Phase 3: Generate platform-specific content using CrewAI"""
    
    def __init__(self, ollama_model: str = "ollama/llama3", base_url: str = "http://localhost:11434"):
        """Initialize CrewAI with Ollama using new LLM wrapper"""
        self.llm = LLM(model=ollama_model, base_url=base_url)
        self.writers = self._create_writers()
    
    def _create_writers(self) -> Dict[str, Agent]:
        """Create platform-specific writer agents with EXPLICIT output instructions"""
        
        writers = {
            "linkedin": Agent(
                role="LinkedIn Content Specialist",
                goal=(
                    "Write a COMPLETE LinkedIn post. "
                    "Output ONLY the final post text, nothing else. "
                    "No 'Thought:', no 'Final Answer:', just the post content."
                ),
                backstory=(
                    "You're a B2B tech content writer. "
                    "CRITICAL INSTRUCTION: Your output must be the actual post text ready to publish. "
                    "Never include thinking process, explanations, or metadata. "
                    "Write 300-500 words with bullet points and 1-3 emojis. "
                    "End with a call-to-action."
                ),
                verbose=False,
                allow_delegation=False,
                llm=self.llm
            ),
            
            "x": Agent(
                role="X (Twitter) Content Creator",
                goal=(
                    "Write a COMPLETE 3-tweet thread. "
                    "Output ONLY the tweets, nothing else. "
                    "No 'Thought:', no explanations, just tweets."
                ),
                backstory=(
                    "You create viral X threads. "
                    "CRITICAL INSTRUCTION: Output must be exactly 3 tweets formatted as:\n"
                    "[1/3] First tweet text here\n\n"
                    "[2/3] Second tweet text here\n\n"
                    "[3/3] Third tweet text here\n\n"
                    "Never include thinking process or explanations. "
                    "Each tweet max 280 characters. Use emojis and hashtags."
                ),
                verbose=False,
                allow_delegation=False,
                llm=self.llm
            ),
            
            "facebook": Agent(
                role="Facebook Community Manager",
                goal=(
                    "Write a COMPLETE Facebook post. "
                    "Output ONLY the post text, nothing else. "
                    "No 'Thought:', no explanations, just the post."
                ),
                backstory=(
                    "You write warm Facebook posts. "
                    "CRITICAL INSTRUCTION: Your output must be the actual post ready to publish. "
                    "Never include thinking process or metadata. "
                    "Write 200-400 words in conversational tone. "
                    "End with a question to spark discussion."
                ),
                verbose=False,
                allow_delegation=False,
                llm=self.llm
            ),
            
            "instagram": Agent(
                role="Instagram Visual Storyteller",
                goal=(
                    "Write a COMPLETE Instagram caption. "
                    "Output ONLY the caption text, nothing else. "
                    "No 'Thought:', no explanations, just the caption."
                ),
                backstory=(
                    "You craft Instagram captions. "
                    "CRITICAL INSTRUCTION: Your output must be the actual caption ready to post. "
                    "Never include thinking process or metadata. "
                    "Write max 2200 characters with line breaks for readability. "
                    "Use 3-5 emojis and end with 5-10 hashtags."
                ),
                verbose=False,
                allow_delegation=False,
                llm=self.llm
            ),
        }
        
        return writers
    
    def generate_content(self, proposals: List[Dict], max_posts: int = None) -> Dict:
        """Generate platform-specific content for each proposal"""
        
        if max_posts:
            proposals = proposals[:max_posts]
        
        results = {
            "total_proposals": len(proposals),
            "posts": []
        }
        
        for i, proposal in enumerate(proposals, 1):
            print(f"\n{'='*60}")
            print(f"[{i}/{len(proposals)}] {proposal['source_page']}")
            print(f"{'='*60}")
            
            post_data = {
                "proposal_id": proposal["id"],
                "source_page": proposal["source_page"],
                "platforms": {}
            }
            
            for platform in proposal["suggested_platforms"]:
                if platform not in self.writers:
                    continue
                
                print(f"\n   📱 {platform.upper()}...")
                
                task = Task(
                    description=f"Create a {platform} post for: {proposal['source_page']}\nContent: {proposal['content_preview']}",
                    expected_output=f"{platform.upper()} post ready to publish",
                    agent=self.writers[platform]
                )
                
                crew = Crew(
                    agents=[self.writers[platform]],
                    tasks=[task],
                    verbose=False
                )
                
                try:
                    result = crew.kickoff()
                    
                    # Extract actual content from various CrewAI output formats
                    content = None
                    
                    # Try multiple extraction methods
                    if hasattr(result, 'raw'):
                        content = result.raw
                    elif hasattr(result, 'output'):
                        content = result.output  
                    elif hasattr(result, 'result'):
                        content = result.result
                    else:
                        content = str(result)
                    
                    # Convert to string if needed
                    content = str(content)
                    
                    # Clean up common CrewAI artifacts
                    lines_to_remove = [
                        "Thought: I now can give a great answer",
                        "Thought: I now have a clear understanding",
                        "Final Answer:",
                        "Thought:",
                    ]
                    
                    for line in lines_to_remove:
                        content = content.replace(line, "")
                    
                    content = content.strip()
                    
                    # Accept anything with content
                    if not content:
                        print(f"         DEBUG: Got empty content")
                        raise ValueError("Agent produced no content")
                    
                    post_data["platforms"][platform] = {
                        "status": "generated",
                        "content": content
                    }
                    print(f"      ✅ Done! ({len(content)} chars)")
                    
                except Exception as e:
                    print(f"      ❌ Error: {e}")
                    post_data["platforms"][platform] = {
                        "status": "error",
                        "error": str(e)
                    }
            
            results["posts"].append(post_data)
        
        return results
    
    def save_posts(self, results: Dict, output_file: str = "generated_posts.json"):
        """Save generated posts to JSON"""
        output_path = Path(__file__).parent.parent / output_file
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Saved: {output_file}")
        return output_path


if __name__ == "__main__":
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(dotenv_path=env_path)
    
    proposals_file = Path(__file__).parent.parent / "proposals.json"
    
    if not proposals_file.exists():
        print("❌ Run Phase 2 first: python src/phase2_approval.py")
        exit(1)
    
    print("📂 Loading proposals...")
    with open(proposals_file, 'r', encoding='utf-8') as f:
        proposals = json.load(f)
    
    print(f"✅ {len(proposals)} proposals\n")  # ← correct
    
    test_mode = input("Test with 3 posts or generate all? (test/all): ").strip().lower()
    
    print("\n🚀 Initializing CrewAI...")
    generator = SocialContentGenerator()
    
    print("\n" + "="*60)
    print("📝 GENERATING CONTENT")
    print("="*60)
    
    max_posts = 3 if test_mode == "test" else None
    results = generator.generate_content(proposals, max_posts=max_posts)
    generator.save_posts(results)
    
    print(f"\n📊 Generated {len(results['posts'])} posts")
    print(f"💾 Check: generated_posts.json")
    
    # Auto-launch viewer
    print(f"\n🎨 Generating visual preview...")
    import subprocess
    try:
        subprocess.run([sys.executable, "src/post_viewer.py"], check=True)
    except:
        print("   (Run manually: python src/post_viewer.py)")
