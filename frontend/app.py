import streamlit as st
import requests

# Set page configuration
st.set_page_config(page_title="Company News Analyzer", layout="wide")

# Add main title
st.title("Company News Analyzer")

# Input section
st.header("Enter Company Details")
company = st.text_input("Enter company name")

if st.button("Analyze"):
    # Show spinner during processing
    with st.spinner("Analyzing company news..."):
        response = requests.post("http://localhost:8000/analyze", json={"company": company})
    
    # Check response and display results
    if response.status_code == 200:
        data = response.json()
        if "Company" in data and "Articles" in data:
            # Display company articles
            st.subheader(f"News Articles for {data['Company']}")
            for article in data["Articles"]:
                st.write(f"**Title:** {article['Title']}")
                st.write(f"**Summary:** {article['Summary']}")
                st.write(f"**Sentiment:** {article['Sentiment']}")
                st.write("---")
            
            # Display comparative sentiment analysis
            st.subheader("Sentiment Analysis Summary")
            sentiment_dist = data["Comparative Sentiment Score"]["Sentiment Distribution"]
            st.write(f"**Positive:** {sentiment_dist['Positive']}")
            st.write(f"**Negative:** {sentiment_dist['Negative']}")
            st.write(f"**Neutral:** {sentiment_dist['Neutral']}")
            
            # Display summaries
            st.subheader("Final Verdict")
            st.write(f"**English Summary:** {data['Comparative Sentiment Score']['Summary']}")
            if "Hindi Summary" in data["Comparative Sentiment Score"]:
                st.write(f"**Hindi Summary:** {data['Comparative Sentiment Score']['Hindi Summary']}")
            
            # Play both audio files if available
            if "AudioEnglish" in data and "AudioHindi" in data:
                st.write("**English Audio:**")
                st.audio(data["AudioEnglish"])
                st.write("**Hindi Audio:**")
                st.audio(data["AudioHindi"])
        else:
            st.error("Incomplete data in the response.")
    else:
        st.error(f"Failed to fetch data from backend. Status code: {response.status_code}")