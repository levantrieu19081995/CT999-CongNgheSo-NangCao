@echo off
chcp 65001 >nul
title CT999 - Dashboard Iris
cd /d "%~dp0.."
set "IRIS_PYTHON=python"
if exist ".venv\Scripts\python.exe" set "IRIS_PYTHON=%CD%\.venv\Scripts\python.exe"
echo CT999 - DASHBOARD DU LIEU IRIS
echo Mo trinh duyet tai http://127.0.0.1:8504
echo Nhan Ctrl+C de dung chuong trinh.
"%IRIS_PYTHON%" -X utf8 -m streamlit run src\dashboard.py --server.address 127.0.0.1 --server.port 8504 --browser.gatherUsageStats false
if errorlevel 1 pause
