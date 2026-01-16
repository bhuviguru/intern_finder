from apscheduler.schedulers.blocking import BlockingScheduler
from src.main import main_job
from src.utils.logger import setup_logger
import json
import os
import signal
import sys

logger = setup_logger()

def load_schedule_time():
    try:
        with open('config/settings.json') as f:
            settings = json.load(f)
            return settings.get('schedule_time', "09:00")
    except Exception as e:
        logger.error(f"Error loading settings: {e}")
        return "09:00"

def job_wrapper():
    logger.info("⏰ Scheduler triggering daily job...")
    try:
        main_job()
        logger.info("✅ Daily job finished.")
    except Exception as e:
        logger.error(f"❌ Daily job failed: {e}")

def run_scheduler():
    scheduler = BlockingScheduler()
    
    time_str = load_schedule_time()
    hour, minute = map(int, time_str.split(':'))
    
    logger.info(f"⏳ Starting Scheduler. Bot will run daily at {time_str}")
    
    # Schedule the job
    scheduler.add_job(job_wrapper, 'cron', hour=hour, minute=minute)
    
    # Graceful shutdown
    def signal_handler(sig, frame):
        logger.info('Stopping scheduler...')
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    run_scheduler()
