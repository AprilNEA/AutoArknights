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
        if 1 << tn["wday"] << 5:  # 周一到周五
            if tn["wday"] in [3, 4]:
                pass
            else:
                pass
            player.anni("a")
            if tn["wday"] == 1:
                for t in range(2):
                    player.resource(3)  # 粉碎防御
            if tn["wday"] == 2:
                for t in range(2):
                    player.resource(1)  # 粉碎防御
            if tn["wday"] == 5:
                for t in range(2):
                    player.resource(5)  # 粉碎防御
        # 4-4x1
        if tn["wday"] == 6:  # 周六
            pass
        if tn["wday"] == 0:  # 周日
            pass
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
