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