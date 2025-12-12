@echo off
chcp 65001
cls
echo ===================================================
echo      نصب کننده مبدل ویدیویی x265 (ویندوز)
echo ===================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] پایتون نصب نیست!
    echo لطفاً پایتون را از python.org دانلود و نصب کنید.
    echo هنگام نصب گزینه "Add Python to PATH" را حتماً تیک بزنید.
    pause
    exit /b 1
)

:: Check for FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] برنامه FFmpeg یافت نشد!
    echo برای کارکرد صحیح برنامه، باید FFmpeg را نصب کنید.
    echo 1. به سایت ffmpeg.org بروید و نسخه ویندوز را دانلود کنید.
    echo 2. فایل را اکسترکت کنید.
    echo 3. پوشه bin را به PATH ویندوز اضافه کنید.
    echo.
    echo آیا می‌خواهید ادامه دهید؟ (ممکن است برنامه کار نکند)
    pause
)

echo.
echo در حال نصب کتابخانه‌های مورد نیاز...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] خطا در نصب کتابخانه‌ها.
    pause
    exit /b 1
)

echo.
echo ===================================================
echo      نصب با موفقیت انجام شد!
echo ===================================================
echo.
echo برای اجرای برنامه می‌توانید از دستورات زیر استفاده کنید:
echo python video_converter.py [فایل]
echo python auto_watch.py
echo.
pause
