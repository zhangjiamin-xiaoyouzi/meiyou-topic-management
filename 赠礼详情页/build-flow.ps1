$assetsDir = "c:\Users\MeetYou\vscode-workspace\赠礼详情页\tapd-assets"
$outputPath = "c:\Users\MeetYou\vscode-workspace\赠礼详情页\交互流程图-赠礼详情页.html"

$b64 = @{}
@("flow-01-初始页面.png","flow-02-确认地址浮层.png","flow-03-二次确认弹窗.png","flow-03a-地址选择页.png","flow-04-二次确认弹窗.png") | ForEach-Object {
    $p = Join-Path $assetsDir $_
    if (Test-Path $p) { $b64[$_] = [Convert]::ToBase64String([IO.File]::ReadAllBytes($p)) }
    Write-Output "$_ loaded: $([Math]::Round($b64[$_].Length/1024))KB"
}

$html = @"
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>赠礼详情页 — 交互流程图</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: -apple-system, "Microsoft YaHei", "PingFang SC", sans-serif; background: #f0f2f5; color: #333; padding: 40px 20px; }
.container { max-width: 480px; margin: 0 auto; }
h1 { text-align: center; font-size: 22px; margin-bottom: 8px; color: #1a1a1a; }
.subtitle { text-align: center; font-size: 13px; color: #999; margin-bottom: 32px; }

.step { position: relative; margin-bottom: 0; }
.step:last-child .step-connector { display: none; }
.step-body { background: #fff; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.08); overflow: hidden; position: relative; z-index: 1; }
.step-header { display: flex; align-items: center; padding: 14px 16px; border-bottom: 1px solid #f0f0f0; }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, #ff6b9d, #e91e63); color: #fff; font-size: 14px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-right: 12px; }
.step-num.branch { background: linear-gradient(135deg, #ff9800, #f57c00); }
.step-title { font-weight: 600; font-size: 15px; color: #333; }
.step-op { font-size: 12px; color: #999; margin-top: 2px; }
.step-img { width: 100%; display: block; border: 0; }
.step-desc { padding: 10px 16px; font-size: 13px; color: #666; background: #fafafa; border-top: 1px solid #f0f0f0; line-height: 1.6; }

.step-connector { display: flex; align-items: center; justify-content: center; padding: 10px 0; position: relative; z-index: 0; }
.arrow-down { width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; color: #e91e63; font-size: 24px; animation: bounce 1.5s infinite; }
.arrow-label { font-size: 12px; color: #666; margin: 0 8px; text-align: center; }
@keyframes bounce { 0%,100% { transform: translateY(0); } 50% { transform: translateY(4px); } }

.branch-section { margin-top: 16px; }
.branch-label-row { text-align: center; margin-bottom: 12px; }
.branch-label { font-size: 12px; color: #ff9800; font-weight: 600; padding: 4px 16px; background: #fff3e0; border-radius: 12px; display: inline-block; }

.final-badge { display: flex; align-items: center; justify-content: center; padding: 12px; margin-top: 24px; }
.final-badge span { background: #e8f5e9; color: #2e7d32; font-weight: 600; font-size: 13px; padding: 6px 16px; border-radius: 16px; }
</style>
</head>
<body>
<div class="container">
<h1>🗺️ 赠礼详情页 — 交互流程图</h1>
<p class="subtitle">用户从进入页面 → 领取赠礼 → 确认地址 → 已领取的完整交互路径</p>

<!-- Step 1 -->
<div class="step">
<div class="step-body">
<div class="step-header">
<div class="step-num">1</div>
<div><div class="step-title">初始页面</div><div class="step-op">用户进入赠礼详情页，浏览赠礼信息</div></div>
</div>
<img class="step-img" src="data:image/png;base64,FLOW_01_PLACEHOLDER" alt="初始页面" />
<div class="step-desc">💡 页面展示赠礼卡片、商品标题、「免费领取」按钮和使用须知</div>
</div>
<div class="step-connector">
<span class="arrow-down">⬇</span>
<div class="arrow-label">点击「免费领取」</div>
<span class="arrow-down">⬇</span>
</div>
</div>

<!-- Step 2 -->
<div class="step">
<div class="step-body">
<div class="step-header">
<div class="step-num">2</div>
<div><div class="step-title">确认地址浮层</div><div class="step-op">底部弹出半屏面板，用户确认收货地址</div></div>
</div>
<img class="step-img" src="data:image/png;base64,FLOW_02_PLACEHOLDER" alt="确认地址浮层" />
<div class="step-desc">💡 展示收货人、手机号、详细地址；用户可「修改」地址或「确认领取」</div>
</div>
<div class="step-connector">
<span class="arrow-label" style="color:#e91e63;">点击「确认领取」→</span>
<span style="margin:0 4px;font-size:16px;">&nbsp;</span>
<span class="arrow-label" style="color:#ff9800;">→ 点击「修改」</span>
</div>
</div>

<!-- 分支：Step 3a -->
<div class="branch-section">
<div class="branch-label-row"><span class="branch-label">🔀 分支：点击「修改」→ 地址选择页</span></div>
<div class="step">
<div class="step-body">
<div class="step-header">
<div class="step-num branch">3a</div>
<div><div class="step-title">地址选择页（独立页面）</div><div class="step-op">选择地址后自动返回详情页</div></div>
</div>
<img class="step-img" src="data:image/png;base64,FLOW_03A_PLACEHOLDER" alt="地址选择页" />
<div class="step-desc">💡 展示用户已有地址列表，选中后自动回传至详情页确认浮层</div>
</div>
<div class="step-connector">
<span class="arrow-down" style="color:#ff9800;">⬇</span>
<div class="arrow-label" style="color:#ff9800;">选择地址 → 返回确认浮层</div>
<span class="arrow-down" style="color:#ff9800;">⬇</span>
</div>
</div>
</div>

<!-- Step 3 -->
<div class="step">
<div class="step-body">
<div class="step-header">
<div class="step-num">3</div>
<div><div class="step-title">二次确认弹窗</div><div class="step-op">居中模态框，防止误操作的最后确认</div></div>
</div>
<img class="step-img" src="data:image/png;base64,FLOW_03_PLACEHOLDER" alt="二次确认弹窗" />
<div class="step-desc">💡 居中模态框提示「确认后地址不可修改」，用户需再次点击确认</div>
</div>
<div class="step-connector">
<span class="arrow-down">⬇</span>
<div class="arrow-label">点击「确认」</div>
<span class="arrow-down">⬇</span>
</div>
</div>

<!-- Step 4 -->
<div class="step">
<div class="step-body">
<div class="step-header">
<div class="step-num">4</div>
<div><div class="step-title">已领取状态</div><div class="step-op">领取完成，展示收货地址与物流信息</div></div>
</div>
<img class="step-img" src="data:image/png;base64,FLOW_04_PLACEHOLDER" alt="已领取状态" />
<div class="step-desc">💡 「免费领取」变为灰色「已领取」；展示收货地址；物流区显示「等待发货」状态</div>
</div>
</div>

<div class="final-badge"><span>✅ 流程结束 — 用户成功领取赠礼，等待发货</span></div>

</div>
</body>
</html>
"@

# Replace placeholders
$html = $html.Replace("FLOW_01_PLACEHOLDER", $b64["flow-01-初始页面.png"])
$html = $html.Replace("FLOW_02_PLACEHOLDER", $b64["flow-02-确认地址浮层.png"])
$html = $html.Replace("FLOW_03A_PLACEHOLDER", $b64["flow-03a-地址选择页.png"])
$html = $html.Replace("FLOW_03_PLACEHOLDER", $b64["flow-03-二次确认弹窗.png"])
$html = $html.Replace("FLOW_04_PLACEHOLDER", $b64["flow-04-二次确认弹窗.png"])

$html | Out-File -FilePath $outputPath -Encoding UTF8
Write-Output "Done! File saved: $outputPath"
Write-Output "File size: $([Math]::Round((Get-Item $outputPath).Length/1024))KB"
