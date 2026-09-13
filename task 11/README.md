# Task 11: Tool & Plugin Integration

## About
This project implements an autonomous AI agent capable of using local tools (file reading and mathematical calculations) to solve tasks. It leverages the native tool and function calling API of Google Gemini 2.5 Flash. Rather than relying on external agent loop orchestrators, this agent is powered by a custom python control loop that interprets function execution instructions, runs the corresponding python tools, and feeds results back to the LLM.

## Features
- Native function calling with Gemini 2.5 Flash.
- Local text file reader tool.
- Local PDF text extraction tool (using `pypdf`).
- Safe mathematical expression evaluation tool.
- Autonomous agent loop with state tracking.

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optional: set a Gemini API key for live function-calling responses. If this is not set, the script runs its local tool-loop fallback for the sample task.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
3. Run the agent:
   ```bash
   python agent.py
   ```
