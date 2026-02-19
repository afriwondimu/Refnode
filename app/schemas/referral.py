from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.referral import ReferralStatus

class ReferralCodeBase(BaseModel):
    code: str
    max_uses: Optional[int] = 1

class ReferralCodeCreate(BaseModel):
    max_uses: Optional[int] = 1
    expiry_days: Optional[int] = None

class ReferralCodeResponse(ReferralCodeBase):
    id: int
    user_id: int
    created_at: datetime
    expires_at: datetime
    is_active: bool
    times_used: int
    
    class Config:
        from_attributes = True

class ReferralResponse(BaseModel):
    id: int
    referral_code_id: int
    referrer_id: int
    referred_by_id: Optional[int] = None
    status: ReferralStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ReferralStats(BaseModel):
    total_referrals: int
    completed_referrals: int
    pending_referrals: int
    expired_referrals: int
    conversion_rate: float
    total_reward_points: int
    viral_coefficient: float

# Add this missing class
class UseReferralRequest(BaseModel):
    referral_code: str