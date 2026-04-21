import os
import time
from fastapi import FastAPI
 fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# ---------------- FastAPI app ----------------
app = FastAPI()

# ---------------- CORS (required for Expo) ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Gemini client ----------------
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY environment variable is NOT set")

client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful study chatbot."
    )
)

# ---------------- Request schema ----------------
class ChatRequest(BaseModel):
    message: str

# ---------------- Endpoint ----------------
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
