from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.model_info import router as model_info_router


app = FastAPI(
    title="MedServe API",
    description="Medical ML inference and monitoring platform backend.",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(model_info_router)