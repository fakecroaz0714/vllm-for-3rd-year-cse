from typing import List, Dict, Any
from app.models.schemas import QuestionItem

# Comprehensive Subject Taxonomy & Seed Questions for cozy.ai
SUBJECTS_CONFIG = {
    "deep_learning": {
        "id": "deep_learning",
        "name": "Deep Learning & Predictive Modelling",
        "icon": "🧠",
        "category": "semester",
        "code": "CS8083",
        "tagline": "Neural networks, optimization, loss functions, and ML classification algorithms.",
        "topics": [
            "Neural Networks", "CNN Architecture", "Backpropagation", "RNN & LSTM", 
            "Optimization & Gradient Descent", "Activation Functions", "Transformers",
            "Regression", "Random Forest", "SVM", "Feature Engineering", "Ensemble Methods"
        ],
        "default_marks": 13,
        "sample_questions": [
            {
                "id": "dl_01",
                "question": "Explain the architecture of Convolutional Neural Networks (CNN) with convolution, pooling, and classification layers.",
                "unit": "Unit II: CNN Architecture",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 96,
                "evidence": "Appears in 5 recent semester papers"
            },
            {
                "id": "dl_02",
                "question": "Explain the Backpropagation algorithm with mathematical formulation and the Chain Rule of calculus.",
                "unit": "Unit I: Neural Fundamentals",
                "marks": 13,
                "year": 2024,
                "category": "🔥 Must Study",
                "importance_score": 93,
                "evidence": "High weightage core theoretical question"
            },
            {
                "id": "dl_03",
                "question": "Compare Stochastic Gradient Descent (SGD), Momentum, and Adam optimizer with equations and convergence rates.",
                "unit": "Unit I: Optimization",
                "marks": 10,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 85,
                "evidence": "Frequently asked 10-mark comparison"
            },
            {
                "id": "dl_04",
                "question": "What is the vanishing gradient problem? How do ReLU activation and Residual Skip Connections mitigate it?",
                "unit": "Unit I: Activation & Loss",
                "marks": 5,
                "year": 2025,
                "category": "⭐ Should Study",
                "importance_score": 78,
                "evidence": "Standard 5-mark conceptual question"
            },
            {
                "id": "dl_05",
                "question": "Differentiate between Random Forest and Gradient Boosting (XGBoost) in Predictive Modelling.",
                "unit": "Unit IV: Ensemble Methods",
                "marks": 8,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 82,
                "evidence": "Core predictive modelling topic"
            }
        ]
    },
    "blockchain": {
        "id": "blockchain",
        "name": "Blockchain & Technology",
        "icon": "⛓️",
        "category": "semester",
        "code": "CS8084",
        "tagline": "Decentralized ledgers, consensus protocols, cryptography, and smart contracts.",
        "topics": [
            "Blockchain Fundamentals", "Distributed Ledger Technology", "SHA-256 & Cryptography",
            "Consensus: PoW vs PoS", "Bitcoin Architecture", "Ethereum & EVM", "Smart Contracts",
            "Hyperledger Fabric", "Merkle Trees", "Wallets & Transactions"
        ],
        "default_marks": 13,
        "sample_questions": [
            {
                "id": "bc_01",
                "question": "Explain the architecture of a Blockchain block, including Block Header, Nonce, Merkle Root, and Hash linking with a neat diagram.",
                "unit": "Unit I: Blockchain Architecture",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 95,
                "evidence": "Essential fundamental question with diagram"
            },
            {
                "id": "bc_02",
                "question": "Compare Proof of Work (PoW) and Proof of Stake (PoS) consensus mechanisms in terms of security, energy consumption, and 51% attack resistance.",
                "unit": "Unit II: Consensus Algorithms",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 94,
                "evidence": "Appears in every previous university exam"
            },
            {
                "id": "bc_03",
                "question": "Describe the lifecycle of a Blockchain Transaction from initiation and broadcasting to mining and ledger confirmation.",
                "unit": "Unit II: Transactions & Mining",
                "marks": 10,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 86,
                "evidence": "Key transaction flow sequence"
            },
            {
                "id": "bc_04",
                "question": "Explain Smart Contracts on Ethereum, the role of Gas, and write a simple Solidity contract for a decentralized token transfer.",
                "unit": "Unit III: Smart Contracts & EVM",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 90,
                "evidence": "High weightage programming + theory question"
            },
            {
                "id": "bc_05",
                "question": "What is a Merkle Tree? Explain how it provides cryptographic verification of transactions in O(log N) time.",
                "unit": "Unit I: Cryptographic Primitives",
                "marks": 5,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 79,
                "evidence": "Core 5-mark short answer"
            }
        ]
    },
    "robotics": {
        "id": "robotics",
        "name": "Robotics & Automation",
        "icon": "🤖",
        "category": "semester",
        "code": "CS8085",
        "tagline": "Kinematics, sensors, actuators, control systems, PLC, SCADA, and industrial automation.",
        "topics": [
            "Robot Anatomy & Degrees of Freedom", "Sensors & Actuators", "End Effectors",
            "Forward Kinematics (DH Parameters)", "Inverse Kinematics", "Motion Planning",
            "Industrial Robots", "PLC Programming", "SCADA Architecture", "Feedback Control Systems"
        ],
        "default_marks": 13,
        "sample_questions": [
            {
                "id": "rob_01",
                "question": "Explain the major components of an Industrial Robot (Manipulator, End Effector, Actuator, Sensors, Controller) with a schematic diagram.",
                "unit": "Unit I: Robot Anatomy & Classification",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 95,
                "evidence": "Foundational diagram-based question"
            },
            {
                "id": "rob_02",
                "question": "Derive Forward Kinematics using Denavit-Hartenberg (D-H) parameter representation for a 2-DOF planar robotic arm.",
                "unit": "Unit II: Robot Kinematics",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 92,
                "evidence": "High priority mathematical derivation"
            },
            {
                "id": "rob_03",
                "question": "Differentiate between Forward Kinematics and Inverse Kinematics. Why is Inverse Kinematics more challenging to solve?",
                "unit": "Unit II: Kinematics",
                "marks": 8,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 84,
                "evidence": "Frequent comparison question"
            },
            {
                "id": "rob_04",
                "question": "Explain Programmable Logic Controllers (PLC) architecture and how ladder logic diagrams are used in industrial automation.",
                "unit": "Unit IV: Industrial Automation & PLC",
                "marks": 10,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 88,
                "evidence": "Core automation syllabus module"
            },
            {
                "id": "rob_05",
                "question": "Compare pneumatic, hydraulic, and electrical actuators used in robotics with respect to payload, speed, and precision.",
                "unit": "Unit I: Actuators",
                "marks": 5,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 76,
                "evidence": "Standard 5-mark tabular comparison"
            }
        ]
    },
    "mobile_dev": {
        "id": "mobile_dev",
        "name": "Mobile App Development",
        "icon": "📱",
        "category": "semester",
        "code": "CS8086",
        "tagline": "Android architecture, activities, fragments, intents, UI layouts, SQLite, and REST APIs.",
        "topics": [
            "Android OS Architecture", "Activity Lifecycle", "Fragments & Backstack",
            "Explicit & Implicit Intents", "UI Layouts (Constraint, Linear, Relative)",
            "SQLite & Room Database", "RecyclerView & Adapters", "REST APIs & Retrofit",
            "Broadcast Receivers & Services", "Firebase Integration"
        ],
        "default_marks": 13,
        "sample_questions": [
            {
                "id": "mob_01",
                "question": "Explain the complete Android Activity Lifecycle with states (onCreate, onStart, onResume, onPause, onStop, onDestroy) and state diagram.",
                "unit": "Unit I: Android Fundamentals",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 97,
                "evidence": "Guaranteed core exam question"
            },
            {
                "id": "mob_02",
                "question": "Explain Explicit and Implicit Intents in Android with code examples demonstrating data passing via Bundles.",
                "unit": "Unit II: Components & Intents",
                "marks": 10,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 89,
                "evidence": "High weightage code + theory question"
            },
            {
                "id": "mob_03",
                "question": "Explain how to implement SQLite database operations (CRUD) in an Android application using SQLiteOpenHelper with Java/Kotlin code.",
                "unit": "Unit III: Local Data Storage",
                "marks": 13,
                "year": 2024,
                "category": "🔥 Must Study",
                "importance_score": 91,
                "evidence": "Frequent 13-mark implementation question"
            },
            {
                "id": "mob_04",
                "question": "Differentiate between an Activity and a Fragment. Explain how Fragments communicate with host Activities.",
                "unit": "Unit II: UI & Fragments",
                "marks": 8,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 82,
                "evidence": "Essential architectural concept"
            },
            {
                "id": "mob_05",
                "question": "Compare ConstraintLayout with LinearLayout and RelativeLayout. Why is ConstraintLayout preferred for complex nested UIs?",
                "unit": "Unit II: UI Layouts",
                "marks": 5,
                "year": 2025,
                "category": "⭐ Should Study",
                "importance_score": 75,
                "evidence": "Standard 5-mark UI question"
            }
        ]
    },
    "java_web": {
        "id": "java_web",
        "name": "Java & Web Programming",
        "icon": "☕",
        "category": "semester",
        "code": "CS8087",
        "tagline": "OOP, Collections, Multithreading, JDBC, Servlets, JSP, REST APIs, and modern Web architecture.",
        "topics": [
            "OOP Principles in Java", "Exception Handling", "Java Collections Framework",
            "Multithreading & Synchronization", "JDBC Database Connectivity",
            "Servlets Lifecycle & Sessions", "JSP & Custom Tags", "RESTful Web Services",
            "HTML5, CSS3, DOM & JavaScript", "HTTP Protocol & Cookies"
        ],
        "default_marks": 13,
        "sample_questions": [
            {
                "id": "jw_01",
                "question": "Explain the four core principles of Object-Oriented Programming (Encapsulation, Inheritance, Polymorphism, Abstraction) with Java code examples.",
                "unit": "Unit I: Core Java OOP",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 96,
                "evidence": "Cornerstone Java semester topic"
            },
            {
                "id": "jw_02",
                "question": "Explain the Servlet Lifecycle (init, service, destroy) and write a Java Servlet that handles HTTP GET and POST requests.",
                "unit": "Unit III: Servlets & Server-Side Web",
                "marks": 13,
                "year": 2025,
                "category": "🔥 Must Study",
                "importance_score": 94,
                "evidence": "Core web programming question"
            },
            {
                "id": "jw_03",
                "question": "Explain Multithreading in Java. Differentiate between extending Thread class and implementing Runnable interface with synchronization code.",
                "unit": "Unit II: Advanced Java",
                "marks": 10,
                "year": 2024,
                "category": "⭐ Should Study",
                "importance_score": 87,
                "evidence": "High frequency multithreading question"
            },
            {
                "id": "jw_04",
                "question": "Explain JDBC architecture and write step-by-step Java code to establish a database connection and execute a PreparedStatement.",
                "unit": "Unit II: Database Connectivity",
                "marks": 10,
                "year": 2024,
                "category": "🔥 Must Study",
                "importance_score": 90,
                "evidence": "Essential JDBC implementation"
            },
            {
                "id": "jw_05",
                "question": "Compare Session tracking mechanisms in web applications: Cookies, HttpSession, URL Rewriting, and Hidden Form Fields.",
                "unit": "Unit IV: Session Management",
                "marks": 8,
                "year": 2025,
                "category": "⭐ Should Study",
                "importance_score": 81,
                "evidence": "Standard session tracking question"
            }
        ]
    },
    "placement": {
        "id": "placement",
        "name": "Placement Training",
        "icon": "🎯",
        "category": "placement",
        "code": "CAREER2025",
        "tagline": "Quantitative Aptitude, Logical Reasoning, DSA Coding in Java/Python, Technical & HR Interviews.",
        "subcategories": {
            "aptitude": {
                "name": "Quantitative & Logical Aptitude",
                "topics": ["Probability", "Time & Work", "Profit & Loss", "Percentages", "Number Systems", "Blood Relations", "Puzzles", "Seating Arrangement"]
            },
            "coding": {
                "name": "Coding & Data Structures (DSA)",
                "topics": ["Arrays & Two Pointers", "Strings & Hashing", "Linked Lists", "Stacks & Queues", "Binary Trees & BST", "Graphs & BFS/DFS", "Dynamic Programming"]
            },
            "technical": {
                "name": "Technical Interview (Core CS)",
                "topics": ["Java Core & Collections", "SQL & DBMS Normalization", "OS (Deadlocks & Paging)", "Computer Networks (TCP/IP & DNS)", "System Design Basics"]
            },
            "hr": {
                "name": "HR & Behavioral Interview",
                "topics": ["Tell me about yourself", "Strengths & Weaknesses", "STAR Method Situations", "Handling Conflict", "Why should we hire you?"]
            }
        },
        "default_marks": 10,
        "sample_questions": [
            {
                "id": "place_01",
                "question": "Two dice are rolled simultaneously. What is the probability that the sum of the numbers appearing on the two dice is a prime number? Solve with step-by-step formula and shortcut.",
                "unit": "Aptitude: Probability",
                "marks": 5,
                "category": "🔥 High Yield",
                "importance_score": 98,
                "topic": "Probability",
                "evidence": "TCS, Infosys, Cognizant frequent aptitude pattern"
            },
            {
                "id": "place_02",
                "question": "A can complete a piece of work in 12 days, and B can complete it in 18 days. If they work together for 4 days, what fraction of work is left?",
                "unit": "Aptitude: Time & Work",
                "marks": 5,
                "category": "🔥 High Yield",
                "importance_score": 96,
                "topic": "Time & Work",
                "evidence": "Top-tier aptitude screening question"
            },
            {
                "id": "place_03",
                "question": "Find the Longest Substring Without Repeating Characters in a given string. Provide optimal sliding window approach in Java/Python with O(N) time and O(min(N, M)) space complexity.",
                "unit": "Coding (DSA): Two Pointers & Hashing",
                "marks": 10,
                "category": "🔥 High Yield",
                "importance_score": 99,
                "topic": "Strings & Hashing",
                "evidence": "Amazon, Microsoft, Service-based company coding rounds"
            },
            {
                "id": "place_04",
                "question": "How does Java HashMap handle collisions internally? Explain Java 8 transition from LinkedList to Red-Black Tree when threshold reaches 8 (TREEIFY_THRESHOLD).",
                "unit": "Technical Interview: Java Collections",
                "marks": 10,
                "category": "🔥 High Yield",
                "importance_score": 98,
                "topic": "Java Core",
                "evidence": "Rank #1 asked Java technical interview question"
            },
            {
                "id": "place_05",
                "question": "Answer the HR question: 'Describe a time when you faced a major challenge in a project and how you overcame it.' Use the STAR method (Situation, Task, Action, Result).",
                "unit": "HR Interview: Behavioral",
                "marks": 10,
                "category": "🔥 High Yield",
                "importance_score": 95,
                "topic": "STAR Method",
                "evidence": "Standard behavioral interview question across all companies"
            }
        ]
    }
}

class SubjectRegistry:
    @classmethod
    def get_all_subjects(cls) -> List[Dict[str, Any]]:
        results = []
        for k, v in SUBJECTS_CONFIG.items():
            sample_qs = v.get("sample_questions")
            q_count = len(sample_qs) if isinstance(sample_qs, list) else 0
            topics_val = v.get("topics")
            if isinstance(topics_val, list):
                topics = topics_val
            elif isinstance(v.get("subcategories"), dict):
                subcats = v.get("subcategories")
                topics = list(subcats.keys()) if isinstance(subcats, dict) else []
            else:
                topics = []
            results.append({
                "id": str(k),
                "name": str(v.get("name", "")),
                "icon": str(v.get("icon", "")),
                "category": str(v.get("category", "")),
                "code": str(v.get("code", "")),
                "tagline": str(v.get("tagline", "")),
                "question_count": q_count,
                "topics": topics
            })
        return results

    @classmethod
    def get_subject_by_id(cls, subject_id: str) -> Dict[str, Any]:
        return SUBJECTS_CONFIG.get(subject_id, SUBJECTS_CONFIG["deep_learning"])

    @classmethod
    def get_questions_for_subject(cls, subject_id: str) -> List[QuestionItem]:
        subj = cls.get_subject_by_id(subject_id)
        raw_list = subj.get("sample_questions", [])
        return [
            QuestionItem(
                id=q["id"],
                subject=subj["name"],
                unit=q.get("unit", "General"),
                question=q["question"],
                marks=q.get("marks", 10),
                year=q.get("year", 2025),
                source=f"{subj['name']} Syllabus Bank",
                difficulty="hard" if q.get("marks", 10) >= 13 else "medium",
                importance_score=q.get("importance_score", 85),
                category=q.get("category", "🔥 Must Study")
            )
            for q in raw_list
        ]
