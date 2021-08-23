#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: notifier.py
# @createtime: 2021/8/2 上午11:33 Green Sulley
# @lastupdate:
# @desc: Arknights Auto Helper based on ADB and Python
# @desc:
import requests


class QQ:
    def __init__(self, qid, qtype, ip='127.0.0.1', port=5700):
        self.url = f"http://{ip}:{port}"
        self.qid = qid
        self.qtype = qtype

    def send_message(self, msg, picture=None):
        if picture:
            for pic in picture:
                msg = f'[CQ:image,file={pic}]' + msg
        if self.qtype == "private":
            data = {
                'user_id': self.qid,
                'message': msg,
                'auto_escape': False
            }
            cq_url = f"{self.url}/send_private_msg"
            rev = requests.post(cq_url, data=data)
        elif self.qtype == "group":
            data = {
                'group_id': self.qid,
                'message': msg,
                'auto_escape': False
            }
            cq_url = f"http://{self.url}/send_group_msg"
            rev = requests.post(cq_url, data=data)
        else:
            return False
        if rev.json()['status'] == 'ok':
            return True
        return False


class Telegram:
    def __init__(self, token, uid):
        self.token = token
        self.uid = uid

    def send_message(self, msg, picture=None):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.uid}&text={msg}'
        rev = requests.get(url)
        # if rev.json()['status'] == 'ok':
        #     return True
        # return False
        return True
