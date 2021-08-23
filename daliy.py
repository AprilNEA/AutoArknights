#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: daliy.py
# @createtime: 2021/8/2 上午10:47 Green Sulley
# @lastupdate:
# @desc: Arknights Auto Helper based on ADB and Python
# @desc:
import time

from loguru import logger

from lib import utils
from arknighs import Player


def daliy_limit():
    player = Player('9887bc394436343530')
    tn = utils.get_bjtime()
    start1 = False
    while start1 is False:
        if 20 >= tn["hour"] >= 8:
            start1 = True
        else:
            time.sleep(300)  # 每过5min检查一次是否开始
    while start1:
        # 周一到周五
        if 1 << tn["wday"] << 5:
            if tn["wday"] in [3, 4]:
                player.stuck('1-7', 2)
            else:
                player.stuck('1-7', 3)
            player.anni("a")
            if tn["wday"] == 1:
                player.resource("粉碎防御", 2)
            if tn["wday"] == 2:
                player.resource("空中威胁", 2)
            if tn["wday"] == 5:
                player.resource("战术演习", 2)
                player.stuck('4-4', 1)
        # 周六
        if tn["wday"] == 6:
            player.stuck('1-7', 3)
            player.anni("切尔诺伯格")
            player.resource("战术演习", 2)
            player.stuck('JT8-2', 1)
        # 周日
        if tn["wday"] == 0:
            player.resource("战术演习", 4)
    start2 = False
    while start2 is False:
        if 22 >= tn["hour"] >= 20:
            if tn["wday"] == 1:
                pass
            if tn["wday"] == 2:
                pass
            if tn["wday"] in [3, 4]:
                pass
            if tn["wday"] in [5, 6]:
                pass
            if tn["wday"] == 0:
                pass
        else:
            time.sleep(300)  # 每过5min检查一次是否开始


def daliy_nolimit():
    player = Player('9887bc394436343530')
    player.login()


def quick(times=1):
    player = Player(1, 1, '9887bc394436343530')
    for i in range(times):
        player.fixed_start()
        logger.info(f"共{times}次 第{i + 1}次")


if __name__ == '__main__':
    # daliy_nolimit()
    quick(50)
    # print(get_bjtime())
    # player = Player(1, 1, '9887bc394436343530')
    # # a = player.anni()
    # player.receive_task()
    # # print(a)
    # # if a:
    # #     player.fixed_start()
    # player.riic()
