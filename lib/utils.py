#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: utils.py
# @createtime: 2021/7/29 17:00 Green Sulley
# @lastupdate: 2021/7/30 11:37 Green Sulley
# @desc: Arknights Auto Helper based on ADB and Python

import cv2
import base64
import numpy as np
from matplotlib import pyplot as plt


def img_cv2(img_path: str):
    return cv2.imread(img_path)


def img_np_cv2(img_path: str):
    """
    中文路径
    :param img_path:
    :return:
    """
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)


def img_base64(img_path: str):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def cv2_to_base64(image):
    return base64.b64encode(cv2.imencode('.jpg', image)[1].tostring())


def base64_to_cv2(base64_str: str):
    return cv2.imdecode(np.fromstring(base64.b64decode(base64_str), np.uint8),
                        cv2.IMREAD_COLOR)


def match_image(temp, target):
    # False: 0.13017292320728302
    # True: 9.214816964231431e-05
    h, w, s = temp.shape
    result = cv2.matchTemplate(target, temp, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if min_val > 0.1:
        return False
    return min_loc[0] + (w / 2), min_loc[1] + (h / 2)
