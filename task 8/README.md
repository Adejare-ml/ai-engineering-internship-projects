# Task 8: Evaluation & Testing

## About
This project implements an automated chatbot evaluation system. It runs a test suite of 10 curated questions across different categories (Geography, AI Concepts, Literature, Science, Mathematics, Civics, Finance, Physics, and Technology). The system queries the Google Gemini 2.5 Flash model and evaluates the accuracy of the responses based on keyword overlap (factual recall check).

## Features
- Automated querying of `gemini-2.5-flash` model.
- Robust rate-limiting protection with exponential backoff on HTTP 429 errors.
- Keyword evaluation algorithm to determine accuracy.
- Automated generation of a detailed Markdown report (`evaluation_report.md`).

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optional: set a Gemini API key for live model calls. If this is not set, the script uses its local fallback responses for offline evaluation.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
3. Run the evaluation script:
   ```bash
   python main.py
   ```
4. View the detailed results in `evaluation_report.md`.
