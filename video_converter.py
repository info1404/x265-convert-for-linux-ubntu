#!/usr/bin/env python3
"""
x265 Video Converter
تبدیل‌کننده ویدیو به x265

A comprehensive tool for converting video files to x265 (HEVC) format
with intelligent quality detection, batch processing, and progress tracking.

ابزار جامع برای تبدیل فایل‌های ویدیویی به فرمت x265 با تشخیص کیفیت هوشمند،
پردازش دسته‌ای و ردیابی پیشرفت.
"""
import os
import sys
import argparse
import glob
from modules.validator import Validator
from modules.converter import Converter
from modules.categorizer import Categorizer
from modules.verifier import Verifier
from modules.logger import logger
from modules.progress import BatchProgressTracker
from modules.resource_manager import ResourceManager
from modules.utils import format_size, format_time


class VideoConverter:
    """
    Main video converter application
    برنامه اصلی تبدیل ویدیو
    """
    
    def __init__(self, output_dir='output', verify=True):
        """
        Initialize video converter
        راه‌اندازی تبدیل‌کننده ویدیو
        """
        self.output_dir = output_dir
        self.verify = verify
    
    def convert_single_file(self, input_file):
        """
        Convert a single video file
        تبدیل یک فایل ویدیو
        
        Returns:
            True if successful, False otherwise
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"پردازش: {os.path.basename(input_file)}")
        logger.info(f"{'='*60}")
        
        # Validate file
        validation = Validator.validate_file(input_file)
        if not validation:
            logger.error(f"✗ خطا: {validation.error_message}")
            return False
        
        metadata = validation.metadata
        
        # Categorize and determine output path
        categorization = Categorizer.categorize_file(input_file, self.output_dir)
        output_file = categorization['output_file']
        
        logger.info(f"نوع: {categorization['type']}")
        logger.info(f"کیفیت: {metadata['quality']}")
        logger.info(f"مسیر خروجی: {output_file}")
        
        # Check if output already exists
        if os.path.exists(output_file):
            logger.warning(f"فایل خروجی از قبل موجود است، رونویسی می‌شود")
        
        # Convert
        converter = Converter(input_file, output_file, metadata)
        success = converter.convert()
        
        if not success:
            logger.error(f"✗ تبدیل ناموفق بود")
            return False
        
        # Verify output
        if self.verify:
            logger.info("بررسی فایل خروجی...")
            expected_duration = metadata.get('duration')
            input_size = os.path.getsize(input_file)
            verified = Verifier.verify_output(output_file, expected_duration, input_size)
            
            if not verified:
                logger.error(f"✗ فایل خروجی معتبر نیست")
                return False
        
        # Display file sizes
        input_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_file)
        compression_ratio = (1 - output_size / input_size) * 100
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ تبدیل موفق")
        logger.info(f"حجم ورودی: {format_size(input_size)}")
        logger.info(f"حجم خروجی: {format_size(output_size)}")
        logger.info(f"فشرده‌سازی: {compression_ratio:.1f}%")
        logger.info(f"{'='*60}\n")
        
        return True
    
    def convert_batch(self, input_files, check_resources=True):
        """
        Convert multiple video files
        تبدیل چندین فایل ویدیو
        
        Returns:
            dict with statistics
        """
        total_files = len(input_files)
        logger.info(f"\n{'='*60}")
        logger.info(f"پردازش دسته‌ای: {total_files} فایل")
        logger.info(f"{'='*60}\n")
        
        # Log system stats
        if check_resources:
            ResourceManager.log_system_stats()
        
        # Initialize batch progress tracker
        batch_progress = BatchProgressTracker(total_files)
        
        # Convert each file
        for input_file in input_files:
            # Check system resources before each conversion
            if check_resources and ResourceManager.is_system_overloaded():
                logger.warning("سیستم تحت فشار است. منتظر می‌مانیم...")
                ResourceManager.wait_for_resources()
            
            # Convert file
            success = self.convert_single_file(input_file)
            
            # Update batch progress
            if success:
                batch_progress.update('completed')
            else:
                batch_progress.update('failed')
        
        # Close batch progress
        batch_progress.close()
        
        # Display summary
        summary = batch_progress.get_summary()
        logger.info(f"\n{'='*60}")
        logger.info(f"خلاصه پردازش دسته‌ای:")
        logger.info(f"  مجموع: {summary['total']}")
        logger.info(f"  موفق: {summary['completed']}")
        logger.info(f"  ناموفق: {summary['failed']}")
        logger.info(f"  رد شده: {summary['skipped']}")
        logger.info(f"{'='*60}\n")
        
        return summary


def collect_video_files(paths):
    """
    Collect all video files from given paths
    جمع‌آوری تمام فایل‌های ویدیویی از مسیرهای داده شده
    """
    from config import SUPPORTED_FORMATS
    
    video_files = []
    
    for path in paths:
        # Expand wildcards
        expanded_paths = glob.glob(path)
        
        for expanded_path in expanded_paths:
            if os.path.isfile(expanded_path):
                # Check if it's a video file
                _, ext = os.path.splitext(expanded_path)
                if ext.lower() in SUPPORTED_FORMATS:
                    video_files.append(os.path.abspath(expanded_path))
                    
            elif os.path.isdir(expanded_path):
                # Recursively find video files in directory
                for root, dirs, files in os.walk(expanded_path):
                    # Exclude directories starting with _ (like _processed, _failed)
                    # and output directory
                    dirs[:] = [d for d in dirs if not d.startswith('_') and d != 'output']
                    
                    for file in files:
                        _, ext = os.path.splitext(file)
                        if ext.lower() in SUPPORTED_FORMATS:
                            full_path = os.path.join(root, file)
                            video_files.append(os.path.abspath(full_path))
    
    # Remove duplicates
    video_files = list(set(video_files))
    
    return video_files


def main():
    """
    Main entry point
    نقطه ورود اصلی
    """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='تبدیل فایل‌های ویدیویی به فرمت x265 (HEVC)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌ها:
  %(prog)s video.mp4                          # تبدیل یک فایل
  %(prog)s video1.mp4 video2.mkv             # تبدیل چند فایل
  %(prog)s /path/to/videos/                  # تبدیل تمام فایل‌های یک پوشه
  %(prog)s *.mp4 --output custom_output      # تبدیل با پوشه خروجی سفارشی
  %(prog)s video.mp4 --no-verify             # تبدیل بدون بررسی خروجی
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='فایل(‌ها) یا پوشه(‌ها) ورودی'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='پوشه خروجی (پیش‌فرض: output)'
    )
    
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='بدون بررسی فایل‌های خروجی'
    )
    
    parser.add_argument(
        '--no-resource-check',
        action='store_true',
        help='بدون بررسی منابع سیستم'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='نمایش اطلاعات تفصیلی'
    )
    
    args = parser.parse_args()
    
    # Set logger level
    if args.verbose:
        logger.logger.setLevel(logger.logger.DEBUG)
    
    # Collect video files
    logger.info("جمع‌آوری فایل‌های ویدیویی...")
    video_files = collect_video_files(args.input)
    
    if not video_files:
        logger.error("هیچ فایل ویدیویی یافت نشد!")
        return 1
    
    logger.info(f"{len(video_files)} فایل ویدیویی یافت شد")
    
    # Check output directory
    if not os.path.exists(args.output):
        try:
            os.makedirs(args.output)
            logger.info(f"پوشه خروجی ایجاد شد: {args.output}")
        except OSError as e:
            logger.error(f"خطا در ایجاد پوشه خروجی: {str(e)}")
            return 1
            
    # Create converter
    converter = VideoConverter(
        output_dir=args.output,
        verify=not args.no_verify
    )
    
    # Convert files
    if len(video_files) == 1:
        # Single file
        success = converter.convert_single_file(video_files[0])
        return 0 if success else 1
    else:
        # Batch processing
        summary = converter.convert_batch(
            video_files,
            check_resources=not args.no_resource_check
        )
        
        # Return 0 if all succeeded, 1 otherwise
        return 0 if summary['failed'] == 0 else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("\n\nبرنامه توسط کاربر متوقف شد")
        sys.exit(130)
    except Exception as e:
        logger.critical(f"خطای غیرمنتظره: {str(e)}")
        sys.exit(1)
