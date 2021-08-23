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
import pkgutil

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
# 导入对应产品模块的client models。
from tencentcloud.ocr.v20181119 import ocr_client, models

from lib import utils

config = yaml.load(pkgutil.get_data('lib', '../config.yaml'),
                   Loader=yaml.FullLoader)

character = json.loads(pkgutil.get_data('lib', '../data/gamedata/character.json'))


def tencent_ocr(img_base64: bytes):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
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
        resp_text = resp.to_json_string()
        return resp_text

    except TencentCloudSDKException as err:
        # print(err)
        return err
