# -*- coding: utf-8 -*-
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

import scraper
import data_manager
import visualizer
# θα χρησιμοποιήσουμε helpers από το visualizer για numeric μετατροπές
from visualizer import _money_to_float, _percent_to_float

def open_chatbot_window(root):
    win = tk.Toplevel(root)
    win.title("Crypto Chatbot")
    win.geometry("520x420")
    frame = ttk.Frame(win, padding=10); frame.pack(fill="both", expand=True)
    transcript = tk.Text(frame, height=16, state="disabled", wrap="word")
    transcript.pack(fill="both", expand=True)
    entry = ttk.Entry(frame); entry.pack(fill="x", pady=8)

    def append(msg, who="bot"):
        transcript.configure(state="normal")
        transcript.insert("end", f"{'Εσύ' if who=='user' else 'Bot'}: {msg}\n")
        transcript.configure(state="disabled"); transcript.see("end")

    def on_ask(event=None):
        from chatbot import chatbot_response
        q = entry.get().strip()
        if not q: return
        append(q, who="user"); entry.delete(0, "end")
        a = chatbot_response(q); append(a, who="bot")

    ttk.Button(frame, text="Ρώτα", command=on_ask).pack()
    entry.bind("<Return>", on_ask)
    append("Γεια! Ρώτησέ με κάτι για κρυπτονομίσματα 😊")

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crypto Tracker (Scrape • CSV • Charts • Chatbot)")
        self.geometry("980x640")
        self.df = data_manager.load_data()

        # Toolbar
        bar = ttk.Frame(self, padding=8); bar.pack(side="top", fill="x")
        ttk.Button(bar, text="Scrape τώρα", command=self.on_scrape).pack(side="left", padx=4)
        ttk.Button(bar, text="Ανανέωση Πίνακα", command=self.refresh_table).pack(side="left", padx=4)
        ttk.Button(bar, text="Export σε νέο CSV", command=self.export_csv).pack(side="left", padx=4)
        ttk.Button(bar, text="Στατιστικά", command=self.show_stats).pack(side="left", padx=4)
        ttk.Button(bar, text="Chatbot", command=lambda: open_chatbot_window(self)).pack(side="left", padx=4)

        # Charts
        charts = ttk.Frame(self, padding=8); charts.pack(side="top", fill="x")
        ttk.Button(charts, text="Bar: Τιμές Top 5", command=self.plot_bar).pack(side="left", padx=4)
        ttk.Button(charts, text="Pie: Κεφαλαιοποίηση Top 5", command=self.plot_pie).pack(side="left", padx=4)
        ttk.Button(charts, text="Line: Μεταβολές 24h/7d", command=self.plot_line).pack(side="left", padx=4)

        # Filter
        filt = ttk.Frame(self, padding=8); filt.pack(side="top", fill="x")
        ttk.Label(filt, text="Επιλογή νομίσματος:").pack(side="left", padx=(0,6))
        self.coin_var = tk.StringVar(value="")
        self.coin_combo = ttk.Combobox(filt, textvariable=self.coin_var, state="readonly")
        self.coin_combo.pack(side="left")
        self.coin_combo.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())
        ttk.Button(filt, text="Επαναφορά", command=self.reset_filter).pack(side="left", padx=6)

        # Table
        frame = ttk.Frame(self, padding=(8,0,8,8)); frame.pack(side="top", fill="both", expand=True)
        cols = ("Date","Name","Price","Change_24h","Change_7d","MarketCap","Volume_24h")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings")
        for c, w in [("Date",140),("Name",160),("Price",110),("Change_24h",110),("Change_7d",110),("MarketCap",130),("Volume_24h",160)]:
            self.tree.heading(c, text=c); self.tree.column(c, width=w, anchor="center")
        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        self.tree.pack(side="left", fill="both", expand=True); vsb.pack(side="right", fill="y")

        self.populate_combo()
        self.refresh_table()

    # Actions
    def on_scrape(self):
        def work():
            try:
                new_df = scraper.scrape_crypto()
                data_manager.save_data(new_df)
                self.df = data_manager.load_data()
                self.after(0, lambda: (self.populate_combo(), self.refresh_table(),
                                       messagebox.showinfo("Έτοιμο", "Ολοκληρώθηκε το scraping & η αποθήκευση.")))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Σφάλμα", f"Αποτυχία scraping:\n{e}"))
        threading.Thread(target=work, daemon=True).start()

    def export_csv(self):
        if self.df.empty:
            messagebox.showwarning("Προσοχή", "Δεν υπάρχουν δεδομένα προς εξαγωγή."); return
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")])
        if not fp: return
        try:
            self.df.to_csv(fp, index=False)
            messagebox.showinfo("OK", f"Αποθηκεύτηκε: {fp}")
        except Exception as e:
            messagebox.showerror("Σφάλμα", f"Αποτυχία αποθήκευσης:\n{e}")

    def plot_bar(self):
        try:
            visualizer.bar_chart(self.df)
        except Exception as e:
            messagebox.showwarning("Προσοχή", str(e))

    def plot_pie(self):
        try:
            visualizer.pie_chart(self.df)
        except Exception as e:
            messagebox.showwarning("Προσοχή", str(e))

    def plot_line(self):
        try:
            visualizer.line_plot(self.df)
        except Exception as e:
            messagebox.showwarning("Προσοχή", str(e))

    def populate_combo(self):
        names = sorted(set(self.df["Name"].dropna().astype(str))) if not self.df.empty else []
        self.coin_combo["values"] = [""] + names

    def reset_filter(self):
        self.coin_var.set("")
        self.refresh_table()

    def refresh_table(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        df = self.df
        sel = self.coin_var.get().strip()
        if sel:
            df = df[df["Name"].str.lower() == sel.lower()]
        # Νεότερες εγγραφές πρώτα
        try:
            d2 = df.copy()
            d2["DateParsed"] = pd.to_datetime(d2["Date"])
            df = d2.sort_values("DateParsed", ascending=False).drop(columns=["DateParsed"])
        except:
            pass
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=[row.get(c,"") for c in self.tree["columns"]])

    def show_stats(self):
        if self.df.empty:
            messagebox.showwarning("Προσοχή", "Δεν υπάρχουν δεδομένα."); return
        d = self.df.copy()
        # numeric μετατροπές
        d["CapNum"] = d["MarketCap"].apply(_money_to_float)
        d["VolNum"] = d["Volume_24h"].apply(_money_to_float)
        d["Ch24"]   = d["Change_24h"].apply(_percent_to_float)
        d["Ch7"]    = d["Change_7d"].apply(_percent_to_float)
        # κράτα πιο πρόσφατη εγγραφή ανά νόμισμα
        try:
            d["DateParsed"] = pd.to_datetime(d["Date"])
            d = d.sort_values("DateParsed", ascending=False).drop_duplicates("Name")
        except:
            d = d.drop_duplicates("Name")

        lines = []
        # Top gainer/loser 24h
        if d["Ch24"].notna().any():
            try:
                lines.append("Top gainer 24h: " + d.loc[d["Ch24"].idxmax(),"Name"] + f" ({d['Ch24'].max():.2f}%)")
                lines.append("Top loser 24h : " + d.loc[d["Ch24"].idxmin(),"Name"] + f" ({d['Ch24'].min():.2f}%)")
            except: pass
        # Top gainer/loser 7d
        if d["Ch7"].notna().any():
            try:
                lines.append("Top gainer 7d : " + d.loc[d["Ch7"].idxmax(),"Name"] + f" ({d['Ch7'].max():.2f}%)")
                lines.append("Top loser 7d  : " + d.loc[d["Ch7"].idxmin(),"Name"] + f" ({d['Ch7'].min():.2f}%)")
            except: pass
        # Market cap share
        if d["CapNum"].notna().any():
            top5 = d.sort_values("CapNum", ascending=False).head(5)
            total = d["CapNum"].sum()
            share = (top5["CapNum"].sum()/total*100) if total else 0
            lines.append(f"Top-5 market cap share: {share:.1f}%")
        # Top-5 Volume (24h)
        if d["VolNum"].notna().any():
            topv = d.sort_values("VolNum", ascending=False).head(5)["Name"].tolist()
            lines.append("Top-5 by Volume (24h): " + ", ".join(topv))

        messagebox.showinfo("Στατιστικά", "\n".join(lines) if lines else "Δεν υπάρχουν επαρκή δεδομένα.")

if __name__ == "__main__":
    app = App()
    app.mainloop()

