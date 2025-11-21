# tests/test_vault_access.py

import os
from pathlib import Path
from dotenv import load_dotenv

def test_vault_access():
    """
    Test if vault path and required folders/files exist
    """
    
    load_dotenv()
    vault_path = os.getenv("OBSIDIAN_VAULT_PATH")
    
    if not vault_path:
        print("❌ OBSIDIAN_VAULT_PATH not set in .env")
        return False
    
    vault = Path(vault_path)
    
    checks = {
        "Vault exists": vault.exists(),
        "Social_Crew_Staging folder": (vault / "Social_Crew_Staging").exists(),
        "Presence.md file": (vault / "Presence.md").exists()
    }
    
    print("🔍 Vault Access Test\n")
    print(f"Vault path: {vault}\n")
    
    all_pass = True
    for check_name, result in checks.items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name}")
        if not result:
            all_pass = False
    
    return all_pass

if __name__ == "__main__":
    success = test_vault_access()
    if success:
        print("\n🎉 All checks passed! Ready to run.")
    else:
        print("\n⚠️ Some checks failed. Fix issues above.")
