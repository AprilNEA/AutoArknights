#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: api.py
# @desc: Arknights Auto Helper based on ADB and Python
from typing import List, Dict

import requests


class ArkAPI:
    def __init__(self, uid, secret):
        self.session = requests.Session()
        self.headers = {
            "uid": uid,
            "secret": secret,
            "X-Unity-Version": "2017.4.39f1",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N935F Build/PPR1.180610.011)"
        }

    def get_sync(self) -> Dict:
        """
        获取基建数据
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/building/sync',
            headers=self.headers, json={})
        return rp.json()

    def assign_char(self, characters: List, roomid: str) -> Dict:
        """
        更换干员
        :param characters:
        :param roomid:
        :return: sync
        """
        rp = self.session.post(
            url="https://ak-gs-gf.hypergryph.com/building/assignChar",
            headers=self.headers,
            json={
                "charInstIdList": characters,
                "roomSlotId": roomid
            })
        return rp.json()

    def settle_manufacture(self, slot: List, supplement: int) -> Dict:
        """
        制造站
        :return: sync
        """
        rp = self.session.post(
            url="https://ak-gs-gf.hypergryph.com/building/settleManufacture",
            headers=self.headers,
            json={
                "roomSlotIdList": slot,
                "supplement": supplement
            })
        return rp.json()

    def delivery_batch_order(self, slot: List) -> Dict:
        """
        订单
        :return: sync
        """
        rp = self.session.post(
            url="https://ak-gs-gf.hypergryph.com/building/deliveryBatchOrder",
            headers=self.headers,
            json={
                "slotList": slot
            })
        return rp.json()

    def gain_alllntimacy(self) -> Dict:
        """
        信赖
        :return: sync
        """
        rp = self.session.post(
            url="https://ak-gs-gf.hypergryph.com/building/gainAllIntimacy",
            headers=self.headers,
            json={})
        return rp.json()

    def use_item(self, inst_id, item_id, cnt):
        rp = self.session.post(
            url='https://ak-as-gf.hypergryph.com/user/useItem',
            headers=self.headers,
            json={
                "instId": inst_id,
                "itemId": item_id,
                "cnt": cnt
            })
        return rp.json()
