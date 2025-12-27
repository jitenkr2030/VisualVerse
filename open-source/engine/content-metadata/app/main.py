"""
Main application for VisualVerse Content Metadata Service.
Provides REST API for knowledge graph and curriculum management.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import logging
from contextlib import asynccontextmanager

from .database import init_database, close_database
from .routes import subjects, courses, concepts
from .config import Settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting VisualVerse Content Metadata Service")
    await init_database()
    yield
    # Shutdown
    logger.info("Shutting down VisualVerse Content Metadata Service")
    await close_database()

# Create FastAPI application
app = FastAPI(
    title="VisualVerse Content Metadata API",
    description="API for managing educational content metadata, knowledge graphs, and curriculum data",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(subjects.router, prefix="/api/v1/subjects", tags=["subjects"])
app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(concepts.router, prefix="/api/v1/concepts", tags=["concepts"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "VisualVerse Content Metadata API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "subjects": "/api/v1/subjects",
            "courses": "/api/v1/courses", 
            "concepts": "/api/v1/concepts"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        from .database import get_db
        async with get_db() as db:
            await db.run_query("MATCH (n) RETURN count(n) LIMIT 1")
        
        return {
            "status": "healthy",
            "service": "content-metadata",
            "version": "1.0.0",
            "timestamp": "2025-12-25T10:59:01Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/metrics")
async def get_metrics():
    """Get service metrics"""
    try:
        from .database import get_db
        async with get_db() as db:
            # Get basic metrics
            subject_count = await db.run_query("MATCH (s:Subject) RETURN count(s) as count")
            course_count = await db.run_query("MATCH (c:Course) RETURN count(c) as count")
            concept_count = await db.run_query("MATCH (k:Concept) RETURN count(k) as count")
            prerequisite_count = await db.run_query("MATCH ()-[r:PREREQUISITE]->() RETURN count(r) as count")
            
            return {
                "subjects": subject_count[0]["count"] if subject_count else 0,
                "courses": course_count[0]["count"] if course_count else 0,
                "concepts": concept_count[0]["count"] if concept_count else 0,
                "prerequisites": prerequisite_count[0]["count"] if prerequisite_count else 0,
                "timestamp": "2025-12-25T10:59:01Z"
            }
    except Exception as e:
        logger.error(f"Failed to get metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get metrics")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
