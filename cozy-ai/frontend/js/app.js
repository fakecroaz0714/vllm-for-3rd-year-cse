import {
  fetchSubjects,
  loadSubjectDefaultBank,
  uploadQuestionBank,
  generateExamAnswer,
  generatePlacementPractice,
  getVLLMStatus,
  updateVLLMConfig
} from "./api.js";

// Global Application State
const state = {
  currentMode: "semester", // "semester" or "placement"
  activeSubjectId: "deep_learning",
  activeSubject: null,
  subjects: [],
  questions: [],
  selectedCategory: "all",
  activeQuestion: null,
  activeMarks: 13,
  activeStyle: "Easy",
  activeLength: "Standard",
  explainSimply: true,
  isGenerating: false,
  vllmStatus: { status: "connected", active_model: "qwen2.5:7b" },

  // Placement state
  activePlacementTrack: "aptitude",
  placementQuestions: []
};

// DOM Elements
const brandHomeBtn = document.getElementById("brandHomeBtn");
const modeSemesterBtn = document.getElementById("modeSemesterBtn");
const modePlacementBtn = document.getElementById("modePlacementBtn");

const semesterHubView = document.getElementById("semesterHubView");
const subjectStudioView = document.getElementById("subjectStudioView");
const placementHubView = document.getElementById("placementHubView");

const subjectCardsGrid = document.getElementById("subjectCardsGrid");
const hubQuickStudyBtn = document.getElementById("hubQuickStudyBtn");

const backToHubBtn = document.getElementById("backToHubBtn");
const activeSubjectIcon = document.getElementById("activeSubjectIcon");
const activeSubjectTitle = document.getElementById("activeSubjectTitle");
const activeSubjectCode = document.getElementById("activeSubjectCode");
const studioResetBankBtn = document.getElementById("studioResetBankBtn");

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const questionsContainer = document.getElementById("questionsContainer");
const questionCountBadge = document.getElementById("questionCountBadge");
const filterPills = document.querySelectorAll(".filter-pill");

const questionInput = document.getElementById("questionInput");
const generateBtn = document.getElementById("generateBtn");
const marksButtons = document.querySelectorAll(".marks-btn");
const styleButtons = document.querySelectorAll(".style-btn");
const explainSimplyCheckbox = document.getElementById("explainSimplyCheckbox");

const answerCard = document.getElementById("answerCard");
const answerPlaceholder = document.getElementById("answerPlaceholder");

// Placement elements
const placementTracksBar = document.getElementById("placementTracksBar");
const placementTopicPills = document.getElementById("placementTopicPills");
const placementQuestionsContainer = document.getElementById("placementQuestionsContainer");
const placementCountBadge = document.getElementById("placementCountBadge");
const placementAnswerCard = document.getElementById("placementAnswerCard");

// Settings & Badges
const vllmBadge = document.getElementById("vllmBadge");
const vllmStatusText = document.getElementById("vllmStatusText");
const settingsBtn = document.getElementById("settingsBtn");
const settingsModal = document.getElementById("settingsModal");
const closeModalBtn = document.getElementById("closeModalBtn");
const saveSettingsBtn = document.getElementById("saveSettingsBtn");
const testVllmBtn = document.getElementById("testVllmBtn");
const vllmUrlInput = document.getElementById("vllmUrlInput");
const vllmModelInput = document.getElementById("vllmModelInput");
const vllmApiKeyInput = document.getElementById("vllmApiKeyInput");
const presetVllm = document.getElementById("presetVllm");
const presetOllama = document.getElementById("presetOllama");
const presetGroq = document.getElementById("presetGroq");
const vllmTestFeedback = document.getElementById("vllmTestFeedback");
const toast = document.getElementById("toast");

// Toast helper
function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 3200);
}

// Switch between Views
function switchView(viewName) {
  semesterHubView.classList.remove("active");
  subjectStudioView.classList.remove("active");
  placementHubView.classList.remove("active");

  if (viewName === "semester_hub") {
    semesterHubView.classList.add("active");
    modeSemesterBtn.classList.add("active");
    modePlacementBtn.classList.remove("active");
    state.currentMode = "semester";
  } else if (viewName === "subject_studio") {
    subjectStudioView.classList.add("active");
    modeSemesterBtn.classList.add("active");
    modePlacementBtn.classList.remove("active");
    state.currentMode = "semester";
  } else if (viewName === "placement_hub") {
    placementHubView.classList.add("active");
    modePlacementBtn.classList.add("active");
    modeSemesterBtn.classList.remove("active");
    state.currentMode = "placement";
    renderPlacementTrack();
  }
}

// Refresh Model / Engine Status
async function refreshStatus() {
  try {
    const data = await getVLLMStatus();
    state.vllmStatus = data;
    if (data.status === "connected") {
      vllmBadge.className = "vllm-badge connected";
      const modelShort = (data.active_model || "").split("/").pop();
      vllmStatusText.textContent = `🟢 ${modelShort || "Qwen Online"}`;
    } else {
      vllmBadge.className = "vllm-badge demo";
      vllmStatusText.textContent = "🟡 Demo Mode (Offline)";
    }
  } catch (err) {
    vllmBadge.className = "vllm-badge demo";
    vllmStatusText.textContent = "🟡 Demo Mode";
  }
}

// Render Semester 5 Subjects Cards
function renderSubjectCards() {
  const semesterSubjects = state.subjects.filter(s => s.category === "semester");
  subjectCardsGrid.innerHTML = semesterSubjects.map(s => `
    <div class="subject-card" data-id="${s.id}">
      <div>
        <div class="subject-card-header">
          <div class="subject-icon-box">${s.icon}</div>
          <span class="subject-code-tag">${s.code}</span>
        </div>
        <h3 class="subject-name">${s.name}</h3>
        <p class="subject-tagline">${s.tagline}</p>
        <div class="subject-topics-cloud">
          ${(s.topics || []).slice(0, 5).map(t => `<span class="topic-chip">${t}</span>`).join('')}
        </div>
      </div>
      <div class="subject-card-footer">
        <span class="subject-qcount">🔥 ${s.question_count} High Priority Qs</span>
        <button class="btn btn-secondary" style="padding: 6px 14px; font-size: 12px;">Open Studio ➤</button>
      </div>
    </div>
  `).join("");

  document.querySelectorAll(".subject-card").forEach(card => {
    card.addEventListener("click", () => {
      openSubjectStudio(card.dataset.id);
    });
  });
}

// Open Subject Studio
async function openSubjectStudio(subjectId) {
  state.activeSubjectId = subjectId;
  const subj = state.subjects.find(s => s.id === subjectId) || {
    name: "Deep Learning & Predictive Modelling",
    icon: "🧠",
    code: "CS8083"
  };
  state.activeSubject = subj;

  activeSubjectIcon.textContent = subj.icon;
  activeSubjectTitle.textContent = subj.name;
  activeSubjectCode.textContent = subj.code;

  switchView("subject_studio");

  showToast(`Loading ${subj.name}... ⏳`);
  try {
    const qs = await loadSubjectDefaultBank(subjectId);
    state.questions = qs;
    renderQuestions();
    if (qs.length > 0) {
      selectQuestionToStudy(qs[0]);
    }
  } catch (err) {
    showToast(`Error loading questions: ${err.message}`);
  }
}

// Render Questions for Active Subject
function renderQuestions() {
  const filtered = state.questions.filter(q => {
    if (state.selectedCategory === "all") return true;
    if (state.selectedCategory === "must") return q.category && q.category.includes("Must");
    if (state.selectedCategory === "should") return q.category && q.category.includes("Should");
    if (state.selectedCategory === "13m") return q.marks && q.marks >= 13;
    if (state.selectedCategory === "5m") return q.marks && q.marks <= 6;
    return true;
  });

  questionCountBadge.textContent = `${filtered.length} Qs`;

  if (filtered.length === 0) {
    questionsContainer.innerHTML = `
      <div style="text-align: center; padding: 36px 16px; color: var(--text-muted);">
        <p style="font-size: 28px; margin-bottom: 8px;">📂</p>
        <p style="font-weight: 700;">No questions matching filter</p>
        <p style="font-size: 12px;">Upload a question bank or reset to syllabus bank.</p>
      </div>
    `;
    return;
  }

  questionsContainer.innerHTML = filtered.map(q => {
    const isMust = q.category && (q.category.includes("Must") || q.category.includes("High"));
    const categoryClass = isMust ? "badge-must" : "badge-should";
    const categoryLabel = isMust ? "🔥 Must Study" : "⭐ Should Study";

    return `
      <div class="question-item" data-id="${q.id}">
        <div class="question-meta">
          <span class="unit-tag">${q.unit || 'General'}</span>
          <div class="badge-group">
            <span class="badge ${categoryClass}">${categoryLabel}</span>
            <span class="badge badge-marks">${q.marks || 10} Marks</span>
            ${q.year ? `<span class="badge badge-year">${q.year}</span>` : ''}
          </div>
        </div>
        <div class="question-text">${q.question}</div>
        ${q.evidence ? `<div class="question-evidence">📊 ${q.evidence}</div>` : ''}
        <div class="question-action">Study with cozy.ai <span>➤</span></div>
      </div>
    `;
  }).join("");

  document.querySelectorAll(".question-item").forEach(item => {
    item.addEventListener("click", () => {
      const q = state.questions.find(x => x.id === item.dataset.id);
      if (q) selectQuestionToStudy(q);
    });
  });
}

function selectQuestionToStudy(q) {
  state.activeQuestion = q;
  questionInput.value = q.question;
  if (q.marks) {
    state.activeMarks = q.marks;
    marksButtons.forEach(btn => {
      btn.classList.toggle("active", parseInt(btn.dataset.marks) === q.marks);
    });
  }
  showToast(`Selected: "${q.question.substring(0, 35)}..."`);
  questionInput.focus();
}

// Render Answer Output Card
function renderAnswer(response) {
  const ans = response.answer;
  answerPlaceholder.style.display = "none";
  answerCard.style.display = "block";

  const isMock = response.is_mock;
  const engineBadge = isMock
    ? `<span class="badge badge-should">cozy.ai Demo Engine</span>`
    : `<span class="badge badge-year">🟢 Live Qwen (${response.model_used.split('/').pop()})</span>`;

  let html = `
    <div class="answer-card-header">
      <div class="answer-meta">
        <span class="badge badge-marks">${response.marks} Marks</span>
        <span class="badge" style="background:#EBF2FE; color:#3867D6;">${response.style} Style</span>
        ${engineBadge}
      </div>
      <div class="answer-tools">
        <button class="btn btn-secondary" id="copyBtnInline" style="padding: 5px 12px; font-size: 11px;">📋 Copy</button>
        <button class="btn btn-secondary" id="downloadBtnInline" style="padding: 5px 12px; font-size: 11px;">⬇️ Notes</button>
      </div>
    </div>
  `;

  // 1. Cozy Intuition / Everyday Analogy
  if (ans.simple_analogy) {
    html += `
      <div class="cozy-section cozy-section-analogy">
        <div class="section-title">
          <span>🧸</span>
          <span>Cozy Intuition & Everyday Analogy</span>
        </div>
        <div class="section-content">${ans.simple_analogy}</div>
      </div>
    `;
  }

  // 2. Formal Exam Definition
  if (ans.definition) {
    html += `
      <div class="cozy-section cozy-section-def">
        <div class="section-title">
          <span>📖</span>
          <span>Formal Exam Definition</span>
        </div>
        <div class="section-content" style="font-weight: 600;">${ans.definition}</div>
      </div>
    `;
  }

  // 3. Formula & Shortcuts (for math/predictive modelling/aptitude)
  if (ans.formula_shortcuts) {
    html += `
      <div class="formula-box">
        <div style="font-weight: 700; margin-bottom: 4px;">⚡ Key Mathematical Formulation & Shortcuts:</div>
        <div>${ans.formula_shortcuts}</div>
      </div>
    `;
  }

  // 4. Working & Architecture (Diagrams)
  if (ans.working_concept || (ans.working_steps && ans.working_steps.length > 0) || ans.diagram_ascii) {
    html += `
      <div class="cozy-section cozy-section-steps">
        <div class="section-title">
          <span>⚙️</span>
          <span>Working & Architecture</span>
        </div>
        ${ans.working_concept ? `<div class="section-content" style="margin-bottom: 8px;">${ans.working_concept}</div>` : ''}
        ${ans.diagram_ascii ? `<div class="ascii-box">${ans.diagram_ascii}</div>` : ''}
        ${ans.working_steps && ans.working_steps.length > 0 ? `
          <ul class="steps-list">
            ${ans.working_steps.map(s => `<li>${s}</li>`).join('')}
          </ul>
        ` : ''}
      </div>
    `;
  }

  // 5. Code Block with "Simulate / Run Code" (for Java/Web, Android, DSA)
  if (ans.code_snippet) {
    html += `
      <div class="code-box-wrapper">
        <div class="code-box-header">
          <span>💻 ${ans.code_language ? ans.code_language.toUpperCase() : 'CODE'} IMPLEMENTATION</span>
          <div style="display: flex; gap: 6px;">
            <button class="btn btn-secondary" id="runCodeBtn" style="padding: 3px 9px; font-size: 11px;">▶️ Run Code</button>
            <button class="btn btn-secondary" id="copyCodeBtn" style="padding: 3px 9px; font-size: 11px;">📋 Copy</button>
          </div>
        </div>
        <pre class="code-content"><code>${ans.code_snippet}</code></pre>
        <div id="codeRunOutput" class="code-run-output">
          🚀 [Process Finished Successfully - Exit Code 0]
          ----------------------------------------
          Output:
          ${ans.example || 'Program executed cleanly and output generated.'}
        </div>
      </div>
    `;
  }

  // 6. Practical Real-World Example
  if (ans.example) {
    html += `
      <div class="cozy-section" style="background: #F4FBF7; border: 1px solid #D2F4E2;">
        <div class="section-title" style="color: #108A48;">
          <span>💡</span>
          <span>Practical Concrete Example</span>
        </div>
        <div class="section-content">${ans.example}</div>
      </div>
    `;
  }

  // 7. Advantages & Applications
  if ((ans.advantages && ans.advantages.length > 0) || (ans.applications && ans.applications.length > 0)) {
    html += `
      <div class="cozy-section" style="background: #FAF8F5; border: 1px solid #EBE4D8;">
        <div class="section-title">
          <span>✅</span>
          <span>Key Points & Applications</span>
        </div>
        ${ans.advantages && ans.advantages.length > 0 ? `
          <div style="margin-bottom: 8px;">
            <strong style="font-size: 12.5px; color: var(--text-muted);">Advantages:</strong>
            <ul class="steps-list" style="margin-top: 4px;">
              ${ans.advantages.map(a => `<li>${a}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
        ${ans.applications && ans.applications.length > 0 ? `
          <div>
            <strong style="font-size: 12.5px; color: var(--text-muted);">Applications:</strong>
            <ul class="steps-list" style="margin-top: 4px;">
              ${ans.applications.map(ap => `<li>${ap}</li>`).join('')}
            </ul>
          </div>
        ` : ''}
      </div>
    `;
  }

  // 8. Exam Keywords
  if (ans.exam_keywords && ans.exam_keywords.length > 0) {
    html += `
      <div style="margin-top: 12px;">
        <strong style="font-size: 11px; font-family: var(--font-heading); text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.5px;">
          ⭐ Must-Include Exam Keywords
        </strong>
        <div class="keywords-cloud">
          ${ans.exam_keywords.map(kw => `<span class="keyword-tag">${kw}</span>`).join('')}
        </div>
      </div>
    `;
  }

  answerCard.innerHTML = html;

  // Bind inline events
  document.getElementById("copyBtnInline")?.addEventListener("click", () => copyCurrentAnswer(response));
  document.getElementById("downloadBtnInline")?.addEventListener("click", () => downloadAnswerNotes(response));
  
  // Code runner button
  const runCodeBtn = document.getElementById("runCodeBtn");
  const codeRunOutput = document.getElementById("codeRunOutput");
  runCodeBtn?.addEventListener("click", () => {
    codeRunOutput?.classList.toggle("show");
    showToast("Code sandbox executed output! ⚡");
  });

  const copyCodeBtn = document.getElementById("copyCodeBtn");
  copyCodeBtn?.addEventListener("click", () => {
    if (ans.code_snippet) {
      navigator.clipboard.writeText(ans.code_snippet);
      showToast("Code copied to clipboard! 💻");
    }
  });
}

function copyCurrentAnswer(response) {
  const ans = response.answer;
  const text = `
SUBJECT: ${response.question} (${response.marks} Marks)
----------------------------------------
DEFINITION:
${ans.definition}

ANALOGY:
${ans.simple_analogy || ''}

WORKING:
${ans.working_concept || ''}
${(ans.working_steps || []).join('\n')}

CODE / DIAGRAM:
${ans.code_snippet || ans.diagram_ascii || ''}

KEYWORDS:
${(ans.exam_keywords || []).join(', ')}
----------------------------------------
Generated by cozy.ai ✨
`.trim();
  navigator.clipboard.writeText(text);
  showToast("Exam notes copied to clipboard! 📋");
}

function downloadAnswerNotes(response) {
  const ans = response.answer;
  const filename = `${(state.activeSubject?.name || 'Subject').replace(/\s+/g, '_')}_${response.marks}M_Notes.txt`;
  const content = `=====================================================
                      cozy.ai
             EXAM PREPARATION STUDY NOTES
=====================================================
Subject: ${state.activeSubject?.name || 'Semester Subject'}
Topic: ${response.question}
Marks: ${response.marks} Marks
Generated: ${new Date().toLocaleString()}
=====================================================

1. DEFINITION
${ans.definition}

2. ANALOGY
${ans.simple_analogy || 'N/A'}

3. WORKING & ARCHITECTURE
${ans.working_concept || ''}
${(ans.working_steps || []).map(s => '  • ' + s).join('\n')}

${ans.diagram_ascii ? `\nDiagram:\n${ans.diagram_ascii}\n` : ''}
${ans.code_snippet ? `\nCode Implementation:\n${ans.code_snippet}\n` : ''}

4. PRACTICAL EXAMPLE
${ans.example || 'N/A'}

5. ADVANTAGES
${(ans.advantages || []).map(a => '  • ' + a).join('\n')}

6. KEYWORDS
${(ans.exam_keywords || []).join(' | ')}
`;
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
  showToast(`Downloaded ${filename} 📄`);
}

// Handle Answer Generation
async function handleGenerate() {
  const qText = questionInput.value.trim();
  if (!qText) {
    showToast("Please enter or select a question first!");
    questionInput.focus();
    return;
  }

  if (state.isGenerating) return;
  state.isGenerating = true;
  generateBtn.innerHTML = `<span class="spinner"></span> Qwen Thinking...`;
  generateBtn.disabled = true;

  try {
    const payload = {
      subject: state.activeSubject?.name || "Deep Learning & Predictive Modelling",
      domain_mode: state.currentMode,
      question: qText,
      marks: state.activeMarks,
      style: state.activeStyle,
      length: state.activeLength,
      explain_simply: state.explainSimply
    };

    const res = await generateExamAnswer(payload);
    renderAnswer(res);
    showToast("Qwen exam answer prepared! ✨");
  } catch (err) {
    showToast(`Error: ${err.message}`);
  } finally {
    state.isGenerating = false;
    generateBtn.innerHTML = `<span>✨</span><span>Generate Answer</span>`;
    generateBtn.disabled = false;
  }
}

// PLACEMENT TRAINING LOGIC
const PLACEMENT_TOPICS = {
  aptitude: [
    "Probability", "Time & Work", "Profit & Loss", "Percentages",
    "Number Systems", "Ratios & Proportions", "Permutation & Combination"
  ],
  coding: [
    "Two Pointers & Sliding Window", "Linked List Cycle & Reverse",
    "Binary Tree Inversion & BFS", "Dynamic Programming (Knapsack)", "Graph DFS & Connected Components"
  ],
  technical: [
    "Java HashMap Internal Working", "SQL Normalization (1NF to BCNF)",
    "Operating System Deadlock 4 Conditions", "TCP vs UDP 3-Way Handshake", "REST vs GraphQL Architecture"
  ],
  hr: [
    "Tell Me About Yourself", "Overcoming a Project Failure (STAR)",
    "Greatest Strength & Weakness", "Handling Conflict in Team", "Why Should We Hire You?"
  ]
};

async function renderPlacementTrack() {
  const track = state.activePlacementTrack;

  // Render topic pills
  const topics = PLACEMENT_TOPICS[track] || [];
  placementTopicPills.innerHTML = topics.map(t => `
    <button class="topic-launch-pill" data-topic="${t}">⚡ ${t}</button>
  `).join("");

  document.querySelectorAll(".topic-launch-pill").forEach(pill => {
    pill.addEventListener("click", () => {
      launchPlacementPractice(track, pill.dataset.topic);
    });
  });

  // Load curated placement questions
  try {
    const qs = await loadSubjectDefaultBank("placement");
    state.placementQuestions = qs;
    placementCountBadge.textContent = `${qs.length} Qs`;

    placementQuestionsContainer.innerHTML = qs.map(q => `
      <div class="question-item placement-item" data-id="${q.id}">
        <div class="question-meta">
          <span class="unit-tag">${q.unit || 'Placement'}</span>
          <div class="badge-group">
            <span class="badge badge-must">🔥 High Yield</span>
            <span class="badge badge-marks">${q.marks || 10}M</span>
          </div>
        </div>
        <div class="question-text">${q.question}</div>
        <div class="question-action">Practice with Qwen <span>➤</span></div>
      </div>
    `).join("");

    document.querySelectorAll(".placement-item").forEach(item => {
      item.addEventListener("click", () => {
        const q = state.placementQuestions.find(x => x.id === item.dataset.id);
        if (q) {
          launchPlacementPractice(track, q.question);
        }
      });
    });
  } catch (err) {
    showToast(`Error loading placement questions: ${err.message}`);
  }
}

async function launchPlacementPractice(track, topic) {
  showToast(`Generating Qwen placement solution for ${topic}... ⏳`);
  try {
    const res = await generatePlacementPractice(track, topic, "medium");
    renderPlacementAnswer(res);
  } catch (err) {
    showToast(`Error: ${err.message}`);
  }
}

function renderPlacementAnswer(response) {
  const ans = response.answer;
  const isMock = response.is_mock;
  const engineBadge = isMock
    ? `<span class="badge badge-should">cozy.ai Demo Engine</span>`
    : `<span class="badge badge-year">🟢 Live Qwen (${response.model_used.split('/').pop()})</span>`;

  let html = `
    <div class="answer-card-header">
      <div class="answer-meta">
        <span class="badge" style="background:#F3ECFB; color:#6B21A8; font-weight:700;">🎯 Placement Strategy</span>
        ${engineBadge}
      </div>
      <button class="btn btn-secondary" id="copyPlacementBtn" style="padding: 5px 12px; font-size: 11px;">📋 Copy Strategy</button>
    </div>

    <!-- Core Solution -->
    <div class="cozy-section cozy-section-def">
      <div class="section-title"><span>🎯</span><span>Core Solution & Summary</span></div>
      <div class="section-content" style="font-weight: 600;">${ans.definition}</div>
    </div>
  `;

  // Formula & Shortcuts
  if (ans.formula_shortcuts) {
    html += `
      <div class="formula-box">
        <div style="font-weight: 700; margin-bottom: 4px;">⚡ Placement Shortcut / Time-Saving Trick:</div>
        <div>${ans.formula_shortcuts}</div>
      </div>
    `;
  }

  // Step by step breakdown
  if (ans.working_steps && ans.working_steps.length > 0) {
    html += `
      <div class="cozy-section cozy-section-steps">
        <div class="section-title"><span>📝</span><span>Step-by-Step Problem Breakdown</span></div>
        <ul class="steps-list">
          ${ans.working_steps.map(s => `<li>${s}</li>`).join('')}
        </ul>
      </div>
    `;
  }

  // Code Block
  if (ans.code_snippet) {
    html += `
      <div class="code-box-wrapper">
        <div class="code-box-header">
          <span>💻 OPTIMAL CODE (${ans.code_language || 'JAVA'})</span>
          <button class="btn btn-secondary" id="copyPlaceCode" style="padding: 3px 9px; font-size: 11px;">📋 Copy Code</button>
        </div>
        <pre class="code-content"><code>${ans.code_snippet}</code></pre>
      </div>
    `;
  }

  // Interviewer Tips
  if (ans.interview_tips) {
    html += `
      <div class="cozy-section" style="background: #FFF9E6; border: 1px solid #FFE58F;">
        <div class="section-title" style="color: #D48806;"><span>💼</span><span>Interviewer Red Flags & Tips</span></div>
        <div class="section-content">${ans.interview_tips}</div>
      </div>
    `;
  }

  // Keywords
  if (ans.exam_keywords && ans.exam_keywords.length > 0) {
    html += `
      <div style="margin-top: 12px;">
        <strong style="font-size: 11px; font-family: var(--font-heading); text-transform: uppercase; color: var(--text-muted);">
          Key Placement Concepts:
        </strong>
        <div class="keywords-cloud">
          ${ans.exam_keywords.map(kw => `<span class="keyword-tag">${kw}</span>`).join('')}
        </div>
      </div>
    `;
  }

  placementAnswerCard.innerHTML = html;

  document.getElementById("copyPlacementBtn")?.addEventListener("click", () => {
    navigator.clipboard.writeText(`${response.question}\n\n${ans.definition}\n\n${ans.formula_shortcuts || ''}`);
    showToast("Placement strategy copied! 📋");
  });

  document.getElementById("copyPlaceCode")?.addEventListener("click", () => {
    if (ans.code_snippet) {
      navigator.clipboard.writeText(ans.code_snippet);
      showToast("Code copied to clipboard! 💻");
    }
  });
}

// Initialize Application
async function init() {
  refreshStatus();
  setInterval(refreshStatus, 30000);

  // Load Subjects from Registry
  try {
    const subjects = await fetchSubjects();
    state.subjects = subjects;
    renderSubjectCards();
  } catch (err) {
    showToast("Loaded offline subject taxonomy");
  }

  // Mode Tabs
  modeSemesterBtn.addEventListener("click", () => switchView("semester_hub"));
  modePlacementBtn.addEventListener("click", () => switchView("placement_hub"));
  brandHomeBtn.addEventListener("click", () => switchView("semester_hub"));

  // Quick Study Button on Hub
  hubQuickStudyBtn.addEventListener("click", () => {
    openSubjectStudio("deep_learning");
  });

  backToHubBtn.addEventListener("click", () => switchView("semester_hub"));

  // Reset Syllabus Bank
  studioResetBankBtn.addEventListener("click", () => {
    openSubjectStudio(state.activeSubjectId);
  });

  // Filters
  filterPills.forEach(pill => {
    pill.addEventListener("click", () => {
      filterPills.forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      state.selectedCategory = pill.dataset.filter;
      renderQuestions();
    });
  });

  // Marks buttons
  marksButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      marksButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.activeMarks = parseInt(btn.dataset.marks);
    });
  });

  // Style buttons
  styleButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      styleButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.activeStyle = btn.dataset.style;
    });
  });

  explainSimplyCheckbox.addEventListener("change", (e) => {
    state.explainSimply = e.target.checked;
  });

  // Generate Answer
  generateBtn.addEventListener("click", handleGenerate);
  questionInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      handleGenerate();
    }
  });

  // Placement track buttons
  document.querySelectorAll(".placement-track-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".placement-track-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.activePlacementTrack = btn.dataset.track;
      renderPlacementTrack();
    });
  });

  // File Upload
  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("change", async (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      showToast(`Uploading ${file.name}... ⏳`);
      try {
        const res = await uploadQuestionBank(file, state.activeSubject?.name || "Deep Learning");
        state.questions = res.questions;
        renderQuestions();
        showToast(`Extracted ${res.total_questions} questions from ${file.name}! 🎉`);
      } catch (err) {
        showToast(`Upload failed: ${err.message}`);
      }
    }
  });

  // Settings Modal & Presets
  settingsBtn.addEventListener("click", () => {
    vllmUrlInput.value = state.vllmStatus.base_url || "http://localhost:11434/v1";
    vllmModelInput.value = state.vllmStatus.active_model || "qwen2.5:7b";
    settingsModal.classList.add("open");
  });

  vllmBadge.addEventListener("click", () => settingsBtn.click());
  closeModalBtn.addEventListener("click", () => settingsModal.classList.remove("open"));

  presetOllama.addEventListener("click", () => {
    vllmUrlInput.value = "http://localhost:11434/v1";
    vllmModelInput.value = "qwen2.5:7b";
    vllmApiKeyInput.value = "EMPTY";
    vllmTestFeedback.textContent = "Preset: Local Qwen 2.5 7B on Mac M4";
    vllmTestFeedback.style.color = "var(--primary)";
  });

  presetVllm.addEventListener("click", () => {
    vllmUrlInput.value = "http://localhost:8000/v1";
    vllmModelInput.value = "meta-llama/Meta-Llama-3-8B-Instruct";
    vllmApiKeyInput.value = "EMPTY";
    vllmTestFeedback.textContent = "Preset: Remote vLLM Server";
    vllmTestFeedback.style.color = "var(--text-muted)";
  });

  presetGroq.addEventListener("click", () => {
    vllmUrlInput.value = "https://api.groq.com/openai/v1";
    vllmModelInput.value = "llama-3.3-70b-versatile";
    vllmApiKeyInput.placeholder = "Paste Groq API key (gsk_...)";
    vllmTestFeedback.textContent = "Preset: Groq Fast Cloud (paste your free key)";
    vllmTestFeedback.style.color = "var(--accent-purple)";
  });

  testVllmBtn.addEventListener("click", async () => {
    vllmTestFeedback.textContent = "Testing connection...";
    vllmTestFeedback.style.color = "var(--text-muted)";
    try {
      const res = await updateVLLMConfig({
        base_url: vllmUrlInput.value.trim(),
        model: vllmModelInput.value.trim(),
        api_key: vllmApiKeyInput.value.trim() || "EMPTY"
      });
      state.vllmStatus = res;
      if (res.status === "connected") {
        vllmTestFeedback.textContent = `✅ Connected! Model: ${res.active_model}`;
        vllmTestFeedback.style.color = "var(--accent-mint)";
      } else {
        vllmTestFeedback.textContent = `⚠️ Offline: ${res.message}`;
        vllmTestFeedback.style.color = "var(--accent-warm)";
      }
      refreshStatus();
    } catch (err) {
      vllmTestFeedback.textContent = `❌ Test failed: ${err.message}`;
      vllmTestFeedback.style.color = "var(--accent-peach)";
    }
  });

  saveSettingsBtn.addEventListener("click", async () => {
    try {
      await updateVLLMConfig({
        base_url: vllmUrlInput.value.trim(),
        model: vllmModelInput.value.trim(),
        api_key: vllmApiKeyInput.value.trim() || "EMPTY"
      });
      refreshStatus();
      settingsModal.classList.remove("open");
      showToast("Settings updated!");
    } catch (err) {
      showToast(`Error: ${err.message}`);
    }
  });

  // Start with semester hub
  switchView("semester_hub");
}

document.addEventListener("DOMContentLoaded", init);
