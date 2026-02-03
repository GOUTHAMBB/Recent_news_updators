import requests
import os
from datetime import datetime, timedelta

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        pass

# Load Secrets
load_dotenv()
api_key = os.getenv("NEWS_API_KEY") 

if not api_key:
    print("Error: No API Key found in environment variables.")
    exit()

# Define the endpoint (Everything is better for specific keyword searches than top-headlines)
url = "https://newsapi.org/v2/everything"

# Helper function to handle the repetition
def fetch_and_save_news(query, filename, api_key):
    # Get date for the last 7 days to keep it fresh
    seven_days_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    params = {
        "q": query,
        "from": seven_days_ago,
        "sortBy": "publishedAt", 
        "language": "en",
        "apiKey": api_key,
        "pageSize": 10 # Limit to top 10 articles per topic to save space
    }

    try:
        print(f"Fetching news for: {query}...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            print(f"No articles found for {query}.")
            return

        print(f"Found {len(articles)} articles. Saving to {filename}...")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"=== REPORT: {query.upper()} ===\n")
            f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            for article in articles:
                title = article.get("title", "No Title")
                description = article.get("description", "No description available.")
                link = article.get("url", "#")
                source = article.get("source", {}).get("name", "Unknown Source")
                
                f.write(f"Source: {source}\n")
                f.write(f"Title:  {title}\n")
                f.write(f"Desc:   {description}\n")
                f.write(f"Link:   {link}\n")
                f.write("-" * 40 + "\n")
        
        print(f"Saved {filename} successfully.\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {query}: {e}\n")

# --- MAIN EXECUTION ---

# 1. AI Technology
fetch_and_save_news(
    query='"Artificial Intelligence" OR "Generative AI" OR "LLM"',
    filename="1_ai_tech_updates.txt",
    api_key=api_key
)

# 2. Programmatic AdTech
fetch_and_save_news(
    query='"Programmatic Advertising" OR "AdTech" OR "Real-time bidding"',
    filename="2_adtech_updates.txt",
    api_key=api_key
)

# 3. Mergers & Breakthroughs
fetch_and_save_news(
    query='"Tech acquisition" OR "Tech merger" OR "technological breakthrough"',
    filename="3_tech_mergers_breakthroughs.txt",
    api_key=api_key
)

print("All tasks completed.")