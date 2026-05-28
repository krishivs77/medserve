from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "medserve-backend"
    }


def test_model_info():
    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model_name"] == "resnet18_finetuned"
    assert data["class_names"] == [
        "glioma",
        "meningioma",
        "notumor",
        "pituitary"
    ]
    assert data["image_size"] == 224
    assert data["test_accuracy"] == 0.91


def test_predict_endpoint():
    test_filename = "test_meningioma.jpg"

    image_path = (
        Path(__file__).resolve().parents[2]
        / "sample_images"
        / test_filename
    )

    with open(image_path, "rb") as image_file:
        response = client.post(
            "/predict",
            files={
                "file": (
                    test_filename,
                    image_file,
                    "image/jpeg"
                )
            }
        )
    
    assert response.status_code == 200

    data = response.json()
    
    assert "predicted_class" in data
    assert "confidence" in data
    assert "probabilities" in data
    assert "latency_ms" in data
    assert "low_confidence_flag" in data


def test_get_predictions():
    response = client.get("/predictions")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_get_prediction_by_id():
    response = client.get("/predictions/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "predicted_class" in data
    assert "confidence" in data
    assert "review_status" in data


def test_update_prediction_review():
    response = client.patch(
        "/predictions/1/review",
        params={
            "review_status": "reviewed",
            "true_label": "meningioma",
            "notes": "Reviewed during automated test."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["review_status"] == "reviewed"
    assert data["true_label"] == "meningioma"
    assert data["correct"] in [True, False]
    assert data["notes"] == "Reviewed during automated test."


def test_metrics_summary():
    response = client.get("/metrics/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_predictions" in data
    assert "average_confidence" in data
    assert "low_confidence_count" in data
    assert "average_latency_ms" in data
    assert "reviewed_count" in data
    assert "reviewed_accuracy" in data