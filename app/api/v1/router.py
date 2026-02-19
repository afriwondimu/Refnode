from fastapi import APIRouter
from app.api.v1.endpoints import auth, referrals

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(referrals.router, prefix="/referrals", tags=["referrals"])