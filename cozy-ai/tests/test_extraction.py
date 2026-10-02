import os
import sys
import pytest

# Add backend directory to sys.path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.services.document_parser import DocumentParser
from app.services.question_extractor import QuestionExtractor

def test_extract_from_text():
    sample_txt = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_deep_learning_qb.txt"))
    raw_text, file_type = DocumentParser.extract_text(sample_txt)
    assert file_type == "txt"
    assert len(raw_text) > 100

    questions = QuestionExtractor.extract_questions(raw_text, default_subject="Deep Learning", source_filename="sample_deep_learning_qb.txt")
    assert len(questions) >= 10, f"Expected at least 10 questions, got {len(questions)}"
    
    # Check that CNN question exists and has marks
    cnn_q = next((q for q in questions if "convolutional" in q.question.lower() or "cnn" in q.question.lower()), None)
    assert cnn_q is not None
    assert cnn_q.marks == 13
    assert "Unit II" in cnn_q.unit or "Unit 2" in cnn_q.unit
    assert cnn_q.category == "🔥 Must Study"

    # Check that Backpropagation question exists
    backprop_q = next((q for q in questions if "backpropagation" in q.question.lower()), None)
    assert backprop_q is not None
    assert backprop_q.marks == 13

def test_extract_from_pdf():
    sample_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample_data", "sample_question_bank.pdf"))
    raw_text, file_type = DocumentParser.extract_text(sample_pdf)
    assert file_type == "pdf"
    assert "deep learning" in raw_text.lower()

    questions = QuestionExtractor.extract_questions(raw_text, default_subject="Deep Learning", source_filename="sample_question_bank.pdf")
    assert len(questions) >= 10
    assert any(q.marks == 13 for q in questions)
