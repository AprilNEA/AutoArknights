#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: logger.py
# @createtime: 2021/8/2 上午10:52 Green Sulley
# @lastupdate:
# @desc: Arknights Auto Helper based on ADB and Python
# @desc:
from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="DEBUG")
