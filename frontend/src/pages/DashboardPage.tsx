import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import "../App.css";

import { 
  getHealth, 
  getMetricsSummary, 
  getModelInfo, 
  getPredictions,
  predictImage, 
} from "../api";

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

type PredictionResult = {
  prediction_id: number;
  predicted_class: string;
  confidence: number;
  probabilities: Record<string, number>;
  model_version: string;
  latency_ms: number;
  low_confidence_flag: boolean;
};

type MetricsSummary = {
  total_predictions: number;
  average_confidence: number | null;
  low_confidence_count: number;
  average_latency_ms: number | null;
  reviewed_count: number;
  reviewed_accuracy: number | null;
};

type Prediction = {
  id: number;
  filename: string;
  predicted_class: string;
  confidence: number;
  review_status: string;
  created_at: string;
  true_label: string | null;
  correct: boolean | null;
  notes: string | null;
};

function DashboardPage() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [error, setError] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [isPredicting, setIsPredicting] = useState(false);
  const [predictionError, setPredictionError] = useState("");
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  const navigate = useNavigate();

  useEffect(() => {
    async function loadBackendStatus() {
      try {
        const healthData = await getHealth();
        const modelData = await getModelInfo();
        const metricsData = await getMetricsSummary();
        const predictionsData = await getPredictions();

        setHealth(healthData);
        setModelInfo(modelData);
        setMetrics(metricsData);
        setPredictions(predictionsData);
      } catch {
        setError("Unable to connect to MedServe backend.");
      }
    }

    loadBackendStatus();
  }, []);

      async function handlePrediction() {
        if (!selectedFile) {
          setPredictionError("Please choose an MRI image first.");
          return;
        }

        setIsPredicting(true);
        setPredictionError("");
        setPrediction(null);

        try {
          const result = await predictImage(selectedFile);
          setPrediction(result);
          navigate(`/predictions/${result.prediction_id}`);
          const updatedMetrics = await getMetricsSummary();
          const updatedPredictions = await getPredictions();

          setMetrics(updatedMetrics);
          setPredictions(updatedPredictions);
        } catch {
          setPredictionError("Prediction failed. Make sure the backend is running.");
        } finally {
          setIsPredicting(false);
        }
      }

      const classCounts = predictions.reduce<Record<string, number>>(
        (counts, prediction) => {
          counts[prediction.predicted_class] =
            (counts[prediction.predicted_class] ?? 0) + 1;

          return counts;
        },
        {}
      );

      const maxClassCount = Math.max(...Object.values(classCounts), 1);

      const reviewCounts = predictions.reduce<Record<string, number>>(
        (counts, prediction) => {
          const status = prediction.review_status ?? "unknown";

          counts[status] = (counts[status] ?? 0) + 1;

          return counts;
        },
        {}
      );

      const maxReviewCount = Math.max(
        ...Object.values(reviewCounts),
        1
      );

      const lowConfidencePredictions = [...predictions]
        .sort((a, b) => a.confidence - b.confidence)
        .slice(0, 5);

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
        <div className="upload-panel">
          <h2>Run MRI Prediction</h2>

          <div className="upload-controls">
            <label className="file-upload">
              <span className="file-button">Choose File</span>
              <span className="file-name">
                {selectedFile ? selectedFile.name : "No file selected"}
              </span>

              <input
                type="file"
                accept="image/*"
                onChange={(event) => {
                  const file = event.target.files?.[0] ?? null;
                  setSelectedFile(file);
                  setPrediction(null);
                  setPredictionError("");
                }}
              />
            </label>

            <button
              className="primary-button"
              onClick={handlePrediction}
              disabled={isPredicting}
            >
              {isPredicting ? "Running prediction..." : "Predict"}
            </button>
          </div>

          {predictionError && <p className="error-text">{predictionError}</p>}

          {prediction && (
            <div className="prediction-result">
              <h3>Prediction Result</h3>

              <p>
                <strong>Class:</strong> {prediction.predicted_class}
              </p>

              <p>
                <strong>Confidence:</strong>{" "}
                {(prediction.confidence * 100).toFixed(2)}%
              </p>

              <p>
                <strong>Latency:</strong> {prediction.latency_ms} ms
              </p>

              <p>
                <strong>Low Confidence:</strong>{" "}
                {prediction.low_confidence_flag ? "Yes" : "No"}
              </p>
            </div>
          )}
        </div>

        {metrics && (
          <div className="metrics-panel">
            <h2>Monitoring Summary</h2>

            <div className="metrics-grid">
              <div>
                <span>Total Predictions</span>
                <strong>{metrics.total_predictions}</strong>
              </div>

              <div>
                <span>Average Confidence</span>
                <strong>
                  {metrics.average_confidence === null
                    ? "N/A"
                    : `${(metrics.average_confidence * 100).toFixed(1)}%`}
                </strong>
              </div>

              <div>
                <span>Low Confidence Cases</span>
                <strong>{metrics.low_confidence_count}</strong>
              </div>

              <div>
                <span>Average Latency</span>
                <strong>
                  {metrics.average_latency_ms === null
                    ? "N/A"
                    : `${metrics.average_latency_ms.toFixed(1)} ms`}
                </strong>
              </div>

              <div>
                <span>Reviewed</span>
                <strong>{metrics.reviewed_count}</strong>
              </div>

              <div>
                <span>Reviewed Accuracy</span>
                <strong>
                  {metrics.reviewed_accuracy === null
                    ? "N/A"
                    : `${(metrics.reviewed_accuracy * 100).toFixed(1)}%`}
                </strong>
              </div>
            </div>
          </div>
        )}

        <div className="charts-grid">
          <div className="chart-panel">
            <h2>Prediction Distribution</h2>

            {Object.entries(classCounts).map(([className, count]) => (
              <div className="chart-row" key={className}>
                <div className="chart-label">
                  <span>{className}</span>
                  <strong>{count}</strong>
                </div>

                <div className="chart-track">
                  <div
                    className="chart-fill"
                    style={{
                      width: `${(count / maxClassCount) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="chart-panel">
            <h2>Review Status Distribution</h2>

            {Object.entries(reviewCounts).map(([status, count]) => (
              <div className="chart-row" key={status}>
                <div className="chart-label">
                  <span>{status}</span>
                  <strong>{count}</strong>
                </div>

                <div className="chart-track">
                  <div
                    className="chart-fill"
                    style={{
                      width: `${(count / maxReviewCount) * 100}%`,
                    }}
                  />
                </div>
              </div>
            ))}
          </div>

          <div className="chart-panel">
            <h2>Lowest Confidence Predictions</h2>

            {lowConfidencePredictions.map((prediction) => (
              <div
                key={prediction.id}
                className="low-confidence-row"
                onClick={() =>
                  navigate(`/predictions/${prediction.id}`)
                }
              >
                <div>
                  <strong>#{prediction.id}</strong>
                </div>

                <div>{prediction.predicted_class}</div>

                <div>
                  {(prediction.confidence * 100).toFixed(2)}%
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="history-panel">
          <h2>Prediction History</h2>

          {predictions.length === 0 ? (
            <p>No predictions logged yet.</p>
          ) : (
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Filename</th>
                    <th>Prediction</th>
                    <th>Confidence</th>
                    <th>Review Status</th>
                  </tr>
                </thead>

                <tbody>
                  {predictions.map((prediction) => (
                    <tr
                      key={prediction.id}
                      onClick={() => navigate(`/predictions/${prediction.id}`)}
                      >
                      <td>{prediction.id}</td>
                      <td>{prediction.filename}</td>
                      <td>{prediction.predicted_class}</td>
                      <td>{(prediction.confidence * 100).toFixed(1)}%</td>
                      <td>{prediction.review_status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
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

export default DashboardPage;