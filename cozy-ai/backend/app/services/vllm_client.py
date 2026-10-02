import json
import logging
import httpx
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional
from app.config import settings
from app.models.schemas import ChatRequest, ChatResponse, StructuredAnswer, VLLMStatusResponse

logger = logging.getLogger(__name__)

class VLLMClient:
    def __init__(self):
        self.base_url = settings.vllm_base_url
        self.model = settings.vllm_model
        self.api_key = settings.vllm_api_key
        self.timeout = settings.vllm_timeout_seconds

    def update_config(self, base_url: str, model: str, api_key: str = "EMPTY"):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key

    async def check_health(self) -> VLLMStatusResponse:
        """Ping the vLLM/Ollama server's /v1/models endpoint."""
        url = f"{self.base_url}/models"
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key and self.api_key != "EMPTY" else {}
        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    data = res.json()
                    models = [m.get("id") for m in data.get("data", [])]
                    active = models[0] if models else self.model
                    return VLLMStatusResponse(
                        status="connected",
                        base_url=self.base_url,
                        active_model=active,
                        available_models=models,
                        message=f"Connected to inference engine ({len(models)} model(s) available)."
                    )
                else:
                    return VLLMStatusResponse(
                        status="offline",
                        base_url=self.base_url,
                        active_model=self.model,
                        available_models=[],
                        message=f"Server responded with HTTP {res.status_code}"
                    )
        except Exception as e:
            return VLLMStatusResponse(
                status="offline",
                base_url=self.base_url,
                active_model=self.model,
                available_models=[],
                message=f"Engine unreachable ({str(e)[:60]}). Cozy.ai running in intelligent demo mode."
            )

    def build_prompt(self, req: ChatRequest) -> Tuple[str, str]:
        """Subject-aware and domain-tuned prompt builder for cozy.ai."""
        marks = req.marks or 10
        style = req.style or "Easy"
        subject = req.subject
        domain = req.domain_mode or ("placement" if "placement" in subject.lower() else "semester")

        # Domain-specific instructions
        domain_guidelines = ""
        if "blockchain" in subject.lower():
            domain_guidelines = (
                "BLOCKCHAIN SPECIALIZATION:\n"
                "- Include an ASCII block diagram or transaction lifecycle flowchart (e.g. Transaction -> Broadcast -> Validation -> Block -> Consensus -> Ledger).\n"
                "- Emphasize cryptographic primitives (SHA-256, Merkle Trees, Nonces, Public-Private Keys).\n"
                "- Provide clear comparison tables for consensus protocols (PoW vs PoS)."
            )
        elif "robotics" in subject.lower():
            domain_guidelines = (
                "ROBOTICS & AUTOMATION SPECIALIZATION:\n"
                "- Explicitly include a 'Draw a Simple Diagram' ASCII section illustrating mechanical schematics (Manipulator, End Effector, Actuator, Sensors, Controller).\n"
                "- For kinematics, provide the mathematical D-H parameter or transformation matrix formulation.\n"
                "- Contrast pneumatic, hydraulic, and electrical actuators."
            )
        elif "mobile" in subject.lower():
            domain_guidelines = (
                "MOBILE APP DEV SPECIALIZATION (Android):\n"
                "- Include Android Activity / Fragment lifecycle state diagram.\n"
                "- Provide clean, idiomatic Java or Kotlin code snippets for UI / SQLite / Intent operations.\n"
                "- Provide a line-by-line explanation of the code snippet."
            )
        elif "java" in subject.lower() or "web" in subject.lower():
            domain_guidelines = (
                "JAVA & WEB PROGRAMMING SPECIALIZATION:\n"
                "- Provide clean, production-quality, runnable Java or Web (HTML/CSS/JS/Servlet) code snippets.\n"
                "- Structure explanation: Concept -> Syntax -> Runnable Code -> Expected Output -> Line-by-line Explanation.\n"
                "- Highlight OOP principles and thread safety where applicable."
            )
        elif "deep learning" in subject.lower() or "predictive" in subject.lower():
            domain_guidelines = (
                "DEEP LEARNING & PREDICTIVE MODELLING SPECIALIZATION:\n"
                "- Include mathematical formulas (activation equations, loss function, gradient update rule).\n"
                "- For 13-mark questions: Definition -> Concept -> Architecture Diagram -> Working -> Example -> Advantages -> Applications -> Exam Keywords.\n"
                "- For numerical or model comparison questions, provide step-by-step calculations."
            )
        elif domain == "placement":
            domain_guidelines = (
                "PLACEMENT TRAINING SPECIALIZATION:\n"
                "- If Aptitude: Provide Step 1 Given Data, Step 2 Core Formula, Step 3 Step-by-step Calculation, Step 4 Quick Shortcut / Time-saving Trick, and Final Answer.\n"
                "- If Coding/DSA: Provide Problem Summary, Optimal Approach, Time & Space Complexity Big-O, Clean Java/Python Solution, Edge Cases.\n"
                "- If Technical Interview: Provide 60-Second Elevator Pitch Answer, Common Follow-up Traps, and Key Gotchas.\n"
                "- If HR Interview: Structure answer strictly using the STAR Method (Situation, Task, Action, Result) with sample winning dialogue."
            )

        marks_guidelines = ""
        if domain == "semester":
            if marks <= 2:
                marks_guidelines = "2 MARKS ANSWER: 2-sentence precise definition + 1 high-yield key point."
            elif marks <= 6:
                marks_guidelines = "5-6 MARKS ANSWER: Definition, clear conceptual explanation, practical example, and 2-3 bullet points."
            else:
                marks_guidelines = (
                    f"{marks} MARKS COMPREHENSIVE EXAM ANSWER: Definition, Concept, Architecture/Diagram, "
                    "Step-by-step Working, Real-world Example, Advantages, Applications, and Exam Keywords."
                )

        system_prompt = (
            f"You are cozy.ai, an expert university exam companion and placement mentor specializing in {subject}.\n"
            "Your answers make complex concepts effortless to understand, perfectly formatted for examiners to award maximum marks.\n"
            "Strictly return output as valid JSON matching the specified schema."
        )

        user_prompt = f"""
DOMAIN: {domain.upper()}
SUBJECT: {subject}
QUESTION: {req.question}
MARKS WEIGHTAGE: {marks} Marks
ANSWER STYLE: {style}
LENGTH PREFERENCE: {req.length}
EXPLAIN SIMPLY MODE: {"Active (include an intuitive beginner analogy)" if req.explain_simply else "Standard"}
STUDENT REQUEST: {req.student_request or "None"}

DOMAIN SPECIFIC GUIDELINES:
{domain_guidelines}

SCORING GUIDANCE:
{marks_guidelines}

Output strictly in valid JSON matching this schema:
{{
  "definition": "Formal, high-scoring exam definition or core problem summary",
  "simple_analogy": "Friendly everyday analogy or intuitive mental model",
  "working_concept": "Detailed conceptual explanation",
  "working_steps": ["Step 1: ...", "Step 2: ..."],
  "diagram_ascii": "ASCII block diagram, workflow, or schematic (especially for Blockchain, Robotics, CNN, Architecture)",
  "code_snippet": "Clean, syntactically correct code (for Java, Android, Solidity, DSA)",
  "code_language": "java/python/solidity/xml",
  "formula_shortcuts": "Key mathematical formulas or aptitude shortcut trick (if applicable)",
  "example": "Concrete real-world application or sample test case",
  "advantages": ["Advantage 1", "Advantage 2"],
  "applications": ["Application 1", "Application 2"],
  "exam_keywords": ["keyword 1", "keyword 2", "keyword 3"],
  "interview_tips": "Interviewer expectations, common trap questions, or STAR advice (for placement)"
}}
"""
        return system_prompt, user_prompt

    async def generate_answer(self, req: ChatRequest) -> ChatResponse:
        """Query Qwen 2.5 / vLLM inference engine, or fall back to high-fidelity demo engine."""
        system_prompt, user_prompt = self.build_prompt(req)
        endpoint = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key and self.api_key != "EMPTY" else ""
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.25,
            "max_tokens": 1800,
            "response_format": {"type": "json_object"}
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                res = await client.post(endpoint, json=payload, headers=headers)
                if res.status_code == 400 and "response_format" in res.text:
                    # Retry without response_format if provider doesn't support json_object parameter
                    payload.pop("response_format", None)
                    res = await client.post(endpoint, json=payload, headers=headers)

                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    structured = self._parse_json_or_text(content, req)
                    return ChatResponse(
                        question=req.question,
                        marks=req.marks or 10,
                        style=req.style or "Easy",
                        answer=structured,
                        model_used=self.model,
                        is_mock=False,
                        timestamp=datetime.now(timezone.utc).isoformat()
                    )
                else:
                    logger.warning(f"Inference provider returned status {res.status_code}: {res.text[:120]}")
        except Exception as e:
            logger.warning(f"vLLM / LLM call failed ({e}). Falling back to cozy.ai mock/demo engine.")

        # Fallback to authentic cozy.ai simulated responses for all 6 subjects
        mock_answer = self._generate_domain_fallback(req)
        return ChatResponse(
            question=req.question,
            marks=req.marks or 10,
            style=req.style or "Easy",
            answer=mock_answer,
            model_used=f"{self.model} (Demo Fallback)",
            is_mock=True,
            timestamp=datetime.now(timezone.utc).isoformat()
        )

    def _parse_json_or_text(self, text: str, req: ChatRequest) -> StructuredAnswer:
        try:
            clean = text.strip()
            if clean.startswith("```json"):
                clean = clean[7:]
            if clean.startswith("```"):
                clean = clean[3:]
            if clean.endswith("```"):
                clean = clean[:-3]
            clean = clean.strip()
            data = json.loads(clean)
            return StructuredAnswer(
                definition=data.get("definition", "Comprehensive exam explanation."),
                simple_analogy=data.get("simple_analogy"),
                working_concept=data.get("working_concept"),
                working_steps=data.get("working_steps", []),
                diagram_ascii=data.get("diagram_ascii"),
                code_snippet=data.get("code_snippet"),
                code_language=data.get("code_language"),
                formula_shortcuts=data.get("formula_shortcuts"),
                example=data.get("example"),
                advantages=data.get("advantages", []),
                applications=data.get("applications", []),
                exam_keywords=data.get("exam_keywords", []),
                interview_tips=data.get("interview_tips"),
                raw_content=text
            )
        except Exception:
            return StructuredAnswer(
                definition="Answer generated by Qwen.",
                working_concept=text,
                raw_content=text
            )

    def _generate_domain_fallback(self, req: ChatRequest) -> StructuredAnswer:
        q_lower = req.question.lower()
        subject_lower = req.subject.lower()

        # 1. BLOCKCHAIN
        if "blockchain" in subject_lower or "proof of" in q_lower or "smart contract" in q_lower or "block" in q_lower:
            return StructuredAnswer(
                definition=(
                    "Blockchain is a decentralized, distributed, and cryptographically secured ledger consisting of chronological "
                    "blocks linked together using cryptographic hashes, ensuring immutability, transparency, and fault tolerance."
                ),
                simple_analogy=(
                    "Think of a shared Google Sheet where hundreds of students have read-only access. When someone adds a new entry, "
                    "everyone's screen must verify and update simultaneously. No single person can delete or tamper with past rows!"
                ),
                working_concept=(
                    "Every block contains a Block Header (Previous Hash, Merkle Root, Timestamp, Nonce) and a Transaction Body. "
                    "Transactions are broadcast to peer nodes, verified, collected into candidates, validated via consensus (PoW/PoS), "
                    "and appended permanently."
                ),
                working_steps=[
                    "1. Transaction Initiation: User signs a transaction using their private key.",
                    "2. P2P Broadcast: Transaction is flooded to network nodes and enters the Mempool.",
                    "3. Block Proposal: Validator/miner groups transactions and constructs a Merkle Tree.",
                    "4. Consensus Check: Network runs consensus (e.g. solving PoW nonce puzzle or PoS validator stake selection).",
                    "5. Ledger Append: The block is linked to the previous block hash and state is finalized."
                ],
                diagram_ascii=(
                    "Transaction Initiated (User Private Key)\n"
                    "         │\n"
                    "         ▼\n"
                    "┌─────────────────┐\n"
                    "│ P2P Broadcast   │ ──► Verified by Network Nodes\n"
                    "└────────┬────────┘\n"
                    "         ▼\n"
                    "┌─────────────────┐\n"
                    "│ Block Creation  │ ──► [Prev Hash | Merkle Root | Nonce]\n"
                    "└────────┬────────┘\n"
                    "         ▼\n"
                    "┌─────────────────┐\n"
                    "│ Consensus       │ ──► Proof of Work / Proof of Stake\n"
                    "└────────┬────────┘\n"
                    "         ▼\n"
                    "Permanent Ledger Entry (Immutable Block Added!)"
                ),
                example="Bitcoin peer-to-peer digital cash transfers and Ethereum ERC-20 decentralized token payments.",
                advantages=[
                    "Immutability: Historical records cannot be altered without rewriting all subsequent blocks.",
                    "Decentralization: Eliminates single points of failure and central authority intermediaries.",
                    "Transparency: Every participant can independently audit the full chain state."
                ],
                applications=[
                    "Cross-border payments & DeFi (Decentralized Finance)",
                    "Supply Chain Provenance & Counterfeit Prevention",
                    "Digital Identity & Verifiable Credentials"
                ],
                exam_keywords=["Distributed Ledger", "Merkle Tree", "SHA-256", "Proof of Work", "Proof of Stake", "Nonce", "Smart Contract", "Byzantine Fault Tolerance"]
            )

        # 2. ROBOTICS & AUTOMATION
        if "robot" in subject_lower or "kinematics" in q_lower or "plc" in q_lower or "actuator" in q_lower:
            return StructuredAnswer(
                definition=(
                    "An Industrial Robot is an automatically controlled, reprogrammable, multipurpose manipulator programmable "
                    "in three or more axes, designed for manufacturing, assembly, material handling, and process automation."
                ),
                simple_analogy=(
                    "Think of a robot like a human arm: joints are the shoulders and elbows (Degrees of Freedom), muscles are actuators "
                    "(motors), nerves are sensors, the hand is the end-effector (gripper), and the brain is the controller computer!"
                ),
                working_concept=(
                    "Robots operate by reading sensor feedback (encoders, vision), computing joint angles via Forward and Inverse Kinematics, "
                    "and delivering current/fluid to actuators to position the end-effector precisely in 3D Cartesian workspace."
                ),
                working_steps=[
                    "Step 1: Motion Planning — Trajectory is calculated from start pose to target coordinates.",
                    "Step 2: Inverse Kinematics — Mathematical transformation converts Cartesian coordinates (X,Y,Z, Roll, Pitch, Yaw) into joint angles (θ1, θ2... θn).",
                    "Step 3: Signal Transmission — Controller sends PWM signals to servo motor driver boards.",
                    "Step 4: Actuation — Electric/hydraulic actuators turn links to commanded angles.",
                    "Step 5: Closed-Loop Feedback — Optical encoders send actual position back to PID controller to eliminate steady-state error."
                ],
                diagram_ascii=(
                    "               [ CONTROLLER / PLC ]\n"
                    "                │              ▲ (Encoder Feedback)\n"
                    "      Control Signal           │\n"
                    "                ▼              │\n"
                    "┌───────────────┐     ┌────────┴──────┐\n"
                    "│ ACTUATORS     │ ──► │ JOINTS & LINKS│ ──► [ END EFFECTOR ]\n"
                    "│ (Motors/Hydr) │     │ (Manipulator) │     (Welder/Gripper)\n"
                    "└───────────────┘     └───────────────┘"
                ),
                example="Automotive assembly lines using 6-DOF KUKA or FANUC articulated robotic arms for robotic spot welding and spray painting.",
                advantages=[
                    "High Repeatability & Precision (down to ±0.02 mm)",
                    "Safety in Hazardous Environments (welding fumes, chemical spraying)",
                    "24/7 Continuous Operation and Increased Production Throughput"
                ],
                applications=[
                    "Automated Pick-and-Place & Packaging",
                    "Semiconductor Wafer Handling",
                    "Surgical Robotics (e.g. da Vinci Surgical System)"
                ],
                exam_keywords=["Degrees of Freedom (DOF)", "Denavit-Hartenberg (D-H)", "Inverse Kinematics", "End Effector", "Actuator", "Closed-Loop PID", "PLC", "SCADA"]
            )

        # 3. MOBILE APP DEVELOPMENT
        if "mobile" in subject_lower or "activity" in q_lower or "intent" in q_lower or "android" in q_lower:
            return StructuredAnswer(
                definition=(
                    "The Android Activity represents a single, focused screen that a user can interact with. The Activity Lifecycle "
                    "is a series of callback states managed by the Android OS as an activity transitions from creation to destruction."
                ),
                simple_analogy=(
                    "Think of an Activity like an actor on a stage: When summoned, they get ready backstage (onCreate), walk onto the stage (onStart), "
                    "start speaking and interacting (onResume). If a phone call interrupts, they pause (onPause), leave the stage (onStop), and take off their costume (onDestroy)."
                ),
                working_concept=(
                    "The OS invokes callback methods to help the app preserve state, release heavy resources (camera, GPS), and recover smoothly without crashing."
                ),
                working_steps=[
                    "1. onCreate(): Called when activity is first initialized; inflate UI layout using setContentView().",
                    "2. onStart(): Activity becomes visible to the user but is not yet interactive.",
                    "3. onResume(): Activity enters the foreground and starts receiving user touch inputs.",
                    "4. onPause(): Another activity enters foreground; pause animations and save transient data.",
                    "5. onStop(): Activity is no longer visible; release memory-intensive hardware resources.",
                    "6. onDestroy(): Final call before activity is terminated or device orientation changes."
                ],
                diagram_ascii=(
                    "      [ App Launched ]\n"
                    "             │\n"
                    "             ▼\n"
                    "        onCreate() ──► UI Layout Inflated\n"
                    "             │\n"
                    "             ▼\n"
                    "        onStart()  ──► Activity Visible\n"
                    "             │\n"
                    "             ▼\n"
                    "        onResume() ──► [ Running / User Interacting ]\n"
                    "             │              ▲\n"
                    "             ▼ (Interruption)│ (Return to App)\n"
                    "        onPause()  ─────────┘\n"
                    "             │\n"
                    "             ▼ (App Minimized)\n"
                    "        onStop()\n"
                    "             │\n"
                    "             ▼ (App Killed)\n"
                    "        onDestroy() ──► Process Finished"
                ),
                code_snippet=(
                    "public class MainActivity extends AppCompatActivity {\n"
                    "    @Override\n"
                    "    protected void onCreate(Bundle savedInstanceState) {\n"
                    "        super.onCreate(savedInstanceState);\n"
                    "        setContentView(R.layout.activity_main);\n"
                    "    }\n"
                    "    @Override\n"
                    "    protected void onPause() {\n"
                    "        super.onPause();\n"
                    "        // Release camera or save draft\n"
                    "    }\n"
                    "}"
                ),
                code_language="java",
                example="Handling phone call interruptions gracefully while a user is typing a message in WhatsApp.",
                advantages=[
                    "Prevents Battery Drain: Suspends heavy background polling when app is minimized.",
                    "Zero State Loss: Preserves form inputs across screen rotations and app switching.",
                    "Optimized Memory Management: OS can safely kill stopped background processes."
                ],
                applications=["All modern native Android mobile applications on Google Play Store."],
                exam_keywords=["Activity Lifecycle", "Bundle", "onCreate", "onResume", "onPause", "onDestroy", "Backstack", "Fragment", "Intent"]
            )

        # 4. JAVA & WEB PROGRAMMING
        if "java" in subject_lower or "servlet" in subject_lower or "oop" in q_lower or "web" in subject_lower:
            return StructuredAnswer(
                definition=(
                    "Object-Oriented Programming (OOP) in Java is a programming paradigm based on the concept of 'objects', "
                    "which contain data (attributes) and code (methods). It is founded on four pillars: Encapsulation, Inheritance, Polymorphism, and Abstraction."
                ),
                simple_analogy=(
                    "Think of a car: Abstraction hides the internal engine mechanics behind simple steering and pedals. "
                    "Encapsulation locks gears and fuel tanks inside the chassis. Inheritance lets an ElectricCar inherit wheels and seats from Car. "
                    "Polymorphism lets the brake pedal work differently on a bicycle vs an airplane!"
                ),
                working_concept=(
                    "Java enforces clean modular architecture through class hierarchies, access specifiers (private, protected, public), "
                    "interfaces, and method overriding."
                ),
                working_steps=[
                    "1. Encapsulation: Binding data members with getter/setter methods to prevent direct modification.",
                    "2. Inheritance: Code reuse using the 'extends' keyword allowing subclasses to inherit superclass methods.",
                    "3. Polymorphism: Method Overloading (Compile-time) and Method Overriding (Runtime via dynamic method dispatch).",
                    "4. Abstraction: Hiding implementation details using 'abstract class' and 'interface'."
                ],
                code_snippet=(
                    "// Core Java OOP Demonstration\n"
                    "abstract class Vehicle {\n"
                    "    private String brand; // Encapsulation\n"
                    "    public Vehicle(String b) { this.brand = b; }\n"
                    "    public String getBrand() { return brand; }\n"
                    "    abstract void start(); // Abstraction\n"
                    "}\n"
                    "\n"
                    "class Car extends Vehicle { // Inheritance\n"
                    "    public Car(String b) { super(b); }\n"
                    "    @Override\n"
                    "    void start() { // Polymorphism\n"
                    "        System.out.println(getBrand() + \" car engine ignited smoothly!\");\n"
                    "    }\n"
                    "}\n"
                    "\n"
                    "public class OOPDemo {\n"
                    "    public static void main(String[] args) {\n"
                    "        Vehicle v = new Car(\"Tesla\");\n"
                    "        v.start();\n"
                    "    }\n"
                    "}"
                ),
                code_language="java",
                diagram_ascii=(
                    "        ┌─────────────────────────┐\n"
                    "        │  Vehicle (Abstract)     │\n"
                    "        │  - brand: String        │\n"
                    "        │  + start(): abstract    │\n"
                    "        └───────────┬─────────────┘\n"
                    "                    ▲ (extends)\n"
                    "                    │\n"
                    "        ┌───────────┴─────────────┐\n"
                    "        │  Car (Concrete)         │\n"
                    "        │  + start(): override    │\n"
                    "        └─────────────────────────┘"
                ),
                example="Designing enterprise banking systems where Account is an abstract base, and SavingsAccount/CheckingAccount inherit customized interest calculation rules.",
                advantages=["Modular Code Maintenance", "Extensibility & Scalability", "Robust Security via Encapsulation", "High Reusability"],
                applications=["Enterprise Spring Boot Backend Systems", "Android Native Apps", "Big Data Pipelines (Apache Spark)"],
                exam_keywords=["Encapsulation", "Inheritance", "Polymorphism", "Abstraction", "Dynamic Method Dispatch", "Interface", "Access Specifiers"]
            )

        # 5. PLACEMENT TRAINING
        if "placement" in subject_lower or "aptitude" in q_lower or "interview" in q_lower or "dsa" in q_lower or "two dice" in q_lower or "probability" in q_lower:
            return StructuredAnswer(
                definition=(
                    "In a two-dice throw experiment, the sample space consists of 6 x 6 = 36 equally likely outcomes. "
                    "A prime number sum is any outcome where the sum belongs to {2, 3, 5, 7, 11}."
                ),
                simple_analogy=(
                    "Think of every dice combination as a square on a 6x6 grid. We just count which squares add up to a prime number!"
                ),
                working_concept=(
                    "Total Outcomes n(S) = 36. Favorable outcomes n(E) for each prime sum:\n"
                    "• Sum = 2: (1,1) -> 1 pair\n"
                    "• Sum = 3: (1,2), (2,1) -> 2 pairs\n"
                    "• Sum = 5: (1,4), (2,3), (3,2), (4,1) -> 4 pairs\n"
                    "• Sum = 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) -> 6 pairs\n"
                    "• Sum = 11: (5,6), (6,5) -> 2 pairs"
                ),
                working_steps=[
                    "Step 1: Total favorable cases n(E) = 1 + 2 + 4 + 6 + 2 = 15.",
                    "Step 2: Total sample space n(S) = 36.",
                    "Step 3: Probability P(E) = n(E) / n(S) = 15 / 36.",
                    "Step 4: Reduce fraction by dividing numerator and denominator by 3: 15/3 = 5, 36/3 = 12.",
                    "Step 5: Final Result: P = 5/12 ≈ 41.67%."
                ],
                formula_shortcuts=(
                    "🔥 EXAM SHORTCUT:\n"
                    "For two dice sums (2 through 12), the number of ways forms a symmetric triangle:\n"
                    "Sum:   2  3  4  5  6  7  8  9 10 11 12\n"
                    "Ways:  1  2  3  4  5  6  5  4  3  2  1\n"
                    "Directly sum primes {2, 3, 5, 7, 11}: 1 + 2 + 4 + 6 + 2 = 15 ways!\n"
                    "Answer: 15/36 = 5/12 in 5 seconds!"
                ),
                example="Standard screening question in TCS NQT, Infosys, Cognizant, and Wipro campus placement rounds.",
                advantages=["Guaranteed full marks with standard reduction steps.", "Shortcut saves 2 minutes in aptitude timer tests."],
                applications=["Campus placement aptitude screenings", "GATE & Competitive entrance exams"],
                exam_keywords=["Sample Space n(S)", "Favorable Outcomes n(E)", "Prime Sums", "Symmetric Dice Triangle", "P = 5/12"],
                interview_tips="During interviews, state the total outcomes (36) first, then list the prime sums methodically to show structured thinking."
            )

        # Fallback to Deep Learning
        return StructuredAnswer(
            definition=f"{req.question.rstrip('?')} is a critical concept in {req.subject}.",
            simple_analogy="Think of this concept like an automated traffic control system directing complex flow with structured rules.",
            working_concept=f"The underlying algorithm in {req.subject} guarantees efficient convergence and stability.",
            working_steps=[
                f"1. Initialization: Establish parameters and baseline state in {req.subject}.",
                "2. Transformation: Apply mathematical operations or logical state transitions.",
                "3. Optimization: Measure error or throughput and adapt internal variables.",
                "4. Evaluation: Validate against benchmark datasets to guarantee accuracy."
            ],
            example=f"Deploying this in production systems for {req.subject}.",
            advantages=["High computational efficiency", "Standardized across academic syllabi", "Robust error tolerance"],
            applications=[f"University exams and practical implementations in {req.subject}."],
            exam_keywords=["Algorithmic Formulation", "Optimization", "Convergence", "Standard Convention"]
        )

vllm_client = VLLMClient()
