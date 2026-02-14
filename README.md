Crypto_app
A comprehensive Python-based ecosystem designed to scrape, analyze, and visualize cryptocurrency market data in real-time.

 Project Goal
The goal of this project is to provide an automated pipeline for monitoring cryptocurrency trends. It combines web scraping, data persistence, and a user-friendly interface to help users make sense of market fluctuations.

 Key Features
Web Scraping (scraper.py): Uses Requests and BeautifulSoup4 to extract live data from CoinMarketCap, including:

Name & Symbol

Price (USD)

24h & 7d Percentage Change

Market Cap & 24h Volume

Data Management: Automatically saves and updates data in CSV format for historical tracking.

Analytics & Visualization: Statistical analysis and trend graphs generated via Matplotlib.

User Interface: A desktop GUI built with Tkinter for easy interaction.

Smart Assistant: A rule-based Chatbot to answer data-related queries.

Automation: Task scheduling integrated through Cron (system-level) and the Python Schedule library.

Installation & Setup
Clone the repository:


git clone https://github.com/your-username/Crypto_app.git
cd Crypto_app
Install dependencies:


pip install requests beautifulsoup4 matplotlib pandas schedule
Run the application:


python main.py
📂 Project Structure
scraper.py: Handles the extraction logic from CoinMarketCap.

data/: Directory containing the generated CSV files.

gui.py: The Tkinter interface code.

analysis.py: Functions for Matplotlib visualizations.
