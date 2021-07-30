#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: SkuMoe
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @file: recruitment.py
# @time: 2021/7/29 21:55
# @desc: Arknights Auto Helper based on ADB and Python
import json
from itertools import combinations
from typing import List, Tuple, Dict

with open('../data/character.json') as f:
    data_character = json.load(f)

with open('../data/character_cn.json') as f:
    data_character_cn = json.load(f)

with open('../data/tag.json') as f:
    data_tags = json.load(f)

with open('../data/tagwithch.json') as f:
    data_tag_with_ch = json.load(f)


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


def get_score(characters: List[Dict[str, int]]) -> int:
    """
    计算Tag组合的分数
    :param characters:
    :return: 分数
    """
    score = 0
    # todo 优化算法
    for character in characters:
        if character["s"] == 6:
            score += 10000
        if character["s"] == 5:
            score += 1000
        if character["s"] == 4:
            score += 100
        if character["s"] == 3:
            score += 10
        # 忽略 1/2星 支援小车特殊处理
        # if character["s"] == 2:
        #     score +=
        # if character["s"] == 1:
        #     score +=
    return score


def recruitment(tags: List) -> Tuple[str]:
    """
    根据获得的公招Tags计算出最优组合
    :param tags: 5个公招Tag
    :return: 最优组合
    """
    all_combinations = get_combinations(tags)
    # print(all_combinations)
    best_comb = None
    for comb in all_combinations:
        char = get_character(comb)
        score = get_score(char)
        if best_comb is None:
            best_comb = [comb, score]
        if score > best_comb[1]:
            best_comb = [comb, score]
    return best_comb[0]


if __name__ == '__main__':
    a = recruitment(['治疗', '狙击干员', '高级资深干员'])
    print(a)
