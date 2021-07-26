#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: SkuMoe
# @license: MIT License
# @contact: sukeycz0@gmail.com
# @software: PyCharm
# @project : ArknightsAutoHelper
# @file: adb.py
# @time: 2021/7/26 下午2:35
# @desc: Arknights Auto Helper based on ADB and Python
import subprocess

import cv2
import numpy as np


class AndroidDebugBridge:

    @staticmethod
    def adb_shell(command):
        # return [i.decode() for i in
        #         subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        #                          stderr=subprocess.PIPE, ).stdout.readlines()]
        return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, ).stdout.read()

    # 二次初始化ADB桥
    def wifi_init(self):
        self.adb_shell('adb kill-server')
        if self.get_devices():
            self.adb_shell('adb tcpip 5555')
            return True
        else:
            return False

    def get_devices(self, host_head='192.168'):
        _result = self.adb_shell('adb devices')
        usbDev = []
        wifiDev = []
        # print(_result)
        for item in _result:  # 筛选有线无线设备
            body_filter = item.split()
            if 'device' in body_filter:
                if host_head in body_filter[0]:
                    self.connectStatus = True
                    wifiDev.append(body_filter[0])
                else:
                    usbDev.append(body_filter[0])
        if len(usbDev) > 0 or len(wifiDev) > 0:
            if len(wifiDev) > 0:  # 优先返回无线设备
                return wifiDev[0]
            else:
                return usbDev[0]
        else:
            print(self.language[10000])
            return False

    def get_devices_model(self):
        return self.adb_shell('adb shell getprop ro.product.model')[0].split()[
            0]

    def get_size(self):
        body = self.adb_shell('adb -s %s shell wm size' % self.dev)
        body_1 = body[0].split()[2]
        body_2 = re.search('(\d+)x(\d+)', body_1)
        return int(body_2.group(1)), int(body_2.group(2))

    def get_android_version(self):
        body = self.adb_shell(
            f'adb -s {self.dev} shell getprop ro.build.version.release')
        return body[0].split()[0]

    def get_ram_Info(self):
        total = None
        memFree = None
        body = self.adb_shell('adb -s %s shell cat /proc/meminfo' % self.dev)
        if len(body) >= 1:
            for item in body:
                if 'MemTotal:' in item.split():
                    total = int(item.split()[1]) // 1024
                if 'MemFree:' in item.split():
                    memFree = int(item.split()[1]) // 1024
            return str(total) + ' M', str(memFree) + ' M'

    def get_cpu_info(self):
        body = self.adb_shell('adb -s %s shell cat /proc/cpuinfo' % self.dev)
        cpuPro = 0
        cpuInfo = ''
        if len(body) >= 1:
            for i in body:
                if 'processor' in i.split():
                    cpuPro += 1
                if 'Hardware' in i.split():
                    cpuInfo = i.split()[2] + '_' + i.split()[3] + '_' + \
                              i.split()[4]
            return str(cpuInfo), str(cpuPro)

    def get_allpacks(self, filter=''):
        name_list = []
        pack3 = self.adb_shell('adb shell pm list packages -3')
        if filter:
            for packName in pack3:
                if filter in packName:
                    name = str(packName).split(':')
                    name_list.append(name[1].split()[0])
            return name_list
        else:
            return pack3

    def get_activity(self, filter=''):
        # win
        # body = self.adb('adb shell dumpsys activity top | findstr ACTIVITY')
        # Linux
        body = self.adb_shell('adb shell dumpsys activity top | grep ACTIVITY')
        for pack_info in body:
            info = pack_info.split()[1]
            if filter in info:
                return info
        else:
            return False

    def start_app(self, activity):
        start_info = self.adb_shell(f'adb shell am start -n {activity}')
        return start_info

    def get_screenshot(self):
        """
        Take a screenshot of the current device
        :return: image in cv2 format
        """
        screenshot = self.adb_shell('adb shell screencap -p')
        screenshot = cv2.imdecode(
            np.frombuffer(screenshot, np.uint8),
            cv2.IMREAD_COLOR)
        # 调试 开发
        # cv2.namedWindow("Image")
        # cv2.imshow("Image", screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cv2.imwrite('start10.jpeg', screenshot)
        return screenshot

    def tap(self, x, y, duration=0):
        if duration:
            return self.adb_shell(f'adb shell input swipe {x} {y} {x} {y} {duration}')
        else:
            return self.adb_shell(f'adb shell input tap {x} {y}')

    def swipe(self, x1, y1, x2, y2):
        return self.adb_shell(f'adb shell input swipe {x1} {y1} {x2} {y2}')

    def keyevent(self, key):
        return self.adb_shell(f'adb shell input keyevent {key}')

    def input_text(self, text):
        return self.adb_shell(f"adb shell input text '{str(text)}'")

    def wake(self):
        return self.keyevent(26)
# 依赖调试
if __name__ == '__main__':
    devices = AndroidDebugBridge()
    # print(devices.get_allpacks())
    # print(devices.get_activity())
    # a = devices.start_app('com.hypergryph.arknights/com.u8.sdk.U8UnityContext')
    # print(a)
    # import time
    # time.sleep(5)
    # devices.get_screenshot()
    print(devices.wake())
