#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: api.py
# @desc: Arknights Auto Helper based on ADB and Python
import json
from typing import List, Dict

import requests
from lib import utils


# 关于 Headers 中的 seqnum 自动, 由于 secret 的一次性的性质, 鹰角服务器会自动记录并返回正确的数值, 故无需在 headers 中携带
class ArkAPI:
    def __init__(self, uid, secret, username):
        self.session = requests.Session()
        self.username = username
        self.headers = {
            "uid": uid,
            "secret": secret,
            "X-Unity-Version": "2017.4.39f1",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; SM-N935F Build/PPR1.180610.011)"
        }

    def _update_sync(self, rp):
        utils.write_data(
            f"../data/account/{self.username}/sync/{utils.get_bjtime()['daytime']}.json",
            'w',
            rp
        )

    def _error_check(self, rp: Dict):
        """
        {'statusCode': 400, 'error': 'Bad Request', 'message': 'server error', 'code': 5571,
        'msg': 'seession secret not exist',
         'info': '{"uid":"taYodyX3gj5ClRxrPtmZIAHqbTFXCby+"}
        :param rp:
        :return:
        """
        if rp['statusCode'] == 400 and rp['code'] == 5571:
            return False

    def get_sync(self) -> Dict:
        """
        获取基建数据
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/building/sync',
            headers=self.headers, json={})
        self._update_sync(rp.text)
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
        self._update_sync(rp.text)
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
        self._update_sync(rp.text)
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
        self._update_sync(rp.text)
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
        self._update_sync(rp.text)
        return rp.json()

    def use_item(self, inst_id, item_id, cnt):
        """
        item_table.json
        :param inst_id:
        :param item_id:
        :param cnt:
        :return:
        """
        rp = self.session.post(
            url='https://ak-as-gf.hypergryph.com/user/useItem',
            headers=self.headers,
            json={
                "instId": inst_id,
                "itemId": item_id,
                "cnt": cnt
            })
        return rp.json()

    def auto_confirm_mission(self, mtype: str) -> Dict:
        """
        自动领取全部任务奖励
        :param mtype: 任务类型,常见值为"DAILY"和"WEEKLY", 主线任务值未知
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/mission/autoConfirmMissions',
            headers=self.headers,
            json={
                "type": mtype
            }
        )
        self._update_sync(rp.text)
        return rp.json()

    def sync_ngacha(self) -> Dict:
        """
        同步招募数据
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/gacha/syncNormalGacha',
            headers=self.headers,
            json={}
        )
        return rp.json()

    def normal_gacha(self, duration: int, slotid: int, taglist: List) -> Dict:
        """
        开启公开招募
        :param duration: 招募时限
        :param slotid: 房间号
        :param taglist: 职业需求
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/gacha/normalGacha',
            headers=self.headers,
            json={
                "duration": duration,
                "slotId": slotid,
                "specialTagId": -1,  # fixme 未知字段
                "tagList": taglist
            }
        )
        return rp.json()

    def boost_ngacha(self, duration: int, slotid: int, taglist: List) -> Dict:
        """
        立即招募
        :param slotid: 房间号
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/gacha/boostNormalGacha',
            headers=self.headers,
            json={
                "buy": 0,
                "slotId": slotid,
            }
        )
        return rp.json()

    def finish_ngacha(self, slotid: int) -> Dict:
        """
        完成招募
        :param slotid: 房间号
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/gacha/normalGacha',
            headers=self.headers,
            json={
                "slotId": slotid,
            }
        )
        return rp.json()

    def receive_social_point(self):
        """
        领取当日信用
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/social/receiveSocialPoint',
            headers=self.headers,
            json={}
        )
        if rp.json()['statusCode'] == 400 and rp.json()['code'] == 5571:
            return False
        return rp.json()

    def get_social_goodlist(self):
        """
        获取信用信用商店列表
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/shop/getSocialGoodList',
            headers=self.headers,
            json={}
        )
        return rp.json()

    def buy_social_good(self, goodid: str):
        """
        购买信用商店
        :return:
        """
        rp = self.session.post(
            url='https://ak-gs-gf.hypergryph.com/shop/buySocialGood',
            headers=self.headers,
            json={
                "count": 1,
                "goodId": goodid
            }
        )
        return rp.json()

    def anni_alculation(self):
        pass
