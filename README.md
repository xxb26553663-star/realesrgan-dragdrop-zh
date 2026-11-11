# 中文拖图超清化 · Real-ESRGAN Drag & Drop

把图片拖到启动图标上，在原图旁生成放大后的 `_HD` 图片。面向 Windows 的轻量封装，使用本机 GPU 执行 Real-ESRGAN，不上传图片。

本项目负责拖拽入口、中文路径、图片格式转换和输出保存。超分算法与模型来自 [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) 和 [Real-ESRGAN-ncnn-vulkan](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan)，原作者为 Xintao Wang 等，详见 [第三方说明](THIRD_PARTY_NOTICES.md)。

## 下载与使用

1. 从本仓库的 [Releases](https://github.com/xxb26553663-star/realesrgan-dragdrop-zh/releases) 下载 `windows-x64.zip`，完整解压到可写文件夹。
2. 首次双击 **初始化引擎.bat**，从原作者 GitHub 下载固定版本的 Windows 引擎与模型（约 44 MB），并校验 SHA-256。需要能访问 GitHub；已有官方同版本 ZIP 可运行 `powershell -File setup-engine.ps1 -Archive "官方ZIP路径"`。
3. 插画、动漫图片拖到 **超清化.bat** 或 `RealesrganDragDrop.exe`；真实照片拖到 **照片超清化.bat**。
4. 原图旁会生成 `_HD.jpg` 或 `_HD.png`；重复处理自动改为 `_HD_1`、`_HD_2`，避免覆盖已有文件。

发布包包含独立启动程序，无需另外安装 Python。引擎初始化后，整份文件夹可以移动使用；常规图片处理不需要联网。仓库源码 ZIP 需要自行准备 Python 环境，见下文。

## 模型与行为

- 默认插画模式：长边小于 4000 像素，用 `realesrgan-x4plus-anime` 放大 4 倍；其余用 `realesr-animevideov3-x2` 放大 2 倍。
- 照片模式：`realesrgan-x4plus`，4 倍。
- 支持 Pillow 能读取的单帧图片，包括 PNG、JPEG、WebP、BMP、TIFF。多帧文件只处理第一帧。
- 自动应用 EXIF 方向；非 JPEG 输出 PNG。处理后长边最多保留 30000 像素，便于后续排版。
- 输出有上限不代表推理显存有上限：超大图片仍可能耗尽显存。先缩小原图，或按场景使用更轻的模型；本工具尚未实现推理前分片规划。
- 中文、空格路径通过临时 ASCII 相对路径交给引擎处理；临时文件在 `runtime` 下，处理后自动清理。
- 默认模型偏插画，文字、脸部细节和纹理可能出现重绘。放大不能保证恢复真实细节。

## 系统要求

Windows 10/11 64 位，支持 Vulkan 的显卡及相应驱动。独立启动程序由 Python 3.12 构建。上游引擎为 20220424 Windows 发布版，不需要 CUDA 或 PyTorch。

## 源码运行

安装 Python 3.12 与 Windows Python Launcher 后，在本目录执行：

```powershell
py -3 -m pip install -r requirements.txt
powershell -File setup-engine.ps1
py -3 upscale.py --no-pause "图片路径.png"
py -3 upscale.py --style photo --no-pause "照片路径.jpg"
```

也可以用 `--engine "引擎exe路径"` 指向已有引擎；对应 `models` 文件夹必须与引擎在同一目录。

## 构建发布包

```powershell
py -3 -m pip install -r requirements-build.txt
powershell -File build.ps1
```

生成的 ZIP 只带封装程序及说明；首次运行初始化脚本获取上游引擎。源码仓库不包含用户图片、处理结果、预训练权重或机器专用路径。

已完成的功能检查及范围见 [验证记录](VALIDATION.md)。

## 来源与许可证

本地拖拽版于 2026-06-22 建立，本仓库是在该脚本基础上整理的便携版本。封装代码采用 MIT 许可证，见 [LICENSE](LICENSE)。上游 Real-ESRGAN 使用 BSD-3-Clause，其 ncnn-vulkan 封装使用 MIT；本项目保留独立许可证文件与来源链接，不宣称原创超分算法或模型。
