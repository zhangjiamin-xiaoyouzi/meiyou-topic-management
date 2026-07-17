"""Embed all images as base64 data URIs."""
import base64
import re
from pathlib import Path

HTML_PATH = Path(r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\PRD-赠礼规格配置与物流管理-美柚中后台版.tapd.html")
ASSETS_DIR = Path(r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\tapd-assets")

html = HTML_PATH.read_text(encoding='utf-8')

# Find all img src attributes that are NOT already base64
pattern = re.compile(r'src="(?!data:image)([^"]+)"')
matches = list(pattern.finditer(html))
print(f"Found {len(matches)} image references to convert")

for m in matches:
    src = m.group(1)
    # Try as absolute path or relative path
    img_path = Path(src)
    
    # Try treating as filename in assets dir
    if not img_path.exists():
        img_path = ASSETS_DIR / img_path.name
    
    if img_path.exists():
        b64 = base64.b64encode(img_path.read_bytes()).decode()
        new_src = f'data:image/png;base64,{b64}'
        html = html.replace(f'src="{src}"', f'src="{new_src}"')
        print(f"  OK: {img_path.name} ({len(b64)} chars)")
    else:
        print(f"  SKIP: {src} (file not found)")

HTML_PATH.write_text(html, encoding='utf-8')

# Verify
remaining = re.findall(r'src="(?!data:image)([^"]+)"', html)
if remaining:
    print(f"\nWARNING: {len(remaining)} non-base64 refs remain: {remaining}")
else:
    print(f"\nVERIFIED: All images are base64 encoded")
print(f"Final size: {len(html)} chars")
