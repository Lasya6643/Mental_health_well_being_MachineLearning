import re
import requests

API_KEY = "Your api key"
SEARCH_ENGINE_ID = "your search engine id"

def get_google_summary(query):
    url = f"your url={query} &key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    data = response.json()

    summary_sentences = []

    if "items" in data:
        for item in data["items"]:
            snippet = item.get("snippet", "")
            if snippet:
                # Remove dates like "Aug 16, 2024"
                cleaned_snippet = re.sub(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{1,2},\s\d{4}\s*', '', snippet)
                
                # Remove "..." that appears in the middle of sentences
                cleaned_snippet = re.sub(r'\s*\.\.\.\s*', ' ', cleaned_snippet)
                
                # Split snippet into sentences
                sentences = re.split(r'(?<=[.!?])\s+', cleaned_snippet)  
                summary_sentences.extend(sentences)  

                # Stop when we reach 6-7 sentences
                if len(summary_sentences) >= 7:
                    break  

    # Join first 6-7 sentences for a complete summary
    summary = " ".join(summary_sentences[:7])  

    return summary if summary else "No relevant information found. Please consult a professional for guidance."

print(get_google_summary("What is PTSD?"))
