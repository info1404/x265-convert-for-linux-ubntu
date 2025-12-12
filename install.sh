#!/bin/bash
# اسکریپت نصب و راه‌اندازی سریع برای لینوکس
# Quick installation script for Linux

echo "=================================="
echo "x265 Video Converter - نصب سریع"
echo "Quick Installation"
echo "=================================="
echo ""

# Check Python
echo "1. بررسی Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python3 یافت نشد!"
    echo "   نصب با: sudo apt install python3 python3-pip"
    exit 1
fi

# Check pip
echo ""
echo "2. بررسی pip..."
if command -v pip3 &> /dev/null; then
    echo "   ✅ pip3 نصب شده است"
else
    echo "   ❌ pip3 یافت نشد!"
    echo "   نصب با: sudo apt install python3-pip"
    exit 1
fi

# Check FFmpeg
echo ""
echo "3. بررسی FFmpeg..."
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n 1)
    echo "   ✅ $FFMPEG_VERSION"
else
    echo "   ❌ FFmpeg یافت نشد!"
    echo "   نصب با: sudo apt install ffmpeg"
    exit 1
fi

# Check ffprobe
if command -v ffprobe &> /dev/null; then
    echo "   ✅ ffprobe نصب شده است"
else
    echo "   ❌ ffprobe یافت نشد!"
    echo "   نصب با: sudo apt install ffmpeg"
    exit 1
fi

# Install Python packages
echo ""
echo "4. نصب کتابخانه‌های Python..."
pip3 install -q tqdm psutil
if [ $? -eq 0 ]; then
    echo "   ✅ tqdm و psutil نصب شدند"
else
    echo "   ❌ خطا در نصب کتابخانه‌ها"
    exit 1
fi

# Test import
echo ""
echo "5. بررسی کتابخانه‌ها..."
python3 -c "import tqdm; import psutil" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "   ✅ همه ماژول‌ها قابل استفاده هستند"
else
    echo "   ❌ خطا در import کتابخانه‌ها"
    exit 1
fi

# Make executable
chmod +x video_converter.py 2>/dev/null

# Test program
echo ""
echo "6. تست برنامه..."
python3 video_converter.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ برنامه آماده اجراست!"
else
    echo "   ⚠️  برنامه ممکن است مشکل داشته باشد"
fi

# Create directories
mkdir -p output logs 2>/dev/null

echo ""
echo "=================================="
echo "✅ نصب با موفقیت انجام شد!"
echo "Installation completed successfully!"
echo "=================================="
echo ""
echo "برای اجرا:"
echo "  python3 video_converter.py video.mp4"
echo ""
echo "برای راهنما:"
echo "  python3 video_converter.py --help"
echo ""
echo "مثال:"
echo "  python3 video_converter.py /path/to/videos/*.mp4"
echo ""
