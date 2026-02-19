from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class ReferralStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    EXPIRED = "expired"
    CANCELLED = "cancelled"

class ReferralCode(Base):
    __tablename__ = "referral_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    times_used = Column(Integer, default=0)
    max_uses = Column(Integer, default=1)
    
    user = relationship("User", back_populates="referral_codes")
    referrals = relationship("Referral", back_populates="referral_code")
    
    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
    
    @property
    def can_be_used(self):
        if not self.is_active or self.is_expired:
            return False
        if self.max_uses > 0 and self.times_used >= self.max_uses:
            return False
        return True

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referral_code_id = Column(Integer, ForeignKey("referral_codes.id"), nullable=False)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    referred_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(ReferralStatus), default=ReferralStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    referrer_reward_given = Column(Boolean, default=False)
    referred_reward_given = Column(Boolean, default=False)
    reward_points = Column(Integer, default=0)
    
    referral_code = relationship("ReferralCode", back_populates="referrals")
    referrer = relationship("User", foreign_keys=[referrer_id], back_populates="referrals_made")
    referred_by = relationship("User", foreign_keys=[referred_by_id], back_populates="referred_users")