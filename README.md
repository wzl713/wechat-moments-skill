# 微信朋友圈自动评论助手

自动评论微信朋友圈，支持 AI 内容识别，根据美食/旅游/自拍/日常等类型生成幽默评论。

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)

---

## 功能特点

- 🤖 **AI 内容识别**：自动识别朋友圈内容类型（美食/旅游/自拍/户外/日常）
- 😄 **智能评论**：根据内容类型生成匹配的幽默评论，标注 `[ai生成]`
- 🎯 **高精准度**：图标匹配度 99%+，避免误触
- 🔄 **批量评论**：支持一次评论多条朋友圈
- 📝 **自定义评论**：也支持手动指定评论内容

---

## 使用方式

### 方式一：在 WorkBuddy 中使用（推荐）

如果你使用 WorkBuddy，直接告诉 WorkBuddy：

> "帮我评论朋友圈"
> "给朋友圈评论 20 条"
> "自动评论朋友圈"

WorkBuddy 会自动加载此技能并执行。

> ⚠️ **WorkBuddy 配置要求**：
> - 将此文件夹放在 `~/.workbuddy/skills/wechat-moments/` 目录
> - WorkBuddy 会自动识别 SKILL.md 并加载此技能
> - 无需手动安装依赖，WorkBuddy 环境已具备

### 方式二：直接运行脚本

适用于不使用 WorkBuddy 的用户。

**环境要求**
- Windows 系统
- Python 3.10+
- 微信电脑版

**安装步骤**

```bash
# 1. 克隆仓库
git clone https://github.com/wzl713/wechat-moments-skill.git
cd wechat-moments-skill

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python scripts/moments_comment.py -c 5
```

---

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `-c <数量>` | 评论多少条朋友圈 | `-c 20` |
| `-m <内容>` | 手动指定评论内容 | `-m "写的真好"` |

**示例**
```bash
# 自动识别内容，智能评论 10 条
python scripts/moments_comment.py -c 10

# 所有朋友圈统一评论
python scripts/moments_comment.py -c 5 -m "写得真好！[ai生成]"
```

---

## 运行前提

1. **微信在发现页**：确保微信在「发现」页面，未进入任何聊天或页面
2. **屏幕清晰**：运行时避免切换窗口或遮挡微信界面
3. **图标匹配**：如遇识别失败，可能需要重新截取图标模板（见下方说明）

---

## 自定义图标模板

不同电脑分辨率不同，图标在屏幕上的样子有细微差别。如遇识别失败：

1. 截取你电脑上对应的图标，保存为 PNG
2. 替换 `scripts/` 目录下对应的文件：

| 文件 | 说明 |
|------|------|
| `moments_icon.png` | 朋友圈入口图标（发现页的朋友圈按钮） |
| `two_dots_correct.png` | 两个点图标（朋友圈右下角的「···」） |
| `comment_icon.png` | 评论图标（弹出菜单中的评论按钮） |
| `send_icon.png` | 发送图标（评论输入框右侧的发送按钮） |

---

## 内容类型识别规则

通过 HSV 颜色分析自动判断：

| 类型 | 识别规则 | 评论示例 |
|------|----------|----------|
| 颜值 | 肤色比例 > 8% | "好帅啊啊啊！" |
| 美食 | 红/橙色比例 > 5% | "馋哭了！报复社会吧！" |
| 旅游 | 蓝色比例 > 15% | "神仙日子！求带飞！" |
| 户外 | 绿色比例 > 15% | "好治愈！" |
| 日常 | 默认 | "今天也是元气满满！" |

---

## 文件结构

```
wechat-moments-skill/
├── README.md              # 本文件
├── SKILL.md               # WorkBuddy 技能描述
├── requirements.txt       # Python 依赖
└── scripts/
    ├── moments_comment.py # 主脚本
    ├── moments_icon.png   # 朋友圈入口图标模板
    ├── two_dots_correct.png # 两个点图标模板
    ├── comment_icon.png   # 评论图标模板
    └── send_icon.png      # 发送图标模板
```

---

## 许可证

MIT License
