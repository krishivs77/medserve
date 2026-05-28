import { useEffect, useState } from "react";

import "./App.css";
import { getHealth, getModelInfo } from "./api";

type HealthStatus = {
  status: string;
  service: string;
};

type ModelInfo = {
  model_name: string;
  class_names: string[];
  image_size: number;
  test_accuracy: number;
};

function App() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadBackendStatus() {
      try {
        const healthData = await getHealth();
        const modelData = await getModelInfo();

        setHealth(healthData);
        setModelInfo(modelData);
      } catch {
        setError("Unable to connect to MedServe backend.");
      }
    }

    loadBackendStatus();
  }, []);

  return (
    <main className="app">
      <section className="hero">
        <div className="eyebrow">Medical ML Monitoring Platform</div>

        <h1>MedServe</h1>

        <p className="hero-text">
          A full-stack platform for serving medical machine learning models,
          logging predictions, and monitoring confidence, latency, and review
          workflows.
        </p>

        <div className="hero-actions">
          <button className="primary-button">Upload MRI</button>
          <button className="secondary-button">View Monitoring</button>
        </div>

        <div className="status-panel">
          <h2>Backend Status</h2>

          {error && <p className="error-text">{error}</p>}

          {!error && !health && <p>Checking backend...</p>}

          {health && modelInfo && (
            <div className="status-grid">
              <div>
                <span>Status</span>
                <strong>{health.status}</strong>
              </div>

              <div>
                <span>Service</span>
                <strong>{health.service}</strong>
              </div>

              <div>
                <span>Model</span>
                <strong>{modelInfo.model_name}</strong>
              </div>

              <div>
                <span>Test Accuracy</span>
                <strong>{(modelInfo.test_accuracy * 100).toFixed(1)}%</strong>
              </div>
            </div>
          )}
        </div>
      </section>

      <section className="cards">
        <div className="card">
          <h2>Model Serving</h2>
          <p>
            Send medical images to a FastAPI backend and receive structured
            prediction results from a PyTorch model.
          </p>
        </div>

        <div className="card">
          <h2>Prediction Logging</h2>
          <p>
            Store predictions, confidence scores, latency, and review metadata
            for later analysis.
          </p>
        </div>

        <div className="card">
          <h2>Monitoring Dashboard</h2>
          <p>
            Track low-confidence cases, reviewed predictions, class distribution,
            and model performance signals.
          </p>
        </div>
      </section>
    </main>
  );
}

export default App;