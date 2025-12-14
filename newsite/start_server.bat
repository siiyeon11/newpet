@echo off
echo ========================================
echo 메이플스토리 API 프록시 서버 시작
echo ========================================
echo.

REM Python이 설치되어 있는지 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [오류] Python이 설치되어 있지 않습니다.
    echo Python을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python으로 프록시 서버를 시작합니다...
echo.
python proxy_server.py

pause


