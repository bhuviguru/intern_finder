# Internship Finder AI Bot

## Overview
Automated bot that scrapes internship sites (Internshala, Unstop, Naukri) daily, matches jobs based on keywords/preferences, facilitates deduplication, and sends top matches via Email/Telegram.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   playwright install
   ```
2. Configure `.env` with your credentials.
3. Update `config/keywords.json` with your preferred roles and filters.

## Recurring Mode (24/7)
To keep the bot running and checking daily at 09:00 AM (configurable in `settings.json`):
```bash
python -m src.scheduler
```

## Manual Run (Once)
Run the main bot once immediately:
```bash
python -m src.main
```
