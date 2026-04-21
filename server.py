import os
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# ---------- FastAPI app ----------
app = FastAPI()

# ---------- CORS (REQUIRED for Expo) ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # okay for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Gemini client ----------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful study chatbot."
    )
)

# ---------- Request model ----------
class ChatRequest(BaseModel):
    message: str

# ---------- Endpoint ----------
@app.post("/chat")
async def chat_with_gemini(req: ChatRequest):
    print("Received:", req.message)

    for attempt in range(5):
        try:
            response = chat.send_message(req.message)
            return {"reply": response.text}
        except ServerError:
            if attempt == 4:
                return {"reply": "Gemini is busy. Try again shortly."}
            time.sleep(2 ** attempt)
