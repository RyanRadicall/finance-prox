import streamlit as st
import plotly.graph_objects as go
from datetime import date
from supabase import create_client, Client

# ══════════════════════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Finance PRO X",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

@st.cache_resource
def get_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_ANON_KEY"])

supabase = get_supabase()

# ══════════════════════════════════════════════════════════════════════════════
#  CSS + ANIMAÇÕES SURREAIS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 1.5rem !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ── BACKGROUND SURREAL ── */
.stApp {
    background: #030508;
    position: relative;
    overflow-x: hidden;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(124,58,237,0.35) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(6,182,212,0.2) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 50% 50%, rgba(16,6,35,0.9) 0%, transparent 100%);
    pointer-events: none;
    z-index: 0;
}

/* ── GRID LINES HOLOGRÁFICAS ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

.block-container { position: relative; z-index: 1; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 16px !important; padding: 4px !important;
    gap: 4px !important; border-bottom: none !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    backdrop-filter: blur(20px) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 12px !important;
    color: rgba(255,255,255,0.35) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 8px 22px !important;
    border: none !important; transition: all .25s !important;
    letter-spacing: .3px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(6,182,212,0.15)) !important;
    color: #fff !important;
    border: 1px solid rgba(124,58,237,0.5) !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.2), inset 0 1px 0 rgba(255,255,255,0.1) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── INPUTS ── */
.stTextInput input, .stNumberInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important; color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    backdrop-filter: blur(10px) !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(124,58,237,0.7) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15), 0 0 20px rgba(124,58,237,0.1) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label {
    color: rgba(255,255,255,0.45) !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(6,182,212,0.1)) !important;
    border: 1px solid rgba(124,58,237,0.4) !important;
    border-radius: 12px !important; color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 9px 22px !important;
    transition: all .25s !important;
    backdrop-filter: blur(10px) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '' !important;
    position: absolute !important;
    inset: 0 !important;
    background: linear-gradient(135deg, rgba(124,58,237,0.4), rgba(6,182,212,0.2)) !important;
    opacity: 0 !important;
    transition: opacity .25s !important;
}
.stButton > button:hover::before { opacity: 1 !important; }
.stButton > button:hover {
    border-color: rgba(124,58,237,0.8) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(124,58,237,0.3), 0 0 0 1px rgba(124,58,237,0.2) !important;
}

/* ══════════════════════════════════════════════
   COMPONENTES CUSTOMIZADOS
══════════════════════════════════════════════ */

/* ── HEADER ── */
.hdr-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding: 16px 24px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    backdrop-filter: blur(20px);
}
.logo {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #fff 0%, #a78bfa 50%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.user-info {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: rgba(255,255,255,0.6);
}
.user-avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 700; color: #fff;
    border: 2px solid rgba(124,58,237,0.5);
}
.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: #4ade80;
    box-shadow: 0 0 8px #4ade80, 0 0 16px rgba(74,222,128,0.4);
    animation: blink 1.5s ease infinite;
    display: inline-block; margin-right: 6px;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(.8)} }

/* ── TICKER ── */
.ticker-outer {
    overflow: hidden;
    margin-bottom: 20px;
    position: relative;
}
.ticker-outer::before, .ticker-outer::after {
    content: '';
    position: absolute;
    top: 0; bottom: 0;
    width: 60px;
    z-index: 2;
}
.ticker-outer::before { left: 0; background: linear-gradient(90deg, #030508, transparent); }
.ticker-outer::after  { right: 0; background: linear-gradient(-90deg, #030508, transparent); }
.ticker-track {
    display: flex; gap: 10px;
    animation: ticker 22s linear infinite;
    width: max-content;
}
.ticker-track:hover { animation-play-state: paused; }
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }
.tick-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 10px 20px;
    flex-shrink: 0;
    cursor: default;
    transition: border-color .2s, transform .2s;
    backdrop-filter: blur(10px);
}
.tick-card:hover { border-color: rgba(124,58,237,0.4); transform: translateY(-2px); }
.tick-sym   { font-size: 12px; font-weight: 700; color: rgba(255,255,255,0.9); }
.tick-price { font-size: 14px; font-weight: 600; color: #fff; margin-top: 2px; }
.tick-up    { font-size: 11px; color: #4ade80; margin-top: 2px; }
.tick-dn    { font-size: 11px; color: #f87171; margin-top: 2px; }

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 20px; }
.kpi-card {
    border-radius: 20px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    cursor: default;
    transition: transform .25s, box-shadow .25s;
    backdrop-filter: blur(20px);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0%, rgba(255,255,255,0.03) 20%, transparent 40%);
    animation: rotate 8s linear infinite;
    opacity: 0;
    transition: opacity .4s;
}
.kpi-card:hover::before { opacity: 1; }
.kpi-card:hover {
    transform: translateY(-5px) scale(1.01);
    box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px var(--glow);
}
@keyframes rotate { 0%{transform:rotate(0deg)} 100%{transform:rotate(360deg)} }

.kpi-card.purple { background: linear-gradient(135deg, rgba(109,40,217,0.2), rgba(76,29,149,0.15)); border: 1px solid rgba(167,139,250,0.25); --glow: rgba(124,58,237,0.2); }
.kpi-card.blue   { background: linear-gradient(135deg, rgba(29,78,216,0.2), rgba(30,58,138,0.15)); border: 1px solid rgba(96,165,250,0.25); --glow: rgba(37,99,235,0.2); }
.kpi-card.cyan   { background: linear-gradient(135deg, rgba(8,145,178,0.2), rgba(14,116,144,0.15)); border: 1px solid rgba(34,211,238,0.25); --glow: rgba(6,182,212,0.2); }
.kpi-card.amber  { background: linear-gradient(135deg, rgba(180,83,9,0.2), rgba(146,64,14,0.15)); border: 1px solid rgba(251,191,36,0.25); --glow: rgba(245,158,11,0.2); }
.kpi-card.rose   { background: linear-gradient(135deg, rgba(190,18,60,0.2), rgba(136,19,55,0.15)); border: 1px solid rgba(251,113,133,0.25); --glow: rgba(244,63,94,0.2); }

.kpi-icon { font-size: 22px; margin-bottom: 12px; filter: drop-shadow(0 0 8px currentColor); }
.kpi-label { font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; color: rgba(255,255,255,0.4); margin-bottom: 6px; }
.kpi-value { font-size: 22px; font-weight: 800; color: #fff; line-height: 1; letter-spacing: -0.5px; }
.kpi-delta { font-size: 11px; margin-top: 10px; display: flex; align-items: center; gap: 4px; }
.up { color: #4ade80; }
.dn { color: #f87171; }

/* ── PANELS ── */
.panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 22px;
    transition: border-color .3s, box-shadow .3s;
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.4), rgba(6,182,212,0.3), transparent);
    opacity: 0;
    transition: opacity .4s;
}
.panel:hover::before { opacity: 1; }
.panel:hover {
    border-color: rgba(124,58,237,0.2);
    box-shadow: 0 0 40px rgba(124,58,237,0.06);
}
.panel-title {
    font-size: 10px;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    margin-bottom: 18px;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-title::before {
    content: '';
    width: 3px; height: 14px;
    border-radius: 2px;
    background: linear-gradient(180deg, #7c3aed, #06b6d4);
    flex-shrink: 0;
}

/* ── TRANSACTION ROWS ── */
.tx-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    margin-bottom: 8px;
    transition: all .2s;
    cursor: default;
}
.tx-row:hover {
    background: rgba(124,58,237,0.08);
    border-color: rgba(124,58,237,0.2);
    transform: translateX(3px);
}
.tx-icon {
    width: 38px; height: 38px;
    border-radius: 12px;
    background: rgba(255,255,255,0.05);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.tx-pos { color: #4ade80; font-weight: 700; font-size: 13px; margin-left: auto; flex-shrink: 0; }
.tx-neg { color: #f87171; font-weight: 700; font-size: 13px; margin-left: auto; flex-shrink: 0; }

/* ── GOAL BARS ── */
.goal-wrap { margin-bottom: 16px; }
.goal-hdr { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px; }
.goal-name { color: rgba(255,255,255,0.8); font-weight: 500; }
.goal-pct { font-weight: 700; }
.goal-track {
    height: 6px;
    background: rgba(255,255,255,0.07);
    border-radius: 6px;
    overflow: hidden;
    position: relative;
}
.goal-fill {
    height: 100%;
    border-radius: 6px;
    position: relative;
    transition: width 1s ease;
}
.goal-fill::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 20px; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4));
    animation: shimmer 2s ease infinite;
}
@keyframes shimmer { 0%,100%{opacity:0} 50%{opacity:1} }
.goal-vals { display: flex; justify-content: space-between; font-size: 10px; color: rgba(255,255,255,0.3); margin-top: 5px; }

/* ── FORM BOX ── */
.form-box {
    background: rgba(124,58,237,0.06);
    border: 1px solid rgba(124,58,237,0.18);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}
.form-box::after {
    content: '';
    position: absolute;
    top: -1px; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,58,237,0.6), transparent);
}
.form-title { font-size: 13px; font-weight: 700; color: #a78bfa; margin-bottom: 16px; letter-spacing: .3px; }

/* ── AI BOX ── */
.ai-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(6,182,212,0.05));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 16px;
    padding: 16px 18px;
    margin-top: 16px;
    position: relative;
    overflow: hidden;
}
.ai-box::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at top left, rgba(124,58,237,0.1), transparent 60%);
    pointer-events: none;
}
.ai-label {
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(167,139,250,0.7);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.ai-label::before {
    content: '';
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #a78bfa;
    box-shadow: 0 0 8px #a78bfa;
    animation: blink 2s ease infinite;
}
.ai-text { font-size: 13px; line-height: 1.75; color: rgba(255,255,255,0.85); }

/* ── DIVIDER ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    margin: 14px 0;
}

/* ── LOGIN ── */
.login-outer {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}
.login-card {
    width: 100%;
    max-width: 420px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 28px;
    padding: 42px 40px;
    backdrop-filter: blur(40px);
    position: relative;
    overflow: hidden;
}
.login-card::before {
    content: '';
    position: absolute;
    top: -80px; left: -80px;
    width: 250px; height: 250px;
    background: radial-gradient(circle, rgba(124,58,237,0.15), transparent 70%);
    pointer-events: none;
}
.login-card::after {
    content: '';
    position: absolute;
    bottom: -80px; right: -80px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(6,182,212,0.1), transparent 70%);
    pointer-events: none;
}
.login-logo {
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #fff, #a78bfa 50%, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.login-sub {
    text-align: center;
    font-size: 13px;
    color: rgba(255,255,255,0.35);
    margin-bottom: 32px;
    letter-spacing: .3px;
}

/* ── STAT BADGE ── */
.stat-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin-right: 8px;
}

/* ── ALERTS ── */
.stAlert { border-radius: 14px !important; backdrop-filter: blur(10px) !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  CONSTANTES
# ══════════════════════════════════════════════════════════════════════════════
ICONES    = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯"]
CATS      = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]
CORES     = ["#7c3aed","#2563eb","#06b6d4","#ca8a04","#dc2626","#16a34a","#db2777","#ea580c","#65a30d"]
CORES_MAP = dict(zip(CATS, CORES))
COR_LABEL = {
    "#7c3aed":"🟣 Roxo","#2563eb":"🔵 Azul","#06b6d4":"🩵 Ciano",
    "#ca8a04":"🟡 Âmbar","#dc2626":"🔴 Vermelho","#16a34a":"🟢 Verde",
    "#db2777":"🩷 Rosa","#ea580c":"🟠 Laranja","#65a30d":"🍏 Lima",
}
TICKER_DATA = [
    {"sym":"PETR4", "price":"R$ 38,42",   "chg":"+2.14%","up":True},
    {"sym":"ITUB4", "price":"R$ 27,80",   "chg":"+0.83%","up":True},
    {"sym":"BTC",   "price":"R$ 312.450", "chg":"-1.20%","up":False},
    {"sym":"VALE3", "price":"R$ 62,10",   "chg":"-0.37%","up":False},
    {"sym":"IVVB11","price":"R$ 318,90",  "chg":"+0.45%","up":True},
    {"sym":"MGLU3", "price":"R$ 9,87",    "chg":"+3.20%","up":True},
    {"sym":"ETH",   "price":"R$ 18.420",  "chg":"+1.85%","up":True},
    {"sym":"BBDC4", "price":"R$ 15,64",   "chg":"-0.57%","up":False},
]

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def plotly_cfg(h=260):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="rgba(255,255,255,0.55)", size=11),
        margin=dict(l=8, r=8, t=8, b=8),
        height=h,
    )

def uid():
    return st.session_state.get("user_id", "")

def primeiro_nome():
    email = st.session_state.get("user_email", "")
    if email:
        n = email.split("@")[0].split(".")[0].split("_")[0]
        return n.capitalize()
    return "Usuário"

# ══════════════════════════════════════════════════════════════════════════════
#  DB HELPERS
# ══════════════════════════════════════════════════════════════════════════════
def db_lancamentos():
    return supabase.table("lancamentos").select("*").eq("user_id",uid()).order("data",desc=True).execute().data or []

def db_add_lancamento(nome,cat,val,tipo,icone,dt):
    supabase.table("lancamentos").insert({"user_id":uid(),"nome":nome,"categoria":cat,"valor":val,"tipo":tipo,"icone":icone,"data":str(dt)}).execute()

def db_del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id",rid).execute()

def db_investimentos():
    return supabase.table("investimentos").select("*").eq("user_id",uid()).execute().data or []

def db_add_investimento(nome,val,chg,cor):
    supabase.table("investimentos").insert({"user_id":uid(),"nome":nome,"valor":val,"variacao":chg,"cor":cor}).execute()

def db_del_investimento(rid):
    supabase.table("investimentos").delete().eq("id",rid).execute()

def db_metas():
    return supabase.table("metas").select("*").eq("user_id",uid()).execute().data or []

def db_add_meta(nome,atual,total,cor):
    supabase.table("metas").insert({"user_id":uid(),"nome":nome,"atual":atual,"total":total,"cor":cor}).execute()

def db_update_meta(rid,atual):
    supabase.table("metas").update({"atual":atual}).eq("id",rid).execute()

def db_del_meta(rid):
    supabase.table("metas").delete().eq("id",rid).execute()

# ══════════════════════════════════════════════════════════════════════════════
#  TELA DE LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def tela_login():
    st.markdown("""
    <div class="login-outer">
        <div class="login-card">
            <div class="login-logo">Finance PRO X</div>
            <div class="login-sub">
                Inteligência financeira de nível institucional
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # container real do formulário
    form_container = st.container()

    with form_container:
        _, col, _ = st.columns([1, 1.2, 1])

        with col:
            aba = st.radio(
                "",
                ["Entrar", "Criar conta"],
                horizontal=True,
                label_visibility="collapsed",
                key="auth_aba"
            )

            email = st.text_input(
                "E-mail",
                placeholder="seu@email.com",
                key="auth_email"
            )

            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="••••••••",
                key="auth_senha"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            # LOGIN
            if aba == "Entrar":

                if st.button(
                    "🔐 Entrar na plataforma",
                    use_container_width=True,
                    key="btn_login"
                ):

                    if not email.strip() or not senha:
                        st.error("Preencha e-mail e senha.")

                    else:
                        try:
                            res = supabase.auth.sign_in_with_password({
                                "email": email.strip(),
                                "password": senha
                            })

                            st.session_state["user_id"] = res.user.id
                            st.session_state["user_email"] = res.user.email
                            st.session_state["logado"] = True

                            st.rerun()

                        except Exception as e:
                            st.error(f"Erro ao entrar: {e}")

            # SIGNUP
            else:

                if st.button(
                    "✨ Criar conta gratuita",
                    use_container_width=True,
                    key="btn_signup"
                ):

                    if not email.strip():
                        st.error("Digite um e-mail.")

                    elif len(senha) < 6:
                        st.error("Senha precisa ter pelo menos 6 caracteres.")

                    else:
                        try:
                            res = supabase.auth.sign_up({
                                "email": email.strip(),
                                "password": senha
                            })

                            st.success("Conta criada com sucesso!")

                        except Exception as e:
                            st.error(f"Erro ao criar conta: {e}")

# ── GUARD ─────────────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    tela_login()
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
#  HEADER
# ══════════════════════════════════════════════════════════════════════════════
h1, h2 = st.columns([5, 1])
with h1:
    st.markdown(f"""
    <div class="hdr-wrap">
      <div style="display:flex;align-items:center;gap:16px">
        <div class="logo">Finance PRO X</div>
        <span class="stat-badge"><span class="live-dot"></span>Ao vivo</span>
        <span class="stat-badge">🇧🇷 BRL</span>
      </div>
      <div class="user-info">
        <div class="user-avatar">{primeiro_nome()[0]}</div>
        <span>Olá, <b>{primeiro_nome()}</b></span>
      </div>
    </div>
    """, unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="btn_logout"):
        try: supabase.auth.sign_out()
        except: pass
        for k in ["logado","user_id","user_email"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── TICKER INFINITO ───────────────────────────────────────────────────────────
items = TICKER_DATA * 2  # duplica para loop contínuo
cards = "".join([
    f'<div class="tick-card"><div class="tick-sym">{a["sym"]}</div>'
    f'<div class="tick-price">{a["price"]}</div>'
    f'<div class="{"tick-up" if a["up"] else "tick-dn"}">'
    f'{"▲" if a["up"] else "▼"} {a["chg"]}</div></div>'
    for a in items
])
st.markdown(f'<div class="ticker-outer"><div class="ticker-track">{cards}</div></div>',
            unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_dash, tab_lanc, tab_invest, tab_metas = st.tabs([
    "⚡  Dashboard", "✏️  Lançamentos", "📈  Investimentos", "🎯  Metas"
])

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    txs   = db_lancamentos()
    invs  = db_investimentos()
    metas = db_metas()

    entradas   = sum(t["valor"] for t in txs if t["tipo"] == "entrada")
    saidas     = sum(t["valor"] for t in txs if t["tipo"] == "saida")
    saldo      = entradas - saidas
    invest     = sum(i["valor"] for i in invs)
    patrimonio = saldo + invest

    # ── KPI GRID ──────────────────────────────────────────────────────────────
    kpis_data = [
        ("💰", "RECEITA",        fmt(entradas),   "▲ Total recebido",   True,  "purple"),
        ("💸", "DESPESAS",       fmt(saidas),     "▼ Total gasto",      False, "blue"),
        ("⚖️", "SALDO",          fmt(saldo),      "▲ Caixa livre",      saldo>=0, "cyan"),
        ("📊", "INVESTIMENTOS",  fmt(invest),     "▲ Aplicado",         True,  "amber"),
        ("🏛️", "PATRIMÔNIO",    fmt(patrimonio), "▲ Patrimônio total", True,  "rose"),
    ]

    cols = st.columns(5)
    for col, (icon, label, value, delta, up, cls) in zip(cols, kpis_data):
        dc = "up" if up else "dn"
        col.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-icon">{icon}</div>
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {dc}">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 2: Gráfico + Transações ───────────────────────────────────────────
    col_chart, col_tx = st.columns([1.6, 1])

    cats_saida = {}
    for t in txs:
        if t["tipo"] == "saida":
            cats_saida[t["categoria"]] = cats_saida.get(t["categoria"], 0) + t["valor"]

    with col_chart:
        st.markdown('<div class="panel"><div class="panel-title">Despesas por Categoria</div>', unsafe_allow_html=True)
        if cats_saida:
            sorted_cats = sorted(cats_saida.items(), key=lambda x: -x[1])
            fig = go.Figure()
            for cat, val in sorted_cats:
                cor = CORES_MAP.get(cat, "#7c3aed")
                fig.add_trace(go.Bar(
                    x=[cat], y=[val],
                    marker=dict(
                        color=cor,
                        line=dict(width=0),
                        opacity=0.85,
                    ),
                    name=cat,
                    hovertemplate=f"<b>{cat}</b><br>{fmt(val)}<extra></extra>",
                ))
            fig.update_layout(
                **plotly_cfg(260),
                showlegend=False,
                bargap=0.35,
                xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11), tickcolor="rgba(255,255,255,0.3)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(size=10), tickcolor="rgba(255,255,255,0.3)"),
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa ainda. Adicione em Lançamentos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tx:
        st.markdown('<div class="panel"><div class="panel-title">Últimas Transações</div>', unsafe_allow_html=True)
        if txs:
            for t in txs[:7]:
                sinal = "+" if t["tipo"]=="entrada" else "-"
                cls   = "tx-pos" if t["tipo"]=="entrada" else "tx-neg"
                st.markdown(f"""
                <div class="tx-row">
                  <div class="tx-icon">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:500;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{t['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Sem transações ainda.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ROW 3: Donut + Metas/IA ───────────────────────────────────────────────
    col_donut, col_metas = st.columns(2)

    with col_donut:
        st.markdown('<div class="panel"><div class="panel-title">Distribuição de Despesas</div>', unsafe_allow_html=True)
        if cats_saida:
            fig_ring = go.Figure(go.Pie(
                labels=list(cats_saida.keys()),
                values=list(cats_saida.values()),
                hole=0.72,
                marker=dict(
                    colors=[CORES_MAP.get(c,"#7c3aed") for c in cats_saida],
                    line=dict(color="rgba(0,0,0,0.3)", width=2),
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
            ))
            fig_ring.update_layout(
                **plotly_cfg(220),
                showlegend=True,
                legend=dict(
                    font=dict(size=11, color="rgba(255,255,255,0.6)"),
                    bgcolor="rgba(0,0,0,0)",
                    orientation="v",
                ),
                annotations=[dict(
                    text=f"<b>{fmt(saidas)}</b>",
                    x=0.5, y=0.5,
                    font=dict(size=13, color="white", family="Space Grotesk"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Nenhuma despesa lançada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_metas:
        st.markdown('<div class="panel"><div class="panel-title">Metas Financeiras</div>', unsafe_allow_html=True)
        if metas:
            for m in metas[:4]:
                pct = min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
                st.markdown(f"""
                <div class="goal-wrap">
                  <div class="goal-hdr">
                    <span class="goal-name">{m['nome']}</span>
                    <span class="goal-pct" style="color:{m['cor']}">{pct}%</span>
                  </div>
                  <div class="goal-track">
                    <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{m['cor']},{m['cor']}aa)"></div>
                  </div>
                  <div class="goal-vals">
                    <span>{fmt(m['atual'])}</span>
                    <span>{fmt(m['total'])}</span>
                  </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("Nenhuma meta cadastrada.")

        # IA Insight
        if saidas > 0 and entradas > 0:
            pct_s = round(saidas/entradas*100)
            maior = max(cats_saida, key=cats_saida.get) if cats_saida else ""
            if pct_s > 80:
                emoji, msg = "⚠️", f"Despesas em {pct_s}% da receita — alto risco orçamentário!"
            elif pct_s > 60:
                emoji, msg = "📊", f"Despesas em {pct_s}% da receita. Monitorar de perto."
            else:
                emoji, msg = "✅", f"Excelente! Apenas {pct_s}% da receita em despesas."
            if maior:
                msg += f" Maior custo: <b>{maior}</b>."
            insight_html = f"{emoji} {msg}"
        else:
            insight_html = "💡 Adicione lançamentos para ativar os insights de IA."

        st.markdown(f"""
        <div class="ai-box">
          <div class="ai-label">IA Financial Insight</div>
          <div class="ai-text">{insight_html}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    col_form, col_lista = st.columns([1, 1.6])

    with col_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>', unsafe_allow_html=True)
        tipo  = st.selectbox("Tipo", ["saida","entrada"],
                    format_func=lambda x:"💸 Saída" if x=="saida" else "💰 Entrada", key="f_tipo")
        nome  = st.text_input("Descrição", placeholder="Ex: Conta de luz", key="f_nome")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="f_valor")
        cats_op = [c for c in CATS if c!="Salário"] if tipo=="saida" else ["Salário","Outros"]
        c1, c2 = st.columns(2)
        with c1: cat  = st.selectbox("Categoria", cats_op, key="f_cat")
        with c2: icon = st.selectbox("Ícone", ICONES, key="f_icon")
        data_l = st.date_input("Data", value=date.today(), key="f_data")
        if st.button("✅ Adicionar lançamento", use_container_width=True, key="btn_add_tx"):
            if nome.strip():
                db_add_lancamento(nome.strip(), cat, valor, tipo, icon, data_l)
                st.success(f"✅ '{nome}' salvo!")
                st.rerun()
            else:
                st.error("Digite uma descrição.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_lista:
        st.markdown('<div class="panel"><div class="panel-title">Todos os Lançamentos</div>', unsafe_allow_html=True)
        txs_all = db_lancamentos()
        filtro = st.selectbox("🔍 Filtrar", ["Todos","Entradas","Saídas"]+CATS, key="filtro_tx")
        if filtro=="Entradas":  txs_all=[t for t in txs_all if t["tipo"]=="entrada"]
        elif filtro=="Saídas":  txs_all=[t for t in txs_all if t["tipo"]=="saida"]
        elif filtro in CATS:    txs_all=[t for t in txs_all if t["categoria"]==filtro]
        if not txs_all:
            st.info("Nenhum lançamento encontrado.")
        for t in txs_all:
            sinal = "+" if t["tipo"]=="entrada" else "-"
            cls   = "tx-pos" if t["tipo"]=="entrada" else "tx-neg"
            ci, cd = st.columns([6,1])
            with ci:
                st.markdown(f"""
                <div class="tx-row">
                  <div class="tx-icon">{t['icone']}</div>
                  <div style="flex:1;min-width:0">
                    <div style="font-size:13px;font-weight:500;color:#fff">{t['nome']}</div>
                    <div style="font-size:10px;color:rgba(255,255,255,0.35);margin-top:2px">{t['categoria']} · {str(t['data'])[:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_tx_{t['id']}"):
                    db_del_lancamento(t["id"])
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    col_if, col_ic = st.columns([1, 1.5])

    with col_if:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>', unsafe_allow_html=True)
        inv_nome = st.text_input("Nome do ativo", placeholder="Ex: Tesouro Selic", key="inv_nome")
        inv_val  = st.number_input("Valor (R$)", min_value=0.0, step=100.0, format="%.2f", key="inv_val")
        inv_chg  = st.text_input("Variação", placeholder="Ex: +5.2%", key="inv_chg")
        inv_cor  = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c,c), key="inv_cor")
        if st.button("✅ Adicionar ativo", use_container_width=True, key="btn_add_inv"):
            if inv_nome.strip():
                db_add_investimento(inv_nome.strip(), inv_val, inv_chg or "0%", inv_cor)
                st.success(f"✅ '{inv_nome}' adicionado!")
                st.rerun()
            else:
                st.error("Digite o nome.")
        st.markdown("</div>", unsafe_allow_html=True)

        invs_list  = db_investimentos()
        total_port = sum(i["valor"] for i in invs_list)
        st.markdown('<div class="panel"><div class="panel-title">Seus Ativos</div>', unsafe_allow_html=True)
        if invs_list:
            for inv in invs_list:
                pct = round(inv["valor"]/total_port*100) if total_port>0 else 0
                chg_c = "#4ade80" if str(inv["variacao"]).startswith("+") else "#f87171"
                ci, cd = st.columns([5,1])
                with ci:
                    st.markdown(f"""
                    <div class="tx-row">
                      <div style="width:10px;height:10px;border-radius:50%;background:{inv['cor']};flex-shrink:0;box-shadow:0 0 8px {inv['cor']}"></div>
                      <div style="flex:1;margin-left:10px;min-width:0">
                        <div style="font-size:13px;font-weight:500;color:#fff">{inv['nome']}</div>
                        <div style="font-size:10px;color:rgba(255,255,255,0.35)">{pct}% do portfolio</div>
                      </div>
                      <div style="text-align:right;flex-shrink:0">
                        <div style="font-size:13px;font-weight:700;color:#fff">{fmt(inv['valor'])}</div>
                        <div style="font-size:11px;color:{chg_c}">{inv['variacao']}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                with cd:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_inv_{inv['id']}"):
                        db_del_investimento(inv["id"])
                        st.rerun()
        else:
            st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ic:
        st.markdown('<div class="panel"><div class="panel-title">Portfolio</div>', unsafe_allow_html=True)
        invs2 = db_investimentos()
        if invs2:
            total_p2 = sum(i["valor"] for i in invs2)
            fig_port = go.Figure(go.Pie(
                labels=[i["nome"] for i in invs2],
                values=[i["valor"] for i in invs2],
                hole=0.70,
                marker=dict(
                    colors=[i["cor"] for i in invs2],
                    line=dict(color="rgba(0,0,0,0.4)", width=2),
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f} (%{percent})<extra></extra>",
            ))
            fig_port.update_layout(
                **plotly_cfg(420),
                showlegend=True,
                legend=dict(font=dict(color="rgba(255,255,255,0.65)",size=12), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(
                    text=f"<b>{fmt(total_p2)}</b>",
                    x=0.38, y=0.5,
                    font=dict(size=14, color="white", family="Space Grotesk"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig_port, use_container_width=True, config={"displayModeBar":False})
        else:
            st.info("Adicione ativos para ver o gráfico.")
        st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    col_mf, col_ml = st.columns([1, 1.5])

    with col_mf:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>', unsafe_allow_html=True)
        meta_nome  = st.text_input("Nome da meta", placeholder="Ex: Fundo de emergência", key="meta_nome")
        meta_atual = st.number_input("Valor atual (R$)", min_value=0.0, step=100.0, format="%.2f", key="meta_atual")
        meta_total = st.number_input("Valor da meta (R$)", min_value=1.0, step=100.0, value=1000.0, format="%.2f", key="meta_total")
        meta_cor   = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c,c), key="meta_cor")
        if st.button("✅ Adicionar meta", use_container_width=True, key="btn_add_meta"):
            if meta_nome.strip():
                db_add_meta(meta_nome.strip(), meta_atual, meta_total, meta_cor)
                st.success(f"✅ Meta '{meta_nome}' criada!")
                st.rerun()
            else:
                st.error("Digite o nome da meta.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ml:
        st.markdown('<div class="panel"><div class="panel-title">Suas Metas</div>', unsafe_allow_html=True)
        metas_list = db_metas()
        if not metas_list:
            st.info("Nenhuma meta cadastrada ainda.")
        for m in metas_list:
            pct = min(round(m["atual"]/m["total"]*100),100) if m["total"]>0 else 0
            st.markdown(f"""
            <div class="goal-wrap" style="margin-bottom:4px">
              <div class="goal-hdr">
                <span class="goal-name" style="font-size:13px">{m['nome']}</span>
                <span class="goal-pct" style="color:{m['cor']};font-size:13px">{pct}%</span>
              </div>
              <div class="goal-track" style="height:8px">
                <div class="goal-fill" style="width:{pct}%;background:linear-gradient(90deg,{m['cor']},{m['cor']}80)"></div>
              </div>
              <div class="goal-vals">
                <span>Atual: {fmt(m['atual'])}</span>
                <span>Meta: {fmt(m['total'])}</span>
              </div>
            </div>""", unsafe_allow_html=True)
            cu, cd = st.columns([4,1])
            with cu:
                novo_a = st.number_input("",
                    value=float(m["atual"]), min_value=0.0,
                    step=100.0, format="%.2f",
                    key=f"upd_{m['id']}", label_visibility="collapsed")
                if st.button("💾 Atualizar", key=f"save_{m['id']}"):
                    db_update_meta(m["id"], novo_a)
                    st.rerun()
            with cd:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"delm_{m['id']}"):
                    db_del_meta(m["id"])
                    st.rerun()
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
