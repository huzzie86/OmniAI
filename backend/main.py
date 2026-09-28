from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .config import settings
from .schemas import ChatRequest, ChatResponse, HealthResponse
from .providers.registry import build_registry
from .orchestrator import Orchestrator

app = FastAPI(title=settings.app_name, version="0.1.0")
providers = build_registry()
orchestrator = Orchestrator(providers)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/", include_in_schema=False)
async def home():
    return FileResponse("frontend/index.html")

@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", providers=list(providers.keys()))

@app.get("/api/providers")
async def provider_list():
    return {"providers": list(providers.keys())}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        return await orchestrator.run(request)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Provider/orchestration error: {exc}")
