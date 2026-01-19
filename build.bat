@echo off
setlocal enabledelayedexpansion

echo [*] Starting build process for InstaSend...

:: Check for uv
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 'uv' not found. Please install uv.
    pause
    exit /b
)

:: Ensure PyInstaller is available in the environment
echo [+] Installing/Ensuring PyInstaller via uv...
uv add pyinstaller --dev

:: Build the executable using uv run pyinstaller
echo [*] Building InstaSend.exe...
uv run pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --icon="assets/icon.ico" ^
    --add-data "assets;assets" ^
    --name "InstaSend" ^
    InstaSend.py

if %errorlevel% equ 0 (
    echo.
    echo [+] Build successful! 
    echo [+] Executable is located in the 'dist' folder.
) else (
    echo.
    echo [-] Build failed. Please check the logs above.
)

pause
