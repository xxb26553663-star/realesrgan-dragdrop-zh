"""Windows drag-and-drop wrapper for the upstream Real-ESRGAN executable."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile

from PIL import Image, ImageOps

VERSION = "1.0.0"
BASE = Path(sys.executable if getattr(sys, "frozen", False) else __file__).resolve().parent
MAX_DIMENSION = 30000


def choose_model(width, height, style="anime"):
    if style == "photo":
        return "realesrgan-x4plus", 4
    if max(width, height) >= 4000:
        return "realesr-animevideov3-x2", 2
    return "realesrgan-x4plus-anime", 4


def check_engine(engine, model):
    if not engine.is_file():
        raise FileNotFoundError("未找到引擎，请先运行同目录的“初始化引擎.bat”。")
    for extension in (".param", ".bin"):
        if not (engine.parent / "models" / (model + extension)).is_file():
            raise FileNotFoundError(f"缺少模型 {model}{extension}，请重新初始化引擎。")


def save_new(image, source):
    suffix = ".jpg" if source.suffix.lower() in (".jpg", ".jpeg") else ".png"
    index = 0
    while True:
        label = "_HD" if index == 0 else f"_HD_{index}"
        destination = source.with_name(source.stem + label + suffix)
        try:
            stream = destination.open("xb")
            break
        except FileExistsError:
            index += 1
    try:
        with stream:
            if suffix == ".jpg":
                with image.convert("RGB") as rgb:
                    rgb.save(stream, format="JPEG", quality=95, subsampling=0)
            else:
                image.save(stream, format="PNG")
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    return destination


def process(source, engine, style):
    source = Path(source).expanduser().resolve(strict=True)
    if not source.is_file():
        raise ValueError("请拖入图片文件，暂不支持文件夹。")
    # All paths passed into the narrow-character upstream program are ASCII
    # relative paths. Its working directory itself may contain Chinese text.
    with tempfile.TemporaryDirectory(prefix="_work_", dir=engine.parent) as work_name:
        work = Path(work_name)
        with Image.open(source) as original:
            with ImageOps.exif_transpose(original) as oriented:
                model, scale = choose_model(*oriented.size, style)
                check_engine(engine, model)
                mode = "RGBA" if "A" in oriented.getbands() or "transparency" in oriented.info else "RGB"
                with oriented.convert(mode) as prepared:
                    prepared.save(work / "input.png")
                print(f"\n{source.name}: {oriented.width}×{oriented.height} → {scale}倍 ({model})", flush=True)
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        subprocess.run(
            [str(engine), "-i", f"{work.name}/input.png", "-o", f"{work.name}/output.png",
             "-m", "models", "-n", model, "-s", str(scale), "-t", "256"],
            cwd=engine.parent, check=True, creationflags=flags,
        )
        with Image.open(work / "output.png") as result:
            if max(result.size) > MAX_DIMENSION:
                ratio = MAX_DIMENSION / max(result.size)
                with result.resize((max(1, round(result.width * ratio)), max(1, round(result.height * ratio))),
                                   Image.Resampling.LANCZOS) as resized:
                    destination = save_new(resized, source)
            else:
                destination = save_new(result, source)
        print(f"完成：{destination}", flush=True)
        return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description="拖入图片，使用本地 Real-ESRGAN 生成 _HD 图片。")
    parser.add_argument("images", nargs="*")
    parser.add_argument("--style", choices=("anime", "photo"), default="anime", help="默认插画；photo 为照片模型")
    parser.add_argument("--engine", type=Path, default=BASE / "runtime" / "realesrgan-ncnn-vulkan.exe")
    parser.add_argument("--no-pause", action="store_true", help="命令行或自动调用时关闭退出等待")
    parser.add_argument("--version", action="version", version=VERSION)
    args = parser.parse_args(argv)
    failures = 0
    if not args.images:
        print("把图片拖到“超清化.bat”或 RealesrganDragDrop.exe 上即可。\n首次使用请先运行“初始化引擎.bat”。")
    else:
        engine = args.engine.expanduser().resolve()
        if not engine.is_file():
            print("未找到引擎，请先运行同目录的“初始化引擎.bat”。", file=sys.stderr)
            failures = len(args.images)
        else:
            for source in args.images:
                try:
                    process(source, engine, args.style)
                except Exception as error:
                    failures += 1
                    print(f"处理失败：{source}\n{error}", file=sys.stderr)
    if not args.no_pause and sys.stdin.isatty():
        try:
            input("\n按回车退出……")
        except EOFError:
            pass
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
