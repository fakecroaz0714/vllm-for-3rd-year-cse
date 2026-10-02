from typing import List, Optional
from fastapi import APIRouter, HTTPException
from app.models.schemas import QuestionItem, SubjectMetadata, PlacementPracticeRequest, ChatRequest, ChatResponse
from app.services.subject_registry import SubjectRegistry, SUBJECTS_CONFIG
from app.api.upload import CURRENT_QUESTIONS
from app.services.vllm_client import vllm_client

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectMetadata])
async def list_all_subjects():
    """Returns the 6 first-class subjects (5 semester modules + Placement Training)."""
    return SubjectRegistry.get_all_subjects()

@router.get("/subjects/{subject_id}/questions", response_model=List[QuestionItem])
async def get_subject_questions(subject_id: str):
    """Retrieve curated question bank for a specific subject module."""
    if subject_id not in SUBJECTS_CONFIG:
        raise HTTPException(status_code=404, detail="Subject not found")
    return SubjectRegistry.get_questions_for_subject(subject_id)

@router.post("/subjects/{subject_id}/load-default", response_model=List[QuestionItem])
async def load_subject_default_bank(subject_id: str):
    """Loads the curated syllabus question bank for the selected subject into active memory."""
    if subject_id not in SUBJECTS_CONFIG:
        raise HTTPException(status_code=404, detail="Subject not found")
    questions = SubjectRegistry.get_questions_for_subject(subject_id)
    
    # Update active questions
    import app.api.upload as upload_module
    upload_module.CURRENT_QUESTIONS = questions
    return questions

@router.post("/placement/practice", response_model=ChatResponse)
async def generate_placement_practice(req: PlacementPracticeRequest):
    """Generate a custom practice question with answer for Placement Training."""
    prompt_question = f"Generate a placement practice problem for {req.track.upper()} on the topic '{req.topic}' at {req.difficulty} difficulty. Provide step-by-step solution, shortcut formulas (for aptitude), optimal time/space complexity (for coding), or STAR framework (for HR)."
    
    chat_req = ChatRequest(
        subject="Placement Training",
        domain_mode="placement",
        topic=req.topic,
        question=prompt_question,
        marks=10,
        style="Exam Ready",
        explain_simply=True
    )
    return await vllm_client.generate_answer(chat_req)
