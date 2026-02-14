# -*- coding: utf-8 -*-
import datetime
import scraper, data_manager

def ts(msg):
    print(f"[{datetime.datetime.now().isoformat(timespec='seconds')}] {msg}")

if __name__ == "__main__":
    try:
        ts("Start cron_fetch")
        df = scraper.scrape_crypto()
        data_manager.save_data(df)
        ts(f"Saved {len(df)} rows to CSV")
        ts("Done")
    except Exception as e:
        ts(f"ERROR: {e}")
        raise


