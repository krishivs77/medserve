from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.model_info import router as model_info_router
from app.api.routes.predict import router as predict_router
from app.api.routes.predictions import router as predictions_router

from app.db.database import Base, engine
from app.db import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MedServe API",
    description="Medical ML inference and monitoring platform backend.",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(model_info_router)
app.include_router(predict_router)
app.include_router(predictions_router)