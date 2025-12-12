# راهنمای سریع | Quick Reference

## نصب | Installation

```bash
cd /home/hossein/antigravit
pip install -r requirements.txt
```

## استفاده پایه | Basic Usage

```bash
# تبدیل یک فایل
python video_converter.py video.mp4

# تبدیل چند فایل
python video_converter.py *.mp4

# تبدیل یک پوشه
python video_converter.py /path/to/videos/

# راهنما
python video_converter.py --help
```

## گزینه‌های خط فرمان | Command-Line Options

| Option | Description (فارسی) | Description (English) |
|--------|-------------------|---------------------|
| `input` | فایل(ها) یا پوشه(ها) ورودی | Input file(s) or directory |
| `-o, --output` | پوشه خروجی (پیش‌فرض: output) | Output directory (default: output) |
| `--no-verify` | بدون بررسی خروجی | Skip output verification |
| `--no-resource-check` | بدون بررسی منابع | Skip system resource monitoring |
| `-v, --verbose` | نمایش اطلاعات تفصیلی | Show detailed debug info |
| `-h, --help` | نمایش راهنما | Show help message |

## تنظیمات کیفیت | Quality Settings

| Resolution | CRF | Preset | Action |
|-----------|-----|--------|--------|
| 720p | 23 | medium | تبدیل مستقیم |
| 1080p | 28 | slow | تبدیل مستقیم |
| >1080p | 28 | slow | کاهش به 1080p |
| <720p | - | - | رد می‌شود ❌ |

## ساختار خروجی | Output Structure

```
output/
├── movies/           # فیلم‌ها
│   └── [name]/
├── series/           # سریال‌ها
│   └── [name]/S01/
└── anime/            # انیمه‌ها
    └── [name]/
```

## پیام‌های خطا | Error Messages

| Error | Meaning |
|-------|---------|
| فرمت فایل پشتیبانی نمی‌شود | Unsupported file format |
| این فایل قبلاً به x265 تبدیل شده است | Already x265 encoded |
| کیفیت فیلم مناسب نیست | Quality too low (<720p) |
| تبدیل ناقص بود | Conversion incomplete |

## فایل‌های لاگ | Log Files

```bash
# مشاهده لاگ‌ها
cat logs/conversion.log    # تمام رویدادها
cat logs/errors.log        # فقط خطاها

# حذف لاگ‌ها
rm logs/*.log
```

## مثال‌های کاربردی | Practical Examples

### مثال 1: فیلم
```bash
python video_converter.py "Inception.mp4"
# → output/movies/Inception/Inception.mkv
```

### مثال 2: سریال
```bash
python video_converter.py "Game of Thrones S01E01.mkv"
# → output/series/Game of Thrones/S01/Game of Thrones S01E01.mkv
```

### مثال 3: انیمه
```bash
python video_converter.py "Naruto anime 001.mp4"
# → output/anime/Naruto anime 001/Naruto anime 001.mkv
```

### مثال 4: پردازش دسته‌ای
```bash
python video_converter.py /downloads/movies/*.mp4 --output /media/converted
```

## عیب‌یابی | Troubleshooting

### خطا: ffmpeg not found
```bash
sudo apt install ffmpeg
```

### خطا: No module named 'tqdm'
```bash
pip install tqdm psutil
```

### سیستم کند می‌شود
```bash
# بررسی منابع را غیرفعال کنید
python video_converter.py video.mp4 --no-resource-check
```

## تنظیمات پیشرفته | Advanced Config

ویرایش `config.py`:

```python
# کیفیت بهتر (فایل بزرگتر)
QUALITY_PRESETS = {
    '1080p': {'crf': 23, 'preset': 'slow'}
}

# تبدیل سریعتر (فایل بزرگتر)
QUALITY_PRESETS = {
    '1080p': {'crf': 28, 'preset': 'faster'}
}

# تغییر محدودیت CPU
MAX_CPU_PERCENT = 90
```

## نکات | Tips

✅ **بهترین کیفیت**: CRF 18-23  
✅ **متعادل**: CRF 23-28 (پیش‌فرض)  
✅ **فایل کوچکتر**: CRF 28-32  

✅ **سریع‌ترین**: preset `ultrafast`  
✅ **متعادل**: preset `medium` / `slow`  
✅ **بهترین فشرده‌سازی**: preset `veryslow`  

---

**برای اطلاعات بیشتر، README.md را مطالعه کنید.**  
**For more information, read README.md**
