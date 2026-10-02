import os
import sys
import pytest

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.models.schemas import ChatRequest
from app.services.vllm_client import vllm_client
from app.services.subject_registry import SubjectRegistry

def test_subject_registry_all_6():
    subjects = SubjectRegistry.get_all_subjects()
    assert len(subjects) == 6
    ids = [s["id"] for s in subjects]
    assert "deep_learning" in ids
    assert "blockchain" in ids
    assert "robotics" in ids
    assert "mobile_dev" in ids
    assert "java_web" in ids
    assert "placement" in ids

def test_subject_curated_questions():
    qs = SubjectRegistry.get_questions_for_subject("blockchain")
    assert len(qs) >= 5
    assert any("Proof of Work" in q.question or "PoW" in q.question for q in qs)

@pytest.mark.anyio
async def test_vllm_prompt_building():
    req = ChatRequest(
        subject="Blockchain & Technology",
        question="Explain Proof of Stake for 13 marks",
        marks=13,
        style="Exam Ready",
        explain_simply=True
    )
    system_prompt, user_prompt = vllm_client.build_prompt(req)
    assert "cozy.ai" in system_prompt
    assert "Blockchain & Technology" in user_prompt
    assert "13 Marks" in user_prompt
    assert "Proof of Stake" in user_prompt
    assert "BLOCKCHAIN SPECIALIZATION" in user_prompt

@pytest.mark.anyio
async def test_domain_fallback_answers():
    # Test Deep Learning
    dl_req = ChatRequest(subject="Deep Learning & Predictive Modelling", question="Explain CNN architecture", marks=13)
    dl_ans = vllm_client._generate_domain_fallback(dl_req)
    assert dl_ans.definition is not None
    assert dl_ans.simple_analogy is not None
    assert len(dl_ans.working_steps) >= 3

    # Test Blockchain
    bc_req = ChatRequest(subject="Blockchain & Technology", question="Explain Proof of Work", marks=13)
    bc_ans = vllm_client._generate_domain_fallback(bc_req)
    assert "Blockchain" in bc_ans.definition or "ledger" in bc_ans.definition.lower()
    assert bc_ans.diagram_ascii is not None

    # Test Java & Web
    jw_req = ChatRequest(subject="Java & Web Programming", question="Explain OOP in Java", marks=13)
    jw_ans = vllm_client._generate_domain_fallback(jw_req)
    assert jw_ans.code_snippet is not None
    assert "class" in jw_ans.code_snippet
