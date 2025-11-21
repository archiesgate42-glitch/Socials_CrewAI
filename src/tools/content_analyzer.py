# tools/content_analyzer.py

from typing import Dict, List


class ContentAnalyzer:
    """Analyze content for tone, topic, and platform suitability"""
    
    @staticmethod
    def analyze_tone(content: str) -> str:
        """Detect content tone"""
        content_lower = content.lower()
        
        # Tone keywords
        tones = {
            "professional": ["business", "enterprise", "solution", "strategy", "innovation"],
            "technical": ["code", "api", "system", "architecture", "implementation"],
            "casual": ["hey", "awesome", "cool", "love", "excited"],
            "educational": ["learn", "guide", "tutorial", "how to", "step by step"]
        }
        
        tone_scores = {}
        for tone, keywords in tones.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            tone_scores[tone] = score
        
        # Return highest scoring tone
        return max(tone_scores, key=tone_scores.get) if tone_scores else "neutral"
    
    @staticmethod
    def suggest_platforms(page_data: Dict) -> List[str]:
        """Suggest best platforms based on content analysis"""
        content = page_data["content"]
        metadata = page_data["metadata"]
        
        # Respect manual platform selection in frontmatter
        if "platforms" in metadata:
            return metadata["platforms"]
        
        suggested = []
        
        # LinkedIn: Professional/technical content
        if any(kw in content.lower() for kw in ["business", "strategy", "innovation", "ai", "tech"]):
            suggested.append("linkedin")
        
        # X (Twitter): Short, punchy topics
        if page_data["word_count"] < 500 or "announcement" in content.lower():
            suggested.append("x")
        
        # Facebook: Community/casual
        if any(kw in content.lower() for kw in ["community", "event", "join", "share"]):
            suggested.append("facebook")
        
        # Instagram: Visual content
        if page_data["images"]:
            suggested.append("instagram")
        
        # Default fallback
        return suggested if suggested else ["linkedin", "x"]
    
    @staticmethod
    def extract_keywords(content: str, top_n: int = 5) -> List[str]:
        """Extract top keywords"""
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "is", "are"}
        words = content.lower().split()
        filtered = [w for w in words if w not in stop_words and len(w) > 3]
        
        from collections import Counter
        word_counts = Counter(filtered)
        return [word for word, _ in word_counts.most_common(top_n)]
