const API_BASE_URL = "http://127.0.0.1:8000";

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error("Failed to fetch backend health status");
  }

  return response.json();
}

export async function getModelInfo() {
  const response = await fetch(`${API_BASE_URL}/model-info`);

  if (!response.ok) {
    throw new Error("Failed to fetch model info");
  }

  return response.json();
}

export async function predictImage(file: File) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to run prediction");
  }

  return response.json();
}

export async function getMetricsSummary() {
  const response = await fetch(`${API_BASE_URL}/metrics/summary`);

  if (!response.ok) {
    throw new Error("Failed to fetch metrics summary");
  }

  return response.json();
}