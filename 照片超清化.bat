@echo off
chcp 65001 >nul
if exist "%~dp0RealesrganDragDrop.exe" (
  "%~dp0RealesrganDragDrop.exe" --style photo %*
) else (
  py -3 "%~dp0upscale.py" --style photo %*
)
