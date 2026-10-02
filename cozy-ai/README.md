# ☁️ cozy.ai — Final Subject Architecture

> **"One Qwen Model — Domain-Focused Semester & Placement Companion"**

**cozy.ai** is an exam preparation and career placement platform tailored for university students. It structures answers with definitions, intuitive analogies, step-by-step working, ASCII architecture diagrams, runnable code, and exam keywords powered by **Qwen 2.5 (7B / 14B)** on Apple Silicon M4.

---

## 🏛️ The 6 First-Class Modules

### 📚 Semester Subjects (5 Modules)

1. **🧠 Deep Learning & Predictive Modelling (`CS8083`)**
   - **Topics**: CNN, Backpropagation, RNN, LSTM, GRU, Gradient Descent, Loss/Activation Functions, Transformers; Regression, Classification, Random Forest, SVM, Ensemble Methods.
   - **Exam Format**: Mathematical formulation, loss curves, architecture diagrams, step-by-step calculations for 13-mark questions.

2. **⛓️ Blockchain & Technology (`CS8084`)**
   - **Topics**: Distributed Ledgers, SHA-256, Merkle Trees, Proof of Work vs Proof of Stake, Smart Contracts, Ethereum EVM, Hyperledger, Wallets.
   - **Exam Format**: Heavy on transaction lifecycle ASCII diagrams (`Transaction -> Broadcast -> Validation -> Block -> Consensus -> Ledger`).

3. **🤖 Robotics & Automation (`CS8085`)**
   - **Topics**: Robot Anatomy, Degrees of Freedom (DOF), Forward/Inverse Kinematics (D-H parameters), Sensors & Actuators, Motion Planning, PLC Ladder Logic, SCADA.
   - **Exam Format**: *"Draw a simple diagram"* schematics, D-H matrix formulations, and actuator comparisons.

4. **📱 Mobile App Development (`CS8086`)**
   - **Topics**: Android Architecture, Activity/Fragment Lifecycle, Explicit & Implicit Intents, UI Layouts (Constraint/Linear), SQLite & Room, REST APIs.
   - **Exam Format**: Lifecycle state diagrams, clean Java/Kotlin code snippets, and line-by-line code explanations.

5. **☕ Java & Web Programming (`CS8087`)**
   - **Topics**: OOP (Encapsulation, Inheritance, Polymorphism, Abstraction), Collections, Multithreading, JDBC, Servlets, JSP, REST APIs, HTML5/CSS/JavaScript.
   - **Exam Format**: Complete runnable code snippets with simulated **▶️ Run Code** preview and OOP architecture breakdowns.

---

### 🎯 Placement Training (Career Module)

6. **🎯 Placement Training (`CAREER2025`)**
   - **🧮 Quantitative Aptitude**: Probability, Time & Work, Profit & Loss, Percentages, Number Systems, Ratios. Features **Formula & Shortcut Tricks**.
   - **🧩 Logical Reasoning**: Blood Relations, Seating Arrangements, Puzzles, Coding-Decoding.
   - **💻 Coding & DSA**: Two Pointers, Sliding Window, Linked Lists, Trees, Graphs, DP. Features **Optimal Time & Space Big-O Complexities**.
   - **💼 Technical Interview**: Java Collections internals (HashMap collision treeify), SQL Normalization, OS Deadlocks, Networking handshakes. Features **60-Second Elevator Pitch & Traps**.
   - **🤝 HR & Behavioral**: Structured answers using the **STAR Method** (Situation, Task, Action, Result).

---

## 🚀 How to Run

1. **Start the local Qwen engine** (if not already running in background):
   ```bash
   ~/.local/bin/ollama serve
   ```
2. **Start cozy.ai**:
   ```bash
   cd cozy-ai
   .venv/bin/python start_server.py
   ```
3. Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** in your browser!

---

## 🧪 Run Unit Tests

```bash
cd cozy-ai
.venv/bin/python -m pytest tests/ -v
```
