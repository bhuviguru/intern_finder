import asyncio
import os
import json
from playwright.async_api import async_playwright
from dotenv import load_dotenv

from src.utils.logger import setup_logger
from src.storage.db import init_db, get_db, save_job, get_unnotified_jobs, mark_jobs_as_sent
from src.scrapers.internshala_scraper import InternshalaScraper
from src.scrapers.unstop_scraper import UnstopScraper
from src.scrapers.naukri_scraper import NaukriScraper
from src.matching.scorer import Scorer
from src.notifier.email_sender import EmailSender
from src.application_helper.generator import AnswerGenerator

# Load env variables
load_dotenv()

# Setup Logger
logger = setup_logger()

async def run_scrapers(keywords):
    jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True) # Set headless=False for debugging
        
        scrapers = [
            InternshalaScraper(browser),
            UnstopScraper(browser),
            NaukriScraper(browser)
        ]
        
        for scraper in scrapers:
            try:
                logger.info(f"Starting {scraper.__class__.__name__}...")
                site_jobs = await scraper.scrape(keywords)
                jobs.extend(site_jobs)
                logger.info(f"Found {len(site_jobs)} jobs from {scraper.__class__.__name__}")
            except Exception as e:
                logger.error(f"Error executing {scraper.__class__.__name__}: {e}")
        
        await browser.close()
    return jobs

def main_job():
    logger.info("Starting Daily Internship Bot Check...")
    
    # 1. Initialize DB
    init_db()
    
    # 2. Load Configs
    try:
        with open('config/keywords.json') as f:
            keyword_config = json.load(f)
            keywords = keyword_config.get('roles', ['Frontend'])
        
        with open('config/settings.json') as f:
            settings = json.load(f)
            top_n = settings.get('top_n', 5)
    except Exception as e:
        logger.error(f"Error loading configs: {e}")
        return

    # 3. Scrape Jobs
    # Since scraping is async, we run it in event loop
    try:
        raw_jobs = asyncio.run(run_scrapers(keywords))
        logger.info(f"Total raw jobs scraped: {len(raw_jobs)}")
    except Exception as e:
        logger.error(f"Scraping process failed: {e}")
        raw_jobs = []

    # 4. Score & Save (Deduplication happens in save_job)
    scorer = Scorer()
    new_jobs_count = 0
    
    # Use context manager for DB session
    db_gen = get_db()
    session = next(db_gen)
    
    for job_data in raw_jobs:
        score = scorer.score_job(job_data)
        job_data['score'] = score
        saved_job = save_job(session, job_data)
        if saved_job:
            new_jobs_count += 1
            
    logger.info(f"New unique jobs saved: {new_jobs_count}")

    # 5. Shortlist & Notify
    # We can fetch un-notified jobs from DB
    unnotified_jobs = get_unnotified_jobs(session, limit=top_n)
    
    if not unnotified_jobs:
        logger.info("No new jobs to notify.")
        session.close()
        return

    logger.info(f"Preparing notification for {len(unnotified_jobs)} jobs.")
    
    # Send Notifications
    email_sender = EmailSender()
    # telegram_sender = TelegramSender() # Disabled
    answer_gen = AnswerGenerator()
    
    notification_sent = False
    
    # Email
    if settings.get('send_email', False):
        subject = f"🔥 Top {len(unnotified_jobs)} Matches + AI Answers"
        body = email_sender.generate_daily_report_html(unnotified_jobs, answer_gen)
        if email_sender.send_email(os.getenv('SMTP_EMAIL'), subject, body):
             notification_sent = True



    # 6. Update notification status in DB
    if notification_sent:
        job_ids = [j.id for j in unnotified_jobs]
        mark_jobs_as_sent(session, job_ids)
        logger.info("Jobs marked as notified.")
    else:
        logger.warning("Notifications were not sent (maybe disabled or failed). Jobs remain un-notified.")

    session.close()
    logger.info("Daily Check Complete.")

if __name__ == "__main__":
    main_job()
