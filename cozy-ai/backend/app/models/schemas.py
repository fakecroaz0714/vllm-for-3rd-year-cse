from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class QuestionItem(BaseModel):
    id: str
    subject: str = "Deep Learning & Predictive Modelling"
    unit: Optional[str] = "General"
    question: str
    marks: Optional[int] = 10
    year: Optional[int] = None
    source: str = "Uploaded Document"
    difficulty: Optional[str] = "medium"
    importance_score: Optional[int] = 50
    category: Optional[str] = "🔥 Must Study" # Must Study, Should Study, Extra Practice, High Yield
    topic: Optional[str] = None
    evidence: Optional[str] = None

class SubjectMetadata(BaseModel):
    id: str
    name: str
    icon: str
    category: str # "semester" or "placement"
    code: str
    tagline: str
    question_count: int
    topics: List[str] = Field(default_factory=list)

class ExtractionResult(BaseModel):
    filename: str
    file_type: str
    subject: str
    total_questions: int
    questions: List[QuestionItem]
    raw_text_preview: str

class ChatRequest(BaseModel):
    subject: str = "Deep Learning & Predictive Modelling"
    domain_mode: Optional[str] = "semester" # "semester" or "placement"
    topic: Optional[str] = None
    question: str
    marks: Optional[int] = 10
    style: Optional[str] = "Easy" # Quick, Easy, Detailed, Exam Ready, Revision
    length: Optional[str] = "Standard" # Brief, Standard, Detailed
    explain_simply: Optional[bool] = False
    student_request: Optional[str] = ""

class StructuredAnswer(BaseModel):
    definition: str
    simple_analogy: Optional[str] = None
    working_concept: Optional[str] = None
    working_steps: List[str] = Field(default_factory=list)
    diagram_ascii: Optional[str] = None
    code_snippet: Optional[str] = None
    code_language: Optional[str] = None
    formula_shortcuts: Optional[str] = None
    example: Optional[str] = None
    advantages: List[str] = Field(default_factory=list)
    applications: List[str] = Field(default_factory=list)
    exam_keywords: List[str] = Field(default_factory=list)
    interview_tips: Optional[str] = None
    star_breakdown: Optional[Dict[str, str]] = None
    raw_content: Optional[str] = None

class ChatResponse(BaseModel):
    question: str
    marks: int
    style: str
    answer: StructuredAnswer
    model_used: str
    is_mock: bool = False
    timestamp: str

class VLLMStatusResponse(BaseModel):
    status: str # "connected" or "offline"
    base_url: str
    active_model: str
    available_models: List[str] = Field(default_factory=list)
    message: str

class VLLMConfigRequest(BaseModel):
    base_url: str
    model: str
    api_key: Optional[str] = "EMPTY"

class PlacementPracticeRequest(BaseModel):
    track: str # "aptitude", "coding", "technical", "hr"
    topic: str
    difficulty: Optional[str] = "medium"
