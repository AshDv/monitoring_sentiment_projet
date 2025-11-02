"""
Bulk import CSV dataset with sentiment analysis.
Columns: id, product, label_gt, message
"""
import os
import sys
import csv
from datetime import datetime, timezone
from elasticsearch import helpers

# Ajoute le dossier parent du script ("monitoring_sentiment_projet") au PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# === Imports internes du projet ===
from app.es import client, ensure_index, INDEX_ALIAS
from app.model import predict_sentiment

# === Constantes ===
DATA_PATH = os.getenv("DATA_PATH", "twitter_training.csv")

# === Générateur de documents à indexer ===
def iter_docs():
    with open(DATA_PATH, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            # chaque ligne contient : id, product, label_gt, message
            if len(row) < 4:
                continue

            _, product, _, message = row

            # Analyse du sentiment
            label, score = predict_sentiment(message)

            yield {
                "_index": INDEX_ALIAS,
                "_source": {
                    "author": "unknown",
                    "source": "twitter",
                    "product": product,
                    "message": message,
                    "sentiment_label": label,
                    "sentiment_score": float(score),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                },
            }

# === Fonction principale ===
def main():
    print("🚀 Lancement de l'import du dataset...")
    ensure_index()
    helpers.bulk(client, iter_docs(), chunk_size=2000, request_timeout=120)
    print("✅ Import terminé avec succès !")

# === Point d'entrée ===
if __name__ == "__main__":
    main()