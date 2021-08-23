#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sullkey
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: recruitment.py
# @createtime: 2021/7/29 21:55 Green Sulley
# @lastupdate: 2021/7/30 11:37 Green Sulley
# @desc: Arknights Auto Helper based on ADB and Python
import json
import pkgutil

from itertools import combinations
from typing import List, Tuple, Dict

from lib import ocr

data_character = json.loads(pkgutil.get_data('lib', '../data/gamedata/character.json'))

data_character_cn = json.loads(
    pkgutil.get_data('lib', '../data/gamedata/character_cn.json'))

data_tags = json.loads(pkgutil.get_data('lib', '../data/gamedata/tag.json'))

data_tag_with_ch = json.loads(pkgutil.get_data('lib', '../data/gamedata/tagwithch.json'))

# 在出现错误之后再进行错误赐予更换
ERROR_MAP = {
    '千员': '干员',
    '滅速': '減速',
    '枳械': '机械',
    '冫口了': '治疗',
}

Guaranteed_FIVE = [
    ['控场'], ['爆发'], ['召唤'],
    ['近卫干员', '防护'],
    ['重装干员', '输出'], ['重装干员', '生存'], ['重装干员', '位移'],
    ['辅助干员', '输出'], ['辅助干员', '削弱'],
    ['术师干员', '治疗'],
    ['特种干员', '输出'], ['特种干员', '生存'], ['特种干员', '减速'], ['特种干员', '削弱'],
    ['先锋干员', '支援'],
    ['治疗', '输出'], ['治疗', '减速'],
    ['支援', '费用回复'],
    ['输出', '防护'], ['输出', '位移'],
    ['生存', '防护'],
    ['群攻', '削弱'],
    ['防护', '位移'],
    ['减速', '位移'],
    ['削弱', '快速复活'], ['削弱', '近战位'],
    ['术师干员', '输出', '减速']
]
Guaranteed_FOUR = [
    ['特种干员'], ['支援'], ['削弱'], ['快速复活'], ['位移'],
    ['近卫干员', '减速'],
    ['狙击干员', '生存'], ['狙击干员', '减速'],
    ['术师干员', '减速'], ['先锋干员', '治疗'],
    ['治疗', '费用回复'], ['输出', '减速'],
    ['生存', '远程位'], ['群攻', '减速'],
    ['减速', '近战位'],
]


def recuitment(tags: List[str]) -> List[int]:
    result = [0]
    return result


def get_intersection(a: List, b: List) -> List:
    """
    两个列表取交集
    :param a: 集合A
    :param b: 集合B
    :return: 集合A交B
    """
    return [val for val in a if val in b]


def get_tag_with_charater() -> Dict[str, List[Dict[str, str]]]:
    """

    :return:
    """
    result = {}
    for num, tag_name in data_tags.items():
        result[tag_name] = []
        for ch_name, ch_info in data_character.items():
            if int(num) in ch_info["tags"] or ch_info["position"]:
                result[tag_name].append({
                    "n": ch_name,
                    "s": ch_info["star"]
                })
    return result


def get_combinations(tags: List[str]) -> List[Tuple[str]]:
    """
    获取公招Tag排列组合
    :param tags: 公招中出现的5个可选Tag
    :return: 5个Tag所有的排列组合
    """
    return list(combinations(tags, 3)) + list(combinations(tags, 2)) + list(
        combinations(tags, 1))


def get_character(combination: Tuple[str]) -> List[Dict[str, int]]:
    """
    获取某组合可能出现的干员
    :param combination: 一种组合
    :return: 可能出现的干员
    """
    num = len(combination)
    if num == 3:
        a = data_tag_with_ch[combination[0]]
        b = data_tag_with_ch[combination[1]]
        c = data_tag_with_ch[combination[2]]
        return get_intersection(get_intersection(a, b), c)
    if num == 2:
        a = data_tag_with_ch[combination[0]]
        b = data_tag_with_ch[combination[1]]
        return get_intersection(a, b)
    if num == 1:
        return data_tag_with_ch[combination[0]]

def ocr_tags(img_base64: bytes) -> List:
    """
    公招OCR
    :param img_base64: 公招截图,最好是1920x1080中的[550:725, 530:1290]
    :return:
    """
    texts = json.loads(ocr.tencent_ocr(img_base64))
    tags = []
    for text in texts["TextDetections"]:
        if text["Confidence"] >= 85:
            tags.append({
                "text": text["DetectedText"],
                "loc": {
                    "x": text["ItemPolygon"]["X"],
                    "y": text["ItemPolygon"]["Y"]
                }
            })
    # fixme 优化算法，！稳定性
    # 排序 标签 位置
    sorted(tags, key=lambda tag: tag['loc']['x'], reverse=True)
    sorted(tags, key=lambda tag: tag['loc']['y'], reverse=True)
    res = []
    for tag in tags:
        # todo 优化纠正方式
        for word_wrong, word_right in ERROR_MAP.items():
            fix_tag = tag["text"].replace(word_wrong, word_right)
        if fix_tag in data_tags.values():
            res.append(fix_tag)
        else:
            # print(tag["text"],fix_tag)
            pass
            # todo 异常处理logger
    print(f"检测到Tag{res}")
    return res


def recruitment(tags: List) -> Tuple:
    """
    根据获得的公招Tags计算出最优组合
    :param tags: 5个公招Tag
    :return: 最优组合
    """
    if '高级资深干员' in tags:
        return (tags.index('高级资深干员'),)  # 元组中只包含一个元素时，需要在元素后面添加逗号
    elif '资深干员' in tags:
        return (tags.index('资深干员'),)
    for tag in Guaranteed_FIVE:
        if set(tag).issubset(set(tags)):
            a = len(tag)
            if a == 1:
                return (tags.index(tag[0]),)
            if a == 2:
                return tags.index(tag[0]), tags.index(tag[1])
            if a == 3:
                return tags.index(tag[0]), tags.index(tag[1]), tags.index(
                    tag[2])
    # todo 四星标签
    if '支援机械' in tags:
        return (tags.index('支援机械'),)
    for tag in Guaranteed_FOUR:
        if set(tag).issubset(set(tags)):
            a = len(tag)
            if a == 1:
                return (tags.index(tag[0]),)
            if a == 2:
                return tags.index(tag[0]), tags.index(tag[1])
            if a == 3:
                return tags.index(tag[0]), tags.index(tag[1]), tags.index(
                    tag[2])
    return False
