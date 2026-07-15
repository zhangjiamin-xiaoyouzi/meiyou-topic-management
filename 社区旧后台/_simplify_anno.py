import re, os

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

NEW_TH = (
    '<th>\n'
    '                    <button class="req-anno-btn" onclick="toggleReqAnno(this)" '
    'style="display:block;margin-bottom:4px">需求说明</button>\n'
    '                    <span class="required">*</span>话题标签\n'
    f'                    <div class="req-anno-box">{ANNO_TEXT}</div>\n'
    '                </th>'
)

NEW_TD = '''\
                <td>
                    <div style="margin-bottom:6px">
                        <label style="width:80px;display:inline-block;color:#555">话题特色：</label>
                        <label><input type="radio" value="1" name="topic_feature"> 特色</label>&nbsp;&nbsp;&nbsp;
                        <label><input type="radio" value="2" name="topic_feature"> 非特色</label>
                    </div>
                    <div style="margin-bottom:6px">
                        <label style="width:80px;display:inline-block;color:#555">话题频率：</label>
                        <label><input type="radio" value="1" name="topic_frequency"> 高频</label>&nbsp;&nbsp;&nbsp;
                        <label><input type="radio" value="2" name="topic_frequency"> 低频</label>
                    </div>
                    <div style="margin-bottom:6px">
                        <label style="width:80px;display:inline-block;color:#555">话题周期：</label>
                        <label><input type="radio" value="1" name="topic_cycle"> 长期</label>&nbsp;&nbsp;&nbsp;
                        <label><input type="radio" value="2" name="topic_cycle"> 短期</label>
                    </div>
                    <div>
                        <label style="width:80px;display:inline-block;color:#555">是否官方：</label>
                        <label><input type="radio" value="1" name="topic_official"> 官方</label>&nbsp;&nbsp;&nbsp;
                        <label><input type="radio" value="2" name="topic_official"> 非官方</label>
                    </div>
                </td>'''

for name in ['添加热议话题.html', '编辑话题.html']:
    path = os.path.join(base, name)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 替换 <th>
    html = html.replace(
        '<th><span class="required">*</span>话题标签</th>',
        NEW_TH, 1
    )

    # 替换整个 <td>（含所有子字段按钮和 anno-box）
    # 用正则匹配从 <td> 到对应 </td>（该 td 紧跟在话题标签 th 之后）
    td_pat = re.compile(
        r'(<td>\s*(?:<div[^>]*>.*?</div>\s*){4}</td>)',
        re.DOTALL
    )
    # 找到包含 topic_feature 的那个 td
    old_td = re.search(
        r'<td>(\s*<div[^>]*>.*?name="topic_official".*?</div>\s*)</td>',
        html, re.DOTALL
    )
    if old_td:
        html = html[:old_td.start()] + NEW_TD + html[old_td.end():]
        print(f'  {name}: td ✓')
    else:
        print(f'  WARN {name}: td not matched')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  {name}: th ✓')

print('Done.')
