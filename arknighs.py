#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @github: GreenSulley/ArknightsAutoHelper
# @file: arknighs.py
# @createtime: 2021/7/26 16:55 Green Sulley
# @lastupdate: 2021/7/30 11:37 Green Sulley
# @desc: Arknights Auto Helper based on ADB and Python
import yaml
import time
from typing import List, Tuple
from random import randint, uniform

from loguru import logger

from lib import adb
from lib import utils
from lib import recruitment  # 公招
from lib import notifier

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

with open('data/tap_location.yaml') as f:
    data_tap_location = yaml.load(f, Loader=yaml.FullLoader)


class Player:
    def __init__(self, username, password, devices_id):
        self.account = {
            "u": username,
            "p": password
        }
        self.devices = adb.AndroidDebugBridge(devices_id)

    def tap_loaction(self, *args: str) -> bool:
        """
        根据固定的屏幕坐标点击, 如果是二维数组(左上角,右上角)那么随机取点
        :param args: 数据逐层解包
        :return: 是否成功
        """
        value = data_tap_location
        try:
            for arg in args:
                value = value[arg]
            if isinstance(value[0], list):
                c = uniform(value[0][0], value[1][0])
                d = uniform(value[0][1], value[1][1])
                self.devices.tap(c, d)
                logger.debug(f"屏幕点击 ({c}, {d})")
            else:
                self.devices.tap(value[0], value[1])
                logger.debug(f"屏幕点击 {value[0]}, {value[1]}")
        except:
            logger.debug(f"屏幕点击 {value[0]}{value[1]} 失败")
            return False
        else:
            return True

    def tap_screenshot(self, *args: str) -> bool:
        """
        根据给定的图片模板匹配在屏幕上的位置,点击中心
        :param args: 数据逐层解包成图片路径
        :return: 是否成功
        """
        n = len(args)
        path = 'image'
        for arg in args:
            path += str("/" + arg)
        locat = utils.match_image(utils.img_np_cv2(path),
                                  self.devices.get_screenshot())
        if locat:
            logger.debug(f"屏幕点击({locat[0]},{locat[1]})")
            self.devices.tap(locat[0], locat[1])
            return True
        else:
            # logger.info()
            return False

    def exist_screenshot(self, *args: str) -> bool:
        """
        判断给定的图片是否存在于当前屏幕
        :param args: 数据逐层解包成图片路径
        :return: 是否成功
        """
        n = len(args)
        path = 'image'
        for arg in args:
            path += str("/" + arg)
        locat = utils.match_image(utils.img_np_cv2(path),
                                  self.devices.get_screenshot())
        if locat:
            return True
        else:
            # logger.info()
            return False

    def signin(self):
        """
        登录并完成签到,关闭公共及活动
        :return:
        """
        while False:
            start_exist = utils.match_image(
                utils.img_np_cv2('image/start.jpeg'),
                self.devices.get_screenshot())
            if start_exist:
                self.devices.tap(start_exist[0], start_exist[1])
                return True
            else:
                time.sleep(30)  # 30秒检查一次
        while False:
            wake = utils.match_image(utils.img_np_cv2('image/开始唤醒.jpeg'),
                                     self.devices.get_screenshot())
            if wake:
                self.devices.tap(wake[0], wake[1])
                return True
            else:
                time.sleep(30)  # 30秒检查一次
        inindex = False  # 是否处于主页
        while inindex is False:
            ter = self.exist_screenshot('终端.jpeg')
            if ter:
                inindex = True
            else:
                pass  # todo
        return True

    def back_to_index(self):
        """
        在任意位置退回主页
        :return:
        """
        if self.exist_screenshot('终端.jpeg'):
            logger.info("已经位于主页")
            return True
        if self.tap_screenshot('主页标签.jpeg'):
            logger.info("点击顶部主页按钮")
            time.sleep(1)
            if self.tap_screenshot('主页标签2.jpeg'):
                logger.info("点击返回主页按钮")
            else:
                logger.info("找不到返回主页按钮")
        else:
            logger.info("找不到顶部主页按钮")
        if self.exist_screenshot('终端.jpeg'):
            return True
        else:
            logger.info("返回主页失败")
            return False

    def public_recruitment(self):
        """
        公共招募,对接OCR
        :return:
        """
        # 收菜
        for i in range(3):
            logger.info(f'招募干员(收菜) 共3次 第{i + 1}次')
            if self.exist_screenshot('公招', f'完成{i + 1}.jpeg'):
                self.tap_screenshot('公招', '完成.jpeg')
                time.sleep(1)
                self.devices.tap(1842, 73)
                time.sleep(1.5)
                self.devices.tap(randint(100, 1800), randint(100, 1080))
                time.sleep(1)
        # 种菜
        for i in range(3):
            logger.info(f'启动新的公招(种菜) 共3次 第{i + 1}次')
            self.tap_screenshot('公招', '启动公招.jpeg')
            time.sleep(0.5)
            while True:
                screenshot = self.devices.get_screenshot()[550:725, 530:1290]
                tags = recruitment.ocr_tags(utils.cv2_to_base64(screenshot))
                selected_tags = recruitment.recruitment(tags)
                if selected_tags:
                    for s_id in selected_tags:
                        self.tap_loaction('recruitment', 'tags', s_id)
                    if '支援机械' in tags:
                        for j in range(3):
                            self.tap_loaction('recruitment', 'hour', 'add')
                        for k in range(10):
                            self.tap_loaction('recruitment', 'minute', 'reduce')
                    else:
                        self.tap_loaction('recruitment', 'hour', 'reduce')
                    self.tap_screenshot('公招', '开始.jpeg')
                    break
                else:
                    # if self.tap_screenshot('公招', '刷新.jpeg'):
                    #     logger.info(f'刷新标签')
                    #     continue
                    # else:
                    #     self.tap_loaction('recruitment', 'hour', 'reduce')
                    #     self.tap_screenshot('公招', '开始.jpeg')
                    #     break
                    self.tap_loaction('recruitment', 'hour', 'reduce')
                    self.tap_screenshot('公招', '开始.jpeg')
                    break
            time.sleep(1.5)

    def fixed_start(self):
        """
        在卡关界面,进入卡关
        :return: 是否成功
        """
        if self.exist_screenshot('卡关','代理指挥开启.jpeg'):  # 在卡关界面判断是否可代理
            logger.info("本卡关可使用代理指挥")
            for j in range(5):  # 5次循环尝试
                location = self.tap_screenshot('卡关','开始行动.jpeg')  # 点击开始行动
                if location:
                    logger.info(f"开始行动 成功进入编队")
                    time.sleep(1)  # 等待进入
                    for i in range(3):  # 3次循环尝试
                        location2 = self.tap_screenshot('卡关','开始行动干员.jpeg')
                        if location2:
                            logger.info(f"干员开始行动 成功进入卡关 第{i + 1}次尝试 ")
                            break
                        else:
                            logger.info(f"无法找到干员开始行动 第{i + 1}次尝试 ")
                            time.sleep(1)
                            if i == 2:
                                return False
                    break
                else:
                    logger.info(f"无法找到开始行动 第{j + 1}次尝试")
                    if j == 4:
                        logger.info(f"无法找到开始行动 第{j + 1}次尝试 已退出")
                        return False
        else:
            logger.info("不可使用代理指挥")
            return False
        # 判读是否出卡关
        over = False
        i = 0
        time.sleep(45)
        while over is False:  # while not over
            i += 1
            screenshot = self.devices.get_screenshot()
            if self.exist_screenshot('卡关','行动结束.jpeg'):
                logger.info(f"卡关已结束 退回界面")
                self.devices.tap(randint(100, 1800),
                                 randint(100, 1080))  # 随机点出结算屏幕
                time.sleep(2)  # 结算点出后,加载的时间
                # todo 如果还未加载出卡关
                over = True
            else:
                logger.info(f"卡关还未结束 第{i}次尝试")
                time.sleep(15)  # 等待下一次屏幕检查
        return True

    def receive_task(self):
        """
        自动领取任务
        :return:
        """
        self.back_to_index()
        if self.tap_loaction('index', 'task'):
            time.sleep(2)
            if self.tap_screenshot('任务', '收集全部.jpeg'):
                while not self.exist_screenshot('任务','主线任务.jpeg'):
                    time.sleep(3)
                    self.devices.tap(randint(300, 1600), randint(500, 1080))
                time.sleep(1)
            if self.tap_screenshot('任务', '周常任务.jpeg'):
                time.sleep(1)
                if self.tap_screenshot('任务', '收集全部.jpeg'):
                    while not self.exist_screenshot('任务', '主线任务.jpeg'):
                        time.sleep(3)
                        self.devices.tap(randint(300, 1600), randint(500, 1080))
                    time.sleep(1)
        else:
            logger.info("未找到任务")
        self.back_to_index()


    def riic(self):
        """
        基建收菜
        :return:
        """
        location = utils.match_image(utils.img_np_cv2(
            'image/基建.jpeg'), self.devices.get_screenshot())  # 点击开始行动
        self.devices.tap(location[0], location[1])
        time.sleep(5)  # 保守点,等5秒
        location = utils.match_image(utils.img_np_cv2(
            'image/基建/基建待办.jpeg'), self.devices.get_screenshot())  # 点击开始行动
        self.devices.tap(location[0], location[1])
        for i in range(3):
            self.tap_loaction('riic', 'matter')
            time.sleep(1)
        return True


    def anni(self, rtype="a"):
        """
        从主页进入终端进入剿灭
        :param: rtype a为切尔诺伯格 b为龙门市区
        :return:
        """
        location = utils.match_image(utils.img_np_cv2(
            'image/终端.jpeg'), self.devices.get_screenshot())  # 点击开始行动
        if location:
            self.devices.tap(location[0], location[1])
            del location
            time.sleep(0.1)  # 等待进入
            self.tap_loaction('terminal', 'anni', 'button')
            time.sleep(0.2)  # 等待进入
            self.tap_loaction('terminal', 'anni', 'current')
            time.sleep(0.3)  # 等待进入
            self.tap_loaction('terminal', 'anni', 'blank')
            time.sleep(0.3)  # 等待进入
            self.tap_loaction('terminal', 'anni', 'map')
            time.sleep(0.3)  # 等待进入
            if rtype == "a":
                qenbg = utils.match_image(
                    utils.img_np_cv2('image/剿灭/切尔诺伯格.jpeg'),
                    self.devices.get_screenshot())
                if qenbg:
                    self.devices.tap(qenbg[0], qenbg[1])
        time.sleep(3)
        return True


    def resource(self, rtype: int):
        """

        :param rtype: 1为空中威胁 2为货物运送 3为粉碎防御 4为资源保障
        :return:
        """
        location = utils.match_image(utils.img_np_cv2(
            'image/终端.jpeg'), self.devices.get_screenshot())  # 点击开始行动
        if location:
            self.devices.tap(location[0], location[1])
            del location
            time.sleep(0.1)  # 等待进入
            self.devices.tap(data_tap_location["terminal"]["resource"][0],
                             data_tap_location["terminal"]["resource"][1])
            time.sleep(0.2)
            # 向左滑动,使四个资源全部展示在屏幕上
            temp = utils.img_np_cv2(f'image/资源收集/{rtype}y.jpeg')
            location = utils.match_image(temp, self.devices.get_screenshot())
            if location:
                self.devices.tap(location[0], location[1])


if __name__ == '__main__':
    xuan = Player(config["account"][1]["username"],
                  config["account"][1]["password"], '9887bc394436343530')
    # xuan.login()
    xuan.receive_task()
