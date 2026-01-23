from elasticsearch import Elasticsearch, helpers
import json
 
es = Elasticsearch(
    "http://localhost:9200",
)
 
index_name = "weather_agent_db"
 
print(f"\nReading index: {index_name}\n")
 
# Use a scroll/scan to fetch all documents safely
results = helpers.scan(
    es,
    index=index_name,
    query={"query": {"match_all": {}}},
    preserve_order=False
)
 


count = 0
for doc in results:
    count += 1
    src = doc["_source"]
 
    print("──────────────────────────────────────────────")
    print(f"Document ID: {doc['_id']}")
    print(f"Session ID : {src.get('session_id')}")
    print(f"User ID    : {src.get('user_id')}")
    print()
    print(f" Content   : {src.get('question')}")
    print(f" Reply      :{src.get('answer')}")
    print()
 
    emb = src.get("readable_embedding"
    "", [])
    if emb:
        print(f"🧠 readable_embedding (first 8 dims): {emb[:8]}")
    else:
        print("⚠ No embedding_raw stored")
 
    print("──────────────────────────────────────────────")
    print()
 
print(f"Total documents read: {count}")