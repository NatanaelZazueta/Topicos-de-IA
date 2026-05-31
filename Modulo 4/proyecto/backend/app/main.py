from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import recognition, auth

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(recognition.router)

@app.get("/")
async def root():
    return {"app": settings.APP_NAME, "version": settings.VERSION, "status": "online"}