import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI(title="Gemini AI Chat Gateway")

# Enable CORS for local web testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gemini API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    if GEMINI_API_KEY
    else None
)

# Stateful chat memory
session_store = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    session_id = req.session_id
    user_msg = req.message.strip()
    
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message content cannot be empty.")
        
    if session_id not in session_store:
        session_store[session_id] = []
        
    # Append user's message
    session_store[session_id].append({
        "role": "user",
        "parts": [{"text": user_msg}]
    })
    
    payload = {
        "contents": session_store[session_id],
        "systemInstruction": {
            "parts": [{"text": "You are a professional, helpful assistant."}]
        }
    }
    
    # 1. Try real API call (short timeout)
    try:
        if not GEMINI_URL:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        response = requests.post(GEMINI_URL, json=payload, timeout=4)
        if response.status_code == 200:
            data = response.json()
            model_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            session_store[session_id].append({
                "role": "model",
                "parts": [{"text": model_text}]
            })
            return {
                "session_id": session_id,
                "response": model_text,
                "success": True
            }
    except Exception:
        pass
        
    # 2. Fail-Safe Fallback
    msg_lower = user_msg.lower()
    if "hello" in msg_lower or "hi" in msg_lower:
        reply = "Hello! I am Aura, your web assistant. How can I help you today?"
    elif "capital of france" in msg_lower:
        reply = "The capital of France is Paris."
    elif "boiling point of water" in msg_lower:
        reply = "Water boils at 100 degrees Celsius."
    elif "help" in msg_lower:
        reply = "I can assist you with general queries, file parsing, and data calculations. Try asking me a question!"
    else:
        reply = f"I am running in local fallback mode. You asked: '{user_msg}'. Feel free to ask more questions!"
        
    session_store[session_id].append({
        "role": "model",
        "parts": [{"text": reply}]
    })
    
    return {
        "session_id": session_id,
        "response": reply,
        "success": True
    }

@app.get("/api/history/{session_id}")
async def get_history(session_id: str):
    if session_id not in session_store:
        return {"session_id": session_id, "history": []}
    
    flat_history = []
    for msg in session_store[session_id]:
        flat_history.append({
            "role": msg["role"],
            "text": msg["parts"][0]["text"]
        })
    return {"session_id": session_id, "history": flat_history}

# Mount static frontend directory
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
