// API Client for cozy.ai
const API_BASE = "";

export async function fetchSubjects() {
  const res = await fetch(`${API_BASE}/api/subjects`);
  if (!res.ok) {
    throw new Error("Failed to load subjects");
  }
  return await res.json();
}

export async function loadSubjectDefaultBank(subjectId) {
  const res = await fetch(`${API_BASE}/api/subjects/${encodeURIComponent(subjectId)}/load-default`, {
    method: "POST"
  });
  if (!res.ok) {
    throw new Error(`Failed to load question bank for ${subjectId}`);
  }
  return await res.json();
}

export async function uploadQuestionBank(file, subject = "Deep Learning") {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("subject", subject);

  const res = await fetch(`${API_BASE}/api/upload`, {
    method: "POST",
    body: formData
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(err.detail || "Failed to upload question bank");
  }
  return await res.json();
}

export async function loadSampleQB(subject = "Deep Learning") {
  const res = await fetch(`${API_BASE}/api/load-sample?subject=${encodeURIComponent(subject)}`, {
    method: "POST"
  });
  if (!res.ok) {
    throw new Error("Failed to load sample question bank");
  }
  return await res.json();
}

export async function fetchQuestions(unit = null, category = null) {
  let url = `${API_BASE}/api/questions?`;
  if (unit) url += `unit=${encodeURIComponent(unit)}&`;
  if (category) url += `category=${encodeURIComponent(category)}&`;

  const res = await fetch(url);
  if (!res.ok) {
    throw new Error("Failed to fetch questions");
  }
  return await res.json();
}

export async function generateExamAnswer(requestData) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestData)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Chat generation failed" }));
    throw new Error(err.detail || "Failed to generate answer");
  }
  return await res.json();
}

export async function generatePlacementPractice(track, topic, difficulty = "medium") {
  const res = await fetch(`${API_BASE}/api/placement/practice`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ track, topic, difficulty })
  });
  if (!res.ok) {
    throw new Error("Failed to generate placement practice");
  }
  return await res.json();
}

export async function getVLLMStatus() {
  const res = await fetch(`${API_BASE}/api/vllm/status`);
  if (!res.ok) {
    return { status: "offline", message: "Cannot reach backend" };
  }
  return await res.json();
}

export async function updateVLLMConfig(config) {
  const res = await fetch(`${API_BASE}/api/vllm/config`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(config)
  });
  if (!res.ok) {
    throw new Error("Failed to update vLLM settings");
  }
  return await res.json();
}
