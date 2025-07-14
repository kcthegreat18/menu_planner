from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.utils.timezone import get_current_timezone, localtime
from datetime import timedelta
from .services import MenuGeneratorService
import logging

logger = logging.getLogger(__name__)

def generate_weekly_menus():
    today = localtime().date()

    # 🔁 Start from next week's Monday
    next_monday = today + timedelta(days=(7 - today.weekday()))

    for i in range(6):  # Monday to Saturday
        day = next_monday + timedelta(days=i)
        service = MenuGeneratorService(date=day)
        menu = service.generate_menu()
        if menu:
            logger.info(f"✅ Generated menu for {day}")
        else:
            logger.info(f"⚠️ Menu already exists for {day}, skipping...")


def start_scheduler():
    scheduler = BackgroundScheduler(timezone=get_current_timezone())
    
    # ⏰ TESTING MODE: Runs at 11:00 PM today
    scheduler.add_job(
        generate_weekly_menus,
        CronTrigger(hour=23, minute=1),
        id="weekly_menu_generation"
    )

    scheduler.start()
