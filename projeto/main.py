from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()  # Certifique-se de que esta linha existe

# Carregar o modelo de classificação de texto
classifier = pipeline("text-classification", model="distilbert-base-uncased")

class EmailRequest(BaseModel):
    email_text: str

@app.post("/classify")
async def classify_email(request: EmailRequest):
    email_text = request.email_text

    # Classificar o email
    try:
        result = classifier(email_text)[0]
        category = result["label"]
        suggestion = "Sugestão de resposta automática."  # Exemplo simples
        return {"category": category, "suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))