---
name: wechat-moments
description: 微信朋友圈评论自动化技能。当用户要求评论朋友圈、给好友动态点赞、自动评论所有朋友圈、或涉及朋友圈操作时使用此技能。支持生成幽默评论（30字左右，结尾标注ai生成），使用高精准度图像识别定位所有图标。
---

# 微信朋友圈评论助手

## 安装与配置

### 环境要求

- Windows 系统
- Python 3.10+
- 微信电脑版（最新版）

### 安装步骤

**1. 克隆仓库**
```bash
git clone https://github.com/wzl713/wechat-moments-skill.git
cd wechat-moments-skill
```

**2. 安装依赖**
```bash
pip install -r requirements.txt
```

**3. 运行**
```bash
# 评论5条朋友圈
python scripts/moments_comment.py -c 5

# 评论50条
python scripts/moments_comment.py -c 50
```

---

## 核心流程

```
微信初始界面 → 图像识别朋友圈入口 → 进入朋友圈 → 滚动 → 图像识别两个点图标 → 图像识别评论图标 → 输入评论 → 图像识别发送图标 → 滚动重复
```

### 详细步骤

| 步骤 | 操作 | 方法 |
|------|------|------|
| 1 | 进入朋友圈 | 图像识别朋友圈入口图标 (`moments_icon.png`) |
| 2 | 找动态 | 滚动浏览 |
| 3 | 打开菜单 | 图像识别两个点图标 (`two_dots_correct.png`)，在屏幕第2列搜索 |
| 4 | 评论 | 图像识别评论图标 (`comment_icon.png`) |
| 5 | 发送 | 图像识别发送图标 (`send_icon.png`) |

## 图像识别模板

所有图标均使用 **99%+ 匹配度** 要求，确保精准定位：

| 模板文件 | 用途 | 匹配度要求 |
|----------|------|-----------|
| `moments_icon.png` | 朋友圈入口图标（发现页） | ≥ 0.99 |
| `two_dots_correct.png` | 两个点菜单图标 | ≥ 0.99，第2列搜索 |
| `comment_icon.png` | 评论图标（弹出菜单中） | ≥ 0.99 |
| `send_icon.png` | 发送图标 | ≥ 0.99 |

### 模板存放位置

```
scripts/
```

## 命令行参数

```bash
python scripts/moments_comment.py -c <数量>   # 评论数量（必填）
python scripts/moments_comment.py -c 5 -m "自定义评论"  # 手动指定评论内容
```

## 评论生成

根据内容类型（HSV颜色分析）自动生成幽默评论，结尾标注 `[ai生成]`：

| 类型 | 判断规则 | 示例 |
|------|----------|------|
| 颜值 | 肤色比例 > 8% | "好帅啊啊啊！[ai生成]" |
| 美食 | 红/橙暖色比例 > 5% | "馋哭了！你这是在报复社会吧[ai生成]" |
| 旅游 | 蓝色比例 > 15% | "神仙日子！求带飞[ai生成]" |
| 户外 | 绿色比例 > 15% | "好治愈！[ai生成]" |
| 日常 | 默认 | "路过！今天也是元气满满呢！[ai生成]" |

## 技术实现

### 高精准度图像识别

所有图标识别均使用 **99%+ 匹配阈值**，核心代码：

```python
def find_icon(gray, template, threshold=0.99):
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val > threshold:
        h, w = template.shape
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y, max_val
    return None, None, max_val
```

### 区域搜索优化

- **两个点图标**：仅在屏幕第2列（中三分之一）搜索，避免误匹配右侧内容
- **其他图标**：全屏搜索

### 滚动策略

每次滚动后重新截图并重新识别图标位置，确保坐标准确（滚动后元素位置会变化）

## 注意事项

1. **确保微信在初始界面**（未进入任何聊天或页面）
2. **确保屏幕上有朋友圈入口**（发现页）
3. **图标模板可能需要定期更新**（微信更新后图标可能变化）
4. **匹配度低于99%会重试**：如果识别失败会自动重试
5. **运行前确保屏幕清晰**：避免其他窗口遮挡微信界面
6. **分辨率兼容性**：如遇图标识别失败，需重新截取对应图标模板替换 `scripts/` 下的文件
