# -*- coding: utf-8 -*-
import nltk
import feedparser
import string
from langdetect import detect
from nltk.corpus import stopwords

nltk.download('popular')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

hindi_stopwords = {
    'है', 'और', 'था', 'थे', 'की', 'के', 'का', 'से', 'को', 'पर', 'यह', 'हैं', 'नहीं',
    'तो', 'भी', 'लेकिन', 'या', 'एक', 'में', 'कर', 'रहा', 'लिए', 'हो', 'रही', 'गया',
    'जैसे', 'जब', 'तक', 'जो', 'जिस', 'जिसे', 'जिसने'
}

stop_words = set(stopwords.words('english')) | hindi_stopwords

rss_urls = {
    "BBC": "http://feeds.bbci.co.uk/news/rss.xml",
    "NDTV": "https://feeds.feedburner.com/NDTV-LatestNews",
    "Navbharat Times": "https://navbharattimes.indiatimes.com/rssfeedsdefault.cms"
}

def fetch_rss_articles(url):
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:5]:
        article = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if 'published' in entry else "N/A",
            "summary": entry.summary
        }
        articles.append(article)
    return articles

def clean_text(text):
    return text

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def get_cleaned_news():
    final_news = []
    for source, url in rss_urls.items():
        articles = fetch_rss_articles(url)
        for article in articles:
            language = detect_language(article['summary'])
            cleaned = clean_text(article['summary'])
            final_news.append({
                "source": source,
                "title": article['title'],
                "language": language,
                "cleaned_summary": cleaned,
                "link": article['link']
            })
    return final_news

def run_tkinter_gui():
    import tkinter as tk
    from tkinter import ttk, scrolledtext

    root = tk.Tk()
    root.title("📰 Multilingual News Aggregator")
    root.geometry("800x600")

    def display_news():
        news = get_cleaned_news()
        output_box.delete(1.0, tk.END)
        for item in news:
            output_box.insert(tk.END, f"\n🗞️ Title: {item['title']}\n")
            output_box.insert(tk.END, f"🌐 Language: {item['language'].upper()}\n")
            output_box.insert(tk.END, f"🧹 Cleaned Summary: {item['cleaned_summary']}\n")
            output_box.insert(tk.END, f"🔗 Link: {item['link']}\n")
            output_box.insert(tk.END, f"Source: {item['source']}\n")
            output_box.insert(tk.END, "\n" + "-"*80 + "\n")

    fetch_button = ttk.Button(root, text="Fetch Latest News", command=display_news)
    fetch_button.pack(pady=10)

    output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
    output_box.pack(expand=True, fill='both', padx=10, pady=10)

    root.mainloop()

def run_streamlit_app():
    import streamlit as st

    st.set_page_config(page_title="📰 Multilingual News Aggregator", layout="wide")
    st.title("🗞️ Multilingual News Aggregator (English + Hindi)")

    if st.button("Fetch News Feeds"):
        news = get_cleaned_news()
        for item in news:
            st.subheader(item['title'])
            st.markdown(f"**Source:** {item['source']} | **Language:** `{item['language'].upper()}`")
            st.markdown(
                f"""<p style='font-family:"Noto Sans Devanagari", "Mangal", "Segoe UI", sans-serif;
                font-size:16px;'>{item['cleaned_summary']}</p>""",
                unsafe_allow_html=True
            )
            st.markdown(f"[Read full article]({item['link']})")
            st.markdown("---")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        run_tkinter_gui()
    elif len(sys.argv) > 1 and sys.argv[1] == 'web':
        run_streamlit_app()
    else:
        try:
            import streamlit as st
            run_streamlit_app()
        except:
            print("Usage: python news_aggregator.py [gui|web]")
