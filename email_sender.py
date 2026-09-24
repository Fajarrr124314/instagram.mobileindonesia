"""
email_sender.py - Kirim email via SMTP dengan template gaya Instagram persis resmi
"""

import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from config import Config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HEADER_LOGO_PATH = os.path.join(BASE_DIR, 'instagram_header_logo.png')
META_LOGO_PATH = os.path.join(BASE_DIR, 'meta_footer_logo.png')


def build_email_html(to_email: str, user_name: str, reset_link: str, use_base64: bool = False) -> str:
    """
    Menghasilkan HTML email yang identik dengan email reset password resmi Instagram.
    """
    if use_base64:
        with open(HEADER_LOGO_PATH, 'rb') as f:
            header_src = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
        with open(META_LOGO_PATH, 'rb') as f:
            meta_src = f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    else:
        header_src = "cid:ig_header_logo"
        meta_src = "cid:meta_footer_logo"

    html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="id">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Atur ulang kata sandi Anda</title>
</head>
<body style="margin:0; padding:0; background-color:#ffffff; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; color:#262626; -webkit-font-smoothing:antialiased;">

  <!-- Outer container: full width white -->
  <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#ffffff; margin:0; padding:0;">
    <tr>
      <td align="center" style="padding: 20px 16px 40px 16px;">

        <!-- Main Content Wrapper: centered max 440px -->
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="max-width:440px; text-align:left; background-color:#ffffff;">

          <!-- Header: Logo IG (Kamera + Teks Instagram) di KIRI -->
          <tr>
            <td align="left" style="padding-top: 10px; padding-bottom: 24px; text-align:left;">
              <img src="{header_src}" width="115" height="32" alt="Instagram" style="display:block; border:0; outline:none; text-decoration:none;" />
            </td>
          </tr>

          <!-- Sapaan -->
          <tr>
            <td style="font-size:14px; line-height:20px; color:#262626; padding-bottom: 14px;">
              Hai {user_name},
            </td>
          </tr>

          <!-- Paragraf Penjelasan -->
          <tr>
            <td style="font-size:14px; line-height:20px; color:#262626; padding-bottom: 22px;">
              Maaf mendengar Anda mengalami kesulitan masuk ke Instagram. Kami menerima pesan bahwa Anda lupa kata sandi Anda. Jika ini terjadi pada Anda, Anda dapat langsung masuk kembali ke akun Anda atau mengatur ulang kata sandi Anda sekarang.
            </td>
          </tr>

          <!-- Tombol 1: Masuk sebagai {user_name} -->
          <tr>
            <td style="padding-bottom: 10px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center" style="background-color:#0095f6; border-radius:4px;">
                    <a href="{reset_link}" target="_blank"
                       style="display:block; padding:10px 16px; font-size:14px; font-weight:600; color:#ffffff; text-decoration:none; text-align:center; border-radius:4px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
                      Masuk sebagai {user_name}
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Tombol 2: Atur ulang kata sandi Anda -->
          <tr>
            <td style="padding-bottom: 24px;">
              <table width="100%" border="0" cellspacing="0" cellpadding="0">
                <tr>
                  <td align="center" style="background-color:#0095f6; border-radius:4px;">
                    <a href="{reset_link}" target="_blank"
                       style="display:block; padding:10px 16px; font-size:14px; font-weight:600; color:#ffffff; text-decoration:none; text-align:center; border-radius:4px; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
                      Atur ulang kata sandi Anda
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Paragraf Bantuan / Link Pelajari lebih lanjut -->
          <tr>
            <td style="font-size:14px; line-height:20px; color:#262626; padding-bottom: 18px;">
              Jika Anda tidak meminta tautan masuk atau pengaturan ulang kata sandi, Anda dapat mengabaikan pesan ini dan <a href="#" style="color:#0095f6; text-decoration:none;">mempelajari lebih lanjut tentang mengapa Anda mungkin menerimanya</a> .
            </td>
          </tr>

          <!-- Paragraf Keamanan -->
          <tr>
            <td style="font-size:14px; line-height:20px; color:#262626; padding-bottom: 36px;">
              Hanya orang yang mengetahui kata sandi Instagram Anda atau mengklik tautan masuk di email ini yang dapat masuk ke akun Anda.
            </td>
          </tr>

          <!-- Footer: from Meta -->
          <tr>
            <td align="center" style="text-align:center; padding-bottom: 2px;">
              <span style="font-size:11px; color:#8e8e8e; display:block; margin-bottom:4px;">from</span>
              <img src="{meta_src}" width="70" height="14" alt="Meta" style="display:inline-block; border:0; outline:none; margin-bottom:14px;" />
            </td>
          </tr>

          <!-- Footer: Copyright & Alamat -->
          <tr>
            <td align="center" style="text-align:center; font-size:11px; line-height:16px; color:#8e8e8e; padding-bottom: 4px;">
              &copy; Instagram. Meta Platforms, Inc., <a href="#" style="color:#8e8e8e; text-decoration:underline;">1601 Willow Road, Menlo Park, CA 94025</a>
            </td>
          </tr>

          <!-- Footer: Penerima & Hapus email -->
          <tr>
            <td align="center" style="text-align:center; font-size:11px; line-height:16px; color:#8e8e8e; padding-bottom: 24px;">
              Pesan ini dikirim ke <a href="mailto:{to_email}" style="color:#8e8e8e; text-decoration:underline;">{to_email}</a> dan ditujukan untuk {user_name}. Bukan profil Anda? <a href="#" style="color:#8e8e8e; text-decoration:underline;">Hapus email Anda</a> dari akun ini.
            </td>
          </tr>

          <!-- Garis Pemisah Bawah -->
          <tr>
            <td style="border-top: 1px solid #ebebeb; padding-top: 8px;"></td>
          </tr>

        </table>

      </td>
    </tr>
  </table>

</body>
</html>"""
    return html


def send_reset_email(to_email: str, user_name: str, reset_link: str) -> bool:
    """
    Kirim email reset password via SMTP dengan template gaya Instagram persis resmi.

    Args:
        to_email: Email tujuan
        user_name: Nama / username user (misal: fjrrnf_26)
        reset_link: URL link reset password

    Returns:
        True jika berhasil, False jika gagal
    """

    subject = "Atur ulang kata sandi Instagram Anda"

    html_body = build_email_html(to_email, user_name, reset_link, use_base64=False)

    text_body = f"""Hai {user_name},

Maaf mendengar Anda mengalami kesulitan masuk ke Instagram. Kami menerima pesan bahwa Anda lupa kata sandi Anda. Jika ini terjadi pada Anda, Anda dapat langsung masuk kembali ke akun Anda atau mengatur ulang kata sandi Anda sekarang.

Masuk sebagai {user_name}:
{reset_link}

Atur ulang kata sandi Anda:
{reset_link}

Jika Anda tidak meminta tautan masuk atau pengaturan ulang kata sandi, abaikan pesan ini.

Hanya orang yang mengetahui kata sandi Instagram Anda atau mengklik tautan masuk di email ini yang dapat masuk ke akun Anda.

from Meta
© Instagram. Meta Platforms, Inc., 1601 Willow Road, Menlo Park, CA 94025
Pesan ini dikirim ke {to_email} dan ditujukan untuk {user_name}.
"""

    # Buat container MIMEMultipart('related') untuk mendukung CID inline images
    msg_root = MIMEMultipart('related')
    msg_root['Subject'] = subject
    msg_root['From'] = f"Instagram <{Config.MAIL_DEFAULT_SENDER[1]}>"
    msg_root['To'] = to_email

    msg_alt = MIMEMultipart('alternative')
    msg_root.attach(msg_alt)

    msg_alt.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg_alt.attach(MIMEText(html_body, 'html', 'utf-8'))

    # Lampirkan logo header sebagai CID image
    if os.path.exists(HEADER_LOGO_PATH):
        try:
            with open(HEADER_LOGO_PATH, 'rb') as f:
                img_header = MIMEImage(f.read(), 'png')
                img_header.add_header('Content-ID', '<ig_header_logo>')
                img_header.add_header('Content-Disposition', 'inline', filename='instagram_header_logo.png')
                msg_root.attach(img_header)
        except Exception as e:
            print(f"[EMAIL WARNING] Gagal melampirkan header logo: {e}")

    # Lampirkan logo meta footer sebagai CID image
    if os.path.exists(META_LOGO_PATH):
        try:
            with open(META_LOGO_PATH, 'rb') as f:
                img_meta = MIMEImage(f.read(), 'png')
                img_meta.add_header('Content-ID', '<meta_footer_logo>')
                img_meta.add_header('Content-Disposition', 'inline', filename='meta_footer_logo.png')
                msg_root.attach(img_meta)
        except Exception as e:
            print(f"[EMAIL WARNING] Gagal melampirkan meta logo: {e}")

    # Kirim via SMTP
    try:
        print(f"[EMAIL] Menghubungi SMTP server: {Config.MAIL_SERVER}:{Config.MAIL_PORT}")

        if Config.MAIL_USE_TLS:
            server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
            server.ehlo()
            server.starttls()
            server.ehlo()
        else:
            server = smtplib.SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT)

        print(f"[EMAIL] Login sebagai: {Config.MAIL_USERNAME}")
        server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)

        print(f"[EMAIL] Mengirim email ke: {to_email}")
        server.sendmail(Config.MAIL_USERNAME, to_email, msg_root.as_string())
        server.quit()

        print(f"[EMAIL] Email berhasil dikirim ke {to_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("[EMAIL ERROR] Autentikasi gagal! Cek username/password SMTP.")
        return False
    except smtplib.SMTPConnectError:
        print("[EMAIL ERROR] Tidak bisa connect ke SMTP server!")
        return False
    except Exception as e:
        print(f"[EMAIL ERROR] Error: {e}")
        return False
