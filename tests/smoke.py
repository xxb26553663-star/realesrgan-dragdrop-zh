"""Real GPU smoke test of an extracted release; writes only generated fixtures."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("launcher", type=Path)
    args = parser.parse_args()
    executable = args.launcher.resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="upscale-smoke-") as temporary:
        folder = Path(temporary) / "中文 空格 测试"
        folder.mkdir()
        bitmap = folder / "图像 样例.bmp"
        transparent = folder / "透明 图像.png"
        photo = folder / "方向 照片.jpg"
        wide = folder / "长边4000.png"
        invalid = folder / "不支持.txt"
        with Image.new("RGB", (24, 16), (100, 50, 200)) as image:
            image.save(bitmap)
            exif = Image.Exif()
            exif[274] = 6
            image.save(photo, exif=exif)
        with Image.new("RGBA", (16, 16), (20, 80, 200, 128)) as image:
            image.save(transparent)
        invalid.write_text("not an image", encoding="utf-8")
        with Image.new("RGB", (4000, 8), (30, 90, 160)) as image:
            image.save(wide)
        originals = {file: digest(file) for file in (bitmap, transparent, photo, wide, invalid)}

        def invoke(*paths, style=None, success=True):
            command = [str(executable), "--no-pause"]
            if style:
                command += ["--style", style]
            command += [str(path) for path in paths]
            result = subprocess.run(command, cwd=temporary, capture_output=True, text=True,
                                    encoding="utf-8", errors="replace", timeout=180)
            if (result.returncode == 0) != success:
                raise AssertionError(result.stdout + result.stderr)

        invoke(bitmap, transparent, photo, wide)
        expected = [("图像 样例_HD.png", (96, 64)), ("透明 图像_HD.png", (64, 64)),
                    ("方向 照片_HD.jpg", (64, 96)), ("长边4000_HD.png", (8000, 16))]
        for name, size in expected:
            with Image.open(folder / name) as image:
                assert image.size == size, (name, image.size)
        with Image.open(folder / "透明 图像_HD.png") as image:
            assert "A" in image.getbands()
        output = folder / "图像 样例_HD.png"
        first = digest(output)
        invoke(bitmap)
        assert digest(output) == first
        assert (folder / "图像 样例_HD_1.png").is_file()
        invoke(photo, style="photo")
        assert (folder / "方向 照片_HD_1.jpg").is_file()
        invoke(invalid, success=False)
        assert not (folder / "不支持_HD.png").exists()
        assert all(digest(file) == before for file, before in originals.items())
        print(json.dumps({"passed": ["Chinese/spaced paths", "foreign working directory", "BMP input",
                                    "PNG alpha", "EXIF orientation", "automatic 2x model", "photo model", "no overwrite",
                                    "originals unchanged", "invalid image failure"]}))


if __name__ == "__main__":
    run()
