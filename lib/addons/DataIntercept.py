#!/usr/bin/python
# -*- coding: UTF-8 -*-def get_path(package, recource):
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: DataIntercept.py
# @desc: Arknights Auto Helper based on ADB and Python
import json

from mitmproxy.http import HTTPFlow
from mitmproxy import master, ctx, http

from lib import utils
from lib.logger import logger

base_url = 'https://ak-gs-gf.hypergryph.com/'


def daytime():
    return utils.get_bjtime()["daytime"]


class DataIntercept:

    def __init__(self, username):
        logger.info("数据拦截已启用")
        self.username = username

    def response(self, flow: HTTPFlow):
        if flow.request.url.startswith('https://ak-gs-gf.hypergryph.com/account/login'):
            data = json.loads(flow.response.get_text())
            logger.info("数据拦截: 已截获账号登录数据")
            token_before = utils.get_data('lib', f"../data/account/{self.username}/token.txt")
            if not token_before:
                if data["secret"] != token_before:
                    utils.write_data('lib', f"../data/account/{self.username}/token.txt", data["secret"])
        if flow.request.url.startswith(f'{base_url}account/syncData'):
            logger.info("数据拦截: 已截获账号数据")
            utils.write_data(
                'lib',
                f'../data/account/{self.username}/syncdata/{daytime()}.json',
                flow.response.get_text()
            )
        if flow.request.url.startswith(f'{base_url}building/sync'):
            logger.info("数据拦截: 已截获基建数据")
            utils.write_data(
                'lib',
                f"../data/account/{self.username}/sync/{daytime()}.json",
                'w',
                flow.response.get_text()
            )
