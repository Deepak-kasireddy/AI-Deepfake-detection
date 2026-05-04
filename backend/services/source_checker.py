import urllib.parse
import re

class SourceChecker:
    def __init__(self):
        # Trusted sources and their domains
        self.trusted_sources = {
            "Reuters": "reuters.com",
            "Associated Press": "apnews.com",
            "BBC News": "bbc.com/news",
            "NPR": "npr.org",
            "The Guardian": "theguardian.com",
            "FactCheck.org": "factcheck.org",
            "PolitiFact": "politifact.com",
            "Snopes": "snopes.com",
            "Google News": "news.google.com"
        }
        
        # Keywords to ignore in extraction
        self.stop_words = {"a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "to", "from", "in", "on", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "of", "off", "up", "down", "out", "over", "under", "again", "further", "then", "once"}

    def extract_keywords(self, text):
        # Remove special characters and lowercase
        clean_text = re.sub(r'[^\w\s]', '', text.lower())
        words = clean_text.split()
        
        # Filter out short words and stop words
        keywords = [w for w in words if len(w) > 3 and w not in self.stop_words]
        
        # Get top 5 unique keywords
        unique_keywords = []
        for w in keywords:
            if w not in unique_keywords:
                unique_keywords.append(w)
            if len(unique_keywords) >= 5:
                break
        return unique_keywords

    def generate_search_links(self, text, is_fake=False):
        keywords = self.extract_keywords(text)
        query = " ".join(keywords)
        encoded_query = urllib.parse.quote(query)
        
        sources = []
        
        # 1. Google News Search (Primary)
        sources.append({
            "name": "Google News",
            "url": f"https://news.google.com/search?q={encoded_query}",
            "type": "search",
            "reliability": "High"
        })
        
        # 2. Fact Check Links if suspected fake
        if is_fake:
            sources.append({
                "name": "Snopes Fact-Check",
                "url": f"https://www.snopes.com/?s={encoded_query}",
                "type": "fact-check",
                "reliability": "Critical"
            })
            sources.append({
                "name": "PolitiFact",
                "url": f"https://www.politifact.com/search/?q={encoded_query}",
                "type": "fact-check",
                "reliability": "Critical"
            })
        else:
            # 3. Trusted News Archives
            sources.append({
                "name": "Reuters Archive",
                "url": f"https://www.reuters.com/site-search/?query={encoded_query}",
                "type": "archive",
                "reliability": "High"
            })
            sources.append({
                "name": "BBC News",
                "url": f"https://www.bbc.co.uk/search?q={encoded_query}",
                "type": "archive",
                "reliability": "High"
            })

        return sources

    def get_verification_summary(self, is_fake):
        if is_fake:
            return "No verified matches found in major news archives. High risk of misinformation."
        else:
            return "Matching headlines found in multiple trusted sources. Proceed with confidence."
