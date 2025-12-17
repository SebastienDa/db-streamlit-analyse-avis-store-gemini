import streamlit as st

def local_css():
    st.markdown("""
    <style>
        /* KPI CARDS */
        div[data-testid="metric-container"] {
            background-color: #262730;
            border: 1px solid #464b5f;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        
        /* THEMES */
        .theme-list { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
        .theme-block { background: #262730; border: 1px solid #464b5f; border-radius: 8px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .theme-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .theme-title { font-weight: bold; font-size: 1.1em; color: #ffffff; }
        .theme-vol { background: #464b5f; color: #e0e0e0; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; }
        .theme-sentiment { margin: 0 0 10px 0; font-size: 0.95em; line-height: 1.4; color: #cccccc; }
        .theme-verbatim { background: #363945; border-left: 3px solid #3498db; padding: 10px; font-style: italic; font-size: 0.9em; color: #e0e0e0; line-height: 1.4; }
        
        .border-pos { border-left: 4px solid #27ae60 !important; }
        .border-neg { border-left: 4px solid #c0392b !important; }
        .border-neu { border-left: 4px solid #95a5a6 !important; }

        /* RECOS */
        .reco-item { display: flex; gap: 15px; margin-bottom: 25px; background: #262730; border: 1px solid #464b5f; padding: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .reco-num { background: #3498db; color: #fff; width: 30px; height: 30px; min-width: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
        .reco-body h4 { margin: 0 0 8px 0; color: #ffffff; font-size: 1.1em; font-weight: bold; }
        .reco-body p { margin: 0 0 10px 0; font-size: 0.95em; color: #cccccc; line-height: 1.5; }
        .reco-proof { border-top: 1px solid #464b5f; padding-top: 10px; font-style: italic; color: #aaaaaa; font-size: 0.9em; display: block; }
        .reco-proof::before { content: "📝 Avis complet : "; font-weight: bold; font-style: normal; color: #ffffff; }
        
        /* TITRES */
        h3 { font-size: 1.2em; text-transform: uppercase; color: #95a5a6; margin-bottom: 15px; letter-spacing: 1px; border-bottom: 1px solid #464b5f; padding-bottom: 10px; }
        
        /* UTILS */
        .subtitle { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
        .reco-container { margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

def display_themes(themes):
    st.markdown("### 🧩 Thématiques Clés")
    html = '<div class="theme-list">'
    for theme in themes:
        border_class = f"border-{theme.get('sentiment_type', 'neu')}"
        html += f"""
<div class="theme-block {border_class}">
    <div class="theme-header">
        <span class="theme-title">{theme['title']}</span>
        <span class="theme-vol">{theme['volume']}</span>
    </div>
    <p class="theme-sentiment">{theme['sentiment']}</p>
    <div class="theme-verbatim">"{theme['verbatim']}"</div>
</div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def display_recos(recos):
    st.markdown("### 🚀 Recommandations Actionnables")
    html = '<div class="reco-container">'
    for i, reco in enumerate(recos, 1):
        html += f"""
<div class="reco-item">
    <div class="reco-num">{i}</div>
    <div class="reco-body">
        <h4>{reco['action']}</h4>
        <p>{reco['why']}</p>
        <span class="reco-proof">"{reco['proof']}"</span>
    </div>
</div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
