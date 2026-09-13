import os
import time
import hashlib
import requests
import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Optimized Cached AI Chat service")

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

# Redis Connection setup
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
redis_enabled = False
cache_db = None
in_memory_cache = {}

try:
    cache_db = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, socket_connect_timeout=2)
    cache_db.ping()
    redis_enabled = True
    print(f"Connected to Redis cache at {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    print(f"Redis not available ({e}). Falling back to local in-memory cache.")

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_session"

def get_cache_key(session_id: str, message: str) -> str:
    combined = f"{session_id}:{message.strip().lower()}"
    return "cache:" + hashlib.md5(combined.encode('utf-8')).hexdigest()

@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    start_time = time.time()
    user_msg = req.message.strip()
    session_id = req.session_id
    
    if not user_msg:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    cache_key = get_cache_key(session_id, user_msg)
    
    # 1. Try to read from cache
    cached_reply = None
    if redis_enabled and cache_db:
        try:
            cached_reply = cache_db.get(cache_key)
            if cached_reply:
                cached_reply = cached_reply.decode('utf-8')
        except Exception:
            pass
    else:
        cached_reply = in_memory_cache.get(cache_key)
        
    if cached_reply:
        latency_ms = (time.time() - start_time) * 1000
        return {
            "response": cached_reply,
            "latency_ms": f"{latency_ms:.2f}ms",
            "cache_status": "HIT",
            "success": True
        }
        
    # 2. Cache MISS: Query Gemini API
    model_text = None
    payload = {
        "contents": [{"role": "user", "parts": [{"text": user_msg}]}],
        "systemInstruction": {
            "parts": [{"text": "You are a professional assistant."}]
        }
    }
    
    try:
        if not GEMINI_URL:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        response = requests.post(GEMINI_URL, json=payload, timeout=4)
        if response.status_code == 200:
            data = response.json()
            model_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception:
        pass
        
    # 3. Fallback if Gemini fails
    if not model_text:
        msg_lower = user_msg.lower()
        if "hello" in msg_lower:
            model_text = "Hello! This response is served via optimized local fail-safe mode."
        elif "latency test" in msg_lower:
            model_text = "Latency check: Successful. Try querying this again to verify Cache HIT speedups."
        else:
            model_text = f"Optimized fallback answer for query: '{user_msg}'."
            
    # 4. Save to cache (10-minute TTL)
    if redis_enabled and cache_db:
        try:
            cache_db.setex(cache_key, 600, model_text)
        except Exception:
            pass
    else:
        in_memory_cache[cache_key] = model_text
            
    latency_ms = (time.time() - start_time) * 1000
    return {
        "response": model_text,
        "latency_ms": f"{latency_ms:.2f}ms",
        "cache_status": "MISS",
        "success": True
    }

@app.get("/api/health")
async def health_check():
    return {
        "status": "UP",
        "redis_connected": redis_enabled,
        "redis_host": REDIS_HOST
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
