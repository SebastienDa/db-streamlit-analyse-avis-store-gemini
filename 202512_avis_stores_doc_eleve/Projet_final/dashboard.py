import streamlit as st
import plotly.express as px
import scraper
import analysis
import ui

def main():
    st.set_page_config(page_title="Dashboard Avis Stores", page_icon="🤖", layout="wide")
    ui.local_css()
    
    st.title("🤖 Avis des stores pour Mistral AI")
    
    df, start_date, end_date = scraper.load_data()
    st.markdown(f"<div class='subtitle'>Analyse du {start_date} au {end_date}</div>", unsafe_allow_html=True)
    
    if df.empty:
        st.warning("Aucune donnée récupérée.")
        return

    # --- KPIs ---
    total = len(df)
    avg_rating = round(df['rating'].mean(), 2)
    promoters = len(df[df['rating'] >= 4])
    detractors = len(df[df['rating'] <= 3])
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Note Moyenne", f"{avg_rating}/5")
    k2.metric("Total Avis", total)
    k3.metric("Satisfaits", promoters)
    k4.metric("Détracteurs", detractors)
    
    st.markdown("---")

    # --- CHARTS ---
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Volumétrie Hebdo")
        daily_counts = df['review_date'].value_counts().sort_index().reset_index()
        daily_counts.columns = ['Date', 'Volume']
        fig_daily = px.bar(daily_counts, x='Date', y='Volume', color_discrete_sequence=['#3498db'])
        fig_daily.update_layout(xaxis_title=None, yaxis_title=None, height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_daily, width="stretch")
        
    with c2:
        st.subheader("Distribution des Notes")
        rating_counts = df['rating'].value_counts().sort_index().reset_index()
        rating_counts.columns = ['Note', 'Volume']
        fig_dist = px.bar(rating_counts, y='Note', x='Volume', orientation='h', color_discrete_sequence=['#f1c40f'])
        fig_dist.update_layout(xaxis_title=None, yaxis_title=None, height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_dist, width="stretch")

    c3, c4 = st.columns(2)
    
    with c3:
        st.subheader("Répartition OS")
        store_counts = df['store'].value_counts().reset_index()
        store_counts.columns = ['Store', 'Volume']
        fig_os = px.pie(store_counts, values='Volume', names='Store', hole=0.6, color_discrete_sequence=['#36A2EB', '#FF6384'])
        fig_os.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0), showlegend=True)
        st.plotly_chart(fig_os, width="stretch")
        
    with c4:
        st.subheader("Note Moyenne par OS")
        avg_by_store = df.groupby('store')['rating'].mean().round(2).reset_index()
        fig_avg = px.bar(avg_by_store, x='store', y='rating', color_discrete_sequence=['#2ecc71'])
        fig_avg.update_layout(xaxis_title=None, yaxis_title=None, height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig_avg, width="stretch")

    st.markdown("---")

    # --- DATA TABLE ---
    st.subheader("📋 Détail des avis")
    
    # Rename columns for display
    display_df = df[['rating', 'store', 'version', 'review_text']].copy()
    display_df.columns = ['Note', 'Environnement', 'Version', 'Commentaire']
    
    st.dataframe(
        display_df,
        column_config={
            "Note": st.column_config.NumberColumn(format="%d ★"),
            "Environnement": st.column_config.TextColumn(width="medium"),
            "Version": st.column_config.TextColumn(width="small"),
            "Commentaire": st.column_config.TextColumn(width="large"),
        },
        width="stretch",
        height=300,
        hide_index=True
    )

    st.markdown("---")

    # --- AI ANALYSIS ---
    if st.button("Lancer l'analyse IA (Gemini)", type="primary"):
        with st.spinner("Analyse en cours..."):
            kpis = {"total": total, "avg": avg_rating}
            data = analysis.generate_ai_analysis_json(df, start_date, end_date, kpis)
            
            if data:
                # 1. EDITO
                st.markdown("### 💡 Édito")
                st.info(data.get("edito", ""))
                
                # 2. THEMES
                ui.display_themes(data.get("themes", []))
                
                # 3. RECOS
                ui.display_recos(data.get("recos", []))

if __name__ == "__main__":
    main()
