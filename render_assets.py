import os
from playwright.sync_api import sync_playwright

with open('instagram_wordmark.svg', 'r', encoding='utf-8') as f:
    wordmark_svg = f.read()

# Tambahkan viewBox jika belum ada
if 'viewBox' not in wordmark_svg:
    wordmark_svg = wordmark_svg.replace('<svg ', '<svg viewBox="0 0 840 300" ')

header_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: #ffffff; display: inline-flex; align-items: center; }
  .box { display: inline-flex; align-items: center; gap: 8px; background: #ffffff; padding: 2px 0; }
  .cam { width: 28px; height: 28px; }
  .wordmark { height: 28px; display: flex; align-items: center; }
  .wordmark svg { height: 28px; width: auto; display: block; }
</style>
</head>
<body>
<div class="box">
  <svg class="cam" viewBox="0 0 24 24" fill="none" stroke="#000000" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
    <circle cx="12" cy="12" r="4.5"/>
    <circle cx="17.5" cy="6.5" r="1.2" fill="#000000" stroke="none"/>
  </svg>
  <div class="wordmark">
""" + wordmark_svg + """
  </div>
</div>
</body>
</html>"""

with open('temp_header.html', 'w', encoding='utf-8') as f:
    f.write(header_html)

with open('meta_logo.svg', 'r', encoding='utf-8') as f:
    meta_svg = f.read()

if 'viewBox' not in meta_svg:
    meta_svg = meta_svg.replace('<svg ', '<svg viewBox="0 0 948 191" ')

meta_html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; }
  body { margin: 0; padding: 0; background: #ffffff; display: inline-block; }
  .meta-box { height: 16px; display: inline-block; }
  .meta-box svg { height: 16px; width: auto; display: block; }
</style>
</head>
<body>
  <div class="meta-box">
""" + meta_svg + """
  </div>
</body>
</html>"""

with open('temp_meta.html', 'w', encoding='utf-8') as f:
    f.write(meta_html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(device_scale_factor=2)

    page.goto('file:///' + os.path.abspath('temp_header.html').replace('\\', '/'))
    box = page.query_selector('.box')
    box.screenshot(path='instagram_header_logo.png')

    page.goto('file:///' + os.path.abspath('temp_meta.html').replace('\\', '/'))
    meta_box = page.query_selector('.meta-box')
    meta_box.screenshot(path='meta_footer_logo.png')

    browser.close()

print('SUCCESS: Created instagram_header_logo.png and meta_footer_logo.png')
