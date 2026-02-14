import scraper

df = scraper.scrape_crypto()
print(df.head())
print("rows:", len(df))

assert len(df) >= 5, "Too few rows - maybe the page structure changed"

required = {"Date","Name","Price","Change_24h","Change_7d","MarketCap","Volume_24h"}
missing = required - set(df.columns)
assert required.issubset(df.columns), "Missing columns: " + str(missing)

print("OK: scraper")
