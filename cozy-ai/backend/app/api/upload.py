import os
import shutil
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.config import settings
from app.models.schemas import ExtractionResult, QuestionItem
from app.services.document_parser import DocumentParser
from app.services.question_extractor import QuestionExtractor

router = APIRouter()

# In-memory store for currently active extracted questions
CURRENT_QUESTIONS: List[QuestionItem] = []

@router.post("/upload", response_model=ExtractionResult)
async def upload_question_bank(
    file: UploadFile = File(...),
    subject: str = Form("Deep Learning")
):
    """
    Accepts PDF, DOCX, TXT, or scanned documents.
    Extracts text and parses questions into structured JSON.
    """
    os.makedirs(settings.upload_dir, exist_ok=True)
    file_path = os.path.join(settings.upload_dir, file.filename)
    
    # Save uploaded file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Extract text
    raw_text, file_type = DocumentParser.extract_text(file_path)
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from document.")

    # Extract questions
    questions = QuestionExtractor.extract_questions(raw_text, default_subject=subject, source_filename=file.filename)
    
    # Update in-memory cache
    global CURRENT_QUESTIONS
    CURRENT_QUESTIONS = questions

    return ExtractionResult(
        filename=file.filename,
        file_type=file_type,
        subject=subject,
        total_questions=len(questions),
        questions=questions,
        raw_text_preview=raw_text[:600] + ("..." if len(raw_text) > 600 else "")
    )

@router.post("/load-sample", response_model=ExtractionResult)
async def load_sample_qb(subject: str = "Deep Learning"):
    """Load the pre-bundled sample question bank for instant test drive."""
    sample_file = os.path.join(settings.sample_dir, "sample_deep_learning_qb.txt")
    if not os.path.exists(sample_file):
        raise HTTPException(status_code=404, detail="Sample question bank file not found.")

    raw_text, file_type = DocumentParser.extract_text(sample_file)
    questions = QuestionExtractor.extract_questions(raw_text, default_subject=subject, source_filename="Deep_Learning_University_QB.pdf")

    global CURRENT_QUESTIONS
    CURRENT_QUESTIONS = questions

    return ExtractionResult(
        filename="Deep_Learning_University_QB.pdf",
        file_type="sample_pdf",
        subject=subject,
        total_questions=len(questions),
        questions=questions,
        raw_text_preview=raw_text[:600]
    )

@router.get("/questions", response_model=List[QuestionItem])
async def get_current_questions(unit: Optional[str] = None, category: Optional[str] = None):
    """Retrieve list of currently extracted questions with optional filtering."""
    results = CURRENT_QUESTIONS
    if unit:
        results = [q for q in results if q.unit and unit.lower() in q.unit.lower()]
    if category:
        results = [q for q in results if q.category and category.lower() in q.category.lower()]
    return results
