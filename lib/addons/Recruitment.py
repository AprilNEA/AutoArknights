#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: Recruitment.py
# @desc: Arknights Auto Helper based on ADB and Python
import json
import pkgutil
from mitmproxy.http import HTTPFlow
from mitmproxy import master, ctx, http

data_tags = json.loads(pkgutil.get_data('lib', '../../data/tag.json'))


class Recruitment:
    def __init__(self):
        print('明日方舟防沉迷破解开启')

    def response(self, flow: HTTPFlow):
        if flow.request.url.startswith(
            'https://ak-gs-gf.hypergryph.com/account/syncData'):
            data = json.loads(flow.response.get_text())
            if data['user']['data']['recruit']:
                recruit_data = data['user']['data']['recruit']
            else:
                return False
            slot = recruit_data['normal']['slot']
            num = 0
            for i in range(4):
                if slot[i]['state'] == 1:
                    num += 1

