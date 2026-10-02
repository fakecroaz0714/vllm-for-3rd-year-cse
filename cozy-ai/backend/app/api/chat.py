from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, VLLMStatusResponse, VLLMConfigRequest
from app.services.vllm_client import vllm_client

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def generate_exam_answer(req: ChatRequest):
    """
    Generate an exam-oriented answer using vLLM inference engine,
    incorporating marks-based structuring and multiple explanation modes.
    """
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    
    response = await vllm_client.generate_answer(req)
    return response

@router.get("/vllm/status", response_model=VLLMStatusResponse)
async def get_vllm_status():
    """Check connectivity to the vLLM server."""
    return await vllm_client.check_health()

@router.post("/vllm/config", response_model=VLLMStatusResponse)
async def update_vllm_config(cfg: VLLMConfigRequest):
    """Update vLLM endpoint configuration and test connection."""
    vllm_client.update_config(cfg.base_url, cfg.model, cfg.api_key)
    return await vllm_client.check_health()
