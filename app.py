import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# AUTORISER L'INTERFACE DE CHAT À SE CONNECTER
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"), 
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "Agent IA Novasky en ligne et prêt à discuter"}

@app.post("/run")
def run_agent(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="qwen/qwen-2.5-72b-instruct:free", 
            messages=[
                {"role": "system", "content": "Tu es un assistant IA utile, concis et direct."},
                {"role": "user", "content": request.message}
            ]
        )
        return {"reponse": response.choices[0].message.content}
    except Exception as e:
        return {"erreur": str(e)}
