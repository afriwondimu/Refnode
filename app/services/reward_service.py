from sqlalchemy.orm import Session
from app.models.user import User
from app.models.referral import Referral, ReferralStatus
from app.core.config import settings

class RewardService:
    def __init__(self, db: Session):
        self.db = db
    
    def credit_signup_reward(self, user: User) -> int:
        user.reward_points += settings.SIGNUP_REWARD_POINTS
        self.db.commit()
        return settings.SIGNUP_REWARD_POINTS
    
    def credit_referral_reward(self, referral: Referral) -> int:
        if referral.status != ReferralStatus.COMPLETED:
            return 0
        
        if not referral.referrer_reward_given:
            referrer = self.db.query(User).filter(User.id == referral.referrer_id).first()
            if referrer:
                referrer.reward_points += settings.REFERRER_REWARD_POINTS
                referral.referrer_reward_given = True
        
        if referral.referred_by_id and not referral.referred_reward_given:
            referred = self.db.query(User).filter(User.id == referral.referred_by_id).first()
            if referred:
                referred.reward_points += settings.SIGNUP_REWARD_POINTS
                referral.referred_reward_given = True
        
        self.db.commit()
        return settings.REFERRER_REWARD_POINTS
    
    def get_user_balance(self, user: User) -> int:
        return user.reward_points