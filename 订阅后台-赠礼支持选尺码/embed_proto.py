#!/usr/bin/env python3
"""Embed prototype screenshots into the PRD HTML tables."""

import re

html_path = r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\PRD-赠礼规格配置与物流管理-美柚中后台版.tapd.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Module → (prototype_image, rowspan)
modules = [
    ("模块一：赠礼库 — 规格配置（新建/编辑页）", "prototype-新建赠礼.png", 8),
    ("模块二：赠礼库 — 列表规格展示", "prototype-赠礼列表.png", 4),
    ("模块三：赠礼物流管理 — 筛选栏", "prototype-赠礼物流列表.png", 7),
    ("模块四：赠礼物流管理 — 数据列表", "prototype-赠礼物流列表.png", 7),
    ("模块五：赠礼物流管理 — 导出发货模板", "prototype-赠礼物流列表.png", 6),
    ("模块六：赠礼物流管理 — 导入发货信息", "prototype-赠礼物流列表.png", 14),
    ("模块七：分页", "prototype-赠礼物流列表.png", 4),
]

asset_dir = r"c:\Users\MeetYou\vscode-workspace\订阅后台-赠礼支持选尺码\tapd-assets"
proto_th = '<th style="background:#d9e2f3;padding:4px 8px;text-align:center;font-size:13px;width:210px">原型截图</th>'

for mod_name, img_file, rowspan in modules:
    h4_pattern = re.escape(f'<h4 style="margin:10px 0 4px 0">{mod_name}</h4>')
    h4_match = re.search(h4_pattern, html)
    if not h4_match:
        print(f"  WARN: Module not found: {mod_name}")
        continue

    table_start = html.find("<table", h4_match.end())
    if table_start == -1:
        print(f"  WARN: No table after module: {mod_name}")
        continue
    table_end = html.find("</table>", table_start) + len("</table>")
    table_html = html[table_start:table_end]

    img_path = f"{asset_dir}\\{img_file}"
    img_td = (
        f'<td rowspan="{rowspan}" style="padding:4px;text-align:center;vertical-align:top;width:210px">'
        f'<img src="{img_path}" style="width:200px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);border:1px solid #e0e0e0" alt="{mod_name}原型" />'
        f'</td>'
    )

    # Insert proto_th into thead tr
    thead_tr = "<thead><tr>"
    idx_tr = table_html.find(thead_tr)
    if idx_tr == -1:
        print(f"  WARN: No <thead><tr> in table for {mod_name}")
        continue
    insert_pos = idx_tr + len(thead_tr)
    new_table = table_html[:insert_pos] + proto_th + table_html[insert_pos:]

    # Insert img_td into tbody first tr
    tbody_tr = "<tbody><tr>"
    idx_tbody_tr = new_table.find(tbody_tr)
    if idx_tbody_tr == -1:
        print(f"  WARN: No <tbody><tr> in table for {mod_name}")
        continue
    insert_pos2 = idx_tbody_tr + len(tbody_tr)
    new_table = new_table[:insert_pos2] + img_td + new_table[insert_pos2:]

    html = html[:table_start] + new_table + html[table_end:]
    print(f"  OK: {mod_name} (rowspan={rowspan}, img={img_file})")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\nDone. Wrote {html_path}")
