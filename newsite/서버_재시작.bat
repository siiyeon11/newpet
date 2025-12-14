@echo off
echo ========================================
echo 기존 서버 종료 중...
echo ========================================

REM 포트 8000을 사용하는 프로세스 찾기 및 종료
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo 프로세스 %%a 종료 중...
    taskkill /F /PID %%a >nul 2>&1
)

timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo 새 서버 시작 중...
echo ========================================
echo.

python proxy_server.py

pause



