"""
config.py - Konfigurasi SMTP dan App
Ganti sesuai email provider kamu
"""

import os

class Config:
    # =========================================================
    # SECRET KEY - untuk keamanan token (ganti dengan string random)
    # =========================================================
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ganti-ini-dengan-secret-key-yang-kuat-2024')

    # =========================================================
    # KONFIGURASI SMTP EMAIL
    # Pilih salah satu provider di bawah dan uncomment
    # =========================================================

    # --- GMAIL (pakai App Password, bukan password biasa) ---
    # Cara dapat App Password Gmail:
    # 1. Buka https://myaccount.google.com/security
    # 2. Aktifkan 2-Step Verification
    # 3. Buka https://myaccount.google.com/apppasswords
    # 4. Buat App Password baru → copy 16 karakter (tanpa spasi)
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USE_SSL  = False
    MAIL_USERNAME = 'instagram.mobileindonesia@gmail.com'   # <-- ganti ini
    MAIL_PASSWORD = 'lvgggxpyzllrcusa'     # <-- ganti ini (tanpa spasi)

    # --- OUTLOOK / HOTMAIL ---
    # MAIL_SERVER   = 'smtp.office365.com'
    # MAIL_PORT     = 587
    # MAIL_USE_TLS  = True
    # MAIL_USERNAME = 'emailkamu@outlook.com'
    # MAIL_PASSWORD = 'password-kamu'

    # --- YAHOO ---
    # MAIL_SERVER   = 'smtp.mail.yahoo.com'
    # MAIL_PORT     = 587
    # MAIL_USE_TLS  = True
    # MAIL_USERNAME = 'emailkamu@yahoo.com'
    # MAIL_PASSWORD = 'app-password-yahoo'

    # --- MAILTRAP (untuk testing, tidak kirim email beneran) ---
    # Daftar gratis di https://mailtrap.io
    # MAIL_SERVER   = 'sandbox.smtp.mailtrap.io'
    # MAIL_PORT     = 587
    # MAIL_USE_TLS  = True
    # MAIL_USERNAME = 'username-mailtrap'
    # MAIL_PASSWORD = 'password-mailtrap'

    # Email pengirim
    MAIL_DEFAULT_SENDER = ('Reset Password App', MAIL_USERNAME)

    # =========================================================
    # TOKEN EXPIRY
    # =========================================================
    RESET_TOKEN_EXPIRY_SECONDS = 3600  # 1 jam

    # =========================================================
    # URL BASE APP (untuk link di email)
    # Otomatis mendeteksi domain Vercel atau domain custom
    # =========================================================
    _vercel_url = os.environ.get('VERCEL_URL')
    if _vercel_url:
        APP_BASE_URL = f"https://{_vercel_url}"
    else:
        APP_BASE_URL = os.environ.get('APP_BASE_URL', 'http://127.0.0.1:5000')
