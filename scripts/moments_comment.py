"""
朋友圈评论自动化脚本 v9
根据用户反馈优化：
1. 只完成：打开朋友圈页面 + 滚动朋友圈页面
2. 两个点图标需要80%以上匹配度才点击
3. 不再打开搜一搜
"""
import sys
import time
import random
import pyperclip
from pathlib import Path
import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
from PIL import ImageGrab, Image

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

SCRIPT_DIR = Path(__file__).parent


def load_icon(name):
    """加载图标模板"""
    path = SCRIPT_DIR / name
    img = Image.open(path)
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)


def find_icon(gray, template, threshold=0.5):
    """在截图中找图标"""
    if gray is None or template is None:
        return None, None, 0
    
    if template.shape[0] > gray.shape[0] or template.shape[1] > gray.shape[1]:
        return None, None, 0
    
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    if max_val > threshold:
        h, w = template.shape
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2
        return center_x, center_y, max_val
    return None, None, max_val


def restore_wechat():
    """还原微信窗口"""
    win = gw.getWindowsWithTitle('微信')
    if win:
        w = win[0]
        if w.isMinimized:
            w.restore()
            time.sleep(0.3)
        w.activate()
        time.sleep(0.2)
        return w
    return None


def enter_moments():
    """进入朋友圈"""
    print('[步骤1] 进入朋友圈...')

    template = load_icon('moments_icon.png')
    if template is None:
        print('[ERROR] 无法加载朋友圈入口图标')
        return False

    img = ImageGrab.grab()
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    x, y, score = find_icon(gray, template, threshold=0.8)
    if x:
        print(f'[OK] 找到朋友圈入口: ({x}, {y}) 匹配度: {score:.3f}')
        pyautogui.click(x, y)
        time.sleep(1.5)  # 等待朋友圈加载
        return True
    else:
        print(f'[ERROR] 未找到朋友圈入口，匹配度: {score:.3f}')
        return False


def scroll_moments():
    """滚动朋友圈页面"""
    print('[步骤2] 滚动朋友圈页面...')
    
    # 用户记录的坐标
    target_x = 1132
    target_y = 1116
    print(f'  移动鼠标到用户指定位置: ({target_x}, {target_y})')
    pyautogui.moveTo(target_x, target_y)
    time.sleep(0.3)
    
    # 截图看看朋友圈内容
    img = ImageGrab.grab()
    img.save(SCRIPT_DIR / 'after_enter_moments.png')
    print(f'[OK] 已保存截图: after_enter_moments.png')
    
    # 滚动
    print('  滚动中...')
    pyautogui.scroll(-400)
    time.sleep(0.8)
    
    img = ImageGrab.grab()
    img.save(SCRIPT_DIR / 'after_scroll_1.png')
    print(f'[OK] 已保存截图: after_scroll_1.png')
    
    pyautogui.scroll(-400)
    time.sleep(0.8)
    
    img = ImageGrab.grab()
    img.save(SCRIPT_DIR / 'after_scroll_2.png')
    print(f'[OK] 已保存截图: after_scroll_2.png')


def find_and_click_two_dots():
    """找两个点图标并点击（需要80%以上匹配度）"""
    print('[步骤3] 找两个点图标...')
    
    # 使用用户提供的清晰图标
    # 使用正确的两个点图标（100%匹配）
    template = load_icon('two_dots_correct.png')
    if template is None:
        print('[ERROR] 无法加载两个点图标')
        return None

    screen_w, screen_h = pyautogui.size()
    
    # 尝试多次
    for attempt in range(3):
        img = ImageGrab.grab()
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # 只搜索屏幕第2列（两个点图标在中间位置）
        screen_w = gray.shape[1]
        col2_start = screen_w // 3
        col2_end = screen_w * 2 // 3
        col2_region = gray[:, col2_start:col2_end]
        
        x, y, score = find_icon(col2_region, template, threshold=0.99)
        
        if x is not None and score >= 0.99:
            full_x = x + col2_start  # 转换回全屏坐标
            print(f'[OK] 找到两个点图标: ({full_x}, {y}) 匹配度: {score:.3f}')
            # 点击
            pyautogui.click(full_x, y)
            time.sleep(0.5)
            return full_x, y
        
        if attempt < 2:
            print(f'  第{attempt+1}次匹配度不够: {score:.3f}，滚动再试...')
            pyautogui.scroll(-300)
            time.sleep(0.5)
    
    print(f'[WARN] 未找到两个点图标（匹配度需>=80%），最高匹配度: {score:.3f}')
    return None


def click_comment_option():
    """点击评论选项"""
    print('[步骤4] 找评论图标...')
    time.sleep(0.5)
    
    # 加载评论图标模板
    template = load_icon('comment_icon.png')
    if template is None:
        print('[ERROR] 无法加载评论图标')
        return False
    
    img = ImageGrab.grab()
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # 全屏搜索评论图标
    x, y, score = find_icon(gray, template, threshold=0.99)
    
    if x is not None and score >= 0.99:
        print(f'[OK] 找到评论图标: ({x}, {y}) 匹配度: {score:.3f}')
        pyautogui.click(x, y)
        time.sleep(0.3)
        return True
    
    print(f'[WARN] 未找到评论图标，匹配度: {score:.3f}')
    return False


def input_comment(text):
    """输入评论"""
    print(f'[步骤5] 输入评论: {text}')
    
    # 粘贴文本
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)


def send_comment():
    """发送评论"""
    print('[步骤6] 找发送图标...')
    time.sleep(0.3)
    
    # 加载发送图标模板
    template = load_icon('send_icon.png')
    if template is None:
        print('[ERROR] 无法加载发送图标')
        return False
    
    img = ImageGrab.grab()
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # 全屏搜索发送图标
    x, y, score = find_icon(gray, template, threshold=0.99)
    
    if x is not None and score >= 0.99:
        print(f'[OK] 找到发送图标: ({x}, {y}) 匹配度: {score:.3f}')
        pyautogui.click(x, y)
        time.sleep(0.5)
        return True
    
    print(f'[WARN] 未找到发送图标，匹配度: {score:.3f}')
    return False


def analyze_moments_content():
    """截屏并分析朋友圈内容类型"""
    print('[步骤2.5] 分析朋友圈内容...')
    img = ImageGrab.grab()
    img.save(SCRIPT_DIR / 'content_analyze.png')
    print(f'[OK] 已保存内容截图: content_analyze.png')
    
    # 转换为OpenCV格式分析颜色
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    h, w = img_cv.shape[:2]
    total = h * w
    
    # 分析颜色比例
    green_mask = cv2.inRange(hsv, (35, 50, 50), (85, 255, 255))
    blue_mask = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
    red_mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
    red_mask2 = cv2.inRange(hsv, (160, 50, 50), (180, 255, 255))
    orange_mask = cv2.inRange(hsv, (10, 50, 50), (25, 255, 255))
    # 肤色检测（自拍/人物）
    skin_mask = cv2.inRange(hsv, (0, 20, 80), (30, 150, 255))
    
    green_ratio = np.sum(green_mask > 0) / total
    blue_ratio = np.sum(blue_mask > 0) / total
    warm_ratio = (np.sum(red_mask1 > 0) + np.sum(red_mask2 > 0) + np.sum(orange_mask > 0)) / total
    skin_ratio = np.sum(skin_mask > 0) / total
    
    # 判断内容类型（按优先级）
    if skin_ratio > 0.08:
        content_type = "颜值"  # 人物/自拍
    elif warm_ratio > 0.05:
        content_type = "美食"
    elif blue_ratio > 0.15:
        content_type = "旅游"
    elif green_ratio > 0.15:
        content_type = "户外"
    else:
        content_type = "日常"
    
    print(f'[AI识别] 内容类型: {content_type} (蓝:{blue_ratio:.2f} 绿:{green_ratio:.2f} 暖:{warm_ratio:.2f} 肤:{skin_ratio:.2f})')
    return content_type


def generate_smart_comment(content_text):
    """根据内容类型生成智能评论"""
    # 内容类型到评论的映射
    comment_map = {
        # 美食类
        "美食": ["馋哭了！这是在报复社会吧[ai生成]", "深夜放毒警告！[ai生成]", "看着就香！[ai生成]", "吃货本货了！[ai生成]"],
        "吃": ["馋哭了！这是在报复社会吧[ai生成]", "深夜放毒警告！[ai生成]", "看着就香！[ai生成]", "吃货本货了！[ai生成]"],
        "好吃": ["馋哭了！这是在报复社会吧[ai生成]", "深夜放毒警告！[ai生成]", "看着就香！[ai生成]"],
        "火锅": ["火锅配冰可乐，绝了！[ai生成]", "这是在喂猪吗？[ai生成]", "馋哭了！[ai生成]"],
        "烧烤": ["人间烟火气！[ai生成]", "撸串配啤酒！[ai生成]", "太治愈了！[ai生成]"],
        "蛋糕": ["甜食控上线！[ai生成]", "卡路里爆表警告！[ai生成]", "甜蜜暴击！[ai生成]"],
        
        # 旅游类
        "旅游": ["神仙日子！求带飞[ai生成]", "这是在人间仙境吗！[ai生成]", "好想去！[ai生成]", "实名羡慕！[ai生成]"],
        "旅行": ["神仙日子！求带飞[ai生成]", "这是在人间仙境吗！[ai生成]", "好想去！[ai生成]", "实名羡慕！[ai生成]"],
        "风景": ["神仙日子！求带飞[ai生成]", "这是在人间仙境吗！[ai生成]", "好美！[ai生成]"],
        "海": ["面朝大海，春暖花开！[ai生成]", "好想去海边！[ai生成]", "蓝色治愈！[ai生成]"],
        "山": ["一览众山小！[ai生成]", "爬山腿废了吗？[ai生成]", "风景独好！[ai生成]"],
        
        # 日常类
        "日常": ["今日份快乐已签收！[ai生成]", "平平淡淡也是真！[ai生成]", "记录生活的人最可爱！[ai生成]"],
        "工作": ["打工人加油！[ai生成]", "搬砖人辛苦了！[ai生成]", "摸鱼愉快！[ai生成]"],
        "加班": ["打工人加油！[ai生成]", "辛苦了！[ai生成]", "摸鱼愉快！[ai生成]"],
        
        # 宠物类
        "猫": ["喵星人入侵！[ai生成]", "好可爱啊啊啊！[ai生成]", "猫奴无疑！[ai生成]"],
        "狗": ["汪星人出没！[ai生成]", "好可爱啊啊啊！[ai生成]", "铲屎官幸福！[ai生成]"],
        "宠物": ["好可爱啊啊啊！[ai生成]", "想rua！[ai生成]", "太治愈了！[ai生成]"],
        
        # 健身运动类
        "健身": ["自律即自由！[ai生成]", "卷起来了！[ai生成]", "加油！[ai生成]"],
        "跑步": ["自律即自由！[ai生成]", "跑起来！[ai生成]", "生命在于运动！[ai生成]"],
        "运动": ["自律即自由！[ai生成]", "卷起来了！[ai生成]", "加油！[ai生成]"],
        
        # 晒娃类
        "娃": ["小可爱！[ai生成]", "未来可期！[ai生成]", "太萌了！[ai生成]"],
        "孩子": ["小可爱！[ai生成]", "未来可期！[ai生成]", "太萌了！[ai生成]"],
        "宝宝": ["小可爱！[ai生成]", "未来可期！[ai生成]", "太萌了！[ai生成]"],
        
        # 学习类
        "学习": ["卷王上线！[ai生成]", "加油！[ai生成]", "学到了！[ai生成]"],
        "考试": ["逢考必过！[ai生成]", "加油！[ai生成]", "稳了稳了！[ai生成]"],
        
        # 娱乐类
        "电影": ["好想看！[ai生成]", "种草了！[ai生成]", "好看吗？[ai生成]"],
        "音乐": ["好听的！[ai生成]", "已加入歌单！[ai生成]", "品味不错！[ai生成]"],
        "游戏": ["带我！[ai生成]", "开黑吗？[ai生成]", "段位多少了？[ai生成]"],
        
        # 颜值类（自拍/人物）
        "颜值": ["好帅啊啊啊！[ai生成]", "神仙颜值！[ai生成]", "杀疯了！[ai生成]", "好绝！[ai生成]", "太可了！[ai生成]", "心动预警！[ai生成]"],
        
        # 心情类
        "开心": ["快乐会传染！[ai生成]", "好心情加分！[ai生成]", "今日份快乐源泉！[ai生成]"],
        "难过": ["抱抱！[ai生成]", "会好起来的！[ai生成]", "加油！[ai生成]"],
    }
    
    # 如果没有内容描述，使用随机评论
    if not content_text or content_text.strip() == "":
        return random.choice([
            "路过支持！[ai生成]",
            "沙发！[ai生成]",
            "点赞！[ai生成]",
            "棒棒哒！[ai生成]",
            "路过~[ai生成]",
        ])
    
    content_lower = content_text.lower()
    
    # 匹配关键词
    for keyword, comments in comment_map.items():
        if keyword in content_lower:
            return random.choice(comments)
    
    # 默认评论
    return random.choice([
        "路过支持！[ai生成]",
        "沙发！[ai生成]",
        "点赞！[ai生成]",
        "棒棒哒！[ai生成]",
    ])


def comment_one_post(smart_comment=None):
    """评论一条朋友圈"""
    # 先截屏分析内容（在没有弹出菜单时截）
    content_type = analyze_moments_content()
    
    # 根据内容类型生成智能评论（如果没有指定）
    if smart_comment is None:
        smart_comment = generate_smart_comment(content_type)
    
    print(f'[AI生成] 智能评论: {smart_comment}')
    
    # 步骤3: 找两个点图标并点击
    result = find_and_click_two_dots()
    if not result:
        return False, content_type
    
    # 步骤4: 点击评论选项
    if not click_comment_option():
        return False, content_type
    
    # 步骤5: 输入评论
    input_comment(smart_comment)
    
    # 步骤6: 发送
    if not send_comment():
        return False, content_type
    
    return True, content_type


def scroll_to_next():
    """滚动到下一条"""
    pyautogui.moveTo(1132, 1116)
    time.sleep(0.2)
    pyautogui.scroll(-600)  # 多滚一点
    time.sleep(0.5)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', '-c', type=int, default=5, help='评论条数')
    parser.add_argument('--smart', '-s', action='store_true', help='使用AI智能评论')
    parser.add_argument('--manual', '-m', type=str, help='手动指定评论内容（覆盖智能）')
    args = parser.parse_args()
    
    print('=' * 50)
    print(f'朋友圈评论助手 v12 - 智能评论版')
    print('=' * 50)

    # 还原微信
    win = restore_wechat()
    if not win:
        print('[ERROR] 未找到微信窗口')
        sys.exit(1)

    # 步骤1: 进入朋友圈
    if not enter_moments():
        print('[ERROR] 无法进入朋友圈')
        sys.exit(1)
    
    # 步骤2: 滚动朋友圈
    scroll_moments()
    
    # 批量评论（默认使用智能评论）
    success = 0
    for i in range(args.count):
        print(f'\n--- 评论第 {i+1}/{args.count} 条 ---')
        
        # 手动指定评论
        comment = args.manual if args.manual else None
        
        if comment_one_post(smart_comment=comment):
            success += 1
            print(f'[OK] 第{i+1}条评论成功')
        else:
            print(f'[ERROR] 第{i+1}条评论失败')
        
        # 滚动到下一条（最后一条不需要滚动）
        if i < args.count - 1:
            scroll_to_next()
    
    print(f'\n{"=" * 50}')
    print(f'完成！成功 {success}/{args.count} 条')
    print('=' * 50)
