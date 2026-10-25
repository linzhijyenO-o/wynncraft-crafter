@echo off
chcp 65001 >nul
cd /d "%~dp0"
python backend\server.py --port 8765 --open
if errorlevel 1 pause
