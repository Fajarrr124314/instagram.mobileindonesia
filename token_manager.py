"""
token_manager.py - Manage token reset password
Pakai itsdangerous untuk generate token yang aman + expired otomatis
"""

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from config import Config

# Serializer untuk generate dan verify token
serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

def generate_reset_token(email: str) -> str:
    """
    Generate token reset password untuk email tertentu.
    Token otomatis expired setelah RESET_TOKEN_EXPIRY_SECONDS.
    """
    token = serializer.dumps(email, salt='password-reset-salt')
    print(f"[TOKEN] Generated token untuk: {email}")
    return token

def verify_reset_token(token: str) -> str | None:
    """
    Verifikasi token reset password.
    Return: email jika valid, None jika expired/invalid
    """
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=Config.RESET_TOKEN_EXPIRY_SECONDS
        )
        print(f"[TOKEN] Token valid untuk: {email}")
        return email
    except SignatureExpired:
        print(f"[TOKEN] Token sudah expired!")
        return None
    except BadSignature:
        print(f"[TOKEN] Token tidak valid / sudah digunakan!")
        return None
    except Exception as e:
        print(f"[TOKEN ERROR] {e}")
        return None

def get_reset_link(token: str) -> str:
    """Generate URL lengkap untuk reset password"""
    return f"{Config.APP_BASE_URL}/reset-password?token={token}"
