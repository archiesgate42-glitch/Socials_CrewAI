# src/main.py

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.crew import SocialCrewAI

def main():
    """
    Main entry point for Socials_CrewAI
    """
    
    # Load environment variables
    load_dotenv()
    
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    
    if not vault_path:
        print("❌ Error: OBSIDIAN_VAULT_PATH not set in .env")
        print("Please create .env file with:")
        print('OBSIDIAN_VAULT_PATH="C:\\Users\\archi\\OneDrive\\Documents\\Mobile_Vaulte"')
        return
    
    print("🚀 Starting Socials_CrewAI...")
    print(f"📂 Vault: {vault_path}\n")
    
    # Initialize crew
    crew = SocialCrewAI(vault_path=vault_path)
    
    # Process staging content
    crew.process_staging_content()
    
    print("✅ Processing complete!")

if __name__ == "__main__":
    main()
