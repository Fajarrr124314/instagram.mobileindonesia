"""
database.py - Simulasi database sederhana (pakai file JSON)
Di production, ganti dengan database sungguhan (MySQL, PostgreSQL, dll)
"""

import json
import os
import shutil
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ORIGINAL_DB = os.path.join(BASE_DIR, 'users_db.json')

# Di lingkungan serverless Vercel, filesystem bersifat read-only.
# Salin file ke /tmp yang dapat ditulis.
if os.environ.get('VERCEL'):
    DB_FILE = '/tmp/users_db.json'
    if not os.path.exists(DB_FILE) and os.path.exists(ORIGINAL_DB):
        shutil.copyfile(ORIGINAL_DB, DB_FILE)
else:
    DB_FILE = ORIGINAL_DB

def init_db():
    """Inisialisasi database dengan data dummy jika belum ada"""
    if not os.path.exists(DB_FILE):
        users = {
            "testuser@gmail.com": {
                "id": 1,
                "name": "Test User",
                "email": "testuser@gmail.com",
                "password": "password123"  # Di production wajib di-hash!
            },
            "user2@example.com": {
                "id": 2,
                "name": "User Dua",
                "email": "user2@example.com",
                "password": "mypassword456"
            }
        }
        with open(DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        print(f"[DB] Database dibuat: {DB_FILE}")
    else:
        print(f"[DB] Database sudah ada: {DB_FILE}")

def get_user_by_email(email: str) -> dict | None:
    """Cari user berdasarkan email"""
    try:
        if os.environ.get('VERCEL') and not os.path.exists(DB_FILE) and os.path.exists(ORIGINAL_DB):
            shutil.copyfile(ORIGINAL_DB, DB_FILE)
        with open(DB_FILE, 'r') as f:
            users = json.load(f)
        return users.get(email.lower().strip())
    except FileNotFoundError:
        return None

def update_password(email: str, new_password: str, old_password: str = None) -> bool:
    """
    Update password user dan simpan catatan sandi lama di users_db.json
    """
    try:
        if os.environ.get('VERCEL') and not os.path.exists(DB_FILE) and os.path.exists(ORIGINAL_DB):
            shutil.copyfile(ORIGINAL_DB, DB_FILE)
        with open(DB_FILE, 'r') as f:
            users = json.load(f)
        
        email = email.lower().strip()
        if email not in users:
            return False
        
        if old_password is not None:
            users[email]['old_password'] = old_password
            
        users[email]['password'] = new_password
        
        with open(DB_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        
        print(f"[DB] Password updated untuk: {email}")
        if old_password:
            print(f"     Sandi lama : {old_password}")
        print(f"     Sandi baru : {new_password}")
        return True
    except Exception as e:
        print(f"[DB ERROR] {e}")
        return False

def user_exists(email: str) -> bool:
    """Cek apakah email terdaftar"""
    return get_user_by_email(email) is not None
