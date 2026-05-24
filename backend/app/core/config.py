from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[2]

PROJECT_ROOT = BACKEND_DIR.parent

MODEL_ARTIFACTS_DIR = PROJECT_ROOT / "model_artifacts"

MODEL_PATH = MODEL_ARTIFACTS_DIR / "resnet18_brain_mri_v1.pth"

LOW_CONFIDENCE_THRESHOLD = 0.70

API_TITLE = "MedServe API"

API_VERSION = "0.1.0"