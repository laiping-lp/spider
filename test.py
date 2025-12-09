import pyautogui
import time

# size（）：以两个整数的元组形式返回屏幕分辨率大小。
Screen_size = pyautogui.size()
print("当前屏幕大小为：",Screen_size)
# position（）：返回鼠标光标的当前X和Y坐标
print('Press Ctrl-C to quit.')
position = []
try:
    while True:
        # 获取当前鼠标光标位置
        x, y = pyautogui.position()
        position.append((x,y))
        # print(x)
        # print(y)
        # rjust()返回长宽右对齐的字符串。
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        print(positionStr, end='')
        print('\b' * len(positionStr), end='', flush=True)
        time.sleep(3)
except KeyboardInterrupt:
    print('\n')
print(position)