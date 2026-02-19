from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    reward_points = Column(Integer, default=0)
    
    referral_codes = relationship("ReferralCode", back_populates="user", cascade="all, delete-orphan")
    referred_users = relationship("Referral", foreign_keys="[Referral.referred_by_id]", back_populates="referred_by")
    referrals_made = relationship("Referral", foreign_keys="[Referral.referrer_id]", back_populates="referrer")