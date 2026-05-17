@echo off
echo 🧠 QuizMaster - Starting Application
echo =====================================

REM Try different Python commands
echo Attempting to start QuizMaster...

REM Method 1: Try python
python app.py 2>nul
if %errorlevel% equ 0 goto :success

REM Method 2: Try py
py app.py 2>nul
if %errorlevel% equ 0 goto :success

REM Method 3: Try python3
python3 app.py 2>nul
if %errorlevel% equ 0 goto :success

REM Method 4: Try full path
"C:\Users\aryan\AppData\Local\Microsoft\WindowsApps\python.exe" app.py 2>nul
if %errorlevel% equ 0 goto :success

REM If all methods fail
echo ❌ Python not found or not working
echo.
echo 💡 Solutions:
echo 1. Install Python from python.org
echo 2. Add Python to PATH
echo 3. Install from Microsoft Store
echo.
echo Press any key to exit...
pause >nul
goto :end

:success
echo ✅ QuizMaster started successfully!

:end