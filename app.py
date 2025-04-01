from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import pickle
import pandas as pd
import requests
import time
from pymongo import MongoClient

app = Flask(__name__)
# MongoDB Connection
client = MongoClient("mongodb+srv://josephpeterjece2021:AJ9Hg6xTtQBUCoGr@cluster1.xaacunv.mongodb.net/feedback?retryWrites=true&w=majority")
db = client["feedback"]
feedback_collection = db["feedbacks"]   

# Load trained model
with open("mental_health_model.pkl", "rb") as f:
    model = pickle.load(f)

YOUTUBE_API_KEY = "AIzaSyCmVoVbMIEUaARPCyKK5t_6DXLsCljKKYI"
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

API_KEY = "AIzaSyAoWbs3ObIbzOFmNEAj_iIFfF6wmqikT0M"
SEARCH_ENGINE_ID = "f55af49847b6c4dc8"

def get_forums(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    results = response.json()
    
    forums = []
    for item in results.get("items", []):
        forums.append({"title": item["title"], "link": item["link"]})

    return forums[:5]

def get_youtube_videos(query):
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": 10,
        "type": "video"
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = response.json()

    videos = []
    if "items" in data:
        for item in data["items"]:
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            videos.append({"title": video_title, "url": video_url})

    return videos
def get_books(query):
    params = {
        "q": query,
        "maxResults": 5,
        "printType": "books"
    }
    response = requests.get(BOOKS_API_URL, params=params)
    data = response.json()

    books = []
    if "items" in data:
        for item in data["items"]:
            title = item["volumeInfo"].get("title", "No Title")
            authors = item["volumeInfo"].get("authors", ["Unknown Author"])
            link = item["volumeInfo"].get("infoLink", "#")
            thumbnail = item["volumeInfo"].get("imageLinks", {}).get("thumbnail", "")

            books.append({"title": title, "authors": ", ".join(authors), "link": link, "thumbnail": thumbnail})

    return books

import re
def get_google_summary(query):
    url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    data = response.json()

    summary_sentences = []

    if "items" in data:
        for item in data["items"]:
            snippet = item.get("snippet", "")
            if snippet:
                cleaned_snippet = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s*', '', snippet)
                cleaned_snippet = re.sub(r'\s*\.\.\.\s*', ' ', cleaned_snippet)
                cleaned_snippet = re.sub(r'[-—]\s+\b(?:and|or|either|including|such as|like)\b.*$', '', cleaned_snippet)
                sentences = re.split(r'(?<=[.!?])\s+', cleaned_snippet)
                sentences = [s for s in sentences if len(s.split()) > 5]

                summary_sentences.extend(sentences)  

                # Stop when we reach 6-7 proper sentences
                if len(summary_sentences) >= 7:
                    break  
    summary = " ".join(summary_sentences[:7])  

    return summary if summary else "No relevant information found. Please consult a professional for guidance."


def predict_mental_health(data):
    mapping = {"yes": 1, "no": 0, "high": 2, "moderate": 1, "low": 0, "disturbed": 2, "irregular": 1, "adequate": 0, "restful": 0}
    
    for key in data:
        if data[key] in mapping:
            data[key] = mapping[data[key]]
    
    df = pd.DataFrame([data])
    
    prediction = model.predict(df)[0] 
    confidence_scores = model.predict_proba(df)
    
    confidence = max(confidence_scores[0]) 
    print(confidence)
    
    return prediction, confidence


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_data = request.form
        name = user_data.get("name")
        age = user_data.get("age")
        gender = user_data.get("gender")
        
        input_data = {
            "mood": int(user_data.get("mood")),
            "sleepQuality": user_data.get("sleep_quality"),
            "hobbies": user_data.get("hobbies"),
            "social": user_data.get("social"),
            "focus": user_data.get("focus"),
            "stressLevel": user_data.get("stress_level"),
            "recentChanges": user_data.get("recent_changes")
        }

        result,confidence = predict_mental_health(input_data)

        return redirect(url_for("result", result=result, name=name, age=age, gender=gender,confidence=confidence))

    return render_template("index.html")

@app.route("/result")
def result():
    result = request.args.get("result")
    confidence = request.args.get("confidence")
    name = request.args.get("name")
    age = request.args.get("age")
    gender = request.args.get("gender")

    videos = get_youtube_videos(result)
    books = get_books(f"{result} mental health")
    forums = get_forums(f"{result} mental health forums")
    summary = get_google_summary(f"{result} mental health summary")
    print(summary)

    return render_template("result.html", result=result,confidence=confidence, name=name, age=age, gender=gender, videos=videos,books=books,forums=forums,summary=summary)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        data = request.get_json()

        feedback_entry = {
            'name': data.get('name'),
            'email': data.get('email'),
            'rating': data.get('rating'),
            'comments': data.get('comments'),
            'result': data.get('result'),
            'age': data.get('age'),
            'gender': data.get('gender'),
            'confidence': data.get('confidence')
        }

        feedback_collection.insert_one(feedback_entry)

        return jsonify({'success': True, 'message': 'Feedback submitted successfully!'})

    # If GET request, render the feedback form
    return render_template('feedback.html')


if __name__ == "__main__":
    app.run(debug=True)
