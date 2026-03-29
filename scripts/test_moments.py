import sys
sys.path.insert(0, '.')
from moments_comment import WeChatMomentsCommenter, generate_funny_comment, capture_window
import pyautogui
import time
from pathlib import Path

commenter = WeChatMomentsCommenter()

# 获取窗口
if not commenter.get_wechat_window():
    print('未找到微信窗口')
    exit()

commenter.activate_window()
print('窗口位置:', commenter.win_rect['left'], commenter.win_rect['top'])
print('窗口大小:', commenter.win_rect['width'], 'x', commenter.win_rect['height'])

# 点击发现入口
print('点击发现...')
commenter.click_relative(0.08, 0.95)
time.sleep(0.5)

# 截图看发现页
img = capture_window()
img.save('discover.png')
print('已保存发现页截图')
