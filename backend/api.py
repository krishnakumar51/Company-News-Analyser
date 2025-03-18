from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils import fetch_news_report, generate_comparative_analysis
import os
from gtts import gTTS
import re
from deep_translator import GoogleTranslator

router = APIRouter()

class CompanyRequest(BaseModel):
    company: str

@router.post("/analyze")
async def analyze_company(request: CompanyRequest):
    """Handle API request to analyze news for a company."""
    try:
        print(f"[INFO] Received request to analyze company: {request.company}")
        articles = fetch_news_report(request.company)
        if not articles:
            raise HTTPException(status_code=404, detail="No articles found for this company.")
        
        comparative_analysis = generate_comparative_analysis(articles)
        sentiment_dist = comparative_analysis["Sentiment Distribution"]
        
        total = len(articles)
        english_summary = (f"Out of {total} articles about {request.company}, "
                           f"{sentiment_dist['Positive']} were positive, "
                           f"{sentiment_dist['Negative']} were negative, "
                           f"and {sentiment_dist['Neutral']} were neutral.")
        
        hindi_summary = GoogleTranslator(source='en', target='hi').translate(english_summary)
        
        safe_company = re.sub(r'\W+', '_', request.company.lower())  
        os.makedirs("static", exist_ok=True)  
        
        english_audio_filename = f"{safe_company}_summary_en.mp3"
        english_audio_path = os.path.join("static", english_audio_filename)
        tts_en = gTTS(text=english_summary, lang="en")
        tts_en.save(english_audio_path)
        
        hindi_audio_filename = f"{safe_company}_summary_hi.mp3"
        hindi_audio_path = os.path.join("static", hindi_audio_filename)
        tts_hi = gTTS(text=hindi_summary, lang="hi")
        tts_hi.save(hindi_audio_path)
        
        base_url = "http://localhost:8000"  
        english_audio_url = f"{base_url}/static/{english_audio_filename}"
        hindi_audio_url = f"{base_url}/static/{hindi_audio_filename}"
        
        response = {
            "Company": request.company,
            "Articles": articles,
            "Comparative Sentiment Score": {
                "Sentiment Distribution": sentiment_dist,
                "Summary": english_summary,
                "Hindi Summary": hindi_summary
            },
            "AudioEnglish": english_audio_url,
            "AudioHindi": hindi_audio_url
        }
        print(f"[DEBUG] Response: {response}")
        return response
    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))