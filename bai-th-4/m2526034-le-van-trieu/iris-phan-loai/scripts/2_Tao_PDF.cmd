@echo off
chcp 65001 >nul
color 0F
mode con cols=136 lines=36
title CT999 - 2_Tao_PDF - Le Van Trieu
cd /d "%~dp0.."
set "BTH4_RUNNER=python"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" set "BTH4_RUNNER=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%~dp0..\..\..\..\..\..\CT605\BoSung_7_8_9_11\runtime" set "PYTHONPATH=%~dp0..\..\..\..\..\..\CT605\BoSung_7_8_9_11\runtime"
set "NODE_PATH=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
echo CT999 - BAI THUC HANH 4 - LE VAN TRIEU - M2526034
echo.
echo ^> python src\tao_bao_cao.py
"%BTH4_RUNNER%" -X utf8 src\tao_bao_cao.py
echo.
echo Ban chup ket qua cua so nay truoc khi nhan phim de dong.
pause
