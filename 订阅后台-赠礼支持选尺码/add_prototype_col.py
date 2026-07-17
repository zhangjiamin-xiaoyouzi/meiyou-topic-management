"""为需求说明表格添加原型截图列，并转 Base64"""
import base64
import re
from pathlib import Path

HTML_PATH = Path(r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\PRD-赠礼规格配置与物流管理-美柚中后台版.tapd.html")
ASSETS_DIR = Path(r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\tapd-assets")

html = HTML_PATH.read_text(encoding='utf-8')

# 模块与原型截图对照
module_images = {
    '模块一': 'prototype-新建赠礼.png',
    '模块二': 'prototype-赠礼列表.png',
    '模块三': 'prototype-赠礼物流列表.png',
    '模块四': 'prototype-赠礼物流列表.png',
    '模块五': 'prototype-赠礼物流列表.png',
    '模块六': 'prototype-赠礼物流列表.png',
    '模块七': 'prototype-赠礼物流列表.png',
}

# 每个模块的行数 (用于 rowspan)
module_rows = {
    '模块一': 8,
    '模块二': 4,
    '模块三': 6,
    '模块四': 6,
    '模块五': 6,
    '模块六': 10,
    '模块七': 4,
}

# 转 Base64
img_base64 = {}
for fname in set(module_images.values()):
    img_path = ASSETS_DIR / fname
    if img_path.exists():
        b64 = base64.b64encode(img_path.read_bytes()).decode()
        img_base64[fname] = f'data:image/png;base64,{b64}'
        print(f"  OK: {fname} ({len(b64)} chars)")

# 逐模块处理
for mod_name, img_file in module_images.items():
    rows = module_rows[mod_name]
    b64_data = img_base64[img_file]
    
    # 构造截图 cell
    img_cell = f'''<td rowspan="{rows}" style="padding:4px;text-align:center;vertical-align:top;width:210px"><img src="{b64_data}" style="width:200px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);border:1px solid #e0e0e0" alt="{mod_name}原型" /></td>'''
    
    # 表头：在 thead tr 最前面插入 th
    th_col = '<th style="background:#d9e2f3;padding:4px 8px;text-align:center;font-size:13px;width:210px">原型截图</th>'
    
    # 找到模块标题后面的表格
    pattern = re.compile(
        rf'(<h4 style="margin:10px 0 4px 0">{mod_name}：[^<]+</h4>\s*)'
        r'(<table[^>]*>)'
        r'(<thead><tr>)'
    )
    
    def replace_match(m):
        before = m.group(1)
        table_open = m.group(2)
        thead_tr = m.group(3)
        return f'{before}{table_open}{thead_tr}{th_col}'
    
    html = pattern.sub(replace_match, html, count=1)
    
    # tbody 首行 tr 最前面插入 td
    # 找到这个模块表格中 tbody 的第一个 <tr>
    # 使用更精确的定位：在模块标题后找 thead... 然后 tbody 的第一个 tr
    mod_pattern = re.compile(
        rf'({re.escape(mod_name)}：[^<]+</h4>\s*<table[^>]*>.*?</thead>\s*)<tbody><tr>',
        re.DOTALL
    )
    
    html = mod_pattern.sub(rf'\1<tbody><tr>{img_cell}', html, count=1)
    print(f"  Module {mod_name}: rowspan={rows}, image={img_file}")

HTML_PATH.write_text(html, encoding='utf-8')
print(f"\nDone. Final size: {len(html)} chars")
