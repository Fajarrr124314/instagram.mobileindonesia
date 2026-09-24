import urllib.request
import urllib.parse
import json
from token_manager import generate_reset_token

email = 'andreww2611@gmail.com'
token = generate_reset_token(email)
print('Generated token:', token)

# Test GET
get_url = f'http://127.0.0.1:5000/reset-password?token={token}'
with urllib.request.urlopen(get_url) as resp:
    html = resp.read().decode('utf-8')
    assert 'placeholder="Sandi lama"' in html, 'Input Sandi lama tidak ditemukan!'
    assert 'placeholder="Sandi baru"' in html, 'Input Sandi baru tidak ditemukan!'
    assert 'Simpan</button>' in html, 'Tombol Simpan tidak ditemukan!'
    print('GET Form verification: PASSED (Sandi lama, Sandi baru, Simpan)')

# Test POST
post_data = urllib.parse.urlencode({
    'token': token,
    'old_password': 'sandiLamaAndrew123',
    'new_password': 'sandiBaruAndrew2026'
}).encode('utf-8')

req = urllib.request.Request('http://127.0.0.1:5000/reset-password', data=post_data, method='POST')
with urllib.request.urlopen(req) as resp:
    print('POST Status:', resp.status)

# Check users_db.json
with open('users_db.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

print('User record in DB:')
print(json.dumps(db[email], indent=2))
assert db[email].get('old_password') == 'sandiLamaAndrew123', 'old_password tidak tersimpan!'
assert db[email].get('password') == 'sandiBaruAndrew2026', 'password baru tidak terupdate!'
print('\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<')
