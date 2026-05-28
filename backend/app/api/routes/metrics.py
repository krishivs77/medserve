from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.prediction_service import prediction_service


router = APIRouter()


@router.get("/metrics/summary")
def get_metrics_summary(
    db: Session = Depends(get_db)
):
    return prediction_service.get_summary_metrics(db)