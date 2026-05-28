import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.prediction_service import prediction_service


router = APIRouter()


@router.get("/predictions")
def get_predictions(
    limit: int = 50,
    db: Session = Depends(get_db)
):
    predictions = prediction_service.get_predictions(
        db=db,
        limit=limit
    )

    return [
        {
            "id": prediction.id,
            "filename": prediction.filename,
            "predicted_class": prediction.predicted_class,
            "confidence": prediction.confidence,
            "probabilities": json.loads(prediction.probabilities_json),
            "model_version": prediction.model_version,
            "latency_ms": prediction.latency_ms,
            "created_at": prediction.created_at,
            "low_confidence_flag": prediction.low_confidence_flag,
            "review_status": prediction.review_status,
            "true_label": prediction.true_label,
            "correct": prediction.correct,
        }
        for prediction in predictions
    ]


@router.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int,
    db: Session = Depends(get_db)
):
    prediction = prediction_service.get_prediction_by_id(
        db=db,
        prediction_id=prediction_id
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found."
        )

    return {
        "id": prediction.id,
        "filename": prediction.filename,
        "predicted_class": prediction.predicted_class,
        "confidence": prediction.confidence,
        "probabilities": json.loads(prediction.probabilities_json),
        "model_version": prediction.model_version,
        "latency_ms": prediction.latency_ms,
        "created_at": prediction.created_at,
        "image_width": prediction.image_width,
        "image_height": prediction.image_height,
        "file_size_kb": prediction.file_size_kb,
        "low_confidence_flag": prediction.low_confidence_flag,
        "review_status": prediction.review_status,
        "notes": prediction.notes,
        "true_label": prediction.true_label,
        "correct": prediction.correct,
    }

@router.patch("/predictions/{prediction_id}/review")
def update_prediction_review(
    prediction_id: int,
    review_status: str | None = None,
    true_label: str | None = None,
    notes: str | None = None,
    db: Session = Depends(get_db)
):
    prediction = prediction_service.update_prediction_review(
        db=db,
        prediction_id=prediction_id,
        review_status=review_status,
        true_label=true_label,
        notes=notes
    )

    if prediction is None:
        raise HTTPException(
            status_code=404,
            detail="Prediction not found."
        )

    return {
        "id": prediction.id,
        "filename": prediction.filename,
        "predicted_class": prediction.predicted_class,
        "review_status": prediction.review_status,
        "true_label": prediction.true_label,
        "correct": prediction.correct,
        "notes": prediction.notes,
    }