# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

def _money_to_float(s):
    if not isinstance(s, str) or not s.strip():
        return None
    x = s.replace("$","").replace(",","").strip()
    mult = 1.0
    if x[-1:] in {"K","M","B","T"}:
        suf = x[-1]
        x = x[:-1]
        mult = {"K":1e3,"M":1e6,"B":1e9,"T":1e12}[suf]
    try:
        return float(x)*mult
    except:
        return None

def _percent_to_float(s):
    if not isinstance(s, str) or not s.strip():
        return None
    x = s.replace("%","").strip()
    try:
        return float(x)
    except:
        return None

def _prep(df: pd.DataFrame) -> pd.DataFrame:
    d = df.copy()
    d["PriceNum"] = d["Price"].apply(_money_to_float)
    d["CapNum"] = d["MarketCap"].apply(_money_to_float)
    d["VolNum"] = d["Volume_24h"].apply(_money_to_float)
    d["Ch24"] = d["Change_24h"].apply(_percent_to_float)
    d["Ch7"]  = d["Change_7d"].apply(_percent_to_float)
    # Κράτα την πιο πρόσφατη εγγραφή ανά νόμισμα
    try:
        d["DateParsed"] = pd.to_datetime(d["Date"])
        d = d.sort_values("DateParsed", ascending=False).drop_duplicates("Name")
    except:
        d = d.drop_duplicates("Name")
    return d

def bar_chart(df: pd.DataFrame):
    d = _prep(df).dropna(subset=["CapNum","PriceNum"]).sort_values("CapNum", ascending=False).head(5)
    if d.empty:
        raise RuntimeError("Δεν υπάρχουν επαρκή δεδομένα για bar chart.")
    plt.figure()
    plt.bar(d["Name"], d["PriceNum"])
    plt.title("Τιμές κορυφαίων 5 (USD)")
    plt.ylabel("USD")
    plt.xlabel("Νόμισμα")
    plt.tight_layout()
    plt.show()

def pie_chart(df: pd.DataFrame):
    d = _prep(df).dropna(subset=["CapNum"]).sort_values("CapNum", ascending=False).head(5)
    if d.empty:
        raise RuntimeError("Δεν υπάρχουν επαρκή δεδομένα για pie chart.")
    plt.figure()
    plt.pie(d["CapNum"], labels=d["Name"], autopct="%1.1f%%")
    plt.title("Κατανομή Κεφαλαιοποίησης (Top 5)")
    plt.tight_layout()
    plt.show()

def line_plot(df: pd.DataFrame):
    d = _prep(df).dropna(subset=["Ch24","Ch7"]).sort_values("CapNum", ascending=False).head(5)
    if d.empty:
        raise RuntimeError("Δεν υπάρχουν επαρκή δεδομένα για line plot.")
    plt.figure()
    for _, row in d.iterrows():
        plt.plot(["24h","7d"], [row["Ch24"], row["Ch7"]], marker="o", label=row["Name"])
    plt.title("Μεταβολή τιμών (24h vs 7d) - Top 5")
    plt.ylabel("%")
    plt.legend()
    plt.tight_layout()
    plt.show()
