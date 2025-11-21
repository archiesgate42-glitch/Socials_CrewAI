# run_crew.py (TOP)

import sys
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

import os
from dotenv import load_dotenv
from crewai import Crew, Task, Agent, LLM

# Import Phase 1 & 2
from phase1_intelligence import ContentIntelligence
from phase2_approval import HITLApproval

# Load environment
load_dotenv()
VAULT_PATH = os.getenv("OBSIDIAN_VAULT_PATH")

# Initialize LLM
llm = LLM(model="ollama/llama3", base_url="http://localhost:11434")

# ===== AGENTS (Same as before) =====
linkedin_writer = Agent(
    role="LinkedIn Content Specialist",
    goal="Create professional, thought-leadership LinkedIn posts",
    backstory="You're a B2B tech content writer. Balance credibility with accessibility.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

x_writer = Agent(
    role="X (Twitter) Content Creator",
    goal="Craft concise, high-impact tweets and threads",
    backstory="Master of brevity and viral patterns. Punchy tweets, strategic emojis.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

facebook_writer = Agent(
    role="Facebook Community Manager",
    goal="Create warm, conversational Facebook posts",
    backstory="Community-focused writer. Warm tone, encourage discussion.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

instagram_writer = Agent(
    role="Instagram Visual Storyteller",
    goal="Craft compelling Instagram captions",
    backstory="Creative writer for visual platforms. Concise, impactful, hashtag master.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# ===== WORKFLOW =====

def main():
    # **PHASE 1: Content Intelligence**
    print("\n🚀 STARTING SOCIAL_CREW PIPELINE\n")
    
    intelligence = ContentIntelligence(VAULT_PATH)
    analyzed_pages = intelligence.run()
    intelligence.save_analysis(analyzed_pages)
    
    # **PHASE 2: HITL Approval**
    approval = HITLApproval()
    selected_content = approval.present_options(analyzed_pages)
    
    if not selected_content:
        print("❌ No content selected. Exiting.")
        return
    
    # **PHASE 3: Platform Generation**
    content = selected_content["content"]
    title = selected_content["title"]
    platforms = selected_content["platforms"]
    
    print("\n" + "=" * 60)
    print(f"📱 GENERATING CONTENT FOR: {', '.join(platforms).upper()}")
    print("=" * 60 + "\n")
    
    # Map platforms to agents
    agent_map = {
        "linkedin": linkedin_writer,
        "x": x_writer,
        "facebook": facebook_writer,
        "instagram": instagram_writer
    }
    
    # Create tasks
    tasks = {}
    for platform in platforms:
        if platform not in agent_map:
            print(f"⚠️ Unknown platform: {platform}, skipping")
            continue
        
        agent = agent_map[platform]
        
        tasks[platform] = Task(
            description=f"Create a {platform} post from:\n\n{content}",
            expected_output=f"{platform.capitalize()} post with appropriate tone and format",
            agent=agent
        )
    
    # Run crews
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    for platform, task in tasks.items():
        print(f"\n{'='*60}")
        print(f"📱 PLATFORM: {platform.upper()}")
        print(f"{'='*60}\n")
        
        crew = Crew(agents=[task.agent], tasks=[task], verbose=True)
        result = crew.kickoff()
        
        # Save
        output_file = output_dir / f"{title.replace(' ', '_')}_{platform}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(str(result))
        
        print(f"\n✅ Saved: {output_file}\n")
    
    print("\n" + "=" * 60)
    print("🎉 ALL PLATFORMS GENERATED!")
    print("=" * 60)


if __name__ == "__main__":
    main()
