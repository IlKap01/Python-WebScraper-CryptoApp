# -*- coding: utf-8 -*-
"""
Τρέξε αυτό το script για να γίνεται καθημερινό scraping και append στο CSV.
Προϋπόθεση: pip install schedule
"""
import time
import schedule
import scraper
import data_manager

def job():
    try:
        df = scraper.scrape_crypto()
        data_manager.save_data(df)
        print("[OK] Saved daily snapshot.")
    except Exception as e:
        print("[ERR] scraping failed:", e)

def main():
    # όρισε την ώρα που σε βολεύει (24h format του συστήματος)
    schedule.every().day.at("09:00").do(job)
    print("Scheduler started. Next run at 09:00 daily.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
