# -*- coding: utf-8 -*-
import re
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://coinmarketcap.com/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
}

money_pat = re.compile(r"\$[\d,]+(?:\.\d+)?[KMBT]?")   # $113,050.81 | $2.25T | $556.52B
percent_pat = re.compile(r"-?\d+(?:\.\d+)?%")          # 0.04% | -1.2%

def _clean_name(cell_text: str) -> str:
    """
    Πολλά rows γυρνούν 'BitcoinBTC'. Κόβουμε το trailing σύμβολο (τελευταίο block ΚΕΦΑΛΑΙΑ).
    """
    t = cell_text.strip()
    m = re.search(r"([A-Z]{2,})$", t)
    if m:
        base = t[:m.start()].strip()
        return base or t
    return t

def scrape_crypto() -> pd.DataFrame:
    """ Top-10 cryptos από CoinMarketCap, ανθεκτικό σε μικρές αλλαγές DOM. """
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    rows = soup.select("table tbody tr")
    data = []

    for tr in rows[:10]:
        texts = tr.get_text(" ", strip=True)
        tds = tr.find_all("td")

        # Προσπάθησε να πάρεις 'name' από 2η/3η στήλη
        raw_name = ""
        if len(tds) >= 3:
            raw_name = tds[2].get_text(" ", strip=True) or tds[1].get_text(" ", strip=True)
        if not raw_name:
            raw_name = texts
        name = _clean_name(raw_name)

        dollars = money_pat.findall(texts)
        percents = percent_pat.findall(texts)

        price = dollars[0] if len(dollars) >= 1 else None
        market_cap = dollars[1] if len(dollars) >= 2 else None
        volume_24h = dollars[2] if len(dollars) >= 3 else None

        change_24h = percents[0] if len(percents) >= 1 else None
        change_7d  = percents[1] if len(percents) >= 2 else None

        data.append({
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Name": name,
            "Price": price,
            "Change_24h": change_24h,
            "Change_7d": change_7d,
            "MarketCap": market_cap,
            "Volume_24h": volume_24h,
        })

    if not data:
        raise RuntimeError("Δεν βρέθηκαν δεδομένα. Ίσως άλλαξε η σελίδα.")
    return pd.DataFrame(data)
