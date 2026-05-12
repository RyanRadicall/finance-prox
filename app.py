import streamlit as st
import plotly.graph_objects as go
from datetime import date, datetime
from supabase import create_client, Client
import os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance PRO X",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Supabase client ───────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 100% !important;
}

[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

.stApp {
    background: radial-gradient(ellipse at top left, rgba(124,58,237,0.18) 0%, transparent 50%),
                radial-gradient(ellipse at top right, rgba(37,99,235,0.12) 0%, transparent 50%),
                radial-gradient(ellipse at bottom, rgba(8,145,178,0.08) 0%, transparent 60%),
                linear-gradient(160deg, #04070F 0%, #0B1020 50%, #0F1828 100%);
}

.stButton > button {
    background: rgba(124,58,237,0.18) !important;
    border: 1px solid rgba(124,58,237,0.4) !important;
    border-radius: 12px !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ICONES = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯","🐶","💈"]
CATS = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def get_user_id():
    return st.session_state.get("user_id")

# ── AUTH CHECK ────────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    st.title("Login necessário")
    st.stop()

# ── HEADER ────────────────────────────────────────────────────────────────────
st.title("Finance PRO X 💜")

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "Dashboard",
    "Lançamentos",
    "Investimentos",
    "Metas"
])

with tab1:
    st.subheader("Dashboard")

with tab2:
    st.subheader("Lançamentos")

with tab3:
    st.subheader("Investimentos")

with tab4:
    st.subheader("Metas")
