#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @author: Green Sulley
# @license: MIT License
# @project : GreenSulley/ArknightsAutoHelper
# @file: mitm.py
# @desc: Arknights Auto Helper based on ADB and Python


from mitmproxy.options import Options
from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.proxy.server import ProxyServer
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.tools.web.master import WebMaster
from mitmproxy.tools.console.master import ConsoleMaster
from mitmproxy import master

from lib.addons import *

addons = [
    AddHeader(),
    NoAntiAddiction()
]

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


if __name__ == '__main__':
    ops = Options(listen_host='0.0.0.0', listen_port=8089, ssl_insecure=True)
    master = run_dump(ops)
    master.addons.add(*addons)  # 加载插件
    master.run()
