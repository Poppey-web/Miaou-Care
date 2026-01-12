import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="MiaouCare 🐱", 
    page_icon="🐱", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLES ---
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; background-color: #0a0a0f; color: #e8e8ed; }
.stApp { background: linear-gradient(180deg, #0a0a0f 0%, #12121a 50%, #0a0a0f 100%); background-attachment: fixed; }
#MainMenu, footer, header, [data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 1rem 1rem 6rem 1rem !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3b3b4f; border-radius: 3px; }
.hero-container { text-align: center; padding: 1.5rem 0 1rem 0; }
.hero-emoji { font-size: 3.5rem; margin-bottom: 0.5rem; filter: drop-shadow(0 0 20px rgba(167, 139, 250, 0.4)); animation: float 3s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
.hero-title { font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #a78bfa 0%, #f0abfc 50%, #fbbf24 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0; }
.hero-subtitle { color: #6b6b7b; font-size: 0.85rem; margin-top: 0.25rem; letter-spacing: 2px; text-transform: uppercase; }
.cat-profile { background: linear-gradient(145deg, rgba(167, 139, 250, 0.1) 0%, rgba(240, 171, 252, 0.05) 100%); border: 1px solid rgba(167, 139, 250, 0.2); border-radius: 24px; padding: 1.25rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; backdrop-filter: blur(10px); }
.cat-avatar { width: 70px; height: 70px; border-radius: 50%; background: linear-gradient(135deg, #a78bfa, #f0abfc); display: flex; align-items: center; justify-content: center; font-size: 2rem; box-shadow: 0 8px 32px rgba(167, 139, 250, 0.3); flex-shrink: 0; }
.cat-info h2 { margin: 0; font-size: 1.4rem; font-weight: 700; color: #fff; }
.cat-info p { margin: 0.2rem 0 0 0; color: #9b9bb0; font-size: 0.85rem; }
.cat-badges { display: flex; gap: 0.5rem; margin-top: 0.5rem; flex-wrap: wrap; }
.cat-badge { background: rgba(167, 139, 250, 0.15); color: #c4b5fd; padding: 0.25rem 0.6rem; border-radius: 20px; font-size: 0.7rem; font-weight: 600; }
.glass-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 20px; padding: 1.25rem; margin-bottom: 0.75rem; backdrop-filter: blur(10px); }
.metric-card { background: linear-gradient(145deg, rgba(30, 30, 45, 0.8) 0%, rgba(20, 20, 30, 0.9) 100%); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 1.25rem; text-align: center; position: relative; overflow: hidden; }
.metric-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, var(--accent-color, #a78bfa), transparent); }
.metric-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.metric-value { font-size: 1.8rem; font-weight: 800; color: #fff; margin: 0.25rem 0; }
.metric-label { color: #7b7b8b; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
.metric-trend { font-size: 0.75rem; margin-top: 0.5rem; padding: 0.2rem 0.5rem; border-radius: 10px; display: inline-block; }
.trend-up { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
.trend-down { background: rgba(239, 68, 68, 0.15); color: #f87171; }
.trend-stable { background: rgba(167, 139, 250, 0.15); color: #a78bfa; }
.inventory-item { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 16px; padding: 1rem 1.25rem; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 1rem; }
.inv-icon { font-size: 1.5rem; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; background: rgba(167, 139, 250, 0.1); border-radius: 12px; flex-shrink: 0; }
.inv-details { flex: 1; min-width: 0; }
.inv-name { font-weight: 600; color: #e8e8ed; font-size: 0.95rem; margin: 0; }
.inv-qty { color: #7b7b8b; font-size: 0.8rem; margin: 0.2rem 0 0 0; }
.inv-status { text-align: right; flex-shrink: 0; }
.days-left { font-size: 1.1rem; font-weight: 700; }
.days-label { font-size: 0.65rem; color: #6b6b7b; text-transform: uppercase; letter-spacing: 1px; }
.progress-container { width: 100%; height: 6px; background: rgba(255, 255, 255, 0.1); border-radius: 3px; margin-top: 0.5rem; overflow: hidden; }
.progress-bar { height: 100%; border-radius: 3px; }
.event-card { background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.06); border-radius: 16px; padding: 1rem; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 1rem; }
.event-date-box { background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%); border-radius: 12px; padding: 0.6rem 0.8rem; text-align: center; min-width: 55px; flex-shrink: 0; }
.event-day { font-size: 1.3rem; font-weight: 800; color: #fff; line-height: 1; }
.event-month { font-size: 0.65rem; color: rgba(255,255,255,0.8); text-transform: uppercase; font-weight: 600; }
.event-info { flex: 1; min-width: 0; }
.event-title { font-weight: 600; color: #e8e8ed; margin: 0; font-size: 0.9rem; }
.event-type { color: #7b7b8b; font-size: 0.75rem; margin: 0.2rem 0 0 0; }
.event-check { width: 28px; height: 28px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.event-check.done { background: linear-gradient(135deg, #22c55e, #16a34a); border-color: transparent; }
.alert-badge { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.75rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }
.alert-critical { background: rgba(239, 68, 68, 0.2); color: #f87171; }
.alert-warning { background: rgba(251, 191, 36, 0.2); color: #fbbf24; }
.alert-info { background: rgba(59, 130, 246, 0.2); color: #60a5fa; }
.alert-success { background: rgba(34, 197, 94, 0.2); color: #4ade80; }
.section-title { display: flex; align-items: center; gap: 0.6rem; margin: 1.5rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.06); }
.section-title h3 { margin: 0; font-size: 1rem; font-weight: 700; color: #e8e8ed; }
.stTabs [data-baseweb="tab-list"] { background: rgba(255, 255, 255, 0.02); border-radius: 16px; padding: 0.4rem; gap: 0.25rem; border: 1px solid rgba(255, 255, 255, 0.05); justify-content: center; }
.stTabs [data-baseweb="tab"] { background: transparent; border-radius: 12px; color: #7b7b8b; font-weight: 600; font-size: 0.75rem; padding: 0.6rem 1rem !important; border: none; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, rgba(167, 139, 250, 0.3), rgba(240, 171, 252, 0.2)) !important; color: #fff !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1rem; }
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div, .stTextArea > div > div > textarea { background: rgba(255, 255, 255, 0.03) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 12px !important; color: #e8e8ed !important; font-family: 'Outfit', sans-serif !important; }
.stButton > button { background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%) !important; color: white !important; border: none !important; border-radius: 12px !important; padding: 0.6rem 1.5rem !important; font-weight: 600 !important; font-family: 'Outfit', sans-serif !important; }
.streamlit-expanderHeader { background: rgba(255, 255, 255, 0.02) !important; border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; font-weight: 600 !important; }
.stSlider > div > div > div { background: linear-gradient(90deg, #a78bfa, #f0abfc) !important; }
.stSuccess, .stInfo, .stWarning, .stError { background: rgba(255, 255, 255, 0.02) !important; border-radius: 12px !important; border: 1px solid rgba(255, 255, 255, 0.06) !important; }
.js-plotly-plot .plotly .main-svg { background: transparent !important; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stTextArea label { color: #9b9bb0 !important; font-weight: 500 !important; font-size: 0.85rem !important; }
.bottom-spacer { height: 80px; }

/* MOBILE RESPONSIVE */
@media screen and (max-width: 768px) {
    .block-container { padding: 0.5rem 0.75rem 5rem 0.75rem !important; }
    .hero-container { padding: 1rem 0 0.75rem 0; }
    .hero-emoji { font-size: 2.5rem; }
    .hero-title { font-size: 1.5rem; }
    .hero-subtitle { font-size: 0.7rem; }
    .cat-profile { padding: 1rem; border-radius: 18px; gap: 0.75rem; }
    .cat-avatar { width: 55px; height: 55px; font-size: 1.5rem; }
    .cat-info h2 { font-size: 1.15rem; }
    .cat-info p { font-size: 0.75rem; }
    .cat-badge { padding: 0.2rem 0.5rem; font-size: 0.6rem; }
    .metric-card { padding: 0.9rem 0.6rem; border-radius: 16px; }
    .metric-icon { font-size: 1.2rem; margin-bottom: 0.3rem; }
    .metric-value { font-size: 1.3rem; }
    .metric-label { font-size: 0.6rem; }
    .metric-trend { font-size: 0.65rem; padding: 0.15rem 0.4rem; }
    .glass-card { padding: 1rem; border-radius: 16px; }
    .inventory-item { padding: 0.85rem 1rem; gap: 0.75rem; border-radius: 14px; }
    .inv-icon { width: 40px; height: 40px; font-size: 1.25rem; border-radius: 10px; }
    .inv-name { font-size: 0.85rem; }
    .inv-qty { font-size: 0.7rem; }
    .days-left { font-size: 1rem; }
    .days-label { font-size: 0.55rem; }
    .event-card { padding: 0.85rem; gap: 0.75rem; border-radius: 14px; }
    .event-date-box { padding: 0.5rem 0.6rem; border-radius: 10px; min-width: 48px; }
    .event-day { font-size: 1.1rem; }
    .event-month { font-size: 0.55rem; }
    .event-title { font-size: 0.8rem; }
    .event-type { font-size: 0.65rem; }
    .event-check { width: 24px; height: 24px; }
    .section-title { margin: 1rem 0 0.75rem 0; }
    .section-title h3 { font-size: 0.9rem; }
    .alert-badge { padding: 0.25rem 0.6rem; font-size: 0.6rem; }
    .stTabs [data-baseweb="tab-list"] { border-radius: 12px; padding: 0.3rem; overflow-x: auto; flex-wrap: nowrap; justify-content: flex-start; -webkit-overflow-scrolling: touch; scrollbar-width: none; }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none; }
    .stTabs [data-baseweb="tab"] { font-size: 0.65rem; padding: 0.5rem 0.7rem !important; border-radius: 10px; white-space: nowrap; flex-shrink: 0; }
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stTextArea > div > div > textarea { font-size: 16px !important; }
    .stSelectbox > div > div { font-size: 16px !important; }
    .stButton > button { padding: 0.55rem 1rem !important; font-size: 0.85rem !important; width: 100%; }
    [data-testid="column"] { padding: 0 0.25rem !important; }
}
@media screen and (max-width: 480px) {
    .block-container { padding: 0.4rem 0.5rem 5rem 0.5rem !important; }
    .hero-emoji { font-size: 2rem; }
    .hero-title { font-size: 1.3rem; }
    .cat-profile { padding: 0.85rem; border-radius: 14px; }
    .cat-avatar { width: 48px; height: 48px; font-size: 1.3rem; }
    .cat-info h2 { font-size: 1rem; }
    .cat-badge { padding: 0.15rem 0.4rem; font-size: 0.55rem; }
    .metric-card { padding: 0.75rem 0.5rem; border-radius: 14px; }
    .metric-value { font-size: 1.15rem; }
    .metric-label { font-size: 0.55rem; }
    .inv-icon { width: 36px; height: 36px; font-size: 1.1rem; }
    .inv-name { font-size: 0.8rem; }
    .event-date-box { min-width: 42px; padding: 0.4rem 0.5rem; }
    .event-day { font-size: 1rem; }
    .stTabs [data-baseweb="tab"] { font-size: 0.6rem; padding: 0.45rem 0.6rem !important; }
}
@media screen and (max-width: 640px) {
    [data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    [data-testid="stHorizontalBlock"] > [data-testid="column"] { width: 50% !important; flex: 0 0 50% !important; min-width: 0 !important; }
}
@supports (padding: max(0px)) {
    .block-container { padding-left: max(0.75rem, env(safe-area-inset-left)) !important; padding-right: max(0.75rem, env(safe-area-inset-right)) !important; padding-bottom: max(5rem, calc(5rem + env(safe-area-inset-bottom))) !important; }
}
@media (pointer: coarse) {
    .stButton > button, .stSelectbox > div > div, .streamlit-expanderHeader, .stTabs [data-baseweb="tab"] { min-height: 44px; }
}
</style>
""", unsafe_allow_html=True)

# --- DATABASE SETUP ---
@st.cache_resource
def init_db():
    conn = sqlite3.connect('miaoucare.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cat_profile (id INTEGER PRIMARY KEY, name TEXT, breed TEXT, birth_date TEXT, color TEXT, microchip TEXT, photo_url TEXT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inventory (id INTEGER PRIMARY KEY AUTOINCREMENT, item TEXT, category TEXT, current_qty REAL, unit TEXT, daily_usage REAL, min_threshold REAL, icon TEXT, last_updated TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS health_records (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, weight REAL, energy INTEGER, appetite INTEGER, hydration INTEGER, litter_status TEXT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, event_type TEXT, icon TEXT, completed INTEGER DEFAULT 0, notes TEXT, reminder_days INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS alerts (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, category TEXT, priority TEXT, created_at TEXT, resolved INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feeding_log (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, time TEXT, food_type TEXT, quantity REAL, unit TEXT, notes TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS vet_visits (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, reason TEXT, vet_name TEXT, diagnosis TEXT, treatment TEXT, cost REAL, next_visit TEXT, documents TEXT)''')
    conn.commit()
    return conn

conn = init_db()

# --- HELPER FUNCTIONS ---
def get_cat_profile():
    df = pd.read_sql("SELECT * FROM cat_profile LIMIT 1", conn)
    return df.iloc[0].to_dict() if not df.empty else None

def get_inventory():
    return pd.read_sql("SELECT * FROM inventory ORDER BY category, item", conn)

def get_health_records(limit=30):
    return pd.read_sql(f"SELECT * FROM health_records ORDER BY date DESC LIMIT {limit}", conn)

def get_events(upcoming_only=True):
    if upcoming_only:
        today = datetime.now().strftime('%Y-%m-%d')
        return pd.read_sql(f"SELECT * FROM events WHERE date >= '{today}' ORDER BY date ASC LIMIT 10", conn)
    return pd.read_sql("SELECT * FROM events ORDER BY date DESC", conn)

def get_alerts(unresolved_only=True):
    if unresolved_only:
        return pd.read_sql("SELECT * FROM alerts WHERE resolved = 0 ORDER BY priority DESC, created_at DESC", conn)
    return pd.read_sql("SELECT * FROM alerts ORDER BY created_at DESC", conn)

def calculate_age(birth_date):
    if not birth_date: return "?"
    birth = datetime.strptime(birth_date, '%Y-%m-%d')
    today = datetime.now()
    years = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    months = (today.month - birth.month) % 12
    return f"{years} an{'s' if years > 1 else ''}" if years > 0 else f"{months} mois"

def check_inventory_alerts():
    c = conn.cursor()
    inv = get_inventory()
    for _, row in inv.iterrows():
        if row['daily_usage'] and row['daily_usage'] > 0:
            days_left = row['current_qty'] / row['daily_usage']
            threshold = row['min_threshold'] if row['min_threshold'] else 7
            if days_left <= threshold:
                existing = pd.read_sql(f"SELECT * FROM alerts WHERE title LIKE '%{row['item']}%' AND resolved = 0", conn)
                if existing.empty:
                    priority = "CRITIQUE" if days_left <= 3 else "ATTENTION"
                    c.execute("INSERT INTO alerts (title, category, priority, created_at) VALUES (?, ?, ?, ?)",
                        (f"Stock bas: {row['item']} ({int(days_left)}j)", "STOCK", priority, datetime.now().strftime('%Y-%m-%d %H:%M')))
    conn.commit()

if 'alerts_checked' not in st.session_state:
    check_inventory_alerts()
    st.session_state['alerts_checked'] = True

# --- HEADER ---
st.markdown("""
<div class="hero-container">
    <div class="hero-emoji">🐱</div>
    <h1 class="hero-title">MiaouCare</h1>
    <p class="hero-subtitle">Compagnon félin intelligent</p>
</div>
""", unsafe_allow_html=True)

# --- CAT PROFILE ---
cat = get_cat_profile()
if cat:
    age = calculate_age(cat.get('birth_date'))
    st.markdown(f"""
    <div class="cat-profile">
        <div class="cat-avatar">😺</div>
        <div class="cat-info">
            <h2>{cat.get('name', 'Mon Chat')}</h2>
            <p>{cat.get('breed', 'Race inconnue')} • {age}</p>
            <div class="cat-badges">
                <span class="cat-badge">🎨 {cat.get('color', '?')}</span>
                <span class="cat-badge">💉 Vacciné</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["🏠 Accueil", "📦 Stock", "❤️ Santé", "📅 Agenda", "⚙️ Config"])

# === TAB 1: DASHBOARD ===
with tabs[0]:
    health = get_health_records(1)
    alerts_df = get_alerts()
    events_df = get_events()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        weight = health.iloc[0]['weight'] if not health.empty else "?"
        st.markdown(f'<div class="metric-card" style="--accent-color: #a78bfa;"><div class="metric-icon">⚖️</div><div class="metric-value">{weight} kg</div><div class="metric-label">Poids</div></div>', unsafe_allow_html=True)
    with col2:
        energy = health.iloc[0]['energy'] if not health.empty and health.iloc[0]['energy'] else "?"
        st.markdown(f'<div class="metric-card" style="--accent-color: #4ade80;"><div class="metric-icon">⚡</div><div class="metric-value">{energy}/10</div><div class="metric-label">Énergie</div></div>', unsafe_allow_html=True)
    with col3:
        alert_count = len(alerts_df)
        st.markdown(f'<div class="metric-card" style="--accent-color: #f87171;"><div class="metric-icon">🔔</div><div class="metric-value">{alert_count}</div><div class="metric-label">Alertes</div></div>', unsafe_allow_html=True)
    with col4:
        next_event = events_df.iloc[0] if not events_df.empty else None
        event_text = "—"
        if next_event is not None:
            event_date = datetime.strptime(next_event['date'], '%Y-%m-%d')
            days_until = (event_date.date() - datetime.now().date()).days
            event_text = f"{days_until}j" if days_until > 0 else "Aujourd'hui"
        st.markdown(f'<div class="metric-card" style="--accent-color: #60a5fa;"><div class="metric-icon">📅</div><div class="metric-value">{event_text}</div><div class="metric-label">Prochain RDV</div></div>', unsafe_allow_html=True)
    
    if not alerts_df.empty:
        st.markdown('<div class="section-title"><span>⚠️</span><h3>Alertes</h3></div>', unsafe_allow_html=True)
        for _, alert in alerts_df.head(3).iterrows():
            st.markdown(f'<div class="glass-card" style="border-left: 3px solid #f87171;"><span class="alert-badge alert-critical">{alert["priority"]}</span><p style="margin: 0.5rem 0 0 0;">{alert["title"]}</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="section-title"><span>📊</span><h3>Évolution du poids</h3></div>', unsafe_allow_html=True)
    health_history = get_health_records(30)
    if not health_history.empty and health_history['weight'].notna().any():
        health_history = health_history.sort_values('date')
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=health_history['date'], y=health_history['weight'], mode='lines+markers', line=dict(color='#a78bfa', width=3), marker=dict(size=8), fill='tozeroy', fillcolor='rgba(167, 139, 250, 0.1)'))
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#7b7b8b'), xaxis=dict(showgrid=False, tickformat='%d/%m'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', ticksuffix=' kg'))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.info("📊 Ajoutez des données de poids")

# === TAB 2: STOCK ===
with tabs[1]:
    st.markdown('<div class="section-title"><span>📦</span><h3>Gestion des stocks</h3></div>', unsafe_allow_html=True)
    inv = get_inventory()
    if inv.empty:
        st.info("📦 Aucun article. Ajoutez-en ci-dessous!")
    else:
        for _, row in inv.iterrows():
            days_left = int(row['current_qty'] / row['daily_usage']) if row['daily_usage'] and row['daily_usage'] > 0 else 999
            status_color = "#f87171" if days_left <= 3 else "#fbbf24" if days_left <= 7 else "#4ade80"
            icon = row['icon'] if row['icon'] else "📦"
            st.markdown(f'<div class="inventory-item"><div class="inv-icon">{icon}</div><div class="inv-details"><p class="inv-name">{row["item"]}</p><p class="inv-qty">{row["current_qty"]} {row["unit"]}</p></div><div class="inv-status"><div class="days-left" style="color: {status_color};">{days_left if days_left < 999 else "∞"}</div><div class="days-label">jours</div></div></div>', unsafe_allow_html=True)
    
    with st.expander("➕ Ajouter un article"):
        with st.form("inventory_form", clear_on_submit=True):
            item_name = st.text_input("Nom *")
            col1, col2 = st.columns(2)
            with col1:
                item_qty = st.number_input("Quantité", min_value=0.0, step=0.1)
                item_category = st.selectbox("Catégorie", [("food", "🍽️ Alimentation"), ("hygiene", "🧹 Hygiène"), ("medication", "💊 Médicaments"), ("other", "📦 Autre")], format_func=lambda x: x[1])
            with col2:
                item_usage = st.number_input("Conso/jour", min_value=0.0, step=0.01)
                item_unit = st.selectbox("Unité", ["kg", "g", "L", "sachets", "unités"])
            if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                if item_name:
                    c = conn.cursor()
                    c.execute("INSERT OR REPLACE INTO inventory (item, category, current_qty, unit, daily_usage, last_updated) VALUES (?, ?, ?, ?, ?, ?)", (item_name, item_category[0], item_qty, item_unit, item_usage, datetime.now().strftime('%Y-%m-%d %H:%M')))
                    conn.commit()
                    st.success(f"✅ {item_name} sauvegardé!")
                    st.rerun()

# === TAB 3: SANTÉ ===
with tabs[2]:
    st.markdown('<div class="section-title"><span>📝</span><h3>Suivi quotidien</h3></div>', unsafe_allow_html=True)
    with st.form("health_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            h_weight = st.number_input("⚖️ Poids (kg)", min_value=0.0, max_value=30.0, step=0.01)
            h_energy = st.slider("⚡ Énergie", 1, 10, 5)
        with col2:
            h_appetite = st.slider("🍽️ Appétit", 1, 10, 5)
            h_hydration = st.slider("💧 Hydratation", 1, 10, 5)
        h_notes = st.text_area("📝 Notes", height=80)
        if st.form_submit_button("✅ Enregistrer", use_container_width=True):
            c = conn.cursor()
            c.execute("INSERT INTO health_records (date, weight, energy, appetite, hydration, notes) VALUES (?, ?, ?, ?, ?, ?)", (datetime.now().strftime('%Y-%m-%d'), h_weight if h_weight > 0 else None, h_energy, h_appetite, h_hydration, h_notes))
            conn.commit()
            st.success("✅ Données enregistrées!")
            st.rerun()
    
    recent = get_health_records(5)
    if not recent.empty:
        st.markdown("**📋 Derniers enregistrements**")
        for _, rec in recent.iterrows():
            date_str = datetime.strptime(rec['date'], '%Y-%m-%d').strftime('%d/%m')
            st.markdown(f'<div class="glass-card" style="padding: 0.8rem;"><span style="color: #a78bfa; font-weight: 600;">{date_str}</span> — ⚖️ {rec["weight"] if rec["weight"] else "—"} kg — ⚡ {rec["energy"]}/10 — 🍽️ {rec["appetite"]}/10</div>', unsafe_allow_html=True)

# === TAB 4: AGENDA ===
with tabs[3]:
    st.markdown('<div class="section-title"><span>📅</span><h3>Événements</h3></div>', unsafe_allow_html=True)
    events_all = pd.read_sql("SELECT * FROM events ORDER BY date ASC", conn)
    if not events_all.empty:
        today = datetime.now().date()
        for _, event in events_all.iterrows():
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            days_until = (event_date.date() - today).days
            if days_until >= 0:
                icon = event['icon'] if event['icon'] else "📌"
                urgency_color = "#f87171" if days_until <= 1 else "#fbbf24" if days_until <= 7 else "#4ade80"
                st.markdown(f'<div class="event-card" style="border-left: 3px solid {urgency_color};"><div class="event-date-box"><div class="event-day">{event_date.strftime("%d")}</div><div class="event-month">{event_date.strftime("%b").upper()}</div></div><div class="event-info"><p class="event-title">{icon} {event["title"]}</p><p class="event-type">{"Aujourd hui!" if days_until == 0 else f"Dans {days_until}j"}</p></div></div>', unsafe_allow_html=True)
    else:
        st.info("📅 Aucun événement")
    
    with st.expander("➕ Nouvel événement"):
        with st.form("event_form", clear_on_submit=True):
            e_title = st.text_input("Titre *")
            e_date = st.date_input("Date")
            e_type = st.selectbox("Type", [("vet", "🏥 Véto"), ("medication", "💊 Médic"), ("grooming", "✂️ Toilettage"), ("other", "📌 Autre")], format_func=lambda x: x[1])
            if st.form_submit_button("📅 Ajouter", use_container_width=True):
                if e_title:
                    icons = {"vet": "🏥", "medication": "💊", "grooming": "✂️", "other": "📌"}
                    c = conn.cursor()
                    c.execute("INSERT INTO events (title, date, event_type, icon, reminder_days) VALUES (?, ?, ?, ?, ?)", (e_title, e_date.strftime('%Y-%m-%d'), e_type[0], icons.get(e_type[0], "📌"), 3))
                    conn.commit()
                    st.success("✅ Événement ajouté!")
                    st.rerun()

# === TAB 5: RÉGLAGES ===
with tabs[4]:
    st.markdown('<div class="section-title"><span>😺</span><h3>Profil du chat</h3></div>', unsafe_allow_html=True)
    cat = get_cat_profile()
    with st.form("cat_profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            p_name = st.text_input("Nom *", value=cat['name'] if cat else "")
            p_breed = st.text_input("Race", value=cat['breed'] if cat else "")
            p_birth = st.date_input("Naissance", value=datetime.strptime(cat['birth_date'], '%Y-%m-%d') if cat and cat['birth_date'] else None)
        with col2:
            p_color = st.text_input("Couleur", value=cat['color'] if cat else "")
            p_chip = st.text_input("N° Puce", value=cat['microchip'] if cat else "")
            p_notes = st.text_area("Notes", value=cat['notes'] if cat else "", height=68)
        if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
            if p_name:
                c = conn.cursor()
                c.execute("DELETE FROM cat_profile")
                c.execute("INSERT INTO cat_profile (id, name, breed, birth_date, color, microchip, notes) VALUES (1, ?, ?, ?, ?, ?, ?)", (p_name, p_breed, p_birth.strftime('%Y-%m-%d') if p_birth else None, p_color, p_chip, p_notes))
                conn.commit()
                st.success("✅ Profil sauvegardé!")
                st.rerun()
    
    st.markdown('<div class="section-title"><span>🔔</span><h3>Alertes</h3></div>', unsafe_allow_html=True)
    alerts = get_alerts(unresolved_only=False)
    active_alerts = alerts[alerts['resolved'] == 0]
    if not active_alerts.empty:
        for _, alert in active_alerts.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{'🔴' if alert['priority'] == 'CRITIQUE' else '🟡'} {alert['title']}")
            with col2:
                if st.button("✓", key=f"resolve_{alert['id']}"):
                    c = conn.cursor()
                    c.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", (alert['id'],))
                    conn.commit()
                    st.rerun()
    else:
        st.success("✅ Aucune alerte active")

st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)
