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
import yaml, json
import time, os
from typing import List, Tuple
from random import randint, uniform

from lib import adb
from lib import utils
from lib import recruitment  # 公招
from lib import notifier

from lib.logger import logger

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

with open('data/tap_location.yaml') as f:
    data_tap_location = yaml.load(f, Loader=yaml.FullLoader)


class Player:
    def __init__(self, account_id, devices_id):
        self.__account_id = account_id
        self.__username = config["account"][account_id]["account"]
        self.adb = adb.AndroidDebugBridge(devices_id)
        self.__datapath = utils.get_path('lib', f"../data/account/{self.__username}/")
        if not os.path.exists(self.__datapath):
            os.mkdir(self.__datapath)

    # ====轮子重写=====
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
                self.adb.tap(c, d)
                logger.debug(f"屏幕点击 ({c}, {d})")
            else:
                self.adb.tap(value[0], value[1])
                logger.debug(f"屏幕点击 ({value[0]}, {value[1]})")
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
                                  self.adb.get_screenshot())
        if locat:
            logger.debug(f"屏幕点击({locat[0]},{locat[1]})")
            self.adb.tap(locat[0], locat[1])
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
                                  self.adb.get_screenshot())
        if locat:
            return True
        else:
            # logger.info()
            return False

    # ====游戏具体方法====
    def login(self):
        if self.tap_screenshot('登录', '账号管理.jpeg'):
            if self.tap_screenshot('登录', '账号登录.jpeg'):
                pass

    def signin(self):
        """
        登录并完成签到,关闭公共及活动
        :return:
        """
        while False:
            start_exist = utils.match_image(
                utils.img_np_cv2('image/start.jpeg'),
                self.adb.get_screenshot())
            if start_exist:
                self.adb.tap(start_exist[0], start_exist[1])
                return True
            else:
                time.sleep(30)  # 30秒检查一次
        while False:
            wake = utils.match_image(utils.img_np_cv2('image/开始唤醒.jpeg'),
                                     self.adb.get_screenshot())
            if wake:
                self.adb.tap(wake[0], wake[1])
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
        time.sleep(1)
        if self.exist_screenshot('终端.jpeg'):
            return True
        else:
            logger.info("返回主页失败")
            return False

    # =====游戏休闲方法=====
    def receive_task(self):
        """
        自动领取任务
        :return:
        """
        self.back_to_index()
        if self.tap_loaction('index', 'task'):
            time.sleep(2)
            if self.tap_screenshot('任务', '收集全部.jpeg'):
                while not self.exist_screenshot('任务', '主线任务.jpeg'):
                    time.sleep(3)
                    self.adb.tap(randint(300, 1600), randint(500, 1080))
                time.sleep(1)
            if self.tap_screenshot('任务', '周常任务.jpeg'):
                time.sleep(1)
                if self.tap_screenshot('任务', '收集全部.jpeg'):
                    while not self.exist_screenshot('任务', '主线任务.jpeg'):
                        time.sleep(3)
                        self.adb.tap(randint(300, 1600), randint(500, 1080))
                    time.sleep(1)
        else:
            logger.info("未找到任务")
        self.back_to_index()

    def public_recruitment(self):
        """
        公共招募,对接OCR
        :return:
        """
        # 收菜
        self.back_to_index()
        if self.tap_screenshot('首页', '公开招募.jpeg'):
            for i in range(3):
                logger.info(f'招募干员(收菜) 共3次 第{i + 1}次')
                if self.exist_screenshot('公招', f'完成{i + 1}.jpeg'):
                    self.tap_screenshot('公招', '完成.jpeg')
                    time.sleep(2)
                    self.adb.tap(1842, 73)
                    time.sleep(2)
                    self.adb.tap(randint(100, 1800), randint(100, 1080))
                    time.sleep(1)
            # 种菜
            for i in range(3):
                logger.info(f'启动新的公招(种菜) 共3次 第{i + 1}次')
                self.tap_screenshot('公招', '启动公招.jpeg')
                time.sleep(1)
                while True:
                    screenshot = self.adb.get_screenshot()[550:725, 530:1290]
                    tags = recruitment.ocr_tags(utils.cv2_to_base64(screenshot))
                    selected_tags = recruitment.recruitment(tags)
                    if selected_tags:
                        for s_id in selected_tags:
                            self.tap_loaction('recruitment', 'tags', s_id)
                        if '支援机械' in tags:
                            for j in range(3):
                                self.tap_loaction('recruitment', 'hour', 'add')
                            for k in range(10):
                                self.tap_loaction('recruitment', 'minute',
                                                  'reduce')
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
                time.sleep(2)

    def social_shop(self):
        self.back_to_index()
        if self.tap_screenshot('首页', '采购中心.jpeg'):
            time.sleep(0.5)
            if self.tap_loaction('shop', 'credit'):
                time.sleep(0.5)
                self.tap_loaction('shop', 'get')
                credit_is_enough: bool = True
                num: int = 0
                numb = ['first', 'second', 'third', 'forth', 'fifth']
                while credit_is_enough:
                    num += 1
                    if num > 5:
                        break
                    screen_bef = self.adb.get_screenshot()
                    logger.debug(f"尝试购买第{num}个商品")
                    self.tap_loaction('shop', 'items', numb[num])
                    time.sleep(0.5)
                    if self.exist_screenshot('商店', '商品内容.jpeg'):
                        if self.tap_screenshot('商店', '购买物品.jpeg'):
                            time.sleep(0.3)
                            if self.tap_screenshot('商店', '获得物品.jpeg'):
                                continue
                            else:
                                if self.exist_screenshot('商店', '信用不足无法购买.jpeg'):
                                    logger.info("今日信用已用完")
                                    break
                    else:
                        logger.info("今日信用已用完")
                        break
        else:
            logger.error("无法进入采购中心")
        self.back_to_index()
        return True

    # =====游戏战斗方法=====
    def fixed_start(self, stuck_name=''):
        """
        在卡关界面,进入卡关
        :return: 是否成功
        """
        time.sleep(0.5)
        self.tap_screenshot('卡关', '代理指挥可用.jpeg')
        if self.exist_screenshot('卡关', '代理指挥开启.jpeg'):  # 在卡关界面判断是否可代理
            logger.info("本卡关可使用代理指挥")
            for j in range(5):  # 5次循环尝试
                location = self.tap_screenshot('卡关', '开始行动.jpeg')  # 点击开始行动
                if location:
                    logger.info(f"开始行动 成功进入编队")
                    time.sleep(1)  # 等待进入
                    for i in range(3):  # 3次循环尝试
                        location2 = self.tap_screenshot('卡关', '开始行动干员.jpeg')
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
        proxy_time = None
        if stuck_name:
            try:
                with open(f'{self.__datapath}/proxy_time.json',
                          mode='r',
                          encoding='utf-8') as f:
                    try:
                        proxy_time = json.load(f)
                    except json.decoder.JSONDecodeError:
                        proxy_time = {}
            except FileNotFoundError:
                check_time = 20
            else:
                if stuck_name in proxy_time:
                    check_time = proxy_time[stuck_name]
                else:
                    check_time = 20
        else:
            check_time = 20
        over = False  # 是否结算标识
        i = 0
        time_start = time.time()
        time.sleep(check_time)
        while over is False:  # while not over
            i += 1
            self.tap_screenshot('卡关', '理智恢复.jpeg')
            if self.exist_screenshot('卡关', '行动结束.jpeg'):
                logger.info(f"卡关已结束 退回界面")
                self.adb.tap(randint(100, 1800), randint(300, 600))
                if stuck_name:
                    with open(f'{self.__datapath}/proxy_time.json',
                              mode='w', encoding='utf-8') as f:
                        if proxy_time:
                            if stuck_name not in proxy_time:
                                proxy_time[stuck_name] = time.time() - time_start
                                f.write(json.dumps(proxy_time))
                        elif i >= 2:
                            proxy_time[stuck_name] = time.time() - time_start
                            f.write(json.dumps(proxy_time))
                time.sleep(2)  # 结算点出后,加载的时间
                # todo 如果还未加载出卡关
                over = True
            else:
                logger.info(f"卡关还未结束 第{i}次尝试")
                time.sleep(5)  # 等待下一次屏幕检查
        return True

    def fixed_starts(self, stuck_name: str, t: int):
        if not stuck_name:
            stuck_name = ''
        for i in range(t):
            self.fixed_start(stuck_name)

    def riic(self):
        """
        基建收菜
        :return:
        """
        location = utils.match_image(utils.img_np_cv2(
            'image/基建.jpeg'), self.adb.get_screenshot())  # 点击开始行动
        self.adb.tap(location[0], location[1])
        time.sleep(5)  # 保守点,等5秒
        location = utils.match_image(utils.img_np_cv2(
            'image/基建/基建待办.jpeg'), self.adb.get_screenshot())  # 点击开始行动
        self.adb.tap(location[0], location[1])
        for i in range(3):
            self.tap_loaction('riic', 'matter')
            time.sleep(1)
        return True

    def anni(self, rtype="切尔诺伯格"):
        """
        从主页进入终端进入剿灭
        :param: rtype a为 b为龙门市区
        :return:
        """
        location = utils.match_image(utils.img_np_cv2(
            'image/终端.jpeg'), self.adb.get_screenshot())  # 点击开始行动
        if location:
            self.adb.tap(location[0], location[1])
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
            if rtype == "切尔诺伯格":
                qenbg = utils.match_image(
                    utils.img_np_cv2('image/剿灭/切尔诺伯格.jpeg'),
                    self.adb.get_screenshot())
                if qenbg:
                    self.adb.tap(qenbg[0], qenbg[1])
        time.sleep(3)
        return True

    def resource(self, rtype: str, t: int):
        """

        :param t: 次数
        :param rtype: 1为空中威胁 2为货物运送 3为粉碎防御 4为资源保障 5为战术演习
        :return:
        """
        self.back_to_index()
        if self.tap_screenshot('终端.jpeg'):
            time.sleep(0.5)  # 等待进入
            self.tap_loaction("terminal", "resource", "button")
            time.sleep(0.5)
            self.adb.swipe(1900, randint(500, 600), 1500, randint(500, 600))
            # 向左滑动,使四个资源全部展示在屏幕上
            if rtype == "空中威胁":
                if self.tap_screenshot('资源收集', '空中威胁.jpeg'):
                    stuck_id = 0
                else:
                    logger.info("资源卡关-空中威胁不可用 改为进行战术演习")
                    stuck_id = 'LS'
            elif rtype == "货物运送":
                if self.tap_screenshot('资源收集', '货物运送.jpeg'):
                    stuck_id = 'CE'
                else:
                    logger.info("资源卡关-货物运送不可用 改为进行战术演习")
                    stuck_id = 'LS'
            elif rtype == "粉碎防御":
                if self.tap_screenshot('资源收集', '粉碎防御.jpeg'):
                    stuck_id = 'AP'
                else:
                    logger.info("资源卡关-粉碎防御不可用 改为进行战术演习")
                    stuck_id = 'LS'
            elif rtype == "资源保障":
                if self.tap_screenshot('资源收集', '资源保障.jpeg'):
                    stuck_id = 'SK'
                else:
                    logger.info("资源卡关-资源保障不可用 改为进行战术演习")
                    stuck_id = 'LS'
            else:  # rtype == 5:
                if self.tap_screenshot('资源收集', '战术演习.jpeg'):
                    stuck_id = 'LS'
                else:
                    logger.error("无任何资源卡关可用")
                    return False
            time.sleep(1)
            for i in [5, 4, 3, 2, 1]:
                stuck_name = f"{stuck_id}-{i}"
                if self.tap_screenshot('资源收集', f'{stuck_name}.jpeg'):
                    self.fixed_starts(stuck_name, t)
                    break
                else:
                    logger.debug(f"{stuck_name}暂未通过,尝试进行{stuck_id}-{i - 1}")
                    continue
            return True

    def stuck(self, stuckid: str, t=1):
        if stuckid in ['1-7', '4-4', 'JT8-2']:
            self.back_to_index()
            if self.tap_screenshot('终端.jpeg'):
                time.sleep(0.5)
                if self.tap_loaction('terminal', 'main', 'button'):
                    time.sleep(0.5)
                    # 选择章节
                    if stuckid == '1-7':
                        # if self.exist_screenshot('卡关', '处于觉醒.jpeg'
                        #                          ) or self.tap_screenshot('卡关', '点击觉醒.jpeg'):
                        if self.tap_loaction('terminal', 'mainline', '觉醒'):
                            time.sleep(0.5)
                            while not self.tap_screenshot('卡关',
                                                          '黑暗时代EP01.jpeg'):
                                self.adb.swipe(1428, 560, 1428 + 447, 560,
                                               t=1000)
                                time.sleep(0.5)
                    if stuckid == '4-4':
                        # if self.exist_screenshot('卡关', '处于幻灭.jpeg'
                        #                          ) or self.tap_screenshot('卡关', '点击幻灭.jpeg'):
                        if self.tap_loaction('terminal', 'mainline', '幻灭'):
                            while not self.tap_screenshot('卡关', '急性衰竭.jpeg'):
                                self.adb.swipe(1428, 560, 1428 + 447, 560,
                                               t=1000)
                                time.sleep(0.5)
                    time.sleep(0.5)

                    if stuckid == 'JT8-2':
                        # if self.exist_screenshot('卡关', '处于幻灭.jpeg'
                        #                          ) or self.tap_screenshot('卡关', '点击幻灭.jpeg'):
                        if self.tap_loaction('terminal', 'mainline', '幻灭'):
                            time.sleep(0.5)
                            while not self.tap_screenshot('卡关', '怒号光明.jpeg'):
                                self.adb.swipe(1428, 560, 1428 + 447, 560,
                                               t=1000)
                                time.sleep(0.5)

                    # 选择具体卡关
                    self.adb.swipe(randint(100, 200), randint(500, 600),
                                   randint(1800, 1900), randint(500, 600))
                    while not self.tap_screenshot('卡关', f'{stuckid}.jpeg'):
                        self.adb.swipe(1800, randint(500, 600), 1300,
                                       randint(500, 600), t=1000)
                        time.sleep(0.5)
                    if self.fixed_starts(stuckid, t):
                        time.sleep(0.5)
                        logger.info(f"完成{stuckid}")

        else:
            logger.info('暂不支持此卡关')


if __name__ == '__main__':
    a = Player(1, '')
    # a.stuck('JT8-2')
    # a.receive_task()
    a.social_shop()
