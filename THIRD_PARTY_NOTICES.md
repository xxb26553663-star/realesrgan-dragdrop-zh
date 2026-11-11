# 第三方来源

本仓库的 MIT LICENSE 只覆盖这里的拖拽封装与辅助脚本。

| 组件 | 用途 | 来源与许可 |
| --- | --- | --- |
| Real-ESRGAN | 超分算法、模型来源 | https://github.com/xinntao/Real-ESRGAN · BSD-3-Clause，见 licenses/Real-ESRGAN-LICENSE.txt |
| Real-ESRGAN-ncnn-vulkan | 本机 Vulkan 推理程序 | https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan · MIT，包含对 nihui/realsr-ncnn-vulkan 的署名，见 licenses/Real-ESRGAN-ncnn-vulkan-LICENSE.txt |
| Python | 发布版启动程序的解释器 | https://www.python.org/ · PSF 及附带许可，见 licenses/Python-LICENSE.txt |
| Pillow | 图片读取、方向处理及保存 | https://github.com/python-pillow/Pillow · HPND 及附带许可，见 licenses/Pillow-LICENSE.txt |
| PyInstaller bootloader | 独立启动程序打包 | https://pyinstaller.org/ · GPL-2.0-or-later 及分发例外，见 licenses/PyInstaller-COPYING.txt；构建时保留随包附带的例外文本 |

引擎与权重不会随本仓库或本项目发布 ZIP 再分发，而由 `setup-engine.ps1` 从原作者发布页获取。上游推理程序还使用 ncnn、libwebp、stb、dirent 等组件，其说明见上游仓库 README。

固定引擎：Real-ESRGAN v0.2.5.0 / realesrgan-ncnn-vulkan-20220424-windows.zip。

SHA-256：`ABC02804E17982A3BE33675E4D471E91EA374E65B70167ABC09E31ACB412802D`。
