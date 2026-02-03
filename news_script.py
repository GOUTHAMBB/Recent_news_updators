import requests
import os
import json
from datetime import datetime, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

api_key = os.getenv("NEWS_API_KEY") 
url = "https://newsapi.org/v2/everything"

# --- EXPANDED TRUSTED SOURCE LISTS (Top ~60) ---

# 1. AI & Deep Tech (Innovation & Research focus)
tech_sources = [
    "techcrunch.com", "wired.com", "theverge.com", "arstechnica.com", 
    "venturebeat.com", "thenextweb.com", "technologyreview.com", # MIT Tech Review
    "spectrum.ieee.org", # IEEE (Hard engineering)
    "zdnet.com", "cnet.com", "engadget.com", "gizmodo.com",
    "theregister.com", "computerworld.com", "infoworld.com",
    "tomshardware.com", "anandtech.com", "geekwire.com",
    "siliconangle.com", "artificialintelligence-news.com"
]

# 2. AdTech & Digital Marketing (Industry Trade focus)
ad_sources = [
    "adweek.com", "adage.com", "digiday.com", "adexchanger.com",
    "thedrum.com", "marketingland.com", "martech.org", 
    "searchengineland.com", "searchenginejournal.com", "mediapost.com",
    "campaignlive.co.uk", "marketingweek.com", "econsultancy.com",
    "dmnews.com", "warc.com", "adnews.com.au", "mumbrella.com.au"
]

# 3. Mergers, Acquisitions & Finance (Reliability focus)
business_sources = [
    "reuters.com", "bloomberg.com", "cnbc.com", "wsj.com", 
    "ft.com", "nytimes.com", "forbes.com", "fortune.com", 
    "businessinsider.com", "marketwatch.com", "economist.com",
    "hbr.org", "inc.com", "entrepreneur.com", "fastcompany.com",
    "qz.com", "barrons.com", "dealbook.nytimes.com"
]

def fetch_and_save_json(query, filename, source_list, api_key):
    # Strictly recent news (last 48 hours for high relevance)
    two_days_ago = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    
    # Join the list into a comma-separated string
    domains_str = ",".join(source_list)

    params = {
        "q": query,
        "domains": domains_str,  # <--- The 20+ sources for this specific topic
        "from": two_days_ago,    
        "sortBy": "relevancy",   
        "language": "en",
        "apiKey": api_key,
        "pageSize": 50           # Increased to 20 to capture the wider net
    }

    try:
        print(f"🔍 Searching '{query}' across {len(source_list)} sources...")
        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        
        # Save as JSON
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, indent=4)
            
        print(f"   ✅ Found {len(articles)} relevant articles -> {filename}")

    except Exception as e:
        print(f"   ❌ Error: {e}")

# --- EXECUTION ---
if api_key:
    # 1. AI Updates 
    fetch_and_save_json(
        '"Artificial Intelligence" OR "Generative AI" OR "LLM" OR "Neural Network"', 
        "news_ai.json", 
        tech_sources, 
        api_key
    )

    # 2. AdTech Updates
    fetch_and_save_json(
        '"Programmatic Advertising" OR "Real-time Bidding" OR "AdTech" OR "Retail Media"', 
        "news_adtech.json", 
        ad_sources, 
        api_key
    )

    # 3. Mergers
    fetch_and_save_json(
        '("Acquisition" OR "Merger" OR "IPO") AND ("Tech" OR "Technology" OR "Startup")', 
        "news_mergers.json", 
        business_sources, 
        api_key
    )
    
    print("\n🎉 Intelligence gathering complete.")
else:
    print("Please set your NEWS_API_KEY")