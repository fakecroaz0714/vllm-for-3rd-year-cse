import os
from pydantic import BaseModel

class Settings(BaseModel):
    # Local Inference Configuration (Ollama on Mac M4 / vLLM)
    vllm_base_url: str = os.getenv("VLLM_BASE_URL", "http://localhost:11434/v1")
    vllm_model: str = os.getenv("VLLM_MODEL", "qwen2.5:7b")
    vllm_api_key: str = os.getenv("VLLM_API_KEY", "EMPTY")
    vllm_timeout_seconds: float = float(os.getenv("VLLM_TIMEOUT", "120.0"))

    # Server configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8080"))

    # Paths
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    upload_dir: str = os.path.join(os.path.dirname(base_dir), "uploads")
    sample_dir: str = os.path.join(os.path.dirname(base_dir), "sample_data")
    frontend_dir: str = os.path.join(os.path.dirname(base_dir), "frontend")

settings = Settings()
