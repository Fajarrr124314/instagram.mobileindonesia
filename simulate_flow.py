import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print('='*55)
print('  SIMULASI FULL FLOW RESET PASSWORD')
print('='*55)

from database import get_user_by_email
from token_manager import generate_reset_token, verify_reset_token, get_reset_link

email = 'fajarnf77@gmail.com'

# STEP 1 - Cek password awal
user = get_user_by_email(email)
print(f'[STEP 1] Password SEKARANG untuk {email}:')
print(f'         password = "{user["password"]}"')

# STEP 2 - Generate token (ini yang dikirim via email)
token = generate_reset_token(email)
link  = get_reset_link(token)
print(f'')
print(f'[STEP 2] Link reset dikirim ke email:')
print(f'         {link}')

# STEP 3 - Simulasi user klik link & verifikasi token
print(f'')
print(f'[STEP 3] User klik link, masuk halaman reset...')
verified_email = verify_reset_token(token)
print(f'         Token valid untuk: {verified_email}')

# STEP 4 - Update password
from database import update_password
new_pass = 'PasswordBaru2024'
update_password(email, new_pass)
print(f'')
print(f'[STEP 4] Password diupdate menjadi: "{new_pass}"')

# STEP 5 - Verifikasi perubahan di DB
user_updated = get_user_by_email(email)
print(f'')
print(f'[STEP 5] Cek users_db.json sekarang:')
print(f'         password = "{user_updated["password"]}" <<< BERHASIL BERUBAH!')

print()
print('Buka users_db.json untuk melihat perubahannya!')
print('='*55)

# Kembalikan ke semula untuk testing ulang
update_password(email, 'password123')
print(f'[INFO]  Password dikembalikan ke "password123" untuk testing ulang.')
