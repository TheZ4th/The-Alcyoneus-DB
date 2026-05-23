# scheduler.py - Untuk scheduling otomatis
"""
Automatic Health Check Scheduler
Integrasi dengan cron / systemd timer
"""

import schedule
import time
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scheduled_health_check():
    """Function to be called by scheduler"""
    from health_check import HealthCheckSystem
    
    logging.info("Starting scheduled health check...")
    hc = HealthCheckSystem()
    results = hc.run_health_check()
    
    # Send summary to log
    logging.info(f"Health check completed: {results['online']}/{results['total_platforms']} online ({results['uptime_percentage']}%)")
    
    if results['changed'] > 0:
        logging.warning(f"Status changed for {results['changed']} platforms")
    
    return results

def run_scheduler():
    """Run the scheduler"""
    # Schedule every 24 hours at 2 AM
    schedule.every().day.at("02:00").do(scheduled_health_check)
    
    # Also schedule every 12 hours for high-priority
    schedule.every(12).hours.do(scheduled_health_check)
    
    logging.info("Health check scheduler started")
    logging.info("Schedule: Daily at 02:00 and every 12 hours")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
