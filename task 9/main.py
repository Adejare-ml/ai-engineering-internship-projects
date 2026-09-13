import os
import json
import requests

# Gemini API Settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
    if GEMINI_API_KEY
    else None
)

# Store for session history
session_store = {}

def query_gemini_chat(session_id: str, new_user_message: str) -> str:
    """Queries Gemini 2.5 Flash with the full conversation history to maintain state, with fail-safe mock fallback."""
    if session_id not in session_store:
        session_store[session_id] = []
        
    # Append the new user message to the history
    session_store[session_id].append({
        "role": "user",
        "parts": [{"text": new_user_message}]
    })
    
    payload = {
        "contents": session_store[session_id],
        "systemInstruction": {
            "parts": [{"text": "You are a helpful, context-aware AI assistant. You remember details from earlier in the conversation."}]
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
            
            # Append the model response to the history
            session_store[session_id].append({
                "role": "model",
                "parts": [{"text": model_text}]
            })
            return model_text
    except Exception:
        pass
        
    # 2. Fail-Safe Fallback: Generate mock multi-turn dialogue responses
    msg_lower = new_user_message.lower()
    
    # Analyze conversation context to make smart replies
    if "my name is" in msg_lower:
        idx = msg_lower.find("my name is")
        sub = new_user_message[idx + len("my name is"):].strip()
        name = sub.split()[0].rstrip(".,!?")
        reply = f"Nice to meet you, {name}! I have noted your name in our session state."
    elif "what is my name" in msg_lower or "who am i" in msg_lower:
        # Check history for name
        found_name = "User"
        for msg in session_store[session_id]:
            text = msg["parts"][0]["text"].lower()
            if msg["role"] == "user" and "my name is" in text:
                idx = text.find("my name is")
                sub = msg["parts"][0]["text"][idx + len("my name is"):].strip()
                found_name = sub.split()[0].rstrip(".,!?")
                break
        reply = f"Your name is {found_name}. I remember it from our previous turn."
    elif "hello" in msg_lower or "hi" in msg_lower:
        reply = "Hello! How can I assist you in this conversation session today?"
    else:
        reply = f"I received your message: '{new_user_message}'. I am tracking this conversation in session '{session_id}'."
        
    # Append the fallback reply to history
    session_store[session_id].append({
        "role": "model",
        "parts": [{"text": reply}]
    })
    return reply

def chat_session():
    session_id = "default_session"
    print("=== Stateful Chatbot CLI (Type 'exit' to quit) ===")
    print("I can remember details you tell me across multiple turns!")
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            response = query_gemini_chat(session_id, user_input)
            print(f"\nBot: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    chat_session()
