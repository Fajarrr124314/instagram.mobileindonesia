"""
test_flow.py - Test alur reset password TANPA browser
Jalankan ini untuk verifikasi semua komponen bekerja
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

print("\n" + "="*60)
print("  TESTING ALUR RESET PASSWORD")
print("="*60)

# ── TEST 1: Database ──────────────────────────────────────────
print("\n[TEST 1] Inisialisasi Database...")
from database import init_db, get_user_by_email, update_password, user_exists

init_db()

user = get_user_by_email("testuser@gmail.com")
assert user is not None, "FAIL: User tidak ditemukan!"
print(f"  ✅ User ditemukan: {user['name']} ({user['email']})")

not_found = get_user_by_email("tidakada@email.com")
assert not_found is None, "FAIL: Seharusnya None!"
print(f"  ✅ Email tidak terdaftar → None (benar)")


# ── TEST 2: Token Manager ─────────────────────────────────────
print("\n[TEST 2] Generate & Verify Token...")
from token_manager import generate_reset_token, verify_reset_token, get_reset_link

email_test = "testuser@gmail.com"
token = generate_reset_token(email_test)
print(f"  Token  : {token[:40]}...")

# Verify token valid
result = verify_reset_token(token)
assert result == email_test, f"FAIL: Expected {email_test}, got {result}"
print(f"  ✅ Token valid → email: {result}")

# Verify token tidak valid
bad_result = verify_reset_token("ini-token-palsu-12345")
assert bad_result is None, "FAIL: Seharusnya None untuk token palsu!"
print(f"  ✅ Token palsu → None (benar)")

# Generate reset link
link = get_reset_link(token)
print(f"  Reset Link: {link[:60]}...")
print(f"  ✅ Reset link berhasil dibuat")


# ── TEST 3: Update Password ───────────────────────────────────
print("\n[TEST 3] Update Password di Database...")
success = update_password("testuser@gmail.com", "newpassword999")
assert success == True, "FAIL: Update password gagal!"
print(f"  ✅ Password berhasil diupdate")

user_after = get_user_by_email("testuser@gmail.com")
assert user_after['password'] == "newpassword999", "FAIL: Password tidak terupdate!"
print(f"  ✅ Verifikasi password baru: {user_after['password']}")

# Restore ke password awal
update_password("testuser@gmail.com", "password123")
print(f"  ✅ Password dikembalikan ke semula")


# ── TEST 4: SMTP Email (opsional, perlu konfigurasi) ─────────
print("\n[TEST 4] SMTP Email Sender...")
print("  ⚠️  Test ini butuh konfigurasi SMTP di config.py")
print("  Apakah mau test kirim email sekarang? (y/n): ", end='')

try:
    answer = input().strip().lower()
except:
    answer = 'n'

if answer == 'y':
    from email_sender import send_reset_email
    from config import Config
    
    test_email = input("  Masukkan email tujuan test: ").strip()
    test_link = get_reset_link(token)
    
    print(f"  Mengirim ke {test_email}...")
    result = send_reset_email(test_email, "Test User", test_link)
    
    if result:
        print(f"  ✅ Email berhasil dikirim ke {test_email}!")
        print(f"  Cek inbox / spam kamu.")
    else:
        print(f"  ❌ Email gagal dikirim. Cek config.py")
        print(f"  Tips: Pastikan App Password Gmail sudah diset")
else:
    print("  ⏭️  Skip test email (konfigurasi SMTP dulu di config.py)")


# ── SUMMARY ──────────────────────────────────────────────────
print("\n" + "="*60)
print("  HASIL TEST:")
print("  ✅ Database  : OK")
print("  ✅ Token     : OK (generate + verify)")
print("  ✅ Password  : OK (update)")
print("  📧 Email     : Perlu konfigurasi SMTP di config.py")
print("="*60)

print("""
LANGKAH SELANJUTNYA:
1. Edit config.py → isi MAIL_USERNAME dan MAIL_PASSWORD
2. Jalankan: python app.py
3. Buka browser: http://127.0.0.1:5000/forgot-password
4. Masukkan email: testuser@gmail.com
5. Cek inbox email untuk link reset
6. Klik link → isi password baru → selesai!

Untuk testing tanpa email sungguhan, gunakan Mailtrap:
→ Daftar di https://mailtrap.io (gratis)
→ Copy SMTP credentials ke config.py
""")
