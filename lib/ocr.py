#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: ocr.py
# @time: 2021/7/29 19:47 Green Sulley
# @lastupdate: 2021/7/30 11:37 Green Sulley
# @desc: Arknights Auto Helper based on ADB and Python
import json
import base64
from typing import List

import yaml

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.ocr.v20181119 import ocr_client, models

import utils

with open('../config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

with open('../data/character.json') as f:
    character = json.load(f)


def tencent_ocr(img_base64: bytes) -> List:
    try:
        # 实例化认证对象
        cred = credential.Credential(config["ocr"]["tencent"]["SecretId"],
                                     config["ocr"]["tencent"]["SecretKey"])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化client选项
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile

        # 实例化请求产品
        client = ocr_client.OcrClient(cred, "ap-beijing", clientProfile)
        req = models.GeneralBasicOCRRequest()
        # 填充请求参数
        params = {
            "ImageBase64": img_base64.decode(),
            "LanguageType": config["ocr"]["tencent"]["LanguageType"]
        }
        req.from_json_string(json.dumps(params))
        resp = client.GeneralBasicOCR(req)
        texts = json.loads(resp.to_json_string())
        tags = []
        for text in texts["TextDetections"]:
            if text["Confidence"] >= 85:
                tags.append({
                    "name": text["DetectedText"],
                    "loc": {
                        "x": text["ItemPolygon"]["X"],
                        "y": text["ItemPolygon"]["Y"]
                    }
                })
        # fixme 优化算法，！稳定性
        # 排序 标签 位置
        sorted(tags, key=lambda tag: tag['loc']['x'], reverse=True)
        sorted(tags, key=lambda tag: tag['loc']['y'], reverse=True)
        # print(tags)
        return tags
    except TencentCloudSDKException as err:
        # print(err)
        return err


def recuitment(tags: List[str]) -> List[int]:
    result = [0]
    return result


if __name__ == '__main__':
    recuitment()
