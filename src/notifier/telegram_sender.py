import requests
import os
import logging
import asyncio

class TelegramSender:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_message(self, message):
        if not self.bot_token or not self.chat_id:
            self.logger.warning("Telegram config not set. Skipping Telegram notification.")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            self.logger.info("Telegram message sent.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send Telegram message: {e}")
            return False

    def format_job_message(self, jobs):
        msg = "🔥 <b>Daily Internship Matches</b>\n\n"
        for i, job in enumerate(jobs, 1):
            msg += f"<b>{i}) {job.company}</b>\n"
            msg += f"   Role: {job.role}\n"
            msg += f"   Stipend: {job.stipend}\n"
            msg += f"   Location: {job.location}\n"
            msg += f"   <a href='{job.link}'>Apply Link</a>\n\n"
        return msg
