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
from pathlib import Path

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
        return True
    return False

def find_and_comment_xuql():
    """找到徐其林的朋友圈并评论"""
    # 还原微信
    restore_wechat()

    commenter = WeChatMomentsCommenter()
    if not commenter.get_wechat_window():
        print('未找到微信窗口')
        return False

    print(f'微信窗口: ({commenter.win_rect["left"]}, {commenter.win_rect["top"]}) {commenter.win_rect["width"]}x{commenter.win_rect["height"]}')

    # ====== 第一步：进入发现 ======
    print('\n[1/5] 进入发现页面...')
    commenter.click_relative(0.08, 0.95)  # 底部发现入口
    time.sleep(0.8)

    img = capture_window()
    img.save('step1_discover.png')
    print('已保存发现页')

    # ====== 第二步：进入朋友圈 ======
    print('\n[2/5] 进入朋友圈...')
    # 朋友圈在发现页面的位置
    commenter.click_relative(0.18, 0.35)  # 朋友圈图标位置
    time.sleep(1)

    img = capture_window()
    img.save('step2_moments.png')
    print('已保存朋友圈页')

    # ====== 第三步：滚动找到徐其林 ======
    print('\n[3/5] 滚动查找徐其林的朋友圈...')
    
    # 先生成一条幽默评论
    comment = generate_funny_comment('徐其林', 'general')
    print(f'生成的评论: {comment}')

    # 滚动浏览朋友圈
    for scroll_count in range(8):
        print(f'  滚动第 {scroll_count + 1} 次...')
        pyautogui.scroll(-400)
        time.sleep(0.5)

        # 截图看看
        img = capture_window()
        img.save(f'scroll_{scroll_count}.png')

    # ====== 第四步：评论 ======
    print('\n[4/5] 评论徐其林的朋友圈...')
    
    # 评论按钮位置（朋友圈动态右下角）
    commenter.click_relative(0.88, 0.72)  # 评论按钮
    time.sleep(0.3)

    # 输入评论
    import pyperclip
    pyperclip.copy(comment)
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # 发送
    commenter.click_relative(0.88, 0.88)  # 发送按钮
    time.sleep(0.5)

    img = capture_window()
    img.save('step4_commented.png')
    print('评论已发送！')

    # ====== 完成 ======
    print('\n[5/5] 完成！')
    return True

if __name__ == '__main__':
    find_and_comment_xuql()
