# Task 10: Complex Workflows

## About
This project implements a multi-step sequential analysis workflow for processing status reports. A coordinator script routes the document to three separate, specialized prompts of the Google Gemini 2.5 Flash model:
1. **Summarization**: Generates a high-level overview.
2. **Action Item Extraction**: Isolates assignees, actions, and deadlines.
3. **Risk Analysis & Technical Recommendations**: Highlights obstacles and engineering solutions.

The three outputs are aggregated and written to a final markdown file.

## Features
- Structured multi-stage prompts using system instructions.
- Parallel-style logical execution aggregated into a single document.
- Local verification with sample reports.

## Setup & Running
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Optional: set a Gemini API key for live model calls. If this is not set, the workflow uses deterministic local fallback analysis for the sample report.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
3. Run the workflow:
   ```bash
   python main.py
   ```
4. View the final compiled report in `analysis_report.md`.
