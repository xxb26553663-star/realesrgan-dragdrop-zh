@echo off
chcp 65001 >nul
if exist "%~dp0RealesrganDragDrop.exe" (
  "%~dp0RealesrganDragDrop.exe" %*
) else (
  py -3 "%~dp0upscale.py" %*
)
