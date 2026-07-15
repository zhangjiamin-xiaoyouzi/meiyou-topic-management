import json

cache = r'c:\Users\MeetYou\AppData\Roaming\Code\User\workspaceStorage\cf617ee12cd8aade66d3770bdfbabca7\GitHub.copilot-chat\chat-session-resources\baf9a33d-205e-4368-8c17-a3133c3256ea\toolu_bdrk_01PnoK7k6VPuFCpjhCtQ4bqg__vscode-1783580363494\content.txt'

with open(cache, encoding='utf-8') as f:
    raw = f.read().strip()[8:]
html = json.loads(raw)

# 找名称 th 行
idx = html.find('必填，新建时须明确标注')  # this should NOT be there yet
print('found anno:', idx)

# 找名称输入区域
idx2 = html.find('name="name"')
print('name input at:', idx2)
print(html[max(0,idx2-300):idx2+200])
