from elasticsearch import Elasticsearch

ES_URL = "http://localhost:9200"
INDEX_NAME = "weather_agent_db"

es = Elasticsearch(ES_URL)

def vector_search(query_embedding, user_id=None, k=3, num_candidates=50):
    """
    KNN vector search on the 'embedding' field.
    Optionally filters by user_id so each user gets their own memory.
    """
    base = {
        "index": INDEX_NAME,
        "knn": {
            "field": "embedding",
            "query_vector": query_embedding,
            "k": k,
            "num_candidates": num_candidates
        }
    }

    if user_id:
        base["query"] = {"term": {"user_id": user_id}}

    resp = es.search(**base)
    hits = resp["hits"]["hits"]
    results = []
    for h in hits:
        src = h["_source"]
        results.append({
            "question": src.get("question", ""),
            "answer":   src.get("answer", ""),
            "score":    h.get("_score", 0.0),
            "user_id":  src.get("user_id"),
            "session_id": src.get("session_id"),
            "doc_type": src.get("doc_type", "weather")
        })
    return results