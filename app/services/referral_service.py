from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import HTTPException, status

from app.models.user import User
from app.models.referral import ReferralCode, Referral, ReferralStatus
from app.schemas.referral import ReferralCodeCreate, ReferralStats
from app.utils.code_generator import generate_referral_code, calculate_expiry_date, calculate_viral_coefficient
from app.core.config import settings

class ReferralService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_referral_code(self, user: User, code_data: ReferralCodeCreate) -> ReferralCode:
        code = generate_referral_code(user.id)
        while self.db.query(ReferralCode).filter(ReferralCode.code == code).first():
            code = generate_referral_code(user.id)
        
        expiry_days = code_data.expiry_days or settings.REFERRAL_EXPIRY_DAYS
        expires_at = calculate_expiry_date(expiry_days)
        
        referral_code = ReferralCode(
            code=code,
            user_id=user.id,
            expires_at=expires_at,
            max_uses=code_data.max_uses,
            is_active=True
        )
        
        self.db.add(referral_code)
        self.db.commit()
        self.db.refresh(referral_code)
        return referral_code
    
    def get_user_referral_codes(self, user: User) -> List[ReferralCode]:
        return self.db.query(ReferralCode).filter(
            ReferralCode.user_id == user.id
        ).order_by(desc(ReferralCode.created_at)).all()
    
    def validate_referral_code(self, code: str) -> ReferralCode:
        referral_code = self.db.query(ReferralCode).filter(ReferralCode.code == code).first()
        
        if not referral_code:
            raise HTTPException(status_code=404, detail="Referral code not found")
        
        if not referral_code.can_be_used:
            if referral_code.is_expired:
                raise HTTPException(status_code=400, detail="Referral code expired")
            elif not referral_code.is_active:
                raise HTTPException(status_code=400, detail="Referral code inactive")
            else:
                raise HTTPException(status_code=400, detail="Referral code max uses reached")
        
        return referral_code
    
    def use_referral_code(self, code: str, new_user: User, ip_address=None, user_agent=None) -> Referral:
        referral_code = self.validate_referral_code(code)
        
        if referral_code.user_id == new_user.id:
            raise HTTPException(status_code=400, detail="Cannot use your own referral code")
        
        existing = self.db.query(Referral).filter(Referral.referred_by_id == new_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Already used a referral code")
        
        referral = Referral(
            referral_code_id=referral_code.id,
            referrer_id=referral_code.user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            status=ReferralStatus.PENDING
        )
        
        self.db.add(referral)
        self.db.commit()
        self.db.refresh(referral)
        return referral
    
    def complete_referral(self, referral_id: int, referred_user_id: int):
        referral = self.db.query(Referral).filter(Referral.id == referral_id).first()
        if not referral:
            raise HTTPException(status_code=404, detail="Referral not found")
        
        referral.status = ReferralStatus.COMPLETED
        referral.completed_at = datetime.utcnow()
        referral.referred_by_id = referred_user_id
        referral.referral_code.times_used += 1
        
        self.db.commit()
        return referral
    
    def get_user_referrals(self, user: User, status_filter=None, skip=0, limit=100) -> List[Referral]:
        query = self.db.query(Referral).filter(Referral.referrer_id == user.id)
        if status_filter:
            query = query.filter(Referral.status == status_filter)
        return query.order_by(desc(Referral.created_at)).offset(skip).limit(limit).all()
    
    def get_referral_stats(self, user: User) -> ReferralStats:
        referrals = self.db.query(Referral).filter(Referral.referrer_id == user.id).all()
        
        total = len(referrals)
        completed = sum(1 for r in referrals if r.status == ReferralStatus.COMPLETED)
        pending = sum(1 for r in referrals if r.status == ReferralStatus.PENDING)
        expired = sum(1 for r in referrals if r.status == ReferralStatus.EXPIRED)
        conversion_rate = (completed / total * 100) if total > 0 else 0
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent = self.db.query(Referral).filter(
            Referral.referrer_id == user.id,
            Referral.created_at >= thirty_days_ago,
            Referral.status == ReferralStatus.COMPLETED
        ).count()
        
        total_users = self.db.query(User).filter(User.created_at >= thirty_days_ago).count()
        viral_coefficient = calculate_viral_coefficient(total_users, recent)
        
        return ReferralStats(
            total_referrals=total,
            completed_referrals=completed,
            pending_referrals=pending,
            expired_referrals=expired,
            conversion_rate=round(conversion_rate, 2),
            total_reward_points=user.reward_points,
            viral_coefficient=viral_coefficient
        )