import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { getPredictionById, getPredictions } from "../api";
import "../App.css";


type PredictionDetails = {
  id: number;
  filename: string;
  predicted_class: string;
  confidence: number;
  probabilities: Record<string, number>;
  model_version: string;
  latency_ms: number;
  created_at: string;
  review_status: string;
  true_label: string | null;
  correct: boolean | null;
  notes: string | null;
};

function PredictionDetailsPage() {
    const { predictionId } = useParams();
		const navigate = useNavigate();

    const [prediction, setPrediction] =
      useState<PredictionDetails | null>(null);

			const [maxPredictionId, setMaxPredictionId] =
				useState<number | null>(null);

    const [error, setError] = useState("");

    useEffect(() => {
      async function loadPrediction() {
        try {
          const predictionData = await getPredictionById(
            Number(predictionId)
          );

          setPrediction(predictionData);
					const predictionsData = await getPredictions();
					const maxId = Math.max(...predictionsData.map((p: { id: number }) => p.id));
					setMaxPredictionId(maxId);
        } catch {
          setError("Unable to load prediction.");
        }
      }

      loadPrediction();
    }, [predictionId]);

    return (
			<main className="app">
				<section className="hero">
					<Link to="/">← Back to dashboard</Link>

					{error && <p>{error}</p>}

					{!prediction && !error && (
						<p>Loading prediction...</p>
					)}

					{prediction && (
						<>
							<h1>Prediction #{prediction.id}</h1>

							<div className="prediction-nav">
								<button
									className="secondary-button"
									onClick={() => navigate(`/predictions/${Number(predictionId) - 1}`)}
									disabled={Number(predictionId) <= 1}
								>
									← Previous
								</button>

								<button
									className="secondary-button"
									onClick={() => navigate(`/predictions/${Number(predictionId) + 1}`)}
									disabled={
										maxPredictionId !== null &&
										Number(predictionId) >= maxPredictionId
									}
								>
									Next →
								</button>
							</div>

							<div className="prediction-details-stack">
								<section className="detail-card">
									<h2>Prediction Summary</h2>

									<div className="detail-list">
										<div>
											<span>Filename</span>
											<strong>{prediction.filename}</strong>
										</div>

										<div>
											<span>Predicted Class</span>
											<strong>{prediction.predicted_class}</strong>
										</div>

										<div>
											<span>Confidence</span>
											<strong>
												{(prediction.confidence * 100).toFixed(2)}%
											</strong>
										</div>
									</div>
								</section>

								<section className="detail-card">
									<h2>Class Probabilities</h2>

									{Object.entries(prediction.probabilities).map(
										([className, probability]) => (
											<div className="probability-row" key={className}>
												<div className="probability-label">
													<span>{className}</span>
													<strong>{(probability * 100).toFixed(2)}%</strong>
												</div>

												<div className="probability-track">
													<div
														className="probability-fill"
														style={{ width: `${probability * 100}%` }}
													/>
												</div>
											</div>
										)
									)}
								</section>

								<section className="details-grid">
									<div className="detail-card">
										<h2>Prediction Metadata</h2>

										<div className="detail-list">
											<div>
												<span>Model Version</span>
												<strong>{prediction.model_version}</strong>
											</div>

											<div>
												<span>Latency</span>
												<strong>{prediction.latency_ms} ms</strong>
											</div>

											<div>
												<span>Created At</span>
												<strong>{new Date(prediction.created_at).toLocaleString()}</strong>
											</div>
										</div>
									</div>

									<div className="detail-card">
										<h2>Review Information</h2>

										<div className="detail-list">
											<div>
												<span>Review Status</span>
												<strong>{prediction.review_status}</strong>
											</div>

											<div>
												<span>True Label</span>
												<strong>{prediction.true_label ?? "—"}</strong>
											</div>

											<div>
												<span>Correct</span>
												<strong>
													{prediction.correct === null
														? "—"
														: prediction.correct
															? "Yes"
															: "No"}
												</strong>
											</div>

											<div>
												<span>Notes</span>
												<strong>{prediction.notes ?? "—"}</strong>
											</div>
										</div>
									</div>
								</section>
							</div>
						</>
					)}
				</section>
			</main>
		);
}

export default PredictionDetailsPage;