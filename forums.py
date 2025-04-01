import requests

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

# Example
forums = google_search("Depression mental health forums")
for f in forums:
    print(f"{f['title']}: {f['link']}")
