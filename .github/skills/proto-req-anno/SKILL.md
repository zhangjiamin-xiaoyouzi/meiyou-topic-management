---
name: proto-req-anno
description: '在原型 HTML 页面的指定字段上注入橙色「需求说明」点击展开标注，替代单独写需求文档。适用于后台管理系统原型、表单页、列表页等场景，字段旁点击可展开/收起淡黄色需求说明块。触发词：需求说明、需求标注、原型注释、加需求说明。'
argument-hint: '描述要标注的页面和字段，例如：给话题管理列表页的"话题标签"筛选和表格列加需求说明'
user-invocable: true
---

# 原型需求说明标注技能

> **角色设定**：你是一个资深的产品经理。当你为原型页面撰写需求说明时，需站在产品视角思考——关注用户场景、业务规则边界、异常流程、数据来源与联动关系，而非技术实现细节。每条说明应让研发、测试、运营都能无歧义理解。

在现有原型 HTML 文件中，为**新增或变更的字段**注入「需求说明」点击展开标注，让原型本身承载需求描述，无需单独维护需求文档。

## 何时使用

- 用户提到"加需求说明"、"原型注释"、"需求标注"、"不想写需求文档"
- 在已还原的后台页面（列表页/表单页/弹窗页）上，对新增字段补充说明
- 需要让评审者在看原型时直接看到字段的业务规则、枚举含义、必填约束

## 不适用场景

- 全新页面（应先用 meiyou-design 或 prd-generator 生成页面骨架）
- 纯文字需求文档（用 create-prd 或 meiyouhoutaiprd）

---

## 工作方式

### 第一步：确认目标字段
询问或分析用户指定的字段，明确：
1. 字段所在的 HTML 文件路径
2. 字段在 HTML 中的定位方式（label 文本 / name 属性 / id / th 文本）
3. 每个字段的需求说明内容（若用户未提供，生成合理占位说明）

### 第二步：注入公共样式与 JS
在每个目标 HTML 文件的 `</head>` 前注入以下代码块（用 `id="__req_tip_style2__"` 防重复）：

```html
<style id="__req_tip_style2__">
.req-anno-btn{display:inline-block;background:#e67e00;color:#fff;border:none;border-radius:3px;
  padding:1px 7px;font-size:11px;line-height:18px;cursor:pointer;margin-right:8px;
  vertical-align:middle;font-weight:600;opacity:.9}
.req-anno-btn:hover{background:#cf6c00;opacity:1}
.req-anno-box{display:none}          /* 仅作数据载体，不展开 */
#__req_modal__ *{box-sizing:border-box}
</style>
<script>
function toggleReqAnno(btn) {
  var box = btn.parentElement.querySelector('.req-anno-box');
  if (!box) return;
  if (document.getElementById('__req_modal__')) return;
  var ov = document.createElement('div');
  ov.id = '__req_modal__';
  ov.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);'
    + 'z-index:999998;display:flex;align-items:center;justify-content:center';
  var card = document.createElement('div');
  card.style.cssText = 'background:#fff;border-radius:8px;padding:24px 28px 20px;max-width:420px;'
    + 'width:92%;box-shadow:0 8px 32px rgba(0,0,0,.22);position:relative;border-top:4px solid #e67e00';
  var cls = document.createElement('button');
  cls.innerHTML = '&times;';
  cls.style.cssText = 'position:absolute;top:10px;right:14px;background:none;border:none;'
    + 'font-size:22px;line-height:1;cursor:pointer;color:#aaa;padding:0';
  cls.onclick = function () { ov.remove(); };
  var ttl = document.createElement('div');
  ttl.style.cssText = 'font-size:13px;font-weight:700;color:#e67e00;margin-bottom:12px;letter-spacing:.5px';
  ttl.textContent = '📋 需求说明';
  var body = document.createElement('div');
  body.style.cssText = 'font-size:12px;color:#5a4000;line-height:1.9;white-space:pre-line;'
    + 'background:#fffbe6;padding:12px 14px;border-radius:6px;border-left:3px solid #e67e00;'
    + 'max-height:60vh;overflow-y:auto';
  body.textContent = box.textContent.trim();
  card.appendChild(cls); card.appendChild(ttl); card.appendChild(body);
  ov.appendChild(card);
  ov.onclick = function (e) { if (e.target === ov) ov.remove(); };
  document.body.appendChild(ov);
}
</script>
```

> 注入前先用正则清除已有的同名 style/script 块，避免重复。

### 第三步：在字段处插入标注元素

> **交互方式**：点击按钮弹出**居中浮层**（遮罩卡片），不影响页面布局；点击 × 或背景关闭。  
> `.req-anno-box` 仅作为数据载体（`display:none`），不在页面内展开。

#### 场景 A：表单页（`<th>` 行级标注）

推荐在 `<th>` 中放一个按钮 + 隐藏的说明数据块，一个字段一个按钮：

```html
<th>
  <button class="req-anno-btn" onclick="toggleReqAnno(this)"
    style="display:block;margin-bottom:4px">需求说明</button>
  <span class="required">*</span>话题标签
  <div class="req-anno-box">【话题标签】说明内容...</div>
</th>
```

若需在 `<td>` 内的子字段上各放一个按钮：

```html
<div style="margin-bottom:6px">
  <button class="req-anno-btn" onclick="toggleReqAnno(this)">需求说明</button>
  <label style="width:80px;...">话题特色：</label>
  <label><input type="radio" ...> 特色</label>
  <label><input type="radio" ...> 非特色</label>
  <div class="req-anno-box">【话题特色】说明内容...</div>
</div>
```

#### 场景 B：列表页筛选区（form-group 布局）

```html
<div class="form-group">
  <button class="req-anno-btn" onclick="toggleReqAnno(this)">需求说明</button>
  <label>话题标签：</label>
  <div class="form-group searchbox">...</div>
  <div class="req-anno-box">【筛选：话题标签】说明内容...</div>
</div>
```

#### 场景 C：列表页表头（`<th>`）

```html
<th style="position:relative">
  <button class="req-anno-btn" onclick="toggleReqAnno(this)"
    style="display:block;margin-bottom:3px;font-size:10px;padding:1px 5px">需求说明</button>
  列名
  <div class="req-anno-box">【列名】说明内容...</div>
</th>
```

---

## 视觉规范

| 元素 | 说明 |
|---|---|
| 按钮颜色 | `#e67e00`（橙色）—— 刻意区别于页面主色，让人一眼识别为"注释层" |
| 浮层遮罩 | `rgba(0,0,0,.45)`，居中卡片，`border-top: 4px solid #e67e00` |
| 说明区背景 | `#fffbe6`（浅黄）+ 左侧 3px 橙色竖线 |
| 字体 | 12px，`color:#5a4000`，行高 1.9，`white-space:pre-line` 支持换行 |
| `.req-anno-box` | 始终 `display:none`，仅作文本数据容器 |
| 关闭方式 | 点击右上角 × 或点击遮罩背景 |

---

## 说明内容写作规范

每条需求说明应包含：
1. **标题行**：`【字段名】`
2. **枚举含义**：逐条说明每个选项的业务含义
3. **约束说明**：必填/选填、影响范围、联动规则
4. **示例**（可选）

```
【话题周期】
长期：无明确下线时间，持续运营；
短期：有明确截止日期，到期后自动降权或下线。
必填，与推荐位到期规则联动。
```

---

## 幂等性保证

- 注入前清除旧的 `<style id="__req_tip_style2__">` 和 `<script>function toggleReqAnno` 块
- 按钮和说明块都在同一个父容器内，不会跨容器查找
- 多次执行不会重复注入

---

## Python 辅助脚本模板

对于批量注入（多文件 / 多字段），推荐用 Python 脚本操作：

```python
import re

STYLE_BLOCK = """<style id="__req_tip_style2__">
.req-anno-btn{display:inline-block;background:#e67e00;color:#fff;border:none;border-radius:3px;padding:1px 7px;font-size:11px;line-height:18px;cursor:pointer;margin-right:8px;vertical-align:middle;font-weight:600;opacity:.9}
.req-anno-btn:hover{background:#cf6c00;opacity:1}
.req-anno-box{display:none}
#__req_modal__ *{box-sizing:border-box}
</style>
<script>
function toggleReqAnno(btn){var box=btn.parentElement.querySelector('.req-anno-box');if(!box)return;if(document.getElementById('__req_modal__'))return;var ov=document.createElement('div');ov.id='__req_modal__';ov.style.cssText='position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.45);z-index:999998;display:flex;align-items:center;justify-content:center';var card=document.createElement('div');card.style.cssText='background:#fff;border-radius:8px;padding:24px 28px 20px;max-width:420px;width:92%;box-shadow:0 8px 32px rgba(0,0,0,.22);position:relative;border-top:4px solid #e67e00';var cls=document.createElement('button');cls.innerHTML='&times;';cls.style.cssText='position:absolute;top:10px;right:14px;background:none;border:none;font-size:22px;line-height:1;cursor:pointer;color:#aaa;padding:0';cls.onclick=function(){ov.remove();};var ttl=document.createElement('div');ttl.style.cssText='font-size:13px;font-weight:700;color:#e67e00;margin-bottom:12px;letter-spacing:.5px';ttl.textContent='📋 需求说明';var body=document.createElement('div');body.style.cssText='font-size:12px;color:#5a4000;line-height:1.9;white-space:pre-line;background:#fffbe6;padding:12px 14px;border-radius:6px;border-left:3px solid #e67e00;max-height:60vh;overflow-y:auto';body.textContent=box.textContent.trim();card.appendChild(cls);card.appendChild(ttl);card.appendChild(body);ov.appendChild(card);ov.onclick=function(e){if(e.target===ov)ov.remove();};document.body.appendChild(ov);}
</script>"""

def inject_style(html):
    html = re.sub(r'<style id="__req_tip_style2__">.*?</style>\n?', '', html, flags=re.DOTALL)
    html = re.sub(r'<script>\s*function toggleReqAnno.*?</script>\n?', '', html, flags=re.DOTALL)
    return html.replace('</head>', STYLE_BLOCK + '\n</head>', 1)

BTN = '<button class="req-anno-btn" onclick="toggleReqAnno(this)">需求说明</button>'

def anno_box(text):
    return f'<div class="req-anno-box">{text}</div>'
```
