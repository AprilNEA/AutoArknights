#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: mitm.py
# @desc: Arknights Auto Helper based on ADB and Python
import json
import pkgutil
from typing import Dict

import yaml
from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.tools.web.master import WebMaster
from mitmproxy.tools.console.master import ConsoleMaster
from mitmproxy import master

from lib import utils
from lib.addons import *

config = yaml.load(pkgutil.get_data('lib', '../config.yaml'),
                   Loader=yaml.FullLoader)

addons = [
    AddHeader()  # 状态检测
]
base_loc = '../../data/account/'


def run_web(options):
    webserver = WebMaster(options)
    webserver.server = ProxyServer(ProxyConfig(options))
    return webserver  # type: master.Master


def run_dump(options):
    server = DumpMaster(options, with_termlog=False, with_dumper=False)
    server.server = ProxyServer(ProxyConfig(options))
    return server  # type: master.Master


def run_console(options):
    server = ConsoleMaster(options)
    server.server = ProxyServer(ProxyConfig(options))
    return server  # type: master.Master


def start(uid, stype='dump'):
    if stype == 'dump':
        if config["noaddiction"]:
            addons.append(NoAntiAddiction())
        if config["mode"] != "img":
            addons.append(DataIntercept(uid))
        ops = Options(listen_host='10.0.0.142', listen_port=8089,
                      ssl_insecure=True)
        master = run_dump(ops)
        master.addons.add(*addons)  # 加载插件
        master.run()


def updata_syncdata(data: Dict, username: str):
    with open(f"{base_loc}{username}/sync/{utils.get_bjtime()['daytime']}.json",
              mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data))
