import sys
sys.path.insert(0, '.')
from moments_comment import (
    WeChatMomentsCommenter, 
    generate_funny_comment, 
    get_wechat_main_window,
    capture_window
)
import pygetwindow as gw
import time
import pyautogui
import pyperclip

def restore_wechat():
    """还原微信窗口"""
    wechat = gw.getWindowsWithTitle('微信')
    if wechat:
        w = wechat[0]
        if w.isMinimized:
            w.restore()
            time.sleep(0.5)
        w.activate()
        time.sleep(0.3)
        return w
    return None

def click_at(abs_x, abs_y):
    """绝对坐标点击"""
    pyautogui.click(abs_x, abs_y)
    time.sleep(0.3)

def find_moments_entrance(win_rect):
    """找到朋友圈入口位置"""
    # 朋友圈在发现页面，通常在中间偏左位置
    # 入口大约在窗口宽度15-20%，高度35-40%的位置
    x = win_rect['left'] + int(win_rect['width'] * 0.17)
    y = win_rect['top'] + int(win_rect['height'] * 0.38)
    return x, y

def comment_xuql_moments():
    """评论徐其林的朋友圈"""
    
    # 还原微信
    win = restore_wechat()
    if not win:
        print('未找到微信窗口')
        return False

    print(f'微信窗口: ({win.left}, {win.top}) {win.width}x{win.height}')

    # ====== 第一步：点击发现 ======
    print('\n[1/6] 点击发现...')
    discover_x = win.left + int(win.width * 0.08)
    discover_y = win.top + int(win.height * 0.95)
    click_at(discover_x, discover_y)
    time.sleep(0.8)

    img = capture_window()
    img.save('v2_step1_discover.png')
    print('发现页已截图')

    # ====== 第二步：点击朋友圈 ======
    print('\n[2/6] 点击朋友圈...')
    moments_x = win.left + int(win.width * 0.17)
    moments_y = win.top + int(win.height * 0.38)
    click_at(moments_x, moments_y)
    time.sleep(1)

    img = capture_window()
    img.save('v2_step2_moments.png')
    print('朋友圈已截图')

    # ====== 第三步：在朋友圈里找徐其林 ======
    print('\n[3/6] 滚动查找徐其林...')
    
    for i in range(10):
        print(f'  滚动第 {i+1} 次...')
        pyautogui.scroll(-300)
        time.sleep(0.4)
        
        # 每滚动几次截个图
        if i % 2 == 0:
            img = capture_window()
            img.save(f'v2_scroll_{i}.png')

    # ====== 第四步：点击徐其林进入他的朋友圈 ======
    print('\n[4/6] 点击徐其林进入他的朋友圈...')
    
    # 徐其林的头像/昵称位置（大约在左侧1/4处）
    # 先尝试点击一个可能的位置
    xuqlin_x = win.left + int(win.width * 0.15)
    xuqlin_y = win.top + int(win.height * 0.25)
    
    # 点击进入个人朋友圈
    click_at(xuqlin_x, xuqlin_y)
    time.sleep(0.8)

    img = capture_window()
    img.save('v2_step4_profile.png')
    print('徐其林朋友圈已截图')

    # ====== 第五步：评论最新动态 ======
    print('\n[5/6] 评论徐其林的最新朋友圈...')
    
    # 生成评论
    comment = generate_funny_comment('徐其林', 'general')
    print(f'评论内容: {comment}')

    # 点击评论按钮（朋友圈动态右下角）
    comment_btn_x = win.left + int(win.width * 0.88)
    comment_btn_y = win.top + int(win.height * 0.72)
    click_at(comment_btn_x, comment_btn_y)
    time.sleep(0.3)

    # 输入评论
    pyperclip.copy(comment)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 点击发送
    send_btn_x = win.left + int(win.width * 0.88)
    send_btn_y = win.top + int(win.height * 0.88)
    click_at(send_btn_x, send_btn_y)
    time.sleep(0.5)

    img = capture_window()
    img.save('v2_step5_commented.png')
    print('评论已发送！')

    # ====== 第六步：返回 ======
    print('\n[6/6] 返回朋友圈...')
    # 按ESC返回
    pyautogui.press('escape')
    time.sleep(0.3)

    print('\n[OK] 完成！')
    return True

if __name__ == '__main__':
    comment_xuql_moments()
