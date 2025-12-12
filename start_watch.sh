#!/bin/bash
# راه‌انداز سریع برای حالت نظارت خودکار
# Quick launcher for auto-watch mode

echo "════════════════════════════════════════════════════════════"
echo "      🔍 حالت نظارت خودکار - Auto Watch Mode"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "این برنامه پوشه 'input' را نظارت می‌کند"
echo "فقط کافیست فایل‌های ویدیو را در پوشه input بگذارید"
echo ""
echo "پوشه‌های ایجاد شده:"
echo "  📂 input/          ← فایل‌های ویدیو را اینجا بگذارید"
echo "  📂 input/_processed/ ← فایل‌های پردازش شده"
echo "  📂 input/_failed/   ← فایل‌های ناموفق"
echo "  📂 output/         ← فایل‌های تبدیل شده (x265)"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Create input directory if not exists
mkdir -p input

echo "✅ پوشه 'input' آماده است"
echo ""
echo "🚀 شروع نظارت..."
echo "   برای توقف: Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

# Start watching
python3 auto_watch.py "$@"
