from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import traceback
from .database import init_db
from .routes import auth_routes, resume_routes, job_routes, match_routes
from .schemas import ErrorResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Resume-Job Matcher API",
    description="Refactored production-ready AI Matching System",
    version="2.0.0"
)

# 1. CORS Configuration (CRITICAL: Added before routers)
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

# 2. Database Initialization
@app.on_event("startup")
def startup_event():
    logger.info("Initializing database...")
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        logger.error(traceback.format_exc())

# 3. Exception Handlers (Ensures CORS headers are included in error responses)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "detail": str(exc.status_code)}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )

# 4. Include Routers
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