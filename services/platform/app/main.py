"""
Platform Services - Main Application Entry Point
Handles licensing, syllabus management, version control, and authentication.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from shared.database import get_db, Base, engine
from shared.database.models import (
    User, Role, Institution, License, Content, ContentVersion,
    Syllabus, AuditLog
)
from shared.auth.jwt_handler import (
    verify_password, get_password_hash, create_access_token,
    create_refresh_token, get_current_user, has_permission, ROLE_ADMIN
)
from shared.schemas.api_schemas import (
    UserCreate, UserLogin, TokenResponse, UserResponse,
    LicenseCreate, LicenseResponse, LicenseVerify, LicenseVerifyResponse,
    SyllabusCreate, SyllabusResponse, ContentCreate, ContentUpdate, ContentResponse,
    ApiResponse, ErrorResponse
)

# Create FastAPI application
app = FastAPI(
    title="VisualVerse Platform Services",
    description="Core platform functionality: Authentication, Licensing, Syllabus, Version Control",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ============== Database Initialization ==============

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    Base.metadata.create_all(bind=engine)


# ============== Authentication Endpoints ==============

@app.post("/api/v1/auth/register", response_model=TokenResponse, tags=["Authentication"])
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account.
    
    Creates a new user with the provided information and returns
    authentication tokens for immediate login.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Get default student role
    student_role = db.query(Role).filter(Role.name == "student").first()
    if not student_role:
        student_role = Role(name="student", description="Basic student role")
        db.add(student_role)
        db.commit()
    
    # Create user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        institution_id=user_data.institution_id,
        role_id=student_role.id,
        is_creator=user_data.is_creator,
        is_instructor=user_data.is_instructor,
        status="active"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create tokens
    token_data = {
        "sub": user.id,
        "email": user.email,
        "role": user.role.name if user.role else "student"
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": user.id})
    
    # Log registration
    audit = AuditLog(
        user_id=user.id,
        action="user_registered",
        resource_type="user",
        resource_id=str(user.id)
    )
    db.add(audit)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            status=user.status.value,
            institution_id=user.institution_id,
            role=user.role.name if user.role else "student",
            created_at=user.created_at,
            is_creator=user.is_creator,
            is_instructor=user.is_instructor
        )
    )


@app.post("/api/v1/auth/login", response_model=TokenResponse, tags=["Authentication"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return access tokens.
    
    Uses OAuth2 password flow for authentication.
    """
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not active"
        )
    
    # Update last login
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # Create tokens
    token_data = {
        "sub": user.id,
        "email": user.email,
        "role": user.role.name if user.role else "student",
        "institution_id": user.institution_id
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token({"sub": user.id})
    
    # Log login
    audit = AuditLog(
        user_id=user.id,
        action="user_login",
        resource_type="user",
        resource_id=str(user.id)
    )
    db.add(audit)
    db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            status=user.status.value,
            institution_id=user.institution_id,
            role=user.role.name if user.role else "student",
            created_at=user.created_at,
            is_creator=user.is_creator,
            is_instructor=user.is_instructor
        )
    )


@app.post("/api/v1/auth/refresh", response_model=TokenResponse, tags=["Authentication"])
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    """
    from shared.auth.jwt_handler import verify_refresh_token
    
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user or user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": user.id,
        "email": user.email,
        "role": user.role.name if user.role else "student",
        "institution_id": user.institution_id
    }
    new_access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token({"sub": user.id})
    
    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            status=user.status.value,
            institution_id=user.institution_id,
            role=user.role.name if user.role else "student",
            created_at=user.created_at,
            is_creator=user.is_creator,
            is_instructor=user.is_instructor
        )
    )


@app.get("/api/v1/auth/me", response_model=UserResponse, tags=["Authentication"])
async def get_current_user_info(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Get current authenticated user's information.
    """
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        status=user.status.value,
        institution_id=user.institution_id,
        role=user.role.name if user.role else "student",
        created_at=user.created_at,
        is_creator=user.is_creator,
        is_instructor=user.is_instructor
    )


# ============== License Management Endpoints ==============

@app.post("/api/v1/licenses", response_model=LicenseResponse, tags=["Licensing"])
async def create_license(
    license_data: LicenseCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new license (admin only).
    """
    if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can create licenses"
        )
    
    license = License(
        license_type=license_data.license_type,
        institution_id=license_data.institution_id,
        user_id=license_data.user_id,
        start_date=license_data.start_date,
        end_date=license_data.end_date,
        max_seats=license_data.max_seats,
        features=license_data.features
    )
    db.add(license)
    db.commit()
    db.refresh(license)
    
    return LicenseResponse(
        id=license.id,
        license_type=license.license_type.value,
        institution_id=license.institution_id,
        user_id=license.user_id,
        start_date=license.start_date,
        end_date=license.end_date,
        max_seats=license.max_seats,
        current_seats=license.current_seats,
        status=license.status,
        features=license.features,
        created_at=license.created_at
    )


@app.get("/api/v1/licenses/{license_id}", response_model=LicenseResponse, tags=["Licensing"])
async def get_license(
    license_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get license details by ID.
    """
    license = db.query(License).filter(License.id == license_id).first()
    if not license:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="License not found"
        )
    
    # Check if user has access to this license
    if current_user.get("role") != ROLE_ADMIN:
        if license.institution_id:
            user = db.query(User).filter(User.id == current_user["user_id"]).first()
            if user.institution_id != license.institution_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this license"
                )
    
    return LicenseResponse(
        id=license.id,
        license_type=license.license_type.value,
        institution_id=license.institution_id,
        user_id=license.user_id,
        start_date=license.start_date,
        end_date=license.end_date,
        max_seats=license.max_seats,
        current_seats=license.current_seats,
        status=license.status,
        features=license.features,
        created_at=license.created_at
    )


@app.post("/api/v1/licenses/verify", response_model=LicenseVerifyResponse, tags=["Licensing"])
async def verify_license_access(
    verify_data: LicenseVerify,
    db: Session = Depends(get_db)
):
    """
    Verify if a user has access to premium content/features.
    """
    valid = False
    license_type = None
    can_access_premium = False
    features = {}
    expires_at = None
    
    if verify_data.license_id:
        license = db.query(License).filter(License.id == verify_data.license_id).first()
        if license and license.status:
            now = datetime.utcnow()
            if license.start_date <= now <= license.end_date:
                valid = True
                license_type = license.license_type.value
                can_access_premium = True
                features = license.features or {}
                expires_at = license.end_date
                current_seats = license.current_seats or 0
                if current_seats < license.max_seats:
                    license.current_seats = current_seats + 1
                    db.commit()
    
    return LicenseVerifyResponse(
        valid=valid,
        license_type=license_type,
        can_access_premium=can_access_premium,
        features=features,
        expires_at=expires_at
    )


# ============== Syllabus Management Endpoints ==============

@app.post("/api/v1/syllabi", response_model=SyllabusResponse, tags=["Syllabus"])
async def create_syllabus(
    syllabus_data: SyllabusCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new syllabus/curriculum.
    """
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    syllabus = Syllabus(
        title=syllabus_data.title,
        description=syllabus_data.description,
        platform=syllabus_data.platform,
        institution_id=user.institution_id if user else None,
        is_public=syllabus_data.is_public,
        structure=syllabus_data.structure
    )
    db.add(syllabus)
    db.commit()
    db.refresh(syllabus)
    
    return SyllabusResponse(
        id=syllabus.id,
        title=syllabus.title,
        description=syllabus.description,
        platform=syllabus.platform,
        institution_id=syllabus.institution_id,
        is_public=syllabus.is_public,
        structure=syllabus.structure,
        created_at=syllabus.created_at,
        updated_at=syllabus.updated_at
    )


@app.get("/api/v1/syllabi", response_model=List[SyllabusResponse], tags=["Syllabus"])
async def list_syllabi(
    platform: Optional[str] = None,
    public_only: bool = True,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List available syllabi.
    """
    query = db.query(Syllabus)
    
    if public_only:
        query = query.filter(Syllabus.is_public == True)
    
    if platform:
        query = query.filter(Syllabus.platform == platform)
    
    syllabi = query.all()
    
    # Filter out non-public syllabi for non-admin users
    user = db.query(User).filter(User.id == current_user["user_id"]).first()
    if user and user.institution_id:
        # Also show institution-specific syllabi
        query = db.query(Syllabus).filter(
            (Syllabus.is_public == True) |
            (Syllabus.institution_id == user.institution_id)
        )
        if platform:
            query = query.filter(Syllabus.platform == platform)
        syllabi = query.all()
    
    return [
        SyllabusResponse(
            id=s.id,
            title=s.title,
            description=s.description,
            platform=s.platform,
            institution_id=s.institution_id,
            is_public=s.is_public,
            structure=s.structure,
            created_at=s.created_at,
            updated_at=s.updated_at
        )
        for s in syllabi
    ]


@app.get("/api/v1/syllabi/{syllabus_id}", response_model=SyllabusResponse, tags=["Syllabus"])
async def get_syllabus(
    syllabus_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get syllabus details by ID.
    """
    syllabus = db.query(Syllabus).filter(Syllabus.id == syllabus_id).first()
    if not syllabus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Syllabus not found"
        )
    
    # Check access
    if not syllabus.is_public:
        user = db.query(User).filter(User.id == current_user["user_id"]).first()
        if not user or user.institution_id != syllabus.institution_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this syllabus"
            )
    
    return SyllabusResponse(
        id=syllabus.id,
        title=syllabus.title,
        description=syllabus.description,
        platform=syllabus.platform,
        institution_id=syllabus.institution_id,
        is_public=syllabus.is_public,
        structure=syllabus.structure,
        created_at=syllabus.created_at,
        updated_at=syllabus.updated_at
    )


# ============== Content Version Control Endpoints ==============

@app.post("/api/v1/content", response_model=ContentResponse, tags=["Content"])
async def create_content(
    content_data: ContentCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create new educational content.
    """
    content = Content(
        title=content_data.title,
        description=content_data.description,
        content_type="animation",
        platform=content_data.platform,
        difficulty=content_data.difficulty,
        creator_id=current_user["user_id"],
        is_premium=content_data.is_premium,
        animation_script=content_data.animation_script,
        metadata=content_data.metadata
    )
    db.add(content)
    db.commit()
    db.refresh(content)
    
    # Create initial version
    version = ContentVersion(
        content_id=content.id,
        version=1,
        change_log="Initial version",
        animation_script=content_data.animation_script,
        created_by=current_user["user_id"]
    )
    db.add(version)
    db.commit()
    
    return ContentResponse(
        id=content.id,
        title=content.title,
        description=content.description,
        platform=content.platform,
        difficulty=content.difficulty.value,
        creator_id=content.creator_id,
        status=content.status.value,
        is_premium=content.is_premium,
        is_sample=content.is_sample,
        animation_output_url=content.animation_output_url,
        thumbnail_url=content.thumbnail_url,
        duration_seconds=content.duration_seconds,
        version=content.version,
        created_at=content.created_at,
        updated_at=content.updated_at
    )


@app.put("/api/v1/content/{content_id}", response_model=ContentResponse, tags=["Content"])
async def update_content(
    content_id: int,
    content_data: ContentUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update existing content (creates new version).
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    # Check ownership
    if content.creator_id != current_user["user_id"]:
        if not has_permission(current_user.get("role", ""), ROLE_ADMIN):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this content"
            )
    
    # Update fields
    if content_data.title:
        content.title = content_data.title
    if content_data.description:
        content.description = content_data.description
    if content_data.animation_script:
        # Create new version
        content.version += 1
        version = ContentVersion(
            content_id=content.id,
            version=content.version,
            change_log="Updated animation script",
            animation_script=content_data.animation_script,
            created_by=current_user["user_id"]
        )
        db.add(version)
        content.animation_script = content_data.animation_script
    if content_data.is_premium is not None:
        content.is_premium = content_data.is_premium
    if content_data.metadata:
        content.metadata = content_data.metadata
    
    content.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(content)
    
    return ContentResponse(
        id=content.id,
        title=content.title,
        description=content.description,
        platform=content.platform,
        difficulty=content.difficulty.value,
        creator_id=content.creator_id,
        status=content.status.value,
        is_premium=content.is_premium,
        is_sample=content.is_sample,
        animation_output_url=content.animation_output_url,
        thumbnail_url=content.thumbnail_url,
        duration_seconds=content.duration_seconds,
        version=content.version,
        created_at=content.created_at,
        updated_at=content.updated_at
    )


@app.get("/api/v1/content/{content_id}/versions", tags=["Content"])
async def get_content_versions(
    content_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get version history for content.
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Content not found"
        )
    
    versions = db.query(ContentVersion).filter(
        ContentVersion.content_id == content_id
    ).order_by(ContentVersion.version.desc()).all()
    
    return [
        {
            "version": v.version,
            "change_log": v.change_log,
            "created_at": v.created_at,
            "created_by": v.created_by
        }
        for v in versions
    ]


# ============== Health Check ==============

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for service monitoring.
    """
    return {"status": "healthy", "service": "platform"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
