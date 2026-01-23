from elasticsearch import Elasticsearch
from dotenv import load_dotenv
from db_search import vector_search
import os
import requests
import json
import re
import time


load_dotenv() 

es = Elasticsearch("http://localhost:9200")

index_name = "weather_agent_db"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
mapping = {
    "mappings": {
        "properties": {
            "session_id": {"type": "keyword"},
            "user_id": {"type": "keyword"},
            "question": {"type": "text"},
            "answer": {"type": "text"},
            "embedding": {                                              #
                "type": "dense_vector",                                 #
                "dims": 768,                                            #  NOT ACCESSIBLE
                "index": True,                                          #
                "similarity": "cosine"                                  # 
            },                                                          
            "readable_embedding": {"type": "float"}                          
        }                                                               
    }
}

def get_embedding(text: str):
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
    # print(f"length: {len(embedding)}")
    return embedding

def build_memory_context(results, k=5):
    if not results:
        return ""

    lines = ["Here are memories you should use:"]

    for r in results[:k]:
        lines.append(f"- {r['question']} -> {r['answer']}")

    return "\n".join(lines) + "\n"

def before_model_callback(callback_context, llm_request):
    try:
        # Check if llm_request exists and has content
        if not llm_request or not llm_request.contents:
            return None  # Continue without modification

        # Extract user prompt from the latest message in the history
        last_message = llm_request.contents[-1]

        if last_message == None: 
            return None

        if last_message.role == "user" and last_message.parts:
            user_prompt = last_message.parts[0].text
            stripped_prompt = str(user_prompt).strip()
            print("\n\n\nUSER PROMPT:" + user_prompt)
            print("STRIPPED PROMPT:" + stripped_prompt +"\n\n\n")
        else:
            return None

        # Access user_id directly from callback_context
        user_id = callback_context.user_id

        # retrieve embeddings, results...
        embedding = get_embedding(user_prompt)
        results = vector_search(embedding, user_id=user_id, k=5)
        memory_block = build_memory_context(results)
       
        if memory_block:
            enriched_prompt = (
                f"Use the following retrieved context to help answer the question if relevant. You must evaluate whether these informations are relevant to the user's prompt"
                f"{memory_block}\n"
                f"Current message: {user_prompt}"
            )           
            llm_request.contents[-1].parts[0].text = enriched_prompt

        print("===========================\n")
        print("enriched prompt:")
        print (enriched_prompt)
        print("\n===========================")

        return ""
    except Exception as e:
        print("before_model_callback ERROR:", e)
        return

def after_model_callback(callback_context, llm_response):
    try:
        session_id = callback_context.session.id
        user_id = callback_context.session.user_id

        # Extract user prompt
        prompt = ""
        if callback_context.user_content and callback_context.user_content.parts:
            prompt = callback_context.user_content.parts[0].text.strip()

        if not prompt:
            print("No prompt found; not saving.")
            return

        parts = getattr(llm_response, "content", None)
        parts = getattr(parts, "parts", []) if parts else []

        #skip tools
        saw_tool_call = False
        for p in parts:
            if getattr(p, "function_call", None):
                saw_tool_call = True
                break

        if saw_tool_call:
            print("Detected tool-call in model response. Skipping save.")
            return

        #extracting text
        reply = ""
        for p in parts:
            if getattr(p, "text", None):
                reply = p.text.strip()
                if reply:
                    break

        if not reply:
            print("No textual reply to save (likely a tool-run only step).")
            return

        if reply.startswith("[TOOL CALL]"):
            print("Reply is a tool-call marker string. Skipping save.")
            return

        #search to avoid duplications
        existing = es.search(
            index=index_name,
            body={
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"session_id": session_id}},
                            {"match_phrase": {"question": prompt}}
                        ]
                    }
                },
                "_source": False,
                "size": 1
            }
        )
        hits_total = (
            existing.get("hits", {}).get("total", {}).get("value")
            if isinstance(existing.get("hits", {}).get("total"), dict)
            else existing.get("hits", {}).get("total", 0)
        )
        if hits_total and hits_total > 0:
            print("Duplicate detected — skipping save.")
            return

        # 5) Build embedding on the final human-readable QA
        combined_text = f"Q: {prompt}\nA: {reply}"
        embedding = get_embedding(combined_text)
        if not embedding:
            print("No embedding returned; skipping save.")
            return

        es.index(
            index=index_name,
            document={
                "session_id": session_id,
                "user_id": user_id,
                "question": prompt,
                "answer": reply,
                "embedding": embedding,
                "readable_embedding": embedding[:8],
                "doc_type": "weather",
            },
            refresh="wait_for",
        )

        print(f"Saved clean QA pair to ES in index '{index_name}'. len(embedding)={len(embedding)}")

    except Exception as e:
        print("after_model_callback ERROR:", e)