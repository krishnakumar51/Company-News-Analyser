import os
from transformers import pipeline
from langchain_groq import ChatGroq
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Initialize models
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, groq_api_key=GROQ_API_KEY)
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def fetch_news_report(company: str) -> list:
    """Fetch at least 10 unique news articles using Serp API."""
    print(f"[INFO] Starting news fetch for company: {company}")
    articles = []
    
    # Check if Serp API key is set
    if not SERP_API_KEY:
        print("[ERROR] SERP_API_KEY is not set in the environment variables.")
        return articles
    
    try:
        # Define search parameters for Google News
        params = {
            "engine": "google",
            "q": company,
            "tbm": "nws",  # News search
            "num": 10,     # Fetch up to 10 results
            "api_key": SERP_API_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])
        
        # Process up to 10 articles
        for article in news_results[:10]:
            title = article.get("title")
            summary = article.get("snippet")
            if title and summary:
                articles.append({
                    "Title": title,
                    "Summary": summary,
                    "Sentiment": analyze_sentiment(summary),
                    "Topics": extract_topics(summary)
                })
        
        print(f"[INFO] Fetched {len(articles)} articles for {company}")
        if len(articles) < 10:
            print("[WARNING] Fewer than 10 articles fetched; consider refining the query.")
    
    except Exception as e:
        print(f"[ERROR] Failed to fetch articles from Serp API: {e}")
    
    return articles

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of the text."""
    print(f"[DEBUG] Analyzing sentiment for text: {text[:30]}...")
    result = sentiment_pipeline(text[:512])[0]  # Truncate for model limit
    label = result["label"]
    # Map the model's labels to readable sentiments
    if label == "LABEL_0":
        sentiment = "Negative"
    elif label == "LABEL_1":
        sentiment = "Neutral"
    elif label == "LABEL_2":
        sentiment = "Positive"
    else:
        sentiment = "Unknown"
    print(f"[DEBUG] Sentiment result: {sentiment}")
    return sentiment

def extract_topics(text: str) -> list:
    """Extract key topics from the text using the language model."""
    print(f"[DEBUG] Extracting topics from text: {text[:30]}...")
    prompt = f"Extract 3 key topics from this text: {text}"
    response = llm.invoke(prompt)
    topics = response.content.split("\n")[:3]
    topics = [topic.strip() for topic in topics if topic.strip()]
    print(f"[DEBUG] Extracted topics: {topics}")
    return topics

def generate_comparative_analysis(articles: list) -> dict:
    """Generate sentiment distribution across articles."""
    print(f"[INFO] Generating comparative analysis for {len(articles)} articles")
    if not articles:
        print("[WARNING] No articles provided for analysis")
        return {"Sentiment Distribution": {"Positive": 0, "Negative": 0, "Neutral": 0}}
    
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = article.get("Sentiment", "Neutral")
        sentiment_dist[sentiment] += 1
    
    analysis = {"Sentiment Distribution": sentiment_dist}
    print(f"[DEBUG] Comparative analysis result: {analysis}")
    return analysis