Socials_CrewAI 🚀
AI-powered multi-platform social media content generator using CrewAI + Ollama (100% local, no cloud)

Automatically transforms project updates from your Obsidian vault into platform-optimized social media posts for LinkedIn, X (Twitter), Facebook, and Instagram.

🎯 Features
✅ Multi-platform content generation - One input → 4 tailored outputs
✅ 100% local AI - Uses Ollama (Llama3) - no API keys, no cloud dependencies
✅ Obsidian integration - Direct vault reading with frontmatter support
✅ IP protection - Presence.md-based filtering to prevent sensitive data leaks
✅ Platform-specific tone - Each agent adapts content to platform style
✅ CrewAI orchestration - Multi-agent system with specialized writers
✅ 3-Phase Pipeline - Intelligence → Approval → Generation
✅ HTML Preview - Visual validation of generated posts

📊 Architecture
text
Phase 1: Intelligence Layer
├── Obsidian Scanner (94 notes detected)
├── Content Classifier (225 images found)
├── IP Filter (Presence.md validation)
└── Content Analyzer

Phase 2: Approval Layer
├── Proposal Generator (63 content items)
└── Human-in-the-Loop (HITL) Review

Phase 3: Generation Layer
├── Orchestrator Agent
├── LinkedIn Writer (Professional)
├── X Writer (Punchy threads)
├── Facebook Writer (Conversational)
└── Instagram Writer (Visual + hashtags)

Output
├── generated_posts.json
└── posts_preview.html (visual validation)
🛠️ Tech Stack
CrewAI 0.86.0 - Multi-agent orchestration framework

Ollama - Local LLM inference (Llama3.1)

LiteLLM - LLM routing layer

Python 3.12 - Core runtime

Obsidian - Content source (markdown vault)

python-frontmatter - YAML metadata parsing

🚀 Quick Start
Prerequisites
Python 3.12+

Ollama installed and running

Obsidian vault (optional, but recommended)

Installation
bash
# Clone the repo
git clone https://github.com/archiesgate42-glitch/Socials_CrewAI.git
cd Socials_CrewAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Pull Llama3.1 model
ollama pull llama3.1
Configuration
Create .env file:

text
OBSIDIAN_VAULT_PATH=C:\Users\YourName\Documents\YourVault
OLLAMA_BASE_URL=http://localhost:11434
Usage
bash
# Phase 1: Scan vault and generate proposals
python src/phase1_intelligence.py

# Phase 2: Review and approve proposals
python src/phase2_approval.py

# Phase 3: Generate platform-specific posts
python src/phase3_content_generation.py
Input: Markdown files in your Obsidian vault
Output:

generated_posts.json - Raw post data

posts_preview.html - Visual preview

📝 Example Input (Obsidian Note)
text
---
title: "Shipped Archie Guardian v1.0"
tags: [tech, ai, security, opensource]
platforms: [linkedin, x]
ready: true
---

🚀 Shipped Archie Guardian v1.0!

Local AI-powered security monitoring with:

✅ 6 widgets (File, Process, Network, Defender, RRNC, Chat)
✅ Multi-agent AI orchestration (OrchA + OrchB)
✅ Ollama Llama3 (100% local, no cloud)
✅ Interactive CLI + AI chat

Built solo in ~24h, v1.0.1 just deployed.

Privacy-first. Transparent. Community-driven.
📤 Example Outputs
LinkedIn (Professional)
🚀 Exciting News! Shipped Archie Guardian v1.0! 🎉
As a pioneer in AI-powered security monitoring, I'm thrilled to announce...
[300-500 words, bullet points, professional tone]

X (Twitter Thread)
Tweet 1: 🚀 Shipped Archie Guardian v1.0! 🔥 A local AI-powered security monitoring system...
Tweet 2: 💡 What would you monitor with an AI security assistant? 🤔...
Tweet 3: ⚡ Built solo in ~24h, v1.0.1 just deployed! 🎯...

Facebook (Conversational)
Hey everyone! 👋 Just shipped Archie Guardian v1.0...
[Warm tone, discussion-prompting, community-focused]

Instagram (Visual)
🚀✨ Archie Guardian v1.0 is LIVE! 💻🔒...
#AI #Security #LocalLLM #OpenSource #Privacy...

🏗️ Project Structure
text
Socials_CrewAI/
├── src/
│   ├── agents/              # Agent definitions
│   │   ├── linkedin_writer.py
│   │   ├── x_writer.py
│   │   ├── facebook_writer.py
│   │   ├── instagram_writer.py
│   │   └── orchestrator.py
│   ├── tools/               # Custom tools
│   │   ├── obsidian_scanner.py
│   │   ├── obsidian_reader.py
│   │   ├── ip_filter.py
│   │   ├── content_classifier.py
│   │   └── content_analyzer.py
│   ├── config/              # YAML configs
│   │   ├── agents.yaml
│   │   └── tasks.yaml
│   ├── phase1_intelligence.py
│   ├── phase2_approval.py
│   ├── phase3_content_generation.py
│   ├── crew.py              # Main crew orchestration
│   └── run_crew.py          # Quick-run script
├── output/                  # Generated posts
├── tests/                   # Test scripts
├── .env                     # Environment variables (not in repo)
├── .gitignore
├── requirements.txt
└── README.md
🔐 IP Protection
Uses Presence.md as source-of-truth for shareable content:

✅ Public updates section → Safe to share

⚠️ Vault-only section → Blocked from posts

Automatic code snippet detection and filtering

🎯 Current Status (Nov 2025)
✅ Phase 1: Intelligence - Production ready
✅ Phase 2: Approval - Production ready
✅ Phase 3: Generation - Production ready (63 posts generated)
✅ HTML Preview - Production ready
🚧 Phase 4: API Publishing - In development (LinkedIn, X, Facebook, Instagram)

🚧 Roadmap
Short-term (Dec 2025)
 LinkedIn API integration

 X (Twitter) API integration

 Scheduling system

 Analytics dashboard

Mid-term (Q1 2026)
 Facebook/Instagram API integration

 Web UI for content review

 Batch processing workflow

 Post performance tracking

Long-term
 Multi-language support

 Image generation integration

 A/B testing framework

 Compliance automation (GDPR, CCPA)

📊 Performance
Latest Test Run (Nov 21, 2025):

✅ 63 posts generated across 4 platforms

✅ <5% error rate (2 harmless edge cases)

✅ Average generation time: ~45s per proposal

✅ 100% local processing (no cloud dependencies)

🤝 Contributing
Contributions welcome! This is a community-driven project.

Fork the repo

Create feature branch (git checkout -b feature/AmazingFeature)

Commit changes (git commit -m 'Add AmazingFeature')

Push to branch (git push origin feature/AmazingFeature)

Open Pull Request

📄 License
MIT License - see LICENSE file for details

🙏 Acknowledgments
CrewAI - Amazing multi-agent framework

Ollama - Local LLM inference made easy

Obsidian - Best knowledge management tool

📞 Contact
Archie Gate (Louis Janssens)

GitHub: @archiesgate42-glitch

Project: Socials_CrewAI

Organization: R.A.T.T. (Raccoon Advanced Tactics & Tech)

🔥 Recent Updates
Nov 21, 2025:

✅ Phase 3 complete (63 production-ready posts)

✅ HTML preview system launched

✅ Strategic partnership discussions underway (Educated Change)

🚧 Phase 4 (API publishing) starting soon

Built with ❤️ using 100% local AI. Privacy-first. Community-driven.