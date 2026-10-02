import re
import uuid
from typing import List, Optional, Tuple
from app.models.schemas import QuestionItem

class QuestionExtractor:
    # Regex patterns for detecting Units/Modules
    UNIT_PATTERN = re.compile(
        r"^(?:UNIT|MODULE|CHAPTER|PART)\s*[-:—]?\s*([IVXLCDM\d]+|[A-E])(?:\s*[-:—]?\s*(.*))?$",
        re.IGNORECASE
    )

    # Regex patterns for detecting Question starts
    QUESTION_START_PATTERN = re.compile(
        r"^(?:(?:Q(?:uestion)?\.?\s*(\d+[a-z]?|\([a-z\d]+\)))|(\d+[\.\)])|([a-z]\))|(•|\-|\*))\s+(.+)",
        re.IGNORECASE
    )

    # Regex patterns for Marks indicators
    # Matches: [13 Marks], (10M), [13], (5 marks), 13 marks, [7+6=13 Marks]
    MARKS_PATTERN = re.compile(
        r"(?:\[|\()?\s*(?:(?:\d+\s*\+\s*)*\d+\s*=\s*)?(\d+)\s*(?:marks?|mark|m)?\s*(?:\]|\)|\b)",
        re.IGNORECASE
    )

    # Regex patterns for Year indicators
    # Matches: (May/June 2024), 2023, [Nov 2022]
    YEAR_PATTERN = re.compile(r"\b(20[12]\d)\b")

    @classmethod
    def extract_questions(cls, text: str, default_subject: str = "Deep Learning", source_filename: str = "upload.pdf") -> List[QuestionItem]:
        lines = [line.strip() for line in text.splitlines()]
        questions: List[QuestionItem] = []
        
        current_unit = "Unit 1"
        current_question_text = ""
        current_marks: Optional[int] = None
        current_year: Optional[int] = None
        
        # Check if subject can be inferred from document header
        subject = cls._detect_subject(lines, default_subject)

        def save_current_question():
            nonlocal current_question_text, current_marks, current_year
            if current_question_text:
                cleaned_q = cls._clean_question_text(current_question_text)
                if len(cleaned_q) > 10: # avoid trivial artifacts
                    marks = current_marks if current_marks is not None else cls._infer_marks(cleaned_q)
                    score, category = cls._calculate_initial_score(cleaned_q, marks)
                    questions.append(
                        QuestionItem(
                            id=str(uuid.uuid4())[:8],
                            subject=subject,
                            unit=current_unit,
                            question=cleaned_q,
                            marks=marks,
                            year=current_year,
                            source=source_filename,
                            difficulty="hard" if marks and marks >= 13 else ("medium" if marks and marks >= 8 else "easy"),
                            importance_score=score,
                            category=category
                        )
                    )
            current_question_text = ""
            current_marks = None
            current_year = None

        for line in lines:
            if not line:
                continue

            # Check if this line is a Unit / Module header
            unit_match = cls.UNIT_PATTERN.match(line)
            if unit_match and len(line) < 80:
                save_current_question()
                unit_num = unit_match.group(1)
                unit_desc = unit_match.group(2)
                current_unit = f"Unit {unit_num}" + (f": {unit_desc.strip()}" if unit_desc else "")
                continue

            # Check if line indicates year header or exam session
            year_match = cls.YEAR_PATTERN.search(line)
            detected_year = int(year_match.group(1)) if year_match else None

            # Check if this line is a new Question start
            q_start_match = cls.QUESTION_START_PATTERN.match(line)
            if q_start_match:
                # Save previous question
                save_current_question()

                content = q_start_match.group(5)
                # Look for marks in this line
                marks_found = cls._extract_marks(line)
                if marks_found:
                    current_marks = marks_found
                if detected_year:
                    current_year = detected_year
                
                current_question_text = content
            else:
                # Could be a continuation of current question, or bullet item
                if current_question_text:
                    marks_found = cls._extract_marks(line)
                    if marks_found and current_marks is None:
                        current_marks = marks_found
                    if detected_year and current_year is None:
                        current_year = detected_year
                    current_question_text += " " + line
                elif len(line) > 20 and any(keyword in line.lower() for keyword in ["explain", "describe", "what is", "compare", "derive", "discuss", "illustrate", "define", "differentiate"]):
                    # Fallback for unnumbered questions
                    marks_found = cls._extract_marks(line)
                    current_marks = marks_found
                    current_year = detected_year
                    current_question_text = line

        # Save last question
        save_current_question()

        # If regex didn't find enough structured questions, perform paragraph-based fallback
        if len(questions) < 2 and len(text.strip()) > 50:
            questions = cls._fallback_extraction(text, subject, source_filename)

        return questions

    @classmethod
    def _extract_marks(cls, text: str) -> Optional[int]:
        # Specific search for explicit mark annotations: [13 Marks], (10M), 13 marks, [15]
        matches = re.findall(r"(?:\[|\()\s*(\d+)\s*(?:marks?|mark|m)?\s*(?:\]|\))", text, re.IGNORECASE)
        if matches:
            try:
                val = int(matches[-1])
                if 1 <= val <= 25:
                    return val
            except ValueError:
                pass
        
        explicit = re.findall(r"\b(\d+)\s*(?:marks?|mark|m)\b", text, re.IGNORECASE)
        if explicit:
            try:
                val = int(explicit[-1])
                if 1 <= val <= 25:
                    return val
            except ValueError:
                pass
        return None

    @classmethod
    def _clean_question_text(cls, text: str) -> str:
        # Strip trailing marks brackets like [13 Marks] or (10M)
        cleaned = re.sub(r"(?:\[|\()\s*(?:(?:\d+\s*\+\s*)*\d+\s*=\s*)?\d+\s*(?:marks?|mark|m)?\s*(?:\]|\))", "", text, flags=re.IGNORECASE)
        # Strip trailing years
        cleaned = re.sub(r"(?:\[|\()\s*(?:May/June|Nov/Dec|Apr/May)?\s*20\d\d\s*(?:\]|\))", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        # Ensure question ends cleanly
        if cleaned and not cleaned.endswith((".", "?", ":")):
            cleaned += "?"
        return cleaned

    @classmethod
    def _infer_marks(cls, question_text: str) -> int:
        q_lower = question_text.lower()
        if any(w in q_lower for w in ["explain architecture", "derive", "detailed working", "design", "elaborate"]):
            return 13
        if any(w in q_lower for w in ["explain", "describe", "discuss", "compare", "differentiate"]):
            return 8
        if any(w in q_lower for w in ["define", "what is", "state", "list", "mention"]):
            return 2
        return 10

    @classmethod
    def _calculate_initial_score(cls, question_text: str, marks: int) -> Tuple[int, str]:
        q_lower = question_text.lower()
        score = 50
        # High marks contribute to importance
        if marks >= 13:
            score += 25
        elif marks >= 8:
            score += 15
        elif marks <= 2:
            score += 5

        # Key exam verbs
        if any(w in q_lower for w in ["architecture", "working", "backpropagation", "cnn", "transformer", "gradient descent", "attention"]):
            score += 20
        elif any(w in q_lower for w in ["compare", "differentiate", "algorithm", "derive"]):
            score += 15

        score = min(score, 98)
        if score >= 80:
            category = "🔥 Must Study"
        elif score >= 65:
            category = "⭐ Should Study"
        else:
            category = "📖 Extra Practice"
        return score, category

    @classmethod
    def _detect_subject(cls, lines: List[str], default_subject: str) -> str:
        for line in lines[:10]:
            lower = line.lower()
            if "deep learning" in lower:
                return "Deep Learning"
            if "machine learning" in lower:
                return "Machine Learning"
            if "database" in lower or "dbms" in lower:
                return "DBMS"
            if "computer networks" in lower or "networks" in lower:
                return "Computer Networks"
            if "operating systems" in lower:
                return "Operating Systems"
        return default_subject

    @classmethod
    def _fallback_extraction(cls, text: str, subject: str, source_filename: str) -> List[QuestionItem]:
        """Fallback to split text by numbered lines or question marks."""
        questions = []
        raw_chunks = re.split(r"\n(?=\d+[\.\)])", text)
        for i, chunk in enumerate(raw_chunks):
            chunk = chunk.strip()
            if len(chunk) > 15:
                marks = cls._extract_marks(chunk) or 10
                cleaned = cls._clean_question_text(chunk)
                score, cat = cls._calculate_initial_score(cleaned, marks)
                questions.append(
                    QuestionItem(
                        id=str(uuid.uuid4())[:8],
                        subject=subject,
                        unit=f"Unit {1 + (i // 4)}",
                        question=cleaned,
                        marks=marks,
                        year=None,
                        source=source_filename,
                        difficulty="medium",
                        importance_score=score,
                        category=cat
                    )
                )
        return questions
