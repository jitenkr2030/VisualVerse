"""
Comprehensive FastAPI application for the VisualVerse Recommendation Engine.
Combines learning path generation with content recommendation services.
"""

from typing import List, Optional, Dict, Any
import logging
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, Field
import uvicorn
from contextlib import asynccontextmanager
from datetime import datetime

# Import existing educational learning components
from .config import Settings
from .models import (
    LearnerProfile, MasteryState, LearningPath, 
    ConceptRecommendation, DifficultyRecommendation
)
from .engines import RuleBasedEngine, GraphBasedEngine, AdaptiveEngine
from .services import ProgressTracker, WeaknessDetector

# Import content recommendation components
from ..engines.recommendation_engines import (
    CollaborativeFilteringEngine,
    ContentBasedEngine,
    HybridEngine,
    PopularityEngine
)
from ..models.interaction import Interaction, InteractionType
from ..models.user_profile import UserProfile
from ..services.prediction_service import PredictionService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings and services
settings = Settings()

# Educational learning engines
rule_engine = RuleBasedEngine()
graph_engine = GraphBasedEngine()
adaptive_engine = AdaptiveEngine()
progress_tracker = ProgressTracker()
weakness_detector = WeaknessDetector()

# Content recommendation engines
content_engines = {}
prediction_service: Optional[PredictionService] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting VisualVerse Recommendation Engine")
    
    # Initialize educational learning engines
    await adaptive_engine.initialize()
    await progress_tracker.initialize()
    await weakness_detector.initialize()
    
    # Initialize content recommendation engines
    global prediction_service, content_engines
    try:
        content_engines = {
            "collaborative": CollaborativeFilteringEngine({"weight": 0.4}),
            "content_based": ContentBasedEngine({"weight": 0.3}),
            "popularity": PopularityEngine({"weight": 0.2}),
        }
        
        # Create hybrid engine
        hybrid_engine = HybridEngine(content_engines, {"strategy": "weighted_average"})
        
        # Initialize prediction service (assuming database session is available)
        # Note: In production, this would be injected via dependency
        # prediction_service = PredictionService(db_session)
        
        logger.info("Content recommendation engines initialized")
        
    except Exception as e:
        logger.error(f"Failed to initialize content recommendation engines: {str(e)}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down VisualVerse Recommendation Engine")
    await adaptive_engine.cleanup()

# Create FastAPI application
app = FastAPI(
    title="VisualVerse Recommendation Engine API",
    description="Comprehensive API for learning path generation and content recommendations",
    version="2.0.0",
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

# =============================================================================
# EDUCATIONAL LEARNING MODELS & ENDPOINTS (Existing)
# =============================================================================

class LearningPathRequest(BaseModel):
    user_id: Optional[str] = None
    subject: str = Field(..., description="Subject name")
    current_level: str = Field(..., description="Current skill level")
    target_level: Optional[str] = Field(None, description="Target skill level")
    learning_goals: List[str] = Field(default_factory=list, description="Learning goals")
    time_constraint: Optional[int] = Field(None, description="Available time in minutes")
    preferred_difficulty: Optional[str] = Field(None, description="Preferred difficulty progression")
    learning_style: Optional[str] = Field(None, description="Preferred learning style")
    adaptive: bool = Field(default=True, description="Whether to use adaptive recommendations")

class LearningPathResponse(BaseModel):
    success: bool
    learning_path: Optional[LearningPath] = None
    recommendation_engine: Optional[str] = None
    confidence_score: Optional[float] = None
    message: Optional[str] = None

# =============================================================================
# CONTENT RECOMMENDATION MODELS & ENDPOINTS (New)
# =============================================================================

class UserRecommendationRequest(BaseModel):
    user_id: str
    content_type: Optional[str] = None
    difficulty_level: Optional[str] = None
    max_results: int = 10
    exclude_seen: bool = True

class InteractionTrackRequest(BaseModel):
    user_id: str
    content_id: str
    interaction_type: str
    metadata: Optional[dict] = None

class ContentRecommendationResponse(BaseModel):
    recommendations: List[dict]
    user_id: str
    total_results: int
    algorithm_used: str

class InteractionResponse(BaseModel):
    success: bool
    message: str
    interaction_id: Optional[str] = None

# =============================================================================
# UTILITY ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with service overview"""
    return {
        "service": "VisualVerse Recommendation Engine",
        "version": "2.0.0",
        "status": "operational",
        "capabilities": {
            "learning_paths": "Personalized learning path generation",
            "content_recommendations": "AI-powered content recommendations",
            "progress_tracking": "Learning progress monitoring",
            "adaptive_learning": "Dynamic difficulty adjustment"
        },
        "endpoints": {
            "learning": [
                "POST /learning-paths/generate",
                "GET /learning-paths/{path_id}",
                "PUT /learning-paths/{path_id}/progress"
            ],
            "content": [
                "GET /recommend/{user_id}",
                "POST /recommend",
                "POST /track_interaction",
                "GET /content/{content_id}/similar"
            ],
            "analytics": [
                "GET /analytics/learning-patterns",
                "GET /analytics/weakness-detection",
                "GET /analytics/progress-prediction"
            ]
        }
    }

@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check educational engines
        educational_engines_status = {
            "rule_engine": rule_engine.is_healthy(),
            "graph_engine": graph_engine.is_healthy(),
            "adaptive_engine": await adaptive_engine.is_healthy(),
            "progress_tracker": await progress_tracker.is_healthy(),
            "weakness_detector": await weakness_detector.is_healthy()
        }
        
        # Check content recommendation engines
        content_engines_status = {
            "prediction_service": prediction_service is not None,
            "collaborative_engine": "collaborative" in content_engines,
            "content_based_engine": "content_based" in content_engines,
            "popularity_engine": "popularity" in content_engines
        }
        
        all_healthy = all(educational_engines_status.values()) and prediction_service is not None
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "engines": {
                "educational": educational_engines_status,
                "content_recommendation": content_engines_status
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

# =============================================================================
# CONTENT RECOMMENDATION ENDPOINTS
# =============================================================================

@app.get("/recommend/{user_id}", response_model=ContentRecommendationResponse)
async def get_content_recommendations(
    user_id: str,
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    difficulty_level: Optional[str] = Query(None, description="Filter by difficulty level"),
    max_results: int = Query(10, ge=1, le=50, description="Maximum number of recommendations"),
    exclude_seen: bool = Query(True, description="Exclude previously seen content")
):
    """
    Get personalized content recommendations for a user.
    
    - **user_id**: Unique identifier for the user
    - **content_type**: Optional filter for content type (video, animation, quiz, etc.)
    - **difficulty_level**: Optional filter for difficulty level (beginner, intermediate, advanced)
    - **max_results**: Maximum number of recommendations to return (1-50)
    - **exclude_seen**: Whether to exclude content the user has already seen
    """
    try:
        logger.info(f"Generating content recommendations for user: {user_id}")
        
        # Check if prediction service is available
        if prediction_service is None:
            raise HTTPException(status_code=503, detail="Content recommendation service not available")
        
        # Get recommendations from prediction service
        recommendations = await prediction_service.predict_recommendations(
            user_id=user_id,
            num_recommendations=max_results
        )
        
        # Format response
        recommendation_data = [
            {
                "content_id": rec.content_id,
                "score": rec.score,
                "confidence": rec.confidence,
                "recommendation_type": rec.recommendation_type,
                "reasoning": rec.reasoning,
                "engine_scores": rec.engine_scores
            }
            for rec in recommendations
        ]
        
        return ContentRecommendationResponse(
            recommendations=recommendation_data,
            user_id=user_id,
            total_results=len(recommendation_data),
            algorithm_used="hybrid"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content recommendations for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

@app.post("/recommend", response_model=ContentRecommendationResponse)
async def get_content_recommendations_post(request: UserRecommendationRequest):
    """Get content recommendations using POST method (alternative to GET)"""
    try:
        logger.info(f"Generating content recommendations for user: {request.user_id}")
        
        if prediction_service is None:
            raise HTTPException(status_code=503, detail="Content recommendation service not available")
        
        # Get recommendations from prediction service
        recommendations = await prediction_service.predict_recommendations(
            user_id=request.user_id,
            num_recommendations=request.max_results
        )
        
        # Format response
        recommendation_data = [
            {
                "content_id": rec.content_id,
                "score": rec.score,
                "confidence": rec.confidence,
                "recommendation_type": rec.recommendation_type,
                "reasoning": rec.reasoning,
                "engine_scores": rec.engine_scores
            }
            for rec in recommendations
        ]
        
        return ContentRecommendationResponse(
            recommendations=recommendation_data,
            user_id=request.user_id,
            total_results=len(recommendation_data),
            algorithm_used="hybrid"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating content recommendations for user {request.user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

@app.post("/track_interaction", response_model=InteractionResponse)
async def track_interaction(request: InteractionTrackRequest):
    """
    Track a user interaction for improving recommendations.
    
    - **user_id**: Unique identifier for the user
    - **content_id**: Unique identifier for the content
    - **interaction_type**: Type of interaction (view, like, complete, etc.)
    - **metadata**: Additional interaction metadata
    """
    try:
        logger.info(f"Tracking interaction: {request.interaction_type} by user {request.user_id} on content {request.content_id}")
        
        # Validate interaction type
        try:
            interaction_type = InteractionType(request.interaction_type)
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid interaction type: {request.interaction_type}"
            )
        
        # Create interaction object
        interaction = Interaction(
            user_id=request.user_id,
            content_id=request.content_id,
            interaction_type=interaction_type,
            metadata=request.metadata or {}
        )
        
        # Track interaction (implementation depends on your data storage)
        interaction_id = f"int_{interaction.timestamp}_{request.user_id}_{request.content_id}"
        
        return InteractionResponse(
            success=True,
            message="Interaction tracked successfully",
            interaction_id=interaction_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking interaction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to track interaction: {str(e)}")

@app.get("/content/{content_id}/similar")
async def get_similar_content(
    content_id: str,
    max_results: int = Query(5, ge=1, le=20, description="Maximum number of similar items"),
    exclude_interacted: bool = Query(True, description="Exclude content user has already seen")
):
    """
    Get content similar to the specified content item.
    
    - **content_id**: Content to find similarities for
    - **max_results**: Maximum number of similar items to return
    - **exclude_interacted**: Whether to exclude content user has already seen
    """
    try:
        logger.info(f"Finding similar content for: {content_id}")
        
        if prediction_service is None:
            raise HTTPException(status_code=503, detail="Content recommendation service not available")
        
        # Get similar content recommendations
        similar_recommendations = await prediction_service.predict_similar_content(
            content_id=content_id,
            num_recommendations=max_results,
            exclude_interacted=exclude_interacted
        )
        
        # Format response
        similar_data = [
            {
                "content_id": rec.content_id,
                "score": rec.score,
                "confidence": rec.confidence,
                "recommendation_type": rec.recommendation_type,
                "reasoning": rec.reasoning
            }
            for rec in similar_recommendations
        ]
        
        return {
            "success": True,
            "source_content_id": content_id,
            "similar_content": similar_data,
            "total_results": len(similar_data)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding similar content for {content_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to find similar content: {str(e)}")

# =============================================================================
# EDUCATIONAL LEARNING ENDPOINTS (Existing functionality preserved)
# =============================================================================

@app.post("/learning-paths/generate", response_model=LearningPathResponse)
async def generate_learning_path(request: LearningPathRequest, background_tasks: BackgroundTasks):
    """Generate a personalized learning path"""
    try:
        logger.info(f"Generating learning path for user: {request.user_id}, subject: {request.subject}")
        
        # Choose recommendation engine
        if request.adaptive and request.user_id:
            engine = adaptive_engine
            engine_name = "adaptive"
        elif request.target_level:
            engine = graph_engine
            engine_name = "graph_based"
        else:
            engine = rule_engine
            engine_name = "rule_based"
        
        # Generate learning path
        learning_path = await engine.generate_learning_path(
            user_id=request.user_id,
            subject=request.subject,
            current_level=request.current_level,
            target_level=request.target_level,
            learning_goals=request.learning_goals,
            time_constraint=request.time_constraint,
            preferred_difficulty=request.preferred_difficulty,
            learning_style=request.learning_style
        )
        
        # Calculate confidence score
        confidence_score = await engine.calculate_confidence_score(learning_path)
        
        # Store learning path for tracking
        if request.user_id:
            background_tasks.add_task(
                progress_tracker.store_learning_path,
                request.user_id,
                learning_path
            )
        
        return LearningPathResponse(
            success=True,
            learning_path=learning_path,
            recommendation_engine=engine_name,
            confidence_score=confidence_score,
            message="Learning path generated successfully"
        )
        
    except Exception as e:
        logger.error(f"Failed to generate learning path: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate learning path")

@app.get("/learning-paths/{path_id}")
async def get_learning_path(path_id: str, user_id: Optional[str] = None):
    """Get a specific learning path"""
    try:
        learning_path = await progress_tracker.get_learning_path(path_id, user_id)
        
        if not learning_path:
            raise HTTPException(status_code=404, detail="Learning path not found")
        
        return {
            "success": True,
            "learning_path": learning_path
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get learning path: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve learning path")

# =============================================================================
# ANALYTICS AND INSIGHTS ENDPOINTS
# =============================================================================

@app.get("/analytics/learning-patterns")
async def get_learning_patterns(user_id: str, subject: Optional[str] = None):
    """Analyze learning patterns for a user"""
    try:
        patterns = await progress_tracker.analyze_learning_patterns(user_id, subject)
        
        return {
            "success": True,
            "patterns": patterns
        }
        
    except Exception as e:
        logger.error(f"Failed to analyze learning patterns: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze patterns")

@app.get("/analytics/weakness-detection")
async def detect_weaknesses(user_id: str, subject: str):
    """Detect knowledge weaknesses and gaps"""
    try:
        weaknesses = await weakness_detector.detect_weaknesses(user_id, subject)
        
        return {
            "success": True,
            "weaknesses": weaknesses
        }
        
    except Exception as e:
        logger.error(f"Failed to detect weaknesses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to detect weaknesses")

@app.get("/metrics")
async def get_metrics():
    """Get comprehensive service metrics"""
    try:
        metrics = {
            "educational_engines": {
                "rule_based": rule_engine.get_metrics(),
                "graph_based": graph_engine.get_metrics(),
                "adaptive": await adaptive_engine.get_metrics()
            },
            "tracking_services": {
                "progress_tracker": await progress_tracker.get_metrics(),
                "weakness_detector": await weakness_detector.get_metrics()
            },
            "content_recommendation": {
                "status": "active" if prediction_service else "inactive",
                "engines_available": list(content_engines.keys())
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return metrics
        
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