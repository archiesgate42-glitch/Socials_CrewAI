# src/tools/content_classifier.py

from crewai_tools import tool

@tool("Content Platform Router")
def classify_content(content: str, metadata: dict) -> dict:
    """
    Analyzes content and determines optimal platform distribution
    
    Args:
        content: The main text content
        metadata: Frontmatter metadata (tags, platforms, etc.)
    
    Returns:
        Dictionary with platform routing decisions
    """
    
    # Check for manual platform specification
    if 'platforms' in metadata and metadata['platforms']:
        return {
            'platforms': metadata['platforms'],
            'content_type': metadata.get('type', 'update'),
            'manual_override': True,
            'reasoning': 'Manual platform specification in frontmatter'
        }
    
    # Auto-classification logic
    classification = {
        'platforms': [],
        'content_type': 'update',
        'priority': 'medium',
        'manual_override': False
    }
    
    tags = metadata.get('tags', [])
    word_count = len(content.split())
    
    # LinkedIn: Professional, technical, long-form
    linkedin_indicators = ['tech', 'ai', 'professional', 'business', 'opensource', 'security']
    if any(tag in linkedin_indicators for tag in tags) or word_count > 300:
        classification['platforms'].append('linkedin')
    
    # X (Twitter): Short, punchy updates
    if word_count < 280 or any(tag in ['update', 'news', 'quick'] for tag in tags):
        classification['platforms'].append('x')
    
    # Instagram: Visual content
    if 'visual' in tags or '![' in content:
        classification['platforms'].append('instagram')
    
    # Facebook: Community, conversational
    if any(tag in ['community', 'discussion', 'social'] for tag in tags):
        classification['platforms'].append('facebook')
    
    # Default: LinkedIn for all professional content
    if not classification['platforms']:
        classification['platforms'] = ['linkedin']
    
    classification['reasoning'] = f"Auto-classified based on {len(tags)} tags and {word_count} words"
    
    return classification
