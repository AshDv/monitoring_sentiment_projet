from elasticsearch import Elasticsearch
import os

ES_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
INDEX_ALIAS = os.getenv("INDEX_ALIAS", "sentiments")
INDEX_NAME = os.getenv("INDEX_NAME", "product_sentiment_v1")

client = Elasticsearch(ES_URL)

MAPPING = {
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "author": {"type": "keyword"},
            "source": {"type": "keyword"},
            "product": {"type": "keyword"},
            "message": {"type": "text"},
            "sentiment_label": {"type": "keyword"},
            "sentiment_score": {"type": "float"},
            "created_at": {"type": "date"},
            "ingested_at": {"type": "date"}
        }
    }
}

def ensure_index():
    if not client.indices.exists(index=INDEX_NAME):
        client.indices.create(index=INDEX_NAME, body=MAPPING)
    if not client.indices.exists_alias(name=INDEX_ALIAS):
        client.indices.put_alias(index=INDEX_NAME, name=INDEX_ALIAS)
    return INDEX_NAME, INDEX_ALIAS
