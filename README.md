# Monitoring Sentiment Projet

Prototype complet ELK + FastAPI pour suivre le sentiment autour d’un produit technologique.

## Lancer la stack
```bash
docker compose up -d --build
curl http://localhost:9200
curl http://localhost:8000/health