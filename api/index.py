import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Add the parent directory to sys.path to allow absolute imports
# This is needed for Netlify and other deployment platforms
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.core.database import create_db_and_tables
from api.v1.router import api_router
from api.core.config import get_settings
from mangum import Mangum

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include routes WITHOUT /api prefix (Netlify redirect handles /api)
app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# Handler for serverless deployment (Netlify, AWS Lambda)
handler = Mangum(app)
