import streamlit as st
import pandas as pd
import requests
from google_play_scraper import reviews, Sort
from datetime import datetime, timedelta
import config

def get_date_window():
    today = datetime.utcnow().date()
    current_week_monday = today - timedelta(days=today.weekday())
    end_date = current_week_monday - timedelta(days=1)
    start_date = end_date - timedelta(days=6)
    return start_date, end_date

@st.cache_data(ttl=3600)
def fetch_google_play_reviews(app_id, start_date, end_date):
    try:
        gp_reviews, _ = reviews(app_id, lang="fr", country="fr", sort=Sort.NEWEST, count=2000)
    except Exception as e:
        st.error(f"Erreur Google Play: {e}")
        return pd.DataFrame()
        
    rows = []
    for r in gp_reviews:
        review_dt = r.get("at")
        if not review_dt: continue
        review_date = review_dt.date()
        if start_date <= review_date <= end_date:
            rows.append({
                "store": "Google Play Store", 
                "rating": r.get("score"), 
                "review_text": r.get("content"), 
                "review_date": review_date.strftime("%Y-%m-%d"),
                "version": r.get("reviewCreatedVersion", "N/A")
            })
        elif review_date < start_date: 
            break
    return pd.DataFrame(rows)

@st.cache_data(ttl=3600)
def fetch_app_store_reviews(app_id, start_date, end_date):
    all_reviews = []
    for page in range(1, 50):
        try:
            url = f"https://itunes.apple.com/fr/rss/customerreviews/page={page}/id={app_id}/sortby=mostrecent/json"
            resp = requests.get(url)
            if resp.status_code != 200: break
            data = resp.json()
            entries = data.get("feed", {}).get("entry", [])
            if len(entries) <= 1: break
            for entry in entries[1:]:
                dt = datetime.fromisoformat(entry["updated"]["label"].replace("Z", "+00:00"))
                review_date = dt.date()
                if start_date <= review_date <= end_date:
                    all_reviews.append({
                        "store": "Apple App Store", 
                        "rating": int(entry["im:rating"]["label"]), 
                        "review_text": entry["content"]["label"], 
                        "review_date": review_date.strftime("%Y-%m-%d"),
                        "version": entry.get("im:version", {}).get("label", "N/A")
                    })
                elif review_date < start_date: 
                    raise StopIteration
        except StopIteration:
            break
        except Exception as e:
            st.error(f"Erreur App Store: {e}")
            break
    return pd.DataFrame(all_reviews)

def load_data():
    start_date, end_date = get_date_window()
    with st.spinner(f"Récupération des avis du {start_date} au {end_date}..."):
        df_gp = fetch_google_play_reviews(config.GOOGLE_PLAY_APP_ID, start_date, end_date)
        df_ios = fetch_app_store_reviews(config.APPLE_APP_ID, start_date, end_date)
        df = pd.concat([df_gp, df_ios], ignore_index=True)
    return df, start_date, end_date
