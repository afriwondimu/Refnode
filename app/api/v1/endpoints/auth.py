from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from typing import Any

from app.core.database import get_db
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, LoginRequest
from app.services.referral_service import ReferralService
from app.services.reward_service import RewardService

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(request: Request, user_data: UserCreate, db: Session = Depends(get_db)) -> Any:
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = db.query(User).filter(User.username == user_data.username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    reward_service = RewardService(db)
    reward_service.credit_signup_reward(new_user)
    
    if user_data.referral_code:
        referral_service = ReferralService(db)
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent")
        referral = referral_service.use_referral_code(
            code=user_data.referral_code,
            new_user=new_user,
            ip_address=ip_address,
            user_agent=user_agent
        )
        referral_service.complete_referral(referral.id, new_user.id)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)) -> Any:
    user = db.query(User).filter(
        (User.username == login_data.username) | (User.email == login_data.username)
    ).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    user.last_login = datetime.utcnow()
    db.commit()
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)) -> Any:
    return current_user