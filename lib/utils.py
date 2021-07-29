#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: SkuMoe
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @file: utils.py
# @time: 2021/7/29 17:00
# @desc: Arknights Auto Helper based on ADB and Python

import cv2
import base64
import numpy as np
from matplotlib import pyplot as plt


def img_cv2(img_path):
    return cv2.imread(img_path)


def img_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def cv2_to_base64(image):
    return base64.b64encode(cv2.imencode('.jpg', image)[1].tostring())


def base64_to_cv2(base64_str):
    return cv2.imdecode(np.fromstring(base64.b64decode(base64_str), np.uint8),
                        cv2.IMREAD_COLOR)


def tap_match_image(temp, target):
    h, w, s = temp.shape
    result = cv2.matchTemplate(target, temp, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    print(min_val, min_loc)
    print(h / 2)
    return min_loc[0] + (w / 2), min_loc[1] + (h / 2)


# 调试测试
if __name__ == '__main__':
    from adb import AndroidDebugBridge

    devices = AndroidDebugBridge('9887bc394436343530')
    # temp = cv2.imread(r'D:\Github\MyArknightsAutoHelper\image\开始唤醒.jpeg')
    # CV2无法识别中文路径
    temp = cv2.imdecode(
        np.fromfile(r"D:\Github\MyArknightsAutoHelper\image\开始唤醒.jpeg",
                    dtype=np.uint8), cv2.IMREAD_COLOR)
    # target = cv2.imread(r'D:\Github\MyArknightsAutoHelper\lib\temp1.jpeg')
    target = devices.get_screenshot()
    a = tap_match_image(temp, target)
    print(a)
    devices.tap(a[0], a[1])
