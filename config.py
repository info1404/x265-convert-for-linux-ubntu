"""
Configuration file for x265 video converter
تنظیمات برنامه تبدیل ویدیو به x265
"""

# Supported video formats
SUPPORTED_FORMATS = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.m4v', '.webm']

# Quality presets
QUALITY_PRESETS = {
    '720p': {
        'crf': 26,
        'preset': 'veryfast',
        'max_height': 720
    },
    '1080p': {
        'crf': 25,
        'preset': 'veryfast',
        'max_height': 1080
    },
    'default': {
        'crf': 25,
        'preset': 'veryfast',
        'max_height': 1080
    }
}

# Audio settings
AUDIO_CODEC = 'aac'
AUDIO_BITRATE = '192k'

# Output settings
OUTPUT_EXTENSION = '.mkv'
OUTPUT_FOLDERS = {
    'movie': 'movies',
    'series': 'series',
    'anime': 'anime'
}

# Resource management
MAX_CPU_PERCENT = 80
MIN_AVAILABLE_MEMORY_GB = 2

# Series patterns (regex)
SERIES_PATTERNS = [
    r'[Ss](\d{1,2})[Ee](\d{1,2})',  # S01E01, s01e01
    r'(\d{1,2})[xX](\d{1,2})',      # 1x01, 1X01
    r'[Ss]eason[\s_]?(\d{1,2})[\s_]?[Ee]pisode[\s_]?(\d{1,2})',  # Season 1 Episode 1
]

# Anime keywords
ANIME_KEYWORDS = ['anime', 'انیمه', 'ova', 'oad']

# Logging
LOG_FILE = 'conversion.log'
ERROR_LOG_FILE = 'errors.log'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# FFmpeg settings
FFMPEG_BINARY = 'ffmpeg'
FFPROBE_BINARY = 'ffprobe'

# Messages (Persian)
MESSAGES = {
    'unsupported_format': 'فرمت فایل پشتیبانی نمی‌شود. فرمت‌های مجاز: mp4, mkv, avi, mov, flv, wmv, m4v, webm',
    'already_x265': 'این فایل قبلاً به فرمت x265 تبدیل شده است و نیازی به تبدیل مجدد ندارد.',
    'low_quality': 'کیفیت فایل ورودی پایین است (کمتر از 720p). تبدیل این فایل باعث افت کیفیت بیشتر می‌شود.',
    'incomplete_conversion': 'فرآیند تبدیل کامل نشد. فایل ناقص به پوشه _incomplete منتقل شد تا بتوانید آن را بررسی کنید.',
    'no_video_audio': 'فایل ورودی فاقد تصویر یا صدا است. لطفاً سالم بودن فایل را بررسی کنید.',
    'file_not_found': 'فایل ورودی پیدا نشد. ممکن است حذف یا جابجا شده باشد.',
    'conversion_started': 'عملیات تبدیل آغاز شد. لطفاً صبر کنید...',
    'conversion_completed': 'تبدیل با موفقیت انجام شد.',
    'conversion_failed': 'متاسفانه تبدیل با خطا مواجه شد.',
    'verification_passed': 'فایل خروجی بررسی شد و سالم است.',
    'verification_failed': 'فایل خروجی مشکل دارد (مثلاً تصویر ندارد یا زمان آن با اصل فایل نمی‌خواند).',
    'disk_full': 'فضای کافی در دیسک وجود ندارد. لطفاً فضای خالی ایجاد کنید.',
    'ffmpeg_error': 'خطای داخلی در موتور تبدیل (FFmpeg). ممکن است فایل ورودی خراب باشد.',
    'timeout': 'زمان تبدیل بیش از حد طول کشید و متوقف شد.',
    'interrupted': 'عملیات توسط کاربر متوقف شد.',
}
