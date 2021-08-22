<p align="center">
  <a href="https://github.com/GreenSulley/AutoArknights">
    <img src="https://cdn.jsdelivr.net/npm/skd@1.0.5/arknights-auto-helper/medal.webp" alt="banner">
  </a>
</p>

<div align="center">

# Automatic Arknights

_基于 [OpenCV](https://github.com/opencv/opencv-python)
和 [Mitmproxy](https://github.com/mitmproxy/mitmproxy) | [Requests](https://github.com/psf/requests)
实现的全自动化舟游_
<p align="center">

![GitHub](https://img.shields.io/github/license/GreenSulley/AutoArknights)
![](https://img.shields.io/github/v/release/GreenSulley/AutoArknights?color=blueviolet&include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/GreenSulley/AutoArknights)
![GitHub Repo stars](https://img.shields.io/github/stars/GreenSulley/AutoArknights?style=social)

![Banner](https://cdn.jsdelivr.net/npm/skd@1.0.5/arknights-auto-helper/banner.webp)
</p>
<p align="center">
  <a href="https://docs.amiya.moe/">文档</a>
  ·
  <a href="https://github.com/GreenSulley/AutoArknights/releases">下载</a>
  ·
  <a href="">开始使用</a>
  ·
  <a href="https://github.com/GreenSulley/AutoArknights/blob/master/CONTRIBUTING.md">参与贡献</a>
</p>
</div>

## 缘起

详见博客: 暂未发布

- 高考在即,必须要有一个能撑住一年的护肝助手.
- 太菜,看不懂大佬代码,想要自定义

## 特性

* 操作基于 Android 调试桥,**可选**用 Requests 进行直接发包
* 图片识别基于 OpenCV 模板匹配, 部分数据**可选**由 Mitmproxy 拦截获取
* 公开招募智能分析自动选择,
  判断保底词条 ([流程图](https://github.com/GreenSulley/AutoArknights/blob/main/dev/%E8%AE%BE%E8%AE%A1%E5%9B%BE/recruitment.png))
* 适配含有时间限制的未成年人账号, 也**可选**通过修改回传数据突破限制 (风险未知)
*

准确地理智计算和线路规划,榨干你的最后一滴理智 ([流程图](https://github.com/GreenSulley/AutoArknights/blob/main/dev/%E8%AE%BE%E8%AE%A1%E5%9B%BE/daliy_queue_nolimit.png))

*风险未知: 涉及修改回传数据.*

## 安装

需要 Python 3.8 或以上版本。

> ⚠ **不建议从 GitHub 下载 zip 源码包安装**：这样做会丢失版本信息，且不便于后续更新。

```bash
git clone https://github.com/GreenSulley/AutoArknights
cd ArknightsAutoHelper

pip install -r requirements.txt
```

## 用法

## 实现

### 功能

- [x] 基建干员效率计算
- [x] 公招标签识别 + 计算
- [x] 任务领取 + 基建收菜
- [x] 进入常用卡关,资源,剿灭
- [x] 流程定制
- [ ] 进入任意主线卡关

### 性能

- [ ] 在 Python 中实现 ADB 协议
- [ ] OpenCV 部分使用 C 外部扩展(提升1%性能)
- [ ] 异步、多线程支持

## API

本项目额外提供一个 API

## 维护者

- [GreenSulley](https://github.com/GreenSulley/)

## 致谢

### 依赖

- [Kengxxiao/ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData)
- [Mrs4s/go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

### 参考

- [ninthDevilHAUNSTER/ArknightsAutoHelper](https://github.com/ninthDevilHAUNSTER/ArknightsAutoHelper)
- [InfiniteTsukuyomi/PyAutoGame](https://github.com/InfiniteTsukuyomi/PyAutoGame)
- [LXG-Shadow/Arknights-Dolos](https://github.com/LXG-Shadow/Arknights-Dolos)
- [GhostStar/Arknights-Armada](https://github.com/GhostStar/Arknights-Armada)
- 以及一些暂未开源的项目

## 如何贡献

本项目所有代码均携带有完整且规范的代码注释, 欢迎各位大佬随时进行 Pull Request

## 许可证

除非另有说明，否则所有数据和代码均受 [MIT License](https://github.com/GreenSulley/AutoArknights/blob/main/LICENSE)
许可并处于公共领域。

`image/`中的图片均来自于[上海鹰角网络科技有限公司](https://www.hypergryph.com/)，并受其条款和许可保护。
