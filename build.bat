@echo off
setlocal enabledelayedexpansion

echo [*] Starting build process for InstaSend...
echo [*] Building InstaSend.exe...
uv run pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --icon="assets/icon.ico" ^
    --add-data "assets;assets" ^
    --name "InstaSend" ^
    InstaSend.py

pause    
