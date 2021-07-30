#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: arknighs.py
# @createtime: 2021/7/26 16:55 Green Sulley
# @lastupdate: 2021/7/30 11:37 Green Sulley
# @desc: Arknights Auto Helper based on ADB and Pytho
import yaml
from lib import adb
from lib import utils

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


class Player:
    def __init__(self, username, password, devices_id):
        self.account = {
            "u": username,
            "p": password
        }
        self.devices = adb.AndroidDebugBridge('9887bc394436343530')

    def login(self):
        temp = utils.img_np_cv2('image/开始唤醒.jpeg')
        target = self.devices.get_screenshot()
        a = utils.tap_match_image(temp, target)
        print(a)
        if a:
            self.devices.tap(a[0], a[1])
        else:
            pass

    @classmethod
    def switch(cls):
        pass


if __name__ == '__main__':
    xuan = Player(config["account"][1]["username"],
                  config["account"][1]["password"], '9887bc394436343530')
    xuan.login()
