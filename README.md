# Company News Analyzer

![GitHub license](https://img.shields.io/github/license/{username}/news_summarizer)
![Python version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Active-green)

Welcome to the **Company News Analyzer**, a powerful tool built with FastAPI and Streamlit that analyzes recent news articles about a specified company, performs sentiment analysis, and generates audio summaries in both English and Hindi. This project leverages advanced NLP models and APIs to provide insights into public sentiment and deliver accessible audio outputs.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Overview
The Company News Analyzer fetches the latest news articles for a given company using the Serp API, analyzes their sentiment using the `cardiffnlp/twitter-roberta-base-sentiment` model, and generates a summary with audio files in English and Hindi. It’s designed for users who want to quickly understand media sentiment and listen to insights in their preferred language.

This project is ideal for:
- Investors tracking company performance.
- Researchers analyzing media trends.
- Developers experimenting with NLP and audio generation.

## Features
- **News Fetching**: Retrieves up to 10 recent news articles per company using Serp API.
- **Sentiment Analysis**: Classifies articles as Positive, Negative, or Neutral using the `cardiffnlp/twitter-roberta-base-sentiment` model.
- **Dual-Language Summaries**: Generates text and audio summaries in English and Hindi.
- **User-Friendly Interface**: Streamlit-based UI with progress indicators and audio playback.
- **Scalable Backend**: FastAPI-powered API for efficient processing and static file serving.

## Installation

### Prerequisites
- Python 3.11.9
- Git (for cloning the repository)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/krishnakumar51/Company-News-Analyser.git
   cd news_summarizer
2. **Create a Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  
3. **Install Dependencies Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
4. **Set Up Environment Variables**
    Create a local .env file (do not commit this to Git)
    ```bash 
    SERP_API_KEY=<API-key>
    GROQ_API_KEY=<API-key>
5. **Run the Application**
    Start the backend server:
    ```bash
    cd backend
    uvicorn main:app --reload

    Start the frontend application:
    ``bash
    cd frontend
    streamlit run app.py

## Usage

- Open your browser and navigate to http://localhost:8501 (Streamlit default port).
- Enter a company name (e.g., "nvidia" or "tesla") in the text input field.
- Click the "Analyze" button to fetch articles, analyze sentiment, and generate summaries.
- View the articles, sentiment breakdown, and listen to the English and Hindi audio summaries.
