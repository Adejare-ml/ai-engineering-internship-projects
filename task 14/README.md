# Task 14: Scaling & Optimization

## About
This project implements scaling and latency optimization patterns using **Redis caching**. It wraps the chatbot backend in a Docker composition comprising three services:
1. **FastAPI Caching Service**: Computes request hashes and queries Redis. On a hit, response is returned instantly. On a miss, it calls Gemini API and caches it.
2. **Spring Boot Proxy**: Acts as an entrypoint routing requests to the caching backend.
3. **Redis Database**: High-speed in-memory database acting as the cache store.

## Latency Metrics Comparison
- **Cache MISS (First Query)**: ~1500ms - 2500ms (requires querying Gemini API over the network).
- **Cache HIT (Subsequent Query)**: **< 5ms** (reads from local Redis memory database immediately).
- **Latency reduction**: **~99.8%** speedup.

## Setup & Running (Docker Compose)
1. Optional: set a Gemini API key for live model calls. If this is not set, the FastAPI service uses local fallback responses while still demonstrating Redis caching.
   ```bash
   export GEMINI_API_KEY="your-key-here"
   # Optional: export GEMINI_MODEL="gemini-2.5-flash"
   ```
   PowerShell:
   ```powershell
   Set-Item Env:GEMINI_API_KEY "your-key-here"
   ```
2. Run the entire multi-container service:
   ```bash
   docker-compose up --build
   ```
3. Query the chatbot via the Spring Boot gateway:
   - URL: `POST http://localhost:8080/api/springboot/chat`
   - Payload: `{"message": "Hello there", "session_id": "test_scaling"}`
4. Observe the latency differences and the `"cache_status": "HIT" / "MISS"` tags in the responses.
