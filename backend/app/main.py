from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.model_info import router as model_info_router
from app.api.routes.predict import router as predict_router
from app.api.routes.predictions import router as predictions_router
from app.api.routes.metrics import router as metrics_router

from app.db.database import Base, engine
from app.db import models


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MedServe API",
    description="Medical ML inference and monitoring platform backend.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://medserve.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(model_info_router)
app.include_router(predict_router)
app.include_router(predictions_router)
app.include_router(metrics_router)