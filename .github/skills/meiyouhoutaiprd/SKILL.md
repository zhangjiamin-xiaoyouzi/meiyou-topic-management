---
name: meiyouhoutaiprd
description: 按美柚中后台标准 PRD 模板生成需求文档（Markdown + HTML）。遵循"背景→目标→方案"三段式结构，包含现状分析表、E-R图、泳道图、功能列表等标准章节，Mermaid 图表自动渲染为 PNG 嵌入，支持将原型截图嵌入需求说明表格。适用于美柚中后台产品的需求文档撰写。
metadata:
  short-description: 按美柚中后台 PRD 模板生成需求文档（Markdown + HTML），含原型截图嵌入
---

# 美柚中后台 PRD 生成器

## 概述

本 skill 基于美柚 TAPD 中后台需求模板（模板ID: 中后台需求模版），按标准三段式结构生成需求文档：

- **需求背景（20%）**：业务大背景 → 业务子背景 → 现状判断及问题
- **项目目标（5%）**：目标描述 + 迭代节奏 + 风险预判
- **需求方案（80%）**：名词定义 → E-R图 → 结构图 → 流程图 → 原型图 → 需求说明 → 协同需求

输出格式：**同时生成 Markdown（.md）和 HTML（.html）两个文件**。HTML 中 Mermaid 图表自动渲染为 PNG 并嵌入，需求说明表格可嵌入原型截图辅助说明。

## 文档结构

完整模板见 `references/template.md`，核心章节：

### 标题格式
`{角色（运营/产品）}可以通过{功能}获得{价值}`

### 一、需求背景（20%）
| 章节 | 占比 | 内容 |
|------|------|------|
| 1.1 业务大背景 | 5% | 对齐团队 OKR，说明需求服务于哪个大 O |
| 1.2 业务子背景 | 5% | 用户反馈/Case 分析，商业化需求则论述客户信息 |
| 1.3 现状判断及问题 | 10% | 四列表格：现状 → 问题判断 → 历史需求 → 解决方案 |

### 二、项目目标（5%）
| 章节 | 内容 |
|------|------|
| 2.1 目标描述 | 本次迭代价值（运营灵活配置/提升人效/降低成本） |
| 2.2 迭代节奏（非必填） | 分阶段实现计划 |
| 2.3 风险预判（非必填） | 技术难点、延期风险、影响范围 |

### 三、需求方案（80%）
| 章节 | 占比 | 内容 |
|------|------|------|
| 3.1 名词定义 | 非必填 | 名词/定义 对照表 |
| 3.2 E-R图 | 非必填 | 实体关系图（必须使用中文命名实体、属性和关系，如"用户"、"包含"、"赠礼配置"，不得使用英文） |
| 3.3 产品结构图 | 10% | 模块/功能脑图 |
| 3.4 产品流程图 | 10% | 多角色泳道图 |
| 3.5 原型图 | 非必填 | 后台原型。若原型已部署到 GitHub Pages，需附带**在线预览地址**和 **GitHub 仓库地址**，格式如下：<br>`<a href="https://xxx.github.io/xxx/" target="_blank">🔗 在线预览 →</a>` <br>`<a href="https://github.com/xxx/xxx" target="_blank">📁 xxx/xxx →</a>` |
| 3.6 需求说明 | 60% | 功能模块/功能点/优先级 + 详细说明（HTML 版可嵌入原型截图，见下方「原型截图嵌入」） |
| 3.7 协同方需求 | 非必填 | 运营/编辑/商务侧配合内容 |

### 元数据字段
- 状态、父需求、分类、业务、迭代、处理人、优先级、需求类型、需求难度、技术等级、预估工时等

## 工作流

### Step 1：确认基本信息
向用户确认：
- **需求标题**：按格式 "XX可以通过XX获得XX"
- **创建模板**：默认"中后台需求模版"
- **分类/业务**：如 会员、广告、内容
- **迭代**：所属迭代版本
- **优先级**：High/Middle/Low
- **需求类型**：基础建设/新功能/优化
- **需求难度**：A 全新能力 / B 现有能力迭代 / C 简单配置
- **处理人**：默认当前用户

### Step 2：填充需求内容
按章节引导用户填写：
1. 需求背景（必须）
2. 项目目标（必须）
3. 需求方案（核心，重点填写 3.3-3.6）

### Step 3：生成文档（Markdown + HTML）
按美柚中后台 PRD 模板同时生成 Markdown 和 HTML 两个文件：

1. **先输出 Markdown**：按模板填充内容，输出为 `PRD-{主题}-美柚中后台版.md`
   - Mermaid 图表（E-R图、产品结构图、产品流程图）直接嵌入 Markdown
   - 所有实体名、属性名、关系名必须使用中文
2. **再生成 HTML**：调用 `scripts/md_to_tapd_html.py` 将 Markdown 转为 HTML
   ```
   python scripts/md_to_tapd_html.py --input PRD-xxx.md --output PRD-xxx.tapd.html
   ```
3. **渲染 Mermaid 为 PNG**：调用 `scripts/render_mermaid_images.py` 将 Mermaid 图表渲染为 PNG 图片
   ```
   python scripts/render_mermaid_images.py --input PRD-xxx.md --output-dir tapd-assets
   ```
4. **嵌入图片到 HTML**：重新执行 `md_to_tapd_html.py` 时带上 `--images-dir` 参数，将 PNG 嵌入 HTML 占位符中
   ```
   python scripts/md_to_tapd_html.py --input PRD-xxx.md --output PRD-xxx.tapd.html --images-dir tapd-assets
   ```

> **前提条件**：脚本目录需安装依赖：`npm install`（需 playwright）

> **注意**：HTML 生成的图表占位符名称为 E-R图、产品结构图、产品流程图-泳道图、状态流转图——生成 Mermaid 图时需与这些名称对应。

### Step 3.5：嵌入原型截图到需求说明表格（必有）

当用户有可交互的 HTML 原型页面时，**必须**将原型截图嵌入 HTML PRD 的「需求说明」表格中，形成图文对照。

**嵌入方案（方案A：表格左侧新增「原型截图」列）**：
- 在每个模块表格**最左侧**插入一列「原型截图」
- 同一模块多行用 `rowspan` 合并为一个截图单元格
- 截图宽度 200px，带圆角阴影与整体视觉统一

**操作步骤**：

1. **截取原型页面各模块截图**：使用浏览器工具打开原型 HTML 页面，逐个截取各模块区域，保存为 PNG 到 `tapd-assets/` 目录
   - 命名规范：`prototype-{模块名}.png`（如 `prototype-优惠券卡片.png`）
   - 截图内容需与该模块的功能说明对应

2. **修改 HTML PRD 表格结构**：直接编辑 `.tapd.html` 文件，在每个模块表格中：
   - `<thead>` 最前面插入 `<th>原型截图</th>`（宽度 210px）
   - `<tbody>` 首行 `<tr>` 最前面插入带 `rowspan` 的 `<td>`，内含 `<img>` 标签
   - `rowspan` 值等于该模块的行数

   ```html
   <!-- 表头：在 thead tr 最前面插入 -->
   <th style="...text-align:center;width:210px">原型截图</th>

   <!-- 首行数据：在 tbody 首行 tr 最前面插入 -->
   <td rowspan="3" style="padding:4px;text-align:center;vertical-align:top;width:210px">
     <img src="tapd-assets/prototype-模块名.png"
          style="width:200px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);border:1px solid #e0e0e0"
          alt="模块名原型" />
   </td>
   ```

**注意事项**：
- 如果原型页面需触发交互才能展示某状态（如弹窗、已领取态），需在浏览器中先操作触发，再截图
- 多个模块可能共用同一张截图（如「收货地址」和「物流信息」都在已领取态中展示）
- **「需求说明标注系统」不应出现在 3.6 需求说明表格中**：原型页面上的橙色「需求说明」标注按钮属于原型辅助工具，不是产品功能需求，不要将其作为独立模块列入 PRD

### Step 3.6：图片 Base64 内嵌（TAPD 复制适配）

HTML 中的 `<img src="...">` 默认使用相对/绝对路径，复制粘贴到 TAPD 时图片无法显示。需将**所有图片**转为 Base64 data URI 内嵌，实现自包含 HTML。

**操作步骤**：

在 PowerShell 中执行以下脚本，将 `tapd-assets/` 下的所有 PNG 图片替换为 Base64：

```powershell
$htmlPath = "完整路径/PRD-xxx.tapd.html"
$html = [IO.File]::ReadAllText($htmlPath)

# 1. 替换原型截图（relative path: tapd-assets/prototype-*.png）
Get-ChildItem "tapd-assets目录" -Filter "prototype-*.png" | ForEach-Object {
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($_.FullName))
    $html = $html.Replace("tapd-assets/$($_.Name)", "data:image/png;base64,$base64")
}

# 2. 替换图表图片（absolute path: E-R图.png, 产品结构图.png, 产品流程图-泳道图.png）
@("E-R图.png","产品结构图.png","产品流程图-泳道图.png") | ForEach-Object {
    $filePath = Join-Path "tapd-assets目录" $_
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($filePath))
    $html = $html.Replace($filePath, "data:image/png;base64,$base64")
}

[IO.File]::WriteAllText($htmlPath, $html)
```

**验证**：替换后用 grep 确认无残留路径引用：
```powershell
# 应返回空结果（所有 src 均为 data:image）
grep -P 'src="(?!data:image)[^"]+"' PRD-xxx.tapd.html
```

**效果**：HTML 文件完全自包含，浏览器打开后 `Ctrl+A` `Ctrl+C` 复制，粘贴到 TAPD 编辑器时图片随 HTML 一起进入。**Base64 内嵌完成后，`tapd-assets/` 目录下的中间 PNG 文件无需保留，最终交付物仅 Markdown + 自包含 HTML 两个文件。**

### Step 4：确认修改
生成后请用户确认 Markdown 和 HTML 两个文件，支持迭代修改。

## 自动填充 TAPD（可选）

生成 PRD 后，可自动将内容填充到指定的 TAPD 需求单。

### 前置条件
- 用户已在 Chrome 中登录 TAPD（tapd.meiyou.com）
- 目标需求单已存在（先手动创建空白需求单，选择"中后台需求模版"）

### 填充流程

1. 生成结构化 JSON 数据
2. 调用 `scripts/fill_tapd.mjs`：
   ```bash
   node scripts/fill_tapd.mjs --story-id <需求ID> --workspace <工作空间ID> --data <json文件路径>
   ```
