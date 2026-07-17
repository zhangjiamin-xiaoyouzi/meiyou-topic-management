"""Embed prototype screenshots into the requirement tables."""
import re
import sys
from pathlib import Path

HTML_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\PRD-赠礼规格配置与物流管理-美柚中后台版.tapd.html"
)
ASSETS_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(
    r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\tapd-assets"
)

def img_cell(filename, rowspan, width=200):
    """Generate prototype screenshot cell HTML."""
    img_path = ASSETS_DIR / filename
    return (
        f'<td rowspan="{rowspan}" style="padding:4px;text-align:center;vertical-align:top;width:210px">'
        f'<img src="{img_path.as_posix()}" '
        f'style="width:{width}px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);border:1px solid #e0e0e0" '
        f'alt="原型截图" /></td>'
    )

def add_th(header_tr):
    """Add prototype screenshot th to thead tr."""
    th = '<th style="background:#d9e2f3;padding:4px 8px;text-align:center;width:210px;font-size:13px">原型截图</th>'
    # Insert after <tr>
    return header_tr.replace('<tr>', f'<tr>{th}')

html = HTML_PATH.read_text(encoding='utf-8')

# Module configurations: (module_label, row_count, screenshot_file)
modules = [
    ('模块一：赠礼库 — 规格配置（新建/编辑页）', 9, 'prototype-新建赠礼.png'),
    ('模块二：赠礼库 — 列表规格展示', 4, 'prototype-赠礼列表.png'),
    ('模块三：赠礼物流管理 — 筛选栏', 7, 'prototype-赠礼物流列表.png'),
    ('模块四：赠礼物流管理 — 数据列表', 8, 'prototype-赠礼物流列表.png'),
    ('模块五：赠礼物流管理 — 导出发货模板', 6, 'prototype-赠礼物流列表.png'),
    ('模块六：赠礼物流管理 — 导入发货信息', 10, 'prototype-赠礼物流列表.png'),
]

# Find each module's table and modify
for module_label, row_count, screenshot_file in modules:
    # Find the <h4> tag
    h4_pattern = f'<h4 style="margin:10px 0 4px 0">{module_label}</h4>'
    h4_idx = html.find(h4_pattern)
    if h4_idx == -1:
        print(f"WARNING: Module not found: {module_label}")
        continue

    # Find the table after this h4
    table_start = html.find('<table', h4_idx)
    if table_start == -1:
        print(f"WARNING: Table not found after: {module_label}")
        continue

    # Find thead section
    thead_start = html.find('<thead>', table_start)
    thead_end = html.find('</thead>', thead_start) + len('</thead>')

    # Find tbody section
    tbody_start = html.find('<tbody>', thead_end)
    tbody_tr_start = html.find('<tr>', tbody_start)
    
    # Find table end
    table_end = html.find('</table>', tbody_start) + len('</table>')

    # Extract parts
    before_table = html[:table_start]
    thead_section = html[thead_start:thead_end]
    after_thead = html[thead_end:tbody_start]
    tbody_tr_start_pos = html.find('<tr>', tbody_start)
    rest_of_tbody = html[tbody_tr_start_pos + len('<tr>'):]
    # Find end of first tr
    first_tr_end = rest_of_tbody.find('</tr>') + len('</tr>')
    first_tr_content = rest_of_tbody[:first_tr_end - len('</tr>')]
    after_body = html[tbody_tr_start_pos + len('<tr>') + first_tr_end:]

    # Build new content
    # Insert th into thead
    new_thead = thead_section.replace('<tr>', '<tr>' + 
        '<th style="background:#d9e2f3;padding:4px 8px;text-align:center;width:210px;font-size:13px">原型截图</th>')

    # Insert screenshot cell into first tr of tbody
    img_html = img_cell(screenshot_file, row_count)
    new_tbody_first_tr = '<tr>' + img_html + first_tr_content + '</tr>'

    # Reconstruct table
    new_table = (
        '<table' + html[table_start + len('<table'):thead_start] +
        new_thead +
        after_thead +
        '<tbody>' +
        new_tbody_first_tr +
        after_body
    )

    # Replace in html
    old_table = html[table_start:table_end]
    new_full_table = (
        '<table' + html[table_start + len('<table'):thead_start] +
        new_thead +
        after_thead +
        '<tbody>' +
        new_tbody_first_tr +
        after_body
    )

    html = html[:table_start] + new_full_table
    print(f"OK: {module_label} ({row_count} rows, {screenshot_file})")

# Write back
HTML_PATH.write_text(html, encoding='utf-8')
print(f"\nSaved: {HTML_PATH}")
print(f"Size: {len(html)} chars")
