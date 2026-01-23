from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200", verify_certs=False)

es.indices.delete(index="weather_agent_db")
 