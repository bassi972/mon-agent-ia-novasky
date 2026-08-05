import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"), 
)

class PromptRequest(BaseModel):
    message: str

@app.get("/")
def health_check():
    return {"status": "Agent IA en ligne"}

@app.post("/run")
def run_agent(request: PromptRequest):
    response = client.chat.completions.create(
        model="qwen/qwen-2.5-72b-instruct:free", 
        messages=[{"role": "user", "content": request.message}]
    )
    return {"reponse": response.choices[0].message.content}
