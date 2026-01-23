from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", verify_certs=False)
 
INDEX = "weather_agent_db"
DIMS = 768 

if es.indices.exists(index=INDEX):
    print(f"Index '{INDEX}' already exists.")
else:
    es.indices.create(
        index=INDEX,
        mappings={
            "properties": {
                "content": { "type": "text" },
                "embedding": {
                    "type": "dense_vector",
                    "dims": DIMS,
                    "index": True,
                    "similarity": "cosine"
                },
                "readable_embedding" :{ "type" : "float"},
                "timestamp": { "type": "date" },
                "metadata": { "type": "object", "enabled": True },
                "user_id": { "type": "keyword" },
                "session_id": { "type": "keyword" }
            }
        }
    )
    print(f"Created index '{INDEX}' with dims={DIMS}\n")