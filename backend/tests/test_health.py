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