@echo off
chcp 65001 >nul
color 0F
mode con cols=136 lines=36
title CT999 - 3_Tao_PowerPoint - Le Van Trieu
cd /d "%~dp0.."
set "BTH4_RUNNER=node"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" set "BTH4_RUNNER=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if exist "%~dp0..\..\..\..\..\..\CT605\BoSung_7_8_9_11\runtime" set "PYTHONPATH=%~dp0..\..\..\..\..\..\CT605\BoSung_7_8_9_11\runtime"
set "NODE_PATH=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
echo CT999 - BAI THUC HANH 4 - LE VAN TRIEU - M2526034
echo.
echo ^> node src\tao_slide.mjs docs\noi_dung_slide.md results\Thuyet_trinh_Iris.pptx
"%BTH4_RUNNER%" src\tao_slide.mjs docs\noi_dung_slide.md results\Thuyet_trinh_Iris.pptx
echo.
echo Ban chup ket qua cua so nay truoc khi nhan phim de dong.
pause
