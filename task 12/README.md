# Task 12: Frontend/Backend Collaboration

## About
This project establishes a full-stack, local AI chat application. It packages the stateful Gemini chatbot API inside a **FastAPI** backend and pairs it with a premium **HTML/CSS/JS** user interface designed using glassmorphism styling, glowing backgrounds, and micro-interactions.

## Features
- **FastAPI backend**: Exposes `/api/chat` (POST) and `/api/history` (GET).
- **Session management**: Client generates unique random sessions to maintain separated conversation tracks.
- **Typing indicators**: Animated loading dots show up while awaiting the Gemini API response.
- **Responsive design**: Layout works beautifully on both desktop monitors and smaller device viewports.

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optional: set a Gemini API key for live model calls. If this is not set, the backend serves local fallback responses so the frontend remains usable offline.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
3. Start the FastAPI server:
   ```bash
   python backend/main.py
   ```
4. Open a web browser and navigate to `http://127.0.0.1:8000` to interact with Aura.
