import time
from google import genai
from google.genai import types
from google.genai.errors import ServerError

client = genai.Client(api_key=AQ.")

chat = client.chats.create(
 model="gemini-2.5-flash",
 config=types.GenerateContentConfig(
 system_instruction="You are a helpful chatbot."
 )
)

print("Chatbot ready. Type 'exit' to quit.\n")

while True:
 user_input = input("You: ")
 if user_input.lower() == "exit":
 break

 for attempt in range(5):
 try:
 response = chat.send_message(user_input)
 print("Bot:", response.text)
 break
 except ServerError as e:
 if attempt == 4:
 print("Bot: I'm busy right now. Try again in a moment.")
 else:
 time.sleep(2 ** attempt)
def chat_with_gemini(req: ChatRequest):
    for attempt in range(5):
        try:
            response = chat.send_message(req.message)
            return { "reply": response.text }
        except ServerError:
            if attempt == 4:
                return { "reply": "I'm busy right now. Try again later." }
            time.sleep(2 ** attempt)
``
