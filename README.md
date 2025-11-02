# Monitoring Sentiment Projet

Prototype complet ELK + FastAPI pour suivre le sentiment autour d’un produit technologique.

## Lancer la stack
```bash
docker compose up -d --build
curl http://localhost:9200
curl http://localhost:8000/health
```

##Lancement et vérification (Docker Compose & Kibana Dev Tools)

1. Démarrage de la stack
```bash
docker compose up -d --build
```

Lancer les trois services : **Elasticsearch**, **Kibana**, et **FastAPI**.

Vérifier que tout est bien démarré :
```bash
docker ps
```

##2. Accès aux interfaces**

- **FastAPI** → http://localhost:8000/docs
- **Kibana** → [http://localhost:5601](http://localhost:5601/)

##3. Vérification d’Elasticsearch
```bash
curl http://localhost:9200
```
Une réponse contenant "You Know, for Search" confirme que le service est opérationnel.

##4 Vérification via Kibana Dev Tools
Dans Kibana → **Dev Tools**, les commandes suivantes m'ont permis de vérifier :
<img width="1470" height="763" alt="Capture d’écran 2025-11-02 à 19 38 20" src="https://github.com/user-attachments/assets/77b52893-bacf-4048-b03a-8249fbb5b625" />

##5 Test de l’API d’analyse
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"text": "The new version is amazing!"}'
```

Réponse attendue :
```bash
{
  "label": "Positive",
  "score": 0.78,
  "timestamp": "2025-11-02T15:45:00Z"
}
```
##6 Arrêt de la stack
```bash
docker compose down
```
