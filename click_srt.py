import pyautogui
import time
import pyperclip
# 输出屏幕尺寸
print(pyautogui.size())
sizex,sizey=pyautogui.size()
# 切换窗口
pyautogui.hotkey('alt','tab')
# 点击坐标
position = [[987,226],[445,329],[231,240],[325,778],[1735,17],[1184,891]]
# 进入剪映
pyautogui.moveTo(position[0][0],position[0][1],duration=1)
pyautogui.click(button='left')
time.sleep(5)
# 导入视频
pyautogui.moveTo(position[1][0],position[1][1],duration=1)
pyautogui.click(button='left')
time.sleep(1)
pyautogui.alert(text='请选择需要处理的视频所在文件夹，选择完成后点击确认',title='PyAutoGUI消息框',button='OK')
time.sleep(5)
pyautogui.moveTo(position[1][0],position[1][1],duration=1)
pyautogui.click(button='left')
# 导入所有视频
pyautogui.hotkey('ctrl','a')
pyautogui.moveTo(998,638,duration=1)
pyautogui.click(button='left')
time.sleep(5)
# 拖入轨道
pyautogui.moveTo(position[2][0],position[2][1],duration=1)
pyautogui.click(button='left')
pyautogui.dragTo(267,826,duration=1)
pyautogui.click(button='right')
# 识别字幕
pyautogui.moveTo(position[3][0],position[3][1],duration=1)
pyautogui.click(button='left')
time.sleep(120)
# 导出
pyautogui.moveTo(position[4][0],position[4][1],duration=1)
pyautogui.click(button='left')
pyautogui.alert(text='请选择导出路径,选择完成路径后点击确认,并选择不导出视频只导出srt字幕文件',title='PyAutoGUI消息框',button='OK')
time.sleep(5)
# 确认
pyautogui.moveTo(position[5][0],position[5][1],duration=1)
pyautogui.click(button='left')
time.sleep(30)
# 消除弹窗
pyautogui.keyDown("esc")
# 删除轨道中素材
pyautogui.moveTo(position[2][0],position[2][1],duration=1)
pyautogui.click(button='left')
pyautogui.keyDown("backspace")
pyautogui.keyDown("enter")
time.sleep(2)
# 循环操作
while True: 
    # 拖入轨道
    pyautogui.moveTo(position[2][0],position[2][1],duration=1)
    pyautogui.click(button='left')
    pyautogui.dragTo(267,826,duration=1)
    pyautogui.click(button='right')
    # 右键识别字幕
    pyautogui.moveTo(position[3][0],position[3][1],duration=1)
    pyautogui.click(button='left')
    time.sleep(120)
    # 导出
    pyautogui.moveTo(position[4][0],position[4][1],duration=1)
    pyautogui.click(button='left')
    pyautogui.alert(text='请选择导出路径,选择完成路径后点击确认,并选择不导出视频只导出srt字幕文件',title='PyAutoGUI消息框',button='OK')
    time.sleep(5)
    # 确认
    pyautogui.moveTo(position[5][0],position[5][1],duration=1)
    pyautogui.click(button='left')
    time.sleep(30)
    # 消除弹窗
    pyautogui.keyDown("esc")
    # 删除轨道中素材
    pyautogui.moveTo(position[2][0],position[2][1],duration=1)
    pyautogui.click(button='left')
    pyautogui.keyDown("backspace")
    pyautogui.keyDown("enter")
    time.sleep(2)