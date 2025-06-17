# 📰 Multilingual News Aggregator

A Python project that fetches and displays cleaned news summaries from popular sources in **English and Hindi**.

Includes both:

- 🖥️ Desktop App (Tkinter GUI)
- 🌐 Web App (Streamlit)

---

## 🔧 Features

- 🧠 Language detection (English / Hindi)
- 🧹 Stopword and punctuation removal
- 📡 Fetches RSS feeds from:
  - BBC News
  - NDTV
  - Navbharat Times
- ✨ Clean, readable summaries
- 📍 Supports Unicode Hindi rendering

---

## 📦 Installation

Install required packages:

```bash
pip install -r requirements.txt

##  To run Tkinter GUI:

bash
python news_aggregator.py gui

##To run Streamlit Web App:

bash
streamlit run news_aggregator.py


