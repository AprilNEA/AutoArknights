#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: ${NAME}.py
# @desc: Arknights Auto Helper based on ADB and Python

class AddHeader:
    """
    mitmproxy测试用
    """
    def __init__(self):
        self.num = 0

    def response(self, flow):
        self.num = self.num + 1
        print(self.num)
        flow.response.headers["count"] = str(self.num)
