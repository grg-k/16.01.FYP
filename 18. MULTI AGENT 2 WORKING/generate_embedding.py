import requests, os, json

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_embedding(text: str):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"text-embedding-004:embedContent?key={GOOGLE_API_KEY}"
    )
    payload = {
        "content": {
            "parts": [{"text": text}]
        }
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
    data = resp.json()
    embedding = data.get("embedding", {}).get("values")
    return embedding

# multiagent system with adk
# A1 kello maa toolseto b jib bas l taes A2
# ykun shwe zake, get me the weather in bey and retrieve all the chat messages related to beirut --> yeedir 

#workflow agent
# sequential, loop, parallel . . . 