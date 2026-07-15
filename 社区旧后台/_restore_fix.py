import json, re

base = r'c:\Users\MeetYou\vscode-workspace\社区旧后台'

ANNO_TEXT = '''【话题标签】必填，新增话题时须完整配置以下 4 个维度：

话题特色
· 特色：运营精选话题，推荐流中享有更高权重分发
· 非特色：普通话题，按正常权重分发

话题频率
· 高频：每周推送 ≥3 次，适合持续热点话题
· 低频：每周推送 ≤1 次，适合长尾或季节性话题

话题周期
· 长期：无明确下线时间，持续运营
· 短期：有明确截止日期，到期后自动降权或下线

是否官方
· 官方：由美柚官方创建或经认证的品牌/活动话题
· 非官方：用户自发创建或第三方话题'''

BTN = '<button class="req-anno-btn" onclick="toggleReqAnno(this)" style="display:block;margin-bottom:4px">需求说明</button>'

NEW_TH = (
    '<th>\n'
    f'                    {BTN}\n'
    '                    <span class="required">*</span>话题标签\n'
    f'                    <div class="req-anno-box">{ANNO_TEXT}</div>\n'
    '                </th>'
)

# 原始名称字段（从缓存提取）
NAME_ROW_ADD = '''            <tr>
                <th><span class="required">*</span>名称:</th>
                <td>
                    <div class="talk-tit">
                        <input type="text" name="name" class="form-control required text w300" value="" limit="60" id="title"> &nbsp;&nbsp;<span style="color: red;">不超出15个字（2个英文或数字算一个字）</span>
                </div>
                </td>
            </tr>'''

# 编辑页名称字段（从 edit 缓存提取）
cache_edit = r'c:\Users\MeetYou\AppData\Roaming\Code\User\workspaceStorage\cf617ee12cd8aade66d3770bdfbabca7\GitHub.copilot-chat\chat-session-resources\baf9a33d-205e-4368-8c17-a3133c3256ea\toolu_bdrk_01AFsZBdJuy8YNko2uXLbcDC__vscode-1783580363496\content.txt'
try:
    with open(cache_edit, encoding='utf-8') as f:
        raw_edit = f.read().strip()[8:]
    orig_edit = json.loads(raw_edit)
    idx_name = orig_edit.find('name="name"')
    # 取包围的 <tr>...</tr>
    tr_start = orig_edit.rindex('<tr>', 0, idx_name)
    tr_end   = orig_edit.index('</tr>', idx_name) + len('</tr>')
    NAME_ROW_EDIT = orig_edit[tr_start:tr_end]
    print('Edit name row extracted:', NAME_ROW_EDIT[:80])
except Exception as e:
    NAME_ROW_EDIT = NAME_ROW_ADD  # fallback
    print('Fallback to add row:', e)

# ── 修复两个文件 ─────────────────────────────────────────────────────
OLD_TH = '<th><span class="required">*</span>名称:</th>'

fixes = [
    ('添加热议话题.html', NAME_ROW_ADD),
    ('编辑话题.html',    NAME_ROW_EDIT),
]

for fname, name_row in fixes:
    path = f'{base}\\{fname}'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    if OLD_TH in html:
        # 替换错误的 th → 正确的话题标签 th（+名称行插在 td 后）
        # 找到 OLD_TH 在文件中的位置
        idx_th = html.index(OLD_TH)
        # 找对应的 </tr>（跳过 th 本身）
        idx_tr_end = html.index('</tr>', idx_th) + len('</tr>')

        old_tr = html[html.rindex('<tr>', 0, idx_th) : idx_tr_end]
        # 构建新 tr：只改 th，td 不变
        new_tr = old_tr.replace(OLD_TH, NEW_TH, 1)
        # 整体替换 + 在后面插入 名称行
        html = html[:html.rindex('<tr>', 0, idx_th)] + new_tr + '\n' + name_row + html[idx_tr_end:]
        print(f'  {fname}: fixed ✓')
    else:
        print(f'  WARN {fname}: OLD_TH not found')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)

print('Done.')
