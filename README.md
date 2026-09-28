# OmniAI — Multi-Model AI Orchestrator

OmniAI is a provider-neutral AI super-app starter. It gives one chat interface to an orchestration layer that can route work to different AI providers, tools, and specialist agents.

## What is included

- Responsive chat UI
- FastAPI backend
- Provider adapter interface
- Mock provider that works immediately without API keys
- Optional OpenAI-compatible provider adapter
- Task classification and routing
- Multi-model "AI Council" mode
- Web-research/tool abstraction
- Conversation/project memory abstraction
- File/tool abstractions
- Cost/latency-aware routing hooks
- Docker support
- Environment configuration
- Security-oriented defaults
- Health endpoint
- API documentation through FastAPI

## Important

There is no legitimate way to literally merge the proprietary internal weights of every commercial AI model into one model. OmniAI instead orchestrates models that you are authorized to access through their APIs or local runtimes.

## Quick start

### 1. Create the environment

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r backend/requirements.txt
```

### 2. Configure

Copy `.env.example` to `.env`.

The default provider is `mock`, so the app works without credentials.

### 3. Run

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`.

## Optional model providers

The provider interface is deliberately modular. Add credentials to `.env` and implement/enable an adapter in `backend/providers/`.

For production, never put provider API keys in the browser.

## Architecture

```text
Browser
   |
   v
FastAPI API
   |
   +--> Task Classifier
   |
   +--> Router ----------------------+
   |                                  |
   |                    +-------------+-------------+
   |                    |             |             |
   v                    v             v             v
General Model       Coding Model  Vision Model  Research Tools
   |                    |             |             |
   +--------------------+-------------+-------------+
                            |
                            v
                       Verifier/Critic
                            |
                            v
                         Response
```

## Production checklist

- Use HTTPS.
- Put authentication in front of the API.
- Store secrets in a secret manager.
- Add rate limits and quotas.
- Encrypt sensitive stored data.
- Add audit logging.
- Add provider timeout/retry/circuit-breaker logic.
- Add moderation and abuse controls.
- Add per-provider cost limits.
- Never expose API keys to the client.
- Add human approval for consequential external actions.
- Add data retention/deletion controls.
- Add tests and monitoring before public launch.
