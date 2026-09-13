# Task 9: Conversational Agents

## About
This project implements a stateful chatbot CLI that maintains dialogue history across turns. Unlike stateless APIs, it stores previous user inputs and assistant responses, and includes the full context in subsequent API calls to the Google Gemini 2.5 Flash model. This enables the assistant to remember details and refer back to them cohesively.

## Features
- Dialogue state management and history tracking.
- Contextual multi-turn reasoning with Gemini 2.5 Flash.
- Minimalistic terminal user interface.

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optional: set a Gemini API key for live model calls. If this is not set, the CLI uses local fallback responses so the memory demo still runs offline.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
3. Run the chatbot:
   ```bash
   python main.py
   ```
4. Exit by typing `exit`.
