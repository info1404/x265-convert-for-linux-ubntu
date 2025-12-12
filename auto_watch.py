#!/usr/bin/env python3
"""
Auto Watch Mode for x265 Video Converter
حالت نظارت خودکار برای تبدیل‌کننده ویدیو

Automatically watches a folder and converts any new video files
به طور خودکار پوشه را نظارت می‌کند و ویدیوهای جدید را تبدیل می‌کند
"""
import os
import sys
import time
import shutil
import argparse
from pathlib import Path
from modules.logger import logger
from modules.validator import Validator
from modules.categorizer import Categorizer
from modules.utils import format_time
from video_converter import VideoConverter, collect_video_files


class WatchFolder:
    """
    Watch folder for new video files and auto-convert
    نظارت بر پوشه و تبدیل خودکار ویدیوهای جدید
    """
    
    def __init__(self, watch_dir='input', output_dir='output', check_interval=5):
        """
        Initialize watch folder
        راه‌اندازی پوشه نظارت
        """
        self.watch_dir = os.path.abspath(watch_dir)
        self.output_dir = output_dir
        self.check_interval = check_interval
        self.processed_files = set()
        self.processing_files = set()
        
        # Create watch directory
        os.makedirs(self.watch_dir, exist_ok=True)
        
        # Initialize converter
        self.converter = VideoConverter(output_dir=output_dir, verify=True)
        
        logger.info(f"📁 پوشه نظارت شده: {self.watch_dir}")
        logger.info(f"📂 پوشه خروجی: {self.output_dir}")
    
    def get_video_files(self):
        """
        Get all video files in watch directory
        دریافت تمام فایل‌های ویدیو در پوشه نظارت
        """
        video_files = collect_video_files([self.watch_dir])
        
        # Filter out files we've already processed or are processing
        new_files = [
            f for f in video_files 
            if f not in self.processed_files and f not in self.processing_files
        ]
        
        return new_files
    
    def is_file_ready(self, filepath, wait_time=2):
        """
        Check if file is completely copied (not being written)
        بررسی کامل بودن کپی فایل
        """
        try:
            initial_size = os.path.getsize(filepath)
            time.sleep(wait_time)
            final_size = os.path.getsize(filepath)
            
            # If size hasn't changed, file is ready
            return initial_size == final_size
        except OSError:
            return False
    
    def process_file(self, filepath):
        """
        Process a single video file
        پردازش یک فایل ویدیو
        """
        filename = os.path.basename(filepath)
        max_retries = 2
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🆕 فایل جدید شناسایی شد: {filename}")
        logger.info(f"{'='*60}")
        
        # Mark as processing
        self.processing_files.add(filepath)
        
        try:
            # Wait for file to be completely copied
            logger.info("⏳ در انتظار کامل شدن کپی فایل...")
            if not self.is_file_ready(filepath, wait_time=3):
                logger.warning("⚠️  فایل هنوز در حال کپی است، صبر می‌کنیم...")
                time.sleep(5)
            
            # --- Check if already converted ---
            # We need to determine the expected output path first
            # Use Validator to get metadata (needed for Categorizer)
            validation = Validator.validate_file(filepath)
            if not validation:
                logger.error(f"❌ فایل نامعتبر است: {filepath}")
                self.processed_files.add(filepath) # Mark as processed to avoid infinite loop
                return

            # Determine output path
            categorization = Categorizer.categorize_file(filepath, self.output_dir)
            output_file = categorization['output_file']
            
            if os.path.exists(output_file):
                logger.info(f"🔍 فایل خروجی یافت شد: {output_file}")
                logger.info("📊 در حال بررسی کامل بودن فایل خروجی...")
                
                # Check duration match
                input_duration = validation.metadata.get('duration', 0)
                
                # Get output duration
                output_validation = Validator.validate_file(output_file)
                output_duration = 0
                if output_validation:
                    output_duration = output_validation.metadata.get('duration', 0)
                
                # Compare durations (allow 1 second difference)
                if abs(input_duration - output_duration) < 2.0:
                    logger.info(f"✅ فایل قبلاً با موفقیت تبدیل شده است (زمان: {format_time(output_duration)})")
                    logger.info("⏭️  عبور از این فایل...")
                    self.processed_files.add(filepath)
                    return
                else:
                    logger.warning(f"⚠️  فایل خروجی ناقص است (اصلی: {format_time(input_duration)}, خروجی: {format_time(output_duration)})")
                    logger.warning("🗑️  حذف فایل خروجی ناقص و شروع مجدد تبدیل...")
                    try:
                        os.remove(output_file)
                    except OSError as e:
                        logger.error(f"خطا در حذف فایل ناقص: {e}")
            
            # --- Start Conversion ---
            
            # Retry loop
            success = False
            for attempt in range(1, max_retries + 1):
                if attempt > 1:
                    logger.warning(f"🔄 تلاش مجدد {attempt}/{max_retries} برای {filename}...")
                
                # Convert file
                success = self.converter.convert_single_file(filepath)
                
                if success:
                    break
                else:
                    logger.error(f"❌ تلاش {attempt} ناموفق بود.")
                    if attempt < max_retries:
                        time.sleep(2)  # Wait a bit before retry
            
            if success:
                logger.info(f"✅ پردازش موفق: {filename}")
                # Do NOT move the file, just mark as processed
                self.processed_files.add(filepath)
            else:
                logger.error(f"❌ پردازش ناموفق برای: {filename}")
                # Do NOT move the file. 
                # We do NOT add to processed_files so it might be retried later if script restarts,
                # but for this session we should probably avoid infinite loop?
                # User said: "if failed... check first...".
                # If we don't add to processed_files, it will be picked up again in next loop (5 sec later).
                # That would cause infinite loop of failures.
                # So we SHOULD add to processed_files (or a failed_files set) to ignore it for THIS session.
                self.processed_files.add(filepath) 
                
        except Exception as e:
            logger.error(f"خطا در پردازش {filename}: {str(e)}")
            self.processed_files.add(filepath) # Avoid getting stuck on this file
        finally:
            # Remove from processing set
            self.processing_files.discard(filepath)
    
    def watch(self):
        """
        Main watch loop
        حلقه اصلی نظارت
        """
        logger.info(f"\n{'='*60}")
        logger.info("🔍 حالت نظارت خودکار فعال شد")
        logger.info(f"{'='*60}")
        logger.info(f"📌 فایل‌های ویدیو را در این پوشه قرار دهید:")
        logger.info(f"   {self.watch_dir}")
        logger.info(f"\n💡 برنامه هر {self.check_interval} ثانیه پوشه را بررسی می‌کند")
        logger.info(f"⏸️  برای توقف: Ctrl+C\n")
        
        try:
            while True:
                # Check for new files
                # logger.debug("Scanning for files...")
                new_files = self.get_video_files()
                
                if new_files:
                    logger.info(f"🔔 {len(new_files)} فایل جدید یافت شد!")
                    logger.debug(f"Files: {new_files}")
                    
                    for filepath in new_files:
                        self.process_file(filepath)
                else:
                    # logger.debug("No new files found.")
                    pass
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n\n🛑 حالت نظارت متوقف شد")
            logger.info(f"📊 تعداد فایل‌های پردازش شده: {len(self.processed_files)}")


def main():
    """
    Main entry point for watch mode
    نقطه ورود اصلی برای حالت نظارت
    """
    parser = argparse.ArgumentParser(
        description='حالت نظارت خودکار - فایل‌ها را در پوشه input قرار دهید',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌ها:
  %(prog)s                                    # نظارت پوشه input (پیش‌فرض)
  %(prog)s --watch /custom/watch/folder      # نظارت پوشه سفارشی
  %(prog)s --interval 10                     # بررسی هر 10 ثانیه
        """
    )
    
    parser.add_argument(
        '-w', '--watch',
        default='input',
        help='پوشه‌ای که نظارت می‌شود (پیش‌فرض: input)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='پوشه خروجی (پیش‌فرض: output)'
    )
    
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=5,
        help='زمان بررسی به ثانیه (پیش‌فرض: 5)'
    )
    
    args = parser.parse_args()
    
    # Create and start watcher
    watcher = WatchFolder(
        watch_dir=args.watch,
        output_dir=args.output,
        check_interval=args.interval
    )
    
    watcher.watch()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nبرنامه توسط کاربر متوقف شد")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"خطای غیرمنتظره: {str(e)}")
        sys.exit(1)
