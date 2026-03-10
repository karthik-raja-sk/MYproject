from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from .database import init_db
from .routes import auth_routes, resume_routes, job_routes, match_routes
from .schemas import ErrorResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume-Job Matcher API",
    description="Refactored production-ready AI Matching System",
    version="2.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
@app.on_event("startup")
def startup_event():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully")

# Include Routers
app.include_router(auth_routes.router)
app.include_router(resume_routes.router)
app.include_router(job_routes.router)
app.include_router(match_routes.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AI Resume-Job Matcher API v2",
        "status": "healthy"
    }

# Centralized Error Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return ErrorResponse(
        error=exc.detail,
        detail=str(exc.status_code)
    ).dict()