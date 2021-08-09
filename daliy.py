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
from datetime import datetime, timezone, timedelta
from arknighs import Player


def get_bjtime():
    tn = time.localtime(time.time())
    return {
        "daytime": f"{tn.tm_year}-{tn.tm_mon}-{tn.tm_mday}",
        "mday": int(tn.tm_mday),
        "hour": int(tn.tm_hour),
        "wday": int(tn.tm_wday)
    }


def daliy_limit():
    tn = get_bjtime()
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
            # 龙门
            if tn["wday"] == 1:
                pass
            if tn["wday"] == 2:
                pass
            if tn["wday"] == 5:
                pass

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
            if tn["wday"] in [5,6]:
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
        print(f"共{times}次 第{i}次")


if __name__ == '__main__':
    # daliy_nolimit()
    # quick(10)
    # print(get_bjtime())
    player = Player(1, 1, '9887bc394436343530')
    # a = player.anni()
    # print(a)
    # if a:
    #     player.fixed_start()
    player.riic()
