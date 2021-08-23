#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: quick.py
# @desc: Arknights Auto Helper based on ADB and Python
from loguru import logger

from arknighs import Player


def quick(times=1):
    player = Player(1, 1, '9887bc394436343530')
    for i in range(times):
        player.fixed_start("DH-9")
        logger.info(f"共{times}次 第{i + 1}次")


if __name__ == '__main__':
    quick(50)
