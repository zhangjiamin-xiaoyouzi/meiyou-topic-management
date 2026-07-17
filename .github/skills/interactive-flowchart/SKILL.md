---
name: interactive-flowchart
description: 生成交互式流程图文档，支持横向/纵向布局，内嵌原型截图，适用于产品交互流程可视化展示。
metadata:
  short-description: 生成交互式流程图（横向/纵向），内嵌原型截图，支持分支流程展示
---

# 交互流程图生成器

## 概述

本 skill 用于生成产品交互流程图，将用户操作流程可视化为带截图的流程图文档。支持两种布局：

- **横向布局**：步骤从左到右排列，适合流程较短、分支较少的场景
- **纵向布局**：步骤从上到下排列，适合流程较长、需要详细说明的场景

输出格式：**HTML 文件**，所有图片内嵌为 Base64，可直接复制到 TAPD 等需求管理平台。

## 使用场景

- 产品需求文档中的交互流程展示
- 原型设计评审时的流程可视化
- 开发团队理解用户操作路径
- 需求评审会议中的流程演示

## 文档结构

### 标题格式
`{产品名称} — 交互流程图`

### 主流程区域
| 元素 | 说明 |
|------|------|
| 步骤卡片 | 包含步骤编号、标题、操作说明、原型截图、详细说明 |
| 箭头连接 | 步骤间的操作说明，带动画效果 |
| 步骤编号 | 圆形徽章，主流程用粉色渐变，分支用橙色渐变 |

### 分支流程区域（可选）
| 元素 | 说明 |
|------|------|
| 分支标签 | 橙色标签，说明分支触发条件 |
| 分支步骤 | 独立步骤卡片，编号带字母后缀（如 3a） |
| 返回指示 | 说明分支如何回到主流程 |

### 图例区域
| 元素 | 说明 |
|------|------|
| 颜色图例 | 各步骤节点颜色含义说明 |
| 流程说明 | 主流程和分支流程的文字描述 |

## 生成步骤

### Step 1: 准备原型截图

1. 使用 Playwright 打开原型页面
2. 按流程顺序截图，保存到 `tapd-assets/` 目录
3. 命名规范：`flow-{步骤号}-{页面名称}.png`
   - 示例：`flow-01-初始页面.png`、`flow-02-确认地址浮层.png`
4. 分支流程截图命名：`flow-{步骤号}{字母}-{页面名称}.png`
   - 示例：`flow-03a-地址选择页.png`

### Step 2: 转换图片为 Base64

使用 Python 脚本将所有流程截图转换为 Base64 编码：

```python
import base64, os

assets = r'{项目路径}\tapd-assets'
files = {
    'flow-01': 'flow-01-初始页面.png',
    'flow-02': 'flow-02-确认地址浮层.png',
    # ... 更多文件
}

b64 = {}
for k, f in files.items():
    path = os.path.join(assets, f)
    with open(path, 'rb') as fh:
        b64[k] = base64.b64encode(fh.read()).decode('ascii')
```

### Step 3: 生成 HTML 文档

#### 横向布局模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{产品名称} — 交互流程图（横向）</title>
<style>
/* 横向流程样式 */
.flow-row {{ display: flex; align-items: flex-start; gap: 0; overflow-x: auto; }}
.step-card {{ flex: 0 0 auto; width: 280px; background: #fff; border-radius: 12px; }}
.arrow-connector {{ flex: 0 0 auto; width: 80px; display: flex; flex-direction: column; align-items: center; }}
</style>
</head>
<body>
<div class="container">
<h1>🗺️ {产品名称} — 交互流程图（横向）</h1>

<!-- 主流程 -->
<div class="flow-row">
  <!-- 步骤卡片 + 箭头连接 -->
</div>

<!-- 分支流程（可选） -->
<div class="branch-row">
  <!-- 分支步骤卡片 -->
</div>
</div>
</body>
</html>
```

#### 纵向布局模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>{产品名称} — 交互流程图（纵向）</title>
<style>
/* 纵向流程样式 */
.step {{ position: relative; margin-bottom: 0; }}
.step-connector {{ display: flex; align-items: center; justify-content: center; }}
</style>
</head>
<body>
<div class="container">
<h1>🗺️ {产品名称} — 交互流程图（纵向）</h1>

<!-- 步骤垂直排列 -->
<div class="step">
  <div class="step-body">
    <!-- 步骤内容 -->
  </div>
  <div class="step-connector">
    <!-- 箭头和操作说明 -->
  </div>
</div>
</div>
</body>
</html>
```

### Step 4: 在浏览器中打开

生成完成后，使用 `open_browser_page` 工具打开 HTML 文件：

```
open_browser_page(url="file:///{文件路径}.html")
```

## 布局选择指南

| 场景 | 推荐布局 | 原因 |
|------|---------|------|
| 流程步骤 ≤ 5 个 | 横向 | 一屏展示，直观清晰 |
| 流程步骤 > 5 个 | 纵向 | 避免横向滚动，易于阅读 |
| 分支流程多 | 纵向 | 分支可独立成行，不拥挤 |
| 需要嵌入 PRD | 横向 | 横向布局更紧凑，适合嵌入文档 |

## 设计规范

### 颜色规范
| 元素 | 颜色 | 用途 |
|------|------|------|
| 主流程步骤 | `#e91e63` → `#ff6b9d` | 粉色渐变，表示主流程 |
| 分支流程步骤 | `#ff9800` → `#f57c00` | 橙色渐变，表示分支 |
| 二次确认/警告 | `#ffc107` | 黄色，表示确认/警告 |
| 完成状态 | `#4caf50` | 绿色，表示成功/完成 |
| 箭头连接 | `#e91e63` | 粉色，主流程箭头 |
| 分支箭头 | `#ff9800` | 橙色，分支箭头 |

### 卡片尺寸
| 布局 | 卡片宽度 | 说明 |
|------|---------|------|
| 横向 | 280px | 固定宽度，保证截图清晰 |
| 纵向 | 100% | 自适应容器宽度 |

### 动画效果
| 元素 | 动画 | 说明 |
|------|------|------|
| 主流程箭头 | `slideRight` / `bounce` | 引导视觉流向 |
| 分支箭头 | `slideRightOrange` | 区分主流程 |

## 示例

### 示例：赠礼详情页交互流程

**流程步骤：**
1. 初始页面 → 2. 确认地址浮层 → 3. 二次确认弹窗 → 4. 已领取状态
**分支流程：** 点击「修改」→ 地址选择页 → 返回步骤 2

**生成文件：**
- `交互流程图-赠礼详情页-横向.html`
- `交互流程图-赠礼详情页-纵向.html`

**截图命名：**
- `flow-01-初始页面.png`
- `flow-02-确认地址浮层.png`
- `flow-03-二次确认弹窗.png`
- `flow-03a-地址选择页.png`
- `flow-04-已领取状态.png`

## 注意事项

1. **图片必须内嵌**：所有截图转换为 Base64 嵌入 HTML，确保复制到 TAPD 后图片不丢失
2. **截图完整性**：使用 `fullPage: true` 确保截取完整页面内容
3. **流程连贯性**：箭头连接必须清晰说明操作步骤（如"点击「免费领取」"）
4. **分支标注**：分支流程必须用橙色标签明确标注触发条件
5. **文件命名**：遵循 `交互流程图-{产品名称}-{布局}.html` 命名规范
