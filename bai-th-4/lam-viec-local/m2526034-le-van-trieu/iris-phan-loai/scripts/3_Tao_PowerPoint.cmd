@echo off
chcp 65001 >nul
color 0F
mode con cols=136 lines=36
title CT999 - 3_Tao_PowerPoint - Le Van Trieu
cd /d "%~dp0.."
set "IRIS_NODE=node"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe" set "IRIS_NODE=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe"
if exist "%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules" set "NODE_PATH=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules"
echo CT999 - BAI THUC HANH 4 - LE VAN TRIEU - M2526034
echo.
echo ^> node src\tao_slide.mjs docs\noi_dung_slide.md results\Thuyet_trinh_Iris.pptx
"%IRIS_NODE%" src\tao_slide.mjs docs\noi_dung_slide.md results\Thuyet_trinh_Iris.pptx
if errorlevel 1 (
 echo Chuong trinh bao loi. Kiem tra thong bao phia tren.
 pause
 exit /b 1
)
echo.
echo Chuong trinh hoan tat. Ket qua da luu trong thu muc results.
pause
