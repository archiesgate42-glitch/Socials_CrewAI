# src/agents/writers/x_writer.py

from crewai import Agent

def create_x_writer(llm) -> Agent:
    """
    X (Twitter) Writer Agent - Short, punchy, viral-focused
    """
    
    x_writer = Agent(  # ✅ Fixed indentation (align with 'def')
        role="X (Twitter) Thread Creator",
        goal="Create viral 3-tweet threads with emojis and hashtags",
        backstory=(
            "You are an expert at creating engaging X threads. You ALWAYS write exactly 3 tweets: "
            "first announces news, second highlights features, third asks a community question. "
            "Each tweet is punchy, uses emojis, and includes relevant hashtags. Never write single tweets."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm
    )
    
    return x_writer  # ✅ Added return statement!
