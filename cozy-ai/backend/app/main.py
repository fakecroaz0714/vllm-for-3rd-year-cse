import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import settings
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.subjects import router as subjects_router

app = FastAPI(
    title="cozy.ai API",
    description="Your cozy exam companion — Question Extraction & vLLM Inference Engine",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(upload_router, prefix="/api", tags=["Question Bank & Extraction"])
app.include_router(chat_router, prefix="/api", tags=["vLLM Inference & Chat"])
app.include_router(subjects_router, prefix="/api", tags=["Subjects & Taxonomy"])

# Ensure directories exist
os.makedirs(settings.upload_dir, exist_ok=True)
os.makedirs(settings.sample_dir, exist_ok=True)

# Mount frontend static files
if os.path.exists(settings.frontend_dir):
    app.mount("/static", StaticFiles(directory=settings.frontend_dir), name="static")

@app.get("/")
async def serve_index():
    index_path = os.path.join(settings.frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to cozy.ai API! Frontend index.html not found yet."}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "cozy.ai-backend"}
