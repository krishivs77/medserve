import time

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import LOW_CONFIDENCE_THRESHOLD
from app.services.image_service import image_service
from app.services.model_service import model_service
from app.db.database import get_db
from app.services.prediction_service import prediction_service


router = APIRouter()


@router.post("/predict")
async def predict_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an image."
        )
    
    image_bytes = await file.read()

    image = image_service.load_image(image_bytes)

    image_width, image_height = image.size

    file_size_kb = round(
        len(image_bytes) / 1024,
        2
    )

    input_tensor = image_service.preprocess_image(image)

    start_time = time.perf_counter()

    prediction = model_service.predict(input_tensor)

    latency_ms = (
        (time.perf_counter() - start_time)
        * 1000
    )

    prediction["latency_ms"] = round(latency_ms, 2)

    prediction["low_confidence_flag"] = (
        prediction["confidence"]
        < LOW_CONFIDENCE_THRESHOLD
    )

    saved_prediction = prediction_service.create_prediction(
    db=db,
    filename=file.filename,
    predicted_class=prediction["predicted_class"],
    confidence=prediction["confidence"],
    probabilities=prediction["probabilities"],
    model_version=prediction["model_version"],
    latency_ms=prediction["latency_ms"],
    image_width=image_width,
    image_height=image_height,
    file_size_kb=file_size_kb,
    low_confidence_flag=prediction["low_confidence_flag"]
    )

    prediction["prediction_id"] = saved_prediction.id

    return prediction