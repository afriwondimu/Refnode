import secrets
import string
import hashlib
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings

def generate_referral_code(user_id: int, length: Optional[int] = None, prefix: str = "") -> str:
    if length is None:
        length = settings.REFERRAL_CODE_LENGTH
    
    timestamp = datetime.utcnow().isoformat()
    random_bytes = secrets.token_bytes(16)
    hash_input = f"{user_id}-{timestamp}-{random_bytes}".encode()
    hash_hex = hashlib.sha256(hash_input).hexdigest()
    
    alphabet = string.ascii_uppercase + string.digits
    code_chars = []
    for i in range(length):
        index = int(hash_hex[i * 2:(i + 1) * 2], 16) % len(alphabet)
        code_chars.append(alphabet[index])
    
    code = ''.join(code_chars)
    return f"{prefix}{code}" if prefix else code

def calculate_expiry_date(days: Optional[int] = None) -> datetime:
    if days is None:
        days = settings.REFERRAL_EXPIRY_DAYS
    return datetime.utcnow() + timedelta(days=days)

def calculate_viral_coefficient(total_users: int, total_referrals: int) -> float:
    if total_users == 0:
        return 0.0
    avg_invites = 1.0
    conversion_rate = total_referrals / total_users if total_users > 0 else 0
    return round(avg_invites * conversion_rate, 3)