import base64, os

assets = r'c:\Users\MeetYou\vscode-workspace\赠礼详情页\tapd-assets'
outpath = r'c:\Users\MeetYou\vscode-workspace\赠礼详情页\交互流程图-赠礼详情页-Mermaid.html'

# 读取 Mermaid 流程图
mermaid_path = os.path.join(assets, 'flow-mermaid.png')
with open(mermaid_path, 'rb') as f:
    mermaid_b64 = base64.b64encode(f.read()).decode('ascii')

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>赠礼详情页 — 交互流程图（Mermaid）</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, "Microsoft YaHei", "PingFang SC", sans-serif; background: #f0f2f5; color: #333; padding: 40px 20px; }}
.container {{ max-width: 900px; margin: 0 auto; }}
h1 {{ text-align: center; font-size: 24px; margin-bottom: 8px; color: #1a1a1a; }}
.subtitle {{ text-align: center; font-size: 14px; color: #999; margin-bottom: 32px; }}

.flow-card {{ background: #fff; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); overflow: hidden; margin-bottom: 24px; }}
.flow-header {{ padding: 20px 24px; border-bottom: 1px solid #f0f0f0; }}
.flow-title {{ font-size: 18px; font-weight: 600; color: #e91e63; margin-bottom: 4px; }}
.flow-desc {{ font-size: 13px; color: #666; }}
.flow-img {{ width: 100%; display: block; }}

.legend {{ background: #fff; border-radius: 12px; padding: 20px 24px; margin-top: 24px; }}
.legend-title {{ font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #333; }}
.legend-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }}
.legend-item {{ display: flex; align-items: center; gap: 10px; }}
.legend-color {{ width: 24px; height: 24px; border-radius: 6px; flex-shrink: 0; }}
.legend-text {{ font-size: 13px; color: #666; }}

.note {{ background: #fff3e0; border-left: 4px solid #ff9800; padding: 12px 16px; margin-top: 24px; border-radius: 0 8px 8px 0; }}
.note-title {{ font-weight: 600; color: #e65100; margin-bottom: 4px; font-size: 14px; }}
.note-text {{ font-size: 13px; color: #666; line-height: 1.6; }}
</style>
</head>
<body>
<div class="container">
<h1>🗺️ 赠礼详情页 — 交互流程图</h1>
<p class="subtitle">用户从"进入页面 → 领取赠礼 → 确认地址 → 已领取"的完整交互路径</p>

<div class="flow-card">
<div class="flow-header">
<div class="flow-title">📊 用户操作流程</div>
<div class="flow-desc">展示用户在赠礼详情页的完整操作路径，包含主流程和分支流程</div>
</div>
<img class="flow-img" src="data:image/png;base64,{mermaid_b64}" alt="交互流程图" />
</div>

<div class="legend">
<div class="legend-title">📋 流程节点说明</div>
<div class="legend-grid">
<div class="legend-item">
<div class="legend-color" style="background: #e91e63;"></div>
<div class="legend-text"><strong>初始页面</strong><br/>赠礼卡片 + 免费领取按钮</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #ff6b9d;"></div>
<div class="legend-text"><strong>确认地址浮层</strong><br/>展示收货地址信息</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #ff9800;"></div>
<div class="legend-text"><strong>地址选择页</strong><br/>独立页面，选择地址</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #ffc107;"></div>
<div class="legend-text"><strong>二次确认弹窗</strong><br/>防止误操作</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #4caf50;"></div>
<div class="legend-text"><strong>已领取状态</strong><br/>展示物流信息</div>
</div>
</div>
</div>

<div class="note">
<div class="note-title">💡 流程说明</div>
<div class="note-text">
<strong>主流程：</strong>初始页面 → 点击「免费领取」→ 确认地址浮层 → 点击「确认领取」→ 二次确认弹窗 → 已领取状态<br/><br/>
<strong>分支流程：</strong>在确认地址浮层点击「修改」→ 跳转地址选择页 → 选择地址后返回确认浮层 → 继续主流程
</div>
</div>

</div>
</body>
</html>'''

with open(outpath, 'w', encoding='utf-8') as f:
    f.write(html)

size_kb = os.path.getsize(outpath) / 1024
print(f'Done! Saved to: {outpath}')
print(f'Size: {size_kb:.0f} KB')
