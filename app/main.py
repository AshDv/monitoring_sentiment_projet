from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import Optional
from es import client, ensure_index, INDEX_ALIAS
from model import predict_sentiment

class InDoc(BaseModel):
    message: str
    author: Optional[str] = "unknown"
    source: Optional[str] = "twitter"
    product: Optional[str] = None

class OutDoc(BaseModel):
    id: str
    sentiment_label: str
    sentiment_score: float

app = FastAPI(title="Sentiment Analysis API", version="1.0")

@app.on_event("startup")
def startup():
    ensure_index()

@app.post("/analyze", response_model=OutDoc)
def analyze(doc: InDoc):
    if not doc.message.strip():
        raise HTTPException(400, "message is required")
    label, score = predict_sentiment(doc.message)
    now = datetime.now(timezone.utc)
    body = {
        "author": doc.author,
        "source": doc.source,
        "product": doc.product,
        "message": doc.message,
        "sentiment_label": label,
        "sentiment_score": score,
        "created_at": now.isoformat(),
        "ingested_at": now.isoformat(),
    }
    res = client.index(index=INDEX_ALIAS, document=body)
    return OutDoc(id=res["_id"], sentiment_label=label, sentiment_score=score)

@app.get("/health")
def health():
    return {"elasticsearch": client.ping(), "index": INDEX_ALIAS}