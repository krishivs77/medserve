import time

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import LOW_CONFIDENCE_THRESHOLD
from app.services.image_service import image_service
from app.services.model_service import model_service


router = APIRouter()


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Uploaded file must be an image."
        )
    
    image_bytes = await file.read()

    image = image_service.load_image(image_bytes)

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

    return prediction