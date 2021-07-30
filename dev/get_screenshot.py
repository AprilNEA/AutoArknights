#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: get_screenshot.py
# @createtime: 2021/7/30 下午3:48 Green Sulley
# @lastupdate:
# @desc: Arknights Auto Helper based on ADB and Python
# @desc:
from lib import adb
import cv2
devices = adb.AndroidDebugBridge('9887bc394436343530')
a = devices.get_screenshot()
b = input("请输入名称：")
cv2.imwrite(f'{b}.jpeg', a)
