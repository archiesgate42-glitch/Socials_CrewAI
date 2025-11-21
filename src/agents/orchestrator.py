# src/agents/orchestrator.py

from crewai import Agent
from langchain_ollama import ChatOllama

def create_orchestrator_agent(llm) -> Agent:
    """
    Creates the main Orchestrator Agent
    Responsibilities: Content intake, classification, routing, IP protection
    """
    
    return Agent(
        role="Social Media Content Orchestrator",
        goal=(
            "Analyze content from Obsidian vault, classify its type and tone, "
            "route it to appropriate platform-specific writers, and ensure "
            "no sensitive IP or code is shared publicly."
        ),
        backstory=(
            "You are an expert content strategist with deep knowledge of "
            "social media platforms (LinkedIn, X, Facebook, Instagram). "
            "You understand tone differences between platforms and can "
            "identify which content fits where. You're also security-aware "
            "and protect intellectual property by filtering sensitive info."
        ),
        verbose=True,
        allow_delegation=True,
        llm=llm
    )
