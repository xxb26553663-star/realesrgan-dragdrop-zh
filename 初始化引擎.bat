@echo off
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-engine.ps1"
if errorlevel 1 echo 初始化失败，请查看上方信息。
pause
