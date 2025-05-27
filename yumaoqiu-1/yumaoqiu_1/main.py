import os
from pynput import mouse
import time
import datetime
import pyautogui
import numpy as np
from PIL import Image
import pygetwindow as gw


def adjust_window():
    # 查找窗口的位置和尺寸（需要提前设置窗口标题）
    window_title = "微健助手"
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
        if window:
            # 调整窗口尺寸
            window.resizeTo(390, 2000)
            window.moveTo(0, 0)  # 移动窗口到屏幕的某个位置
            window.activate()

    except IndexError:
        print(f"未找到窗口：{window_title}")


def get_color(image_path):
    # 读取图像
    image = Image.open(image_path)

    image_rgb = image.convert('RGB')
    img_array = np.array(image_rgb)
    r_avg = np.mean(img_array[:, :, 0])
    g_avg = np.mean(img_array[:, :, 1])
    b_avg = np.mean(img_array[:, :, 2])

    return round(r_avg), round(g_avg), round(b_avg)


def wait_time():
    current_time = datetime.datetime.now()
    target_time = datetime.datetime(current_time.year, current_time.month, current_time.day, 23, 59, 59)
    if current_time < target_time:
        time_difference = target_time - current_time
        seconds_to_wait_1 = time_difference.total_seconds()
        return seconds_to_wait_1


# ————————————————————————————————————————————————————————————————————————————————————————————————————————————
# ————————————————————————————————————————————————————————————————————————————————————————————————————————————

adjust_window()

# 获取当前脚本所在目录
current_script_dir = os.path.dirname(os.path.abspath(__file__))

# 创建文件夹名称
folder_name_1 = "tu_1"
folder_name_2 = "tu_2"
folder_name_3 = "tu_3"

# 拼接文件夹的完整路径
folder_path_1 = os.path.join(current_script_dir, folder_name_1)
folder_path_2 = os.path.join(current_script_dir, folder_name_2)
folder_path_3 = os.path.join(current_script_dir, folder_name_3)

# 判断文件夹是否存在，如果不存在就创建
if not os.path.exists(folder_path_1):
    os.makedirs(folder_path_1)
    print(f"文件夹 '{folder_name_1}' 已创建！")
if not os.path.exists(folder_path_2):
    os.makedirs(folder_path_2)
    print(f"文件夹 '{folder_name_2}' 已创建！")
if not os.path.exists(folder_path_3):
    os.makedirs(folder_path_3)
    print(f"文件夹 '{folder_name_3}' 已创建！")

while wait_time() > 0:
    seconds_to_wait = wait_time()
    hours = seconds_to_wait // 3600
    minutes = (seconds_to_wait % 3600) // 60
    seconds = seconds_to_wait % 60
    print("距离主体程序运行还有：")
    print(f"当前时间：{datetime.datetime.now()}")
    print(f"{int(hours)}小时 {int(minutes)}分钟 {int(seconds)}秒")
    print(f"{seconds_to_wait}秒\n")
    if seconds_to_wait >= 1:
        time.sleep(1)
    else:
        if seconds_to_wait > 0.01:
            time.sleep(seconds_to_wait-0.007)
        else:
            time.sleep(seconds_to_wait*0.9)
        break

# adjust_window()


M = mouse.Controller()
print("主体程序0.001s后开始运行")
time.sleep(0.11)

M.position = (156, 320)
M.click(mouse.Button.left, 1)
print(f"{datetime.datetime.now()}时点击第二天位置：{M.position}")


signal_0 = False
signal_1 = False
sign_1 = False

# 🔺 判断点击第二天场地后，界面是否已经出现，第一个界面(1号场地字体区域是否是 非灰色）
for i in range(300):
    time.sleep(0.015)
    img_2 = pyautogui.screenshot(region=(28, 157, 5, 5))  # 1号字体左侧的灰色区域:rgb=（84，85，103）
    img_1 = pyautogui.screenshot(region=(164, 99, 30, 30))  # 日期的黑色区域:rgb=（84，85，103）
    img_0 = pyautogui.screenshot(region=(20, 200, 200, 400))  # 下半部分区域（非灰色就代表新的界面出现）：≠（240，239，245）
    img_2.save(os.path.join(folder_path_3, f'{i}.jpg'))
    img_1.save(os.path.join(folder_path_2, f'{i}.jpg'))
    img_0.save(os.path.join(folder_path_1, f'{i}.jpg'))
    print(f"第一个界面已经截图第{i}次")

    # 返回图片颜色的平均RGB三色数值
    img_0_path = os.path.join(folder_path_1, f'{i}.jpg')
    color_0 = get_color(img_0_path)
    img_1_path = os.path.join(folder_path_2, f'{i}.jpg')
    color_1 = get_color(img_1_path)
    img_2_path = os.path.join(folder_path_3, f'{i}.jpg')
    color_2 = get_color(img_2_path)
    print(f"第一个界面: 下半部分区域（非灰色就代表新的界面出现）的rgb：{color_0}，###rgb≠（240，239，245）代表出现\n")
    print(f"第一个界面: 黑色日期区域的RGB三色数值为：{color_1}，###rgb=（84，85，102）代表通过（离开了第一帧画面\n")
    print(f"第一个界面: 1号场地左侧灰色区域的RGB三色数值为：{color_2}，###rgb=（240，239，244）代表通过（离开了第一帧画面\n")
    print(f"标志0:{signal_0}，标志1:{signal_1},标志2:{color_0 != (240, 239, 244)}")

    r1,g1,b1 = color_1
    judge_color_1 = abs(r1-84) + abs(g1-85) + abs(b1-102)
    r2, g2, b2 = color_2
    judge_color_2 = abs(r2 - 240) + abs(g2 - 239) + abs(b2 - 244)
    if judge_color_1 < 6:
        signal_0 = True
    if judge_color_2 < 6:
        signal_1 = True

    # 如果刷新出界面（非灰色）且场地不可以抢（color_1是灰色的），则说明点早了，需要退出截图判断的内层循环，重新点击第二天刷新
    if signal_0 and signal_1 and color_0 != (240, 239, 244):
        print("找到第一个界面的目标图片\n")
        sign_1 = True
        break

if not sign_1:
    print("没找到第一个界面")
else:
    print(f"{datetime.datetime.now()}时 第一个界面出现\n")
    time.sleep(0.25)
    # 两个场地的位置：(799, 395)  (797, 478)
    M.position = (192, 617)
    M.click(mouse.Button.left, 1)
    time.sleep(0.2)
    M.position = (192, 663)
    time.sleep(0.2)
    M.click(mouse.Button.left, 1)
    time.sleep(0.12)
    M.position = (192, 705)
    time.sleep(0.12)
    M.click(mouse.Button.left, 1)
    time.sleep(0.1)

"""
判断第二个界面的代码
"""
#
#     # 确认预约的位置(200, 998)
#     M.position = (200, 998)
#     print(f"{datetime.datetime.now()}时点击第一个确认预约位置：{M.position}")
#     # time.sleep(0.2)
#     M.click(mouse.Button.left, 1)
#
# # # 🔺 判断点击确认支付后，前往支付界面是否出现
# # for i in range(300):
# #     time.sleep(0.02)
# #     print(f"鼠标坐标{pyautogui.position()}")
# #     img_1 = pyautogui.screenshot(region=(58, 988, 50, 20))  # 前往支付字体区域
# #     img_1.save(os.path.join(folder_path_2, f'{i}.jpg'))
# #     print(f"第二个界面已经截图第{i}次")
# #
# #     # 返回图片颜色的平均RGB三色数值
# #     img_1_path = os.path.join(folder_path_2, f'{i}.jpg')
# #     color_1 = get_color(img_0_path)
# #     print(f"第二个界面: 前往支付区域的RGB三色数值为：{color_1}\n")
# #
# #     r1, g1, b1 = color_1
# #     if abs(r1-240) + abs(g1-239) + abs(b1-244) > 10:
# #         print("找到第二个界面的目标图片\n")
# #         sign_2 = True
# #         break
# # print(f"{datetime.datetime.now()}时 第二个界面出现\n")
#
#
# time.sleep(0.2)



M.position = (144, 1327)

for i in range(15):
    M.click(mouse.Button.left, 1)
    time.sleep(0.16)
    print(f"{datetime.datetime.now()}时点击最下角的位置：{M.position}")
