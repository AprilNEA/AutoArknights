#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: SkuMoe
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @file: ocr.py
# @time: 2021/7/29 19:47
# @desc: Arknights Auto Helper based on ADB and Python
import json
import base64

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


def tencent_ocr(img_base64):
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
        sorted(tags, key=lambda tag: tag['loc']['x'], reverse=True)
        sorted(tags, key=lambda tag: tag['loc']['y'], reverse=True)
        # print(tags)
        return tags
    except TencentCloudSDKException as err:
        # print(err)
        return err


if __name__ == '__main__':
    img = utils.img_cv2(r'D:\Github\MyArknightsAutoHelper\lib\temp3.jpeg')
    img = img[550:725, 530:1290]  # 裁剪坐标为[y0:y1, x0:x1]
    tencent_ocr(utils.cv2_to_base64(img))
