import requests

API_KEY = "your api key"
SEARCH_ENGINE_ID = "search enigine id"

def get_forums(query):
    url = f"your url ={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"
    response = requests.get(url)
    results = response.json()
    
    forums = []
    for item in results.get("items", []):
        forums.append({"title": item["title"], "link": item["link"]})

    return forums[:5]

# Example
forums = google_search("Depression mental health forums")
for f in forums:
    print(f"{f['title']}: {f['link']}")
