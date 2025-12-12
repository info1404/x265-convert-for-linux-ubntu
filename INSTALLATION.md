# راهنمای اجرای برنامه | How to Run

<div dir="rtl">

این برنامه روی **لینوکس، ویندوز، و macOS** قابل اجرا است.

</div>

---

## 🐧 راهنمای اجرا در لینوکس | Linux Installation

### مرحله 1: نصب پیش‌نیازها

```bash
# به‌روزرسانی سیستم
sudo apt update

# نصب Python 3 (اگر نصب نیست)
sudo apt install python3 python3-pip

# نصب FFmpeg
sudo apt install ffmpeg

# بررسی نصب
python3 --version    # باید Python 3.8+ نمایش دهد
ffmpeg -version      # باید FFmpeg نمایش دهد
```

### مرحله 2: نصب کتابخانه‌های Python

```bash
cd /home/hossein/antigravit

# نصب وابستگی‌ها
pip3 install -r requirements.txt

# یا نصب دستی
pip3 install tqdm psutil
```

### مرحله 3: اجرای برنامه

```bash
# تبدیل یک فایل
python3 video_converter.py video.mp4

# تبدیل چند فایل
python3 video_converter.py video1.mp4 video2.mkv

# تبدیل تمام فایل‌های یک پوشه
python3 video_converter.py /path/to/videos/

# نمایش راهنما
python3 video_converter.py --help
```

### نکات لینوکس:
- ✅ از `python3` به جای `python` استفاده کنید
- ✅ اگر خطای permission دریافت کردید: `chmod +x video_converter.py`
- ✅ برای نصب در سطح کاربر: `pip3 install --user tqdm psutil`

---

## 🪟 راهنمای اجرا در ویندوز | Windows Installation

### مرحله 1: نصب Python

1. دانلود Python از [python.org](https://www.python.org/downloads/)
2. نصب Python (حتماً گزینه "Add Python to PATH" را فعال کنید ✅)
3. بررسی نصب:

```cmd
python --version
```

### مرحله 2: نصب FFmpeg

**روش 1: دانلود مستقیم (توصیه می‌شود)**

1. دانلود FFmpeg از [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
2. یا از [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) نسخه `ffmpeg-release-essentials.zip` را دانلود کنید
3. فایل ZIP را استخراج کنید (مثلاً در `C:\ffmpeg`)
4. اضافه کردن به PATH:
   - Settings → System → About → Advanced system settings
   - Environment Variables → System variables → Path
   - اضافه کردن: `C:\ffmpeg\bin`

5. بررسی نصب:

```cmd
ffmpeg -version
ffprobe -version
```

**روش 2: با Chocolatey (اگر نصب است)**

```cmd
choco install ffmpeg
```

**روش 3: با Scoop**

```cmd
scoop install ffmpeg
```

### مرحله 3: نصب کتابخانه‌های Python

```cmd
cd C:\path\to\antigravit

# نصب وابستگی‌ها
pip install -r requirements.txt

# یا نصب دستی
pip install tqdm psutil
```

### مرحله 4: اجرای برنامه

```cmd
# تبدیل یک فایل
python video_converter.py video.mp4

# تبدیل چند فایل
python video_converter.py video1.mp4 video2.mkv

# تبدیل تمام فایل‌های یک پوشه
python video_converter.py "C:\Videos\*"

# نمایش راهنما
python video_converter.py --help
```

### نکات ویندوز:
- ✅ در ویندوز از `python` (نه `python3`) استفاده کنید
- ✅ مسیرهایی با فاصله را داخل `" "` قرار دهید
- ✅ از PowerShell یا CMD استفاده کنید
- ✅ اگر خطای "python not found" دریافت کردید، Python را مجدداً نصب کنید و "Add to PATH" را فعال کنید

---

## 🍎 راهنمای اجرا در macOS | macOS Installation

### مرحله 1: نصب Homebrew (اگر نصب نیست)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### مرحله 2: نصب پیش‌نیازها

```bash
# نصب Python
brew install python

# نصب FFmpeg
brew install ffmpeg

# بررسی
python3 --version
ffmpeg -version
```

### مرحله 3: نصب کتابخانه‌ها و اجرا

```bash
cd /path/to/antigravit
pip3 install -r requirements.txt
python3 video_converter.py video.mp4
```

---

## 📝 مثال‌های کاربردی | Practical Examples

### لینوکس:

```bash
# تبدیل یک فیلم
python3 video_converter.py "/home/user/Downloads/Movie.mp4"

# تبدیل سریال
python3 video_converter.py ~/Downloads/Series/*.mkv

# پوشه خروجی سفارشی
python3 video_converter.py *.mp4 --output /media/converted
```

### ویندوز:

```cmd
# تبدیل یک فیلم
python video_converter.py "C:\Downloads\Movie.mp4"

# تبدیل سریال
python video_converter.py "C:\Downloads\Series\*.mkv"

# پوشه خروجی سفارشی
python video_converter.py *.mp4 --output "D:\Converted"
```

---

## 🔧 عیب‌یابی | Troubleshooting

### خطا: "python: command not found" (لینوکس)

```bash
# نصب Python
sudo apt install python3 python3-pip

# یا ایجاد alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

### خطا: "python is not recognized" (ویندوز)

**راه‌حل:**
1. Python را مجدداً نصب کنید
2. حتماً گزینه "Add Python to PATH" را فعال کنید
3. یا دستی به PATH اضافه کنید:
   - Settings → System → Environment Variables
   - افزودن: `C:\Users\YourName\AppData\Local\Programs\Python\Python3X`

### خطا: "ffmpeg: command not found"

**لینوکس:**
```bash
sudo apt install ffmpeg
```

**ویندوز:**
- FFmpeg را دانلود و به PATH اضافه کنید (مراحل بالا)
- یا فایل `ffmpeg.exe` را در همان پوشه برنامه قرار دهید

### خطا: "No module named 'tqdm'"

```bash
# لینوکس
pip3 install tqdm psutil

# ویندوز
pip install tqdm psutil
```

### خطا: "Permission denied" (لینوکس)

```bash
chmod +x video_converter.py
```

### برنامه خیلی کند است

```bash
# غیرفعال کردن بررسی منابع
python video_converter.py video.mp4 --no-resource-check

# یا تغییر preset به faster در config.py
```

---

## 🚀 بهینه‌سازی برای سیستم‌های مختلف

### برای سیستم‌های قوی (8+ CPU cores):

ویرایش `config.py`:
```python
QUALITY_PRESETS = {
    '720p': {'crf': 23, 'preset': 'fast'},      # سریع‌تر
    '1080p': {'crf': 28, 'preset': 'medium'}   # سریع‌تر
}
```

### برای سیستم‌های ضعیف (2-4 CPU cores):

```python
QUALITY_PRESETS = {
    '720p': {'crf': 25, 'preset': 'veryfast'},   # خیلی سریع
    '1080p': {'crf': 30, 'preset': 'fast'}      # سریع
}

MAX_CPU_PERCENT = 90  # استفاده بیشتر از CPU
```

---

## 📊 تفاوت‌های سیستم عامل‌ها | OS Differences

| ویژگی | لینوکس | ویندوز | macOS |
|-------|--------|--------|-------|
| **Python Command** | `python3` | `python` | `python3` |
| **Pip Command** | `pip3` | `pip` | `pip3` |
| **FFmpeg نصب** | `apt install` | دانلود دستی | `brew install` |
| **مسیرها** | `/home/user/` | `C:\Users\` | `/Users/` |
| **Wildcards** | `*.mp4` ✅ | `*.mp4` ⚠️ | `*.mp4` ✅ |
| **عملکرد** | بهترین ⭐ | خوب ✅ | عالی ⭐ |

**نکته:** در ویندوز، wildcards (`*.mp4`) ممکن است در PowerShell بهتر کار کند تا CMD.

---

## ✅ بررسی موفقیت نصب

### تست کامل (همه سیستم‌ها):

```bash
# 1. بررسی Python
python3 --version  # یا python در ویندوز

# 2. بررسی FFmpeg
ffmpeg -version
ffprobe -version

# 3. بررسی کتابخانه‌ها
python3 -c "import tqdm; import psutil; print('✅ All modules installed')"

# 4. تست برنامه
python3 video_converter.py --help

# 5. نمایش پوشه خروجی
ls output/  # یا dir output\ در ویندوز
```

اگر همه دستورات بدون خطا اجرا شدند، برنامه آماده است! ✅

---

## 🎯 اجرای سریع | Quick Start

### لینوکس (یک خط):

```bash
cd /home/hossein/antigravit && pip3 install -r requirements.txt && python3 video_converter.py --help
```

### ویندوز (یک خط):

```cmd
cd C:\path\to\antigravit && pip install -r requirements.txt && python video_converter.py --help
```

---

## 💡 نکات حرفه‌ای | Pro Tips

### 1. ایجاد Alias (لینوکس/macOS)

```bash
# اضافه کردن به ~/.bashrc یا ~/.zshrc
alias x265conv="python3 /home/hossein/antigravit/video_converter.py"

# استفاده
x265conv video.mp4
```

### 2. ایجاد Batch File (ویندوز)

ایجاد `convert.bat`:
```bat
@echo off
python "C:\path\to\antigravit\video_converter.py" %*
```

استفاده:
```cmd
convert.bat video.mp4
```

### 3. اجرای Batch در Background (لینوکس)

```bash
nohup python3 video_converter.py /videos/* &> conversion.log &
```

---

## 📞 پشتیبانی | Support

اگر مشکلی داشتید:

1. **لاگ‌ها را بررسی کنید:**
   ```bash
   cat logs/errors.log
   ```

2. **با verbose mode اجرا کنید:**
   ```bash
   python3 video_converter.py video.mp4 --verbose
   ```

3. **نسخه‌ها را چک کنید:**
   ```bash
   python3 --version   # باید 3.8+ باشد
   ffmpeg -version     # باید 4.0+ باشد
   ```

---

<div align="center" dir="rtl">

**✅ برنامه برای لینوکس، ویندوز و macOS بهینه شده است**

**Ready to run on Linux, Windows, and macOS!**

</div>
