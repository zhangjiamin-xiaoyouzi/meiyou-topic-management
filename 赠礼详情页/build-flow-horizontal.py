import base64, os

assets = r'c:\Users\MeetYou\vscode-workspace\赠礼详情页\tapd-assets'
outpath = r'c:\Users\MeetYou\vscode-workspace\赠礼详情页\交互流程图-赠礼详情页-横向.html'

files = {
    'flow-01': 'flow-01-初始页面.png',
    'flow-02': 'flow-02-确认地址浮层.png',
    'flow-03': 'flow-03-二次确认弹窗.png',
    'flow-03a': 'flow-03a-地址选择页.png',
    'flow-04': 'flow-04-二次确认弹窗.png',
}

b64 = {}
for k, f in files.items():
    path = os.path.join(assets, f)
    with open(path, 'rb') as fh:
        b64[k] = base64.b64encode(fh.read()).decode('ascii')

html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>赠礼详情页 — 交互流程图（横向）</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, "Microsoft YaHei", "PingFang SC", sans-serif; background: #f0f2f5; color: #333; padding: 40px 20px; }}
.container {{ max-width: 1400px; margin: 0 auto; }}
h1 {{ text-align: center; font-size: 24px; margin-bottom: 8px; color: #1a1a1a; }}
.subtitle {{ text-align: center; font-size: 14px; color: #999; margin-bottom: 40px; }}

/* 横向流程容器 */
.flow-row {{ display: flex; align-items: flex-start; gap: 0; overflow-x: auto; padding: 20px 0; }}

/* 步骤卡片 */
.step-card {{ flex: 0 0 auto; width: 280px; background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; position: relative; }}
.step-header {{ display: flex; align-items: center; padding: 12px 14px; border-bottom: 1px solid #f0f0f0; }}
.step-num {{ width: 26px; height: 26px; border-radius: 50%; background: linear-gradient(135deg, #ff6b9d, #e91e63); color: #fff; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-right: 10px; }}
.step-num.branch {{ background: linear-gradient(135deg, #ff9800, #f57c00); }}
.step-title {{ font-weight: 600; font-size: 14px; color: #333; }}
.step-op {{ font-size: 11px; color: #999; margin-top: 2px; }}
.step-img {{ width: 100%; display: block; border: 0; }}
.step-desc {{ padding: 8px 14px; font-size: 12px; color: #666; background: #fafafa; border-top: 1px solid #f0f0f0; line-height: 1.5; }}

/* 箭头连接 */
.arrow-connector {{ flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 80px; padding: 40px 0; position: relative; }}
.arrow-right {{ font-size: 28px; color: #e91e63; animation: slideRight 1.5s infinite; }}
.arrow-label {{ font-size: 11px; color: #666; margin-top: 4px; text-align: center; white-space: nowrap; }}
@keyframes slideRight {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(6px); }} }}

/* 分支行 */
.branch-row {{ margin-top: 32px; }}
.branch-label {{ display: inline-block; font-size: 12px; color: #ff9800; font-weight: 600; padding: 4px 16px; background: #fff3e0; border-radius: 12px; margin-bottom: 16px; }}
.branch-flow {{ display: flex; align-items: flex-start; gap: 0; }}
.branch-arrow {{ flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 60px; padding: 30px 0; }}
.branch-arrow .arrow-right {{ color: #ff9800; animation: slideRightOrange 1.5s infinite; }}
@keyframes slideRightOrange {{ 0%,100% {{ transform: translateX(0); }} 50% {{ transform: translateX(6px); }} }}

/* 最终标识 */
.final-badge {{ display: flex; align-items: center; justify-content: center; padding: 16px; margin-top: 32px; }}
.final-badge span {{ background: #e8f5e9; color: #2e7d32; font-weight: 600; font-size: 14px; padding: 8px 20px; border-radius: 20px; }}

/* 图例 */
.legend {{ background: #fff; border-radius: 12px; padding: 20px 24px; margin-top: 32px; }}
.legend-title {{ font-size: 15px; font-weight: 600; margin-bottom: 12px; color: #333; }}
.legend-grid {{ display: flex; gap: 20px; flex-wrap: wrap; }}
.legend-item {{ display: flex; align-items: center; gap: 8px; }}
.legend-color {{ width: 20px; height: 20px; border-radius: 50%; flex-shrink: 0; }}
.legend-text {{ font-size: 12px; color: #666; }}
</style>
</head>
<body>
<div class="container">
<h1>🗺️ 赠礼详情页 — 交互流程图（横向）</h1>
<p class="subtitle">用户从"进入页面 → 领取赠礼 → 确认地址 → 已领取"的完整交互路径</p>

<!-- 主流程 -->
<div class="flow-row">
<!-- Step 1 -->
<div class="step-card">
<div class="step-header">
<div class="step-num">1</div>
<div><div class="step-title">初始页面</div><div class="step-op">浏览赠礼信息</div></div>
</div>
<img class="step-img" src="data:image/png;base64,{b64['flow-01']}" alt="初始页面" />
<div class="step-desc">💡 赠礼卡片 + 商品标题 + 「免费领取」按钮</div>
</div>

<!-- Arrow 1→2 -->
<div class="arrow-connector">
<span class="arrow-right">➤</span>
<div class="arrow-label">点击「免费领取」</div>
</div>

<!-- Step 2 -->
<div class="step-card">
<div class="step-header">
<div class="step-num">2</div>
<div><div class="step-title">确认地址浮层</div><div class="step-op">底部半屏面板</div></div>
</div>
<img class="step-img" src="data:image/png;base64,{b64['flow-02']}" alt="确认地址浮层" />
<div class="step-desc">💡 展示收货人/地址/手机号；可「修改」或「确认领取」</div>
</div>

<!-- Arrow 2→3 -->
<div class="arrow-connector">
<span class="arrow-right">➤</span>
<div class="arrow-label">点击「确认领取」</div>
</div>

<!-- Step 3 -->
<div class="step-card">
<div class="step-header">
<div class="step-num">3</div>
<div><div class="step-title">二次确认弹窗</div><div class="step-op">居中模态框</div></div>
</div>
<img class="step-img" src="data:image/png;base64,{b64['flow-03']}" alt="二次确认弹窗" />
<div class="step-desc">💡 提示「确认后地址不可修改」，需再次确认</div>
</div>

<!-- Arrow 3→4 -->
<div class="arrow-connector">
<span class="arrow-right">➤</span>
<div class="arrow-label">点击「确认」</div>
</div>

<!-- Step 4 -->
<div class="step-card">
<div class="step-header">
<div class="step-num">4</div>
<div><div class="step-title">已领取状态</div><div class="step-op">领取完成</div></div>
</div>
<img class="step-img" src="data:image/png;base64,{b64['flow-04']}" alt="已领取状态" />
<div class="step-desc">💡 按钮变灰 + 展示收货地址 + 物流信息</div>
</div>
</div>

<!-- 分支流程 -->
<div class="branch-row">
<div class="branch-label">🔀 分支：点击「修改」→ 地址选择页 → 返回确认浮层</div>
<div class="branch-flow">
<!-- Branch Step 3a -->
<div class="step-card">
<div class="step-header">
<div class="step-num branch">3a</div>
<div><div class="step-title">地址选择页</div><div class="step-op">独立页面</div></div>
</div>
<img class="step-img" src="data:image/png;base64,{b64['flow-03a']}" alt="地址选择页" />
<div class="step-desc">💡 展示地址列表，选中后自动回传至确认浮层</div>
</div>

<!-- Branch Arrow -->
<div class="branch-arrow">
<span class="arrow-right">➤</span>
<div class="arrow-label">选择地址后返回</div>
</div>

<!-- Back to Step 2 -->
<div class="step-card" style="opacity: 0.7;">
<div class="step-header">
<div class="step-num">2</div>
<div><div class="step-title">确认地址浮层</div><div class="step-op">更新后的地址</div></div>
</div>
<div style="padding: 40px; text-align: center; color: #999; font-size: 13px;">↩ 返回步骤 2<br/>继续主流程</div>
</div>
</div>
</div>

<div class="final-badge"><span>✅ 流程结束 — 用户成功领取赠礼，等待发货</span></div>

<!-- 图例 -->
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
<div class="legend-color" style="background: #ffc107;"></div>
<div class="legend-text"><strong>二次确认弹窗</strong><br/>防止误操作</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #4caf50;"></div>
<div class="legend-text"><strong>已领取状态</strong><br/>展示物流信息</div>
</div>
<div class="legend-item">
<div class="legend-color" style="background: #ff9800;"></div>
<div class="legend-text"><strong>地址选择页</strong><br/>独立页面，选择地址</div>
</div>
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
