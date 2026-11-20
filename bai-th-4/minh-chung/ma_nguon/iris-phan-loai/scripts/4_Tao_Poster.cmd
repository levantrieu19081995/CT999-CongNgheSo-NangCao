@echo off
chcp 65001 >nul
color 0F
mode con cols=136 lines=36
title CT999 - 4_Tao_Poster - Le Van Trieu
cd /d "%~dp0.."
set "IRIS_PYTHON=python"
if exist ".venv\Scripts\python.exe" set "IRIS_PYTHON=%CD%\.venv\Scripts\python.exe"
echo CT999 - BAI THUC HANH 4 - LE VAN TRIEU - M2526034
echo.
echo ^> python src\tao_poster.py --project . --out results\Poster_Iris_A0.pdf
"%IRIS_PYTHON%" -X utf8 src\tao_poster.py --project . --out results\Poster_Iris_A0.pdf
if errorlevel 1 (
 echo Chuong trinh bao loi. Kiem tra thong bao phia tren.
 pause
 exit /b 1
)
echo.
echo Chuong trinh hoan tat. Ket qua da luu trong thu muc results.
pause
