from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.referral import (
    ReferralCodeCreate, ReferralCodeResponse, ReferralResponse,
    ReferralStats, UseReferralRequest
)
from app.services.referral_service import ReferralService

router = APIRouter()

@router.post("/code", response_model=ReferralCodeResponse)
async def create_referral_code(
    code_data: ReferralCodeCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = ReferralService(db)
    referral_code = service.create_referral_code(current_user, code_data)
    return referral_code

@router.get("/my-codes", response_model=List[ReferralCodeResponse])
async def get_my_referral_codes(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = ReferralService(db)
    return service.get_user_referral_codes(current_user)

@router.get("/my-referrals", response_model=List[ReferralResponse])
async def get_my_referrals(
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = ReferralService(db)
    return service.get_user_referrals(current_user, status, skip, limit)

@router.get("/stats", response_model=ReferralStats)
async def get_referral_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = ReferralService(db)
    return service.get_referral_stats(current_user)

@router.post("/use/{code}")
async def use_referral_code(
    code: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    service = ReferralService(db)
    referral = service.use_referral_code(code, current_user)
    return {"message": "Referral code applied successfully", "referral_id": referral.id}