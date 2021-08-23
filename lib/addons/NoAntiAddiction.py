#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: NoAntiAddiction.py
# @desc: Arknights Auto Helper based on ADB and Python
import json
from mitmproxy.http import HTTPFlow
from mitmproxy import master, ctx, http

from lib.logger import logger


class NoAntiAddiction:
    """
    解除防沉迷限制
    """

    def __init__(self):
        logger.info('明日方舟防沉迷破解开启')
        # 是否完成唤醒
        self.entryGame = True

    def response(self, flow: HTTPFlow):
        if flow.request.url.startswith(
            # 进入游戏开始唤醒界面都会调用这个
            "https://ak-conf.hypergryph.com/config/prod/announce_meta/Android/preannouncement.meta.json") or flow.request.url.startswith(
            "https://ak-conf.hypergryph.com/config/prod/announce_meta/IOS/preannouncement.meta.json"):
            logger.debug("防沉迷: 已进入游戏唤醒界面")
            self.entryGame = True
        if flow.request.url.startswith(
            "https://as.hypergryph.com/online/v1/ping"):
            j = json.loads(flow.response.get_text())
            logger.debug("防沉迷: 已取消防沉迷限制")
            if self.entryGame:
                flow.response.set_text(
                    '{"result":0,"message":"OK","interval":5400,"timeLeft":-1,"alertTime":600}')
                self.entryGame = False
            else:
                flow.response = http.HTTPResponse.make(404)
