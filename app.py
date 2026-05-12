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

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem !important; max-width: 100% !important; }
[data-testid="stDecoration"] { display: none; }
section[data-testid="stSidebar"] { display: none; }

/* ── App background ── */
.stApp {
    background:
        radial-gradient(ellipse at top left,  rgba(124,58,237,0.18) 0%, transparent 50%),
        radial-gradient(ellipse at top right, rgba(37,99,235,0.12)  0%, transparent 50%),
        radial-gradient(ellipse at bottom,    rgba(8,145,178,0.08)  0%, transparent 60%),
        linear-gradient(160deg, #04070F 0%, #0B1020 50%, #0F1828 100%);
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 14px !important; padding: 4px !important;
    gap: 4px !important; border-bottom: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border-radius: 10px !important;
    color: rgba(255,255,255,0.45) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 8px 20px !important; border: none !important;
    transition: all .2s !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(124,58,237,0.25) !important; color: #fff !important;
    border: 1px solid rgba(124,58,237,0.45) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Inputs ── */
.stTextInput input, .stNumberInput input, .stTextInput input:focus, .stNumberInput input:focus {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 12px !important; color: #fff !important;
    transition: border-color .2s !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: rgba(124,58,237,0.6) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.12) !important;
}
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label {
    color: rgba(255,255,255,0.55) !important; font-size: 12px !important;
    letter-spacing: .5px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(124,58,237,0.18) !important;
    border: 1px solid rgba(124,58,237,0.4) !important;
    border-radius: 12px !important; color: #fff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 13px !important; padding: 8px 20px !important;
    transition: all .2s !important;
}
.stButton > button:hover {
    background: rgba(124,58,237,0.35) !important;
    border-color: rgba(124,58,237,0.7) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.25) !important;
}

/* ── Cards / panels ── */
.kpi-card { border-radius: 18px; padding: 20px 22px; transition: transform .2s; }
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label { font-size: 10px; letter-spacing: 2px; text-transform: uppercase; opacity:.55; margin-bottom:8px; }
.kpi-value { font-size: 26px; font-weight: 700; line-height: 1.15; }
.kpi-delta { font-size: 12px; margin-top: 8px; opacity:.8; }
.delta-up   { color: #4ade80; }
.delta-down { color: #f87171; }
.kpi-purple { background: linear-gradient(135deg,#160428,#2d1066); border:1px solid rgba(167,139,250,.3); }
.kpi-blue   { background: linear-gradient(135deg,#001630,#002952); border:1px solid rgba(59,130,246,.3); }
.kpi-green  { background: linear-gradient(135deg,#001f14,#003825); border:1px solid rgba(34,197,94,.3); }
.kpi-amber  { background: linear-gradient(135deg,#221200,#3d2000); border:1px solid rgba(251,191,36,.3); }
.kpi-rose   { background: linear-gradient(135deg,#1a0011,#300020); border:1px solid rgba(244,63,94,.3); }

.panel {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px; padding: 22px;
    transition: border-color .3s;
}
.panel:hover { border-color: rgba(124,58,237,0.2); }
.panel-title {
    font-size: 11px; font-weight: 600; opacity:.6;
    margin-bottom: 16px; text-transform: uppercase; letter-spacing: 1.2px;
}

/* ── Transactions ── */
.tx-row {
    display:flex; align-items:center; gap:12px;
    padding:10px 14px; background:rgba(255,255,255,0.04);
    border-radius:12px; margin-bottom:8px;
    transition: background .15s;
}
.tx-row:hover { background:rgba(255,255,255,0.07); }
.tx-pos { color:#4ade80; font-weight:600; font-size:13px; margin-left:auto; }
.tx-neg { color:#f87171; font-weight:600; font-size:13px; margin-left:auto; }

/* ── Goals ── */
.goal-track { height:6px; background:rgba(255,255,255,0.1); border-radius:6px; overflow:hidden; margin:8px 0 4px; }

/* ── Forms ── */
.form-box {
    background: linear-gradient(135deg,rgba(124,58,237,0.07),rgba(37,99,235,0.05));
    border: 1px solid rgba(124,58,237,0.22);
    border-radius: 18px; padding: 20px; margin-bottom: 16px;
}
.form-title { font-size:13px; font-weight:600; color:#a78bfa; margin-bottom:14px; }
.divider { height:1px; background:rgba(255,255,255,0.07); margin:14px 0; }

/* ── Header ── */
.logo-text { font-size:24px; font-weight:700; letter-spacing:-.8px; }
.logo-text span { color:#a78bfa; }
.live-badge {
    background:rgba(124,58,237,0.15); border:1px solid rgba(124,58,237,0.35);
    border-radius:20px; padding:5px 16px; font-size:12px; color:#a78bfa; display:inline-block;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.6} }

/* ── Ticker ── */
.ticker-wrap { display:flex; gap:10px; margin-bottom:20px; overflow-x:auto; padding-bottom:4px; }
.tick-item {
    background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09);
    border-radius:14px; padding:12px 20px; flex-shrink:0;
    transition: border-color .2s, transform .2s;
}
.tick-item:hover { border-color:rgba(124,58,237,0.4); transform:translateY(-2px); }
.tick-sym   { font-size:13px; font-weight:700; }
.tick-price { font-size:14px; font-weight:600; margin-top:3px; }
.tick-up    { font-size:11px; color:#4ade80; margin-top:2px; }
.tick-dn    { font-size:11px; color:#f87171; margin-top:2px; }

/* ── AI box ── */
.ai-box {
    background:linear-gradient(135deg,rgba(124,58,237,0.1),rgba(37,99,235,0.07));
    border:1px solid rgba(124,58,237,0.25); border-radius:16px; padding:18px; margin-top:16px;
}

/* ── Login screen ── */
.login-wrap {
    max-width: 440px; margin: 60px auto 0;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 28px; padding: 40px;
}
.login-title { font-size:28px; font-weight:700; text-align:center; margin-bottom:6px; }
.login-sub   { font-size:14px; opacity:.5; text-align:center; margin-bottom:32px; }

/* ── Alerts ── */
.stAlert { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────────────────
ICONES = ["💼","🏠","🛒","🚗","📺","💊","🎓","✈️","💡","🍕","🎮","👗","🏋️","📱","🎵","🏦","💳","🎯","🐶","💈"]
CATS   = ["Moradia","Alimentação","Transporte","Saúde","Lazer","Educação","Viagem","Salário","Outros"]
CORES  = ["#7c3aed","#2563eb","#16a34a","#ca8a04","#dc2626","#0891b2","#db2777","#ea580c","#65a30d"]
CORES_MAP = dict(zip(CATS, CORES))
COR_LABEL = {
    "#7c3aed":"🟣 Roxo","#2563eb":"🔵 Azul","#16a34a":"🟢 Verde",
    "#ca8a04":"🟡 Âmbar","#dc2626":"🔴 Vermelho","#0891b2":"🩵 Ciano",
    "#db2777":"🩷 Rosa","#ea580c":"🟠 Laranja","#65a30d":"🍏 Lima"
}
ATIVOS_TICKER = [
    {"sym":"PETR4","price":"R$ 38,42","chg":"+2.14%","up":True},
    {"sym":"ITUB4","price":"R$ 27,80","chg":"+0.83%","up":True},
    {"sym":"BTC",  "price":"R$ 312.450","chg":"-1.20%","up":False},
    {"sym":"VALE3","price":"R$ 62,10","chg":"-0.37%","up":False},
    {"sym":"IVVB11","price":"R$ 318,90","chg":"+0.45%","up":True},
]

# ── Helpers ───────────────────────────────────────────────────────────────────
def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def plotly_cfg():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="rgba(255,255,255,0.65)", size=11),
        margin=dict(l=10,r=10,t=10,b=10),
    )

# ── Supabase helpers ──────────────────────────────────────────────────────────
def get_user_id():
    user_id = st.session_state.get("user_id")
    return user_id

def db_get_lancamentos():
    uid = get_user_id()
    r = supabase.table("lancamentos").select("*").eq("user_id", uid).order("data", desc=True).execute()
    return r.data or []

def db_add_lancamento(nome, cat, val, tipo, icone, dt):

    user_id = get_user_id()

    def db_add_lancamento(nome, cat, val, tipo, icone, dt):
    user_id = get_user_id()

    if not user_id:
        st.error("Usuário não autenticado")
        return

    try:
        supabase.table("lancamentos").insert({
            "user_id": user_id,
            "nome": nome,
            "categoria": cat,
            "valor": val,
            "tipo": tipo,
            "icone": icone,
            "data": str(dt)
        }).execute()

    except Exception as e:
        st.error(f"Erro Supabase: {e}")
    except Exception as e:
        st.error(f"Erro Supabase: {e}")
        
    if not uid():
        st.error("Usuário não autenticado")
        return

    supabase.table("lancamentos").insert({
        "user_id": uid(),
        "nome": nome,
        "categoria": cat,
        "valor": val,
        "tipo": tipo,
        "icone": icone,
        "data": str(dt)
    }).execute()

def db_del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id", rid).execute()

def db_get_investimentos():
    uid = get_user_id()
    r = supabase.table("investimentos").select("*").eq("user_id", uid).execute()
    return r.data or []

def db_add_investimento(nome, val, chg, cor):
    uid = get_user_id()
    supabase.table("investimentos").insert({
        "user_id": uid, "nome": nome, "valor": val, "variacao": chg, "cor": cor
    }).execute()

def db_del_investimento(rid):
    supabase.table("investimentos").delete().eq("id", rid).execute()

def db_get_metas():
    uid = get_user_id()
    r = supabase.table("metas").select("*").eq("user_id", uid).execute()
    return r.data or []

def db_add_meta(nome, atual, total, cor):
    uid = get_user_id()
    supabase.table("metas").insert({
        "user_id": uid, "nome": nome, "atual": atual, "total": total, "cor": cor
    }).execute()

def db_update_meta(rid, atual):
    supabase.table("metas").update({"atual": atual}).eq("id", rid).execute()

def db_del_meta(rid):
    supabase.table("metas").delete().eq("id", rid).execute()

# ── Auth ──────────────────────────────────────────────────────────────────────
def login_screen():
    st.markdown("""
    <div style="text-align:center;margin-top:40px;margin-bottom:40px">
        <div style="font-size:36px;font-weight:800;letter-spacing:-1px">
            Finance <span style="color:#a78bfa">PRO X</span>
        </div>
        <div style="font-size:15px;opacity:.45;margin-top:8px">
            Sua plataforma de inteligência financeira
        </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 1.2, 1])[1]
    with col:
        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)

        aba = st.radio("", ["Entrar", "Criar conta"], horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("E-mail", placeholder="seuemail@exemplo.com", key="auth_email")
        senha = st.text_input("Senha", type="password", placeholder="••••••••", key="auth_senha")

        if aba == "Entrar":
            if st.button("🔐 Entrar na conta", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": senha})
                    st.session_state["user_id"]    = res.user.id
                    st.session_state["user_email"] = res.user.email
                    st.session_state["logado"]     = True
                    st.rerun()
                except Exception as e:
                    st.error("E-mail ou senha incorretos.")
        else:
            if st.button("✨ Criar minha conta", use_container_width=True):
                if not email.strip():
                    st.error("Digite seu e-mail.")
                elif len(senha) < 6:
                    st.error("A senha precisa ter pelo menos 6 caracteres.")
                else:
                    try:
                        res = supabase.auth.sign_up({"email": email, "password": senha})
                        if res.user:
                            st.success("✅ Conta criada! Agora clique em Entrar.")
                        else:
                            st.warning("Verifique seu e-mail para confirmar o cadastro.")
                    except Exception as e:
                        msg = str(e)
                        if "already registered" in msg:
                            st.error("Este e-mail já está cadastrado. Use a opção Entrar.")
                        else:
                            st.error(f"Erro: {msg}")

        st.markdown("</div>", unsafe_allow_html=True)

# ── Session guard ─────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login_screen()
    st.stop()

if "logado" not in st.session_state or not st.session_state["logado"]:
    login_screen()
    st.stop()

if not get_user_id():
    st.error("Sessão inválida. Faça login novamente.")
    st.stop()
    
# ── MAIN APP ──────────────────────────────────────────────────────────────────

# ── Header ────────────────────────────────────────────────────────────────────
h1, h2 = st.columns([3, 1])
with h1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:18px">
        <div class="logo-text">Finance <span>PRO X</span></div>
        <div class="live-badge">● Ao vivo</div>
    </div>""", unsafe_allow_html=True)
with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Sair", key="logout"):
        supabase.auth.sign_out()
        for k in ["logado","user_id","user_email"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── Ticker ────────────────────────────────────────────────────────────────────
ticker_html = '<div class="ticker-wrap">'
for a in ATIVOS_TICKER:
    cc = "tick-up" if a["up"] else "tick-dn"
    ticker_html += f'<div class="tick-item"><div class="tick-sym">{a["sym"]}</div><div class="tick-price">{a["price"]}</div><div class="{cc}">{a["chg"]}</div></div>'
ticker_html += "</div>"
st.markdown(ticker_html, unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_lanc, tab_invest, tab_metas = st.tabs([
    "📊  Dashboard", "✏️  Lançamentos", "📈  Investimentos", "🎯  Metas"
])

# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:
    txs   = db_get_lancamentos()
    invs  = db_get_investimentos()
    metas = db_get_metas()

    entradas  = sum(t["valor"] for t in txs if t["tipo"] == "entrada")
    saidas    = sum(t["valor"] for t in txs if t["tipo"] == "saida")
    saldo     = entradas - saidas
    invest    = sum(i["valor"] for i in invs)
    patrimonio = saldo + invest

    # KPIs
    kpis = [
        ("RECEITA",       fmt(entradas),    "Total recebido",         True,       "kpi-purple"),
        ("DESPESAS",      fmt(saidas),      "Total gasto",            saidas==0,  "kpi-blue"),
        ("SALDO",         fmt(saldo),       "Receita − Despesas",     saldo >= 0, "kpi-green"),
        ("INVESTIMENTOS", fmt(invest),      "Total aplicado",         True,       "kpi-amber"),
        ("PATRIMÔNIO",    fmt(patrimonio),  "Investimentos + Saldo",  True,       "kpi-rose"),
    ]
    cols = st.columns(5)
    for col, (label, value, delta, up, cls) in zip(cols, kpis):
        dc = "delta-up" if up else "delta-down"
        col.markdown(f"""
        <div class="kpi-card {cls}">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-delta {dc}">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts row
    col_flow, col_tx = st.columns([1.6, 1])

    with col_flow:
        st.markdown('<div class="panel"><div class="panel-title">📊 Despesas por Categoria</div>', unsafe_allow_html=True)
        cats_saida = {}
        for t in txs:
            if t["tipo"] == "saida":
                cats_saida[t["categoria"]] = cats_saida.get(t["categoria"], 0) + t["valor"]

        if cats_saida:
            fig_bar = go.Figure()
            for cat, val in sorted(cats_saida.items(), key=lambda x: -x[1]):
                fig_bar.add_trace(go.Bar(
                    x=[cat], y=[val],
                    marker_color=CORES_MAP.get(cat, "#7c3aed"),
                    marker_line_width=0, name=cat,
                    hovertemplate=f"<b>{cat}</b><br>{fmt(val)}<extra></extra>",
                ))
            fig_bar.update_layout(**plotly_cfg(), height=240, showlegend=False,
                xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=11)),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(size=10)),
                bargap=0.3)
            st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma despesa ainda. Adicione em ✏️ Lançamentos.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_tx:
        st.markdown('<div class="panel"><div class="panel-title">🧾 Últimas Transações</div>', unsafe_allow_html=True)
        for t in txs[:6]:
            sinal = "+" if t["tipo"] == "entrada" else "-"
            cls   = "tx-pos" if t["tipo"] == "entrada" else "tx-neg"
            dt_fmt = t["data"][:10] if t["data"] else ""
            st.markdown(f"""
            <div class="tx-row">
              <div style="font-size:20px;width:36px;text-align:center">{t['icone']}</div>
              <div style="flex:1">
                <div style="font-size:13px;font-weight:500">{t['nome']}</div>
                <div style="font-size:11px;opacity:.5;margin-top:2px">{t['categoria']} · {dt_fmt}</div>
              </div>
              <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
            </div>""", unsafe_allow_html=True)
        if not txs:
            st.info("Sem transações.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_ring, col_mv = st.columns(2)

    with col_ring:
        st.markdown('<div class="panel"><div class="panel-title">🍩 Distribuição de Despesas</div>', unsafe_allow_html=True)
        if cats_saida:
            fig_ring = go.Figure(go.Pie(
                labels=list(cats_saida.keys()),
                values=list(cats_saida.values()),
                hole=0.7,
                marker_colors=[CORES_MAP.get(c, "#7c3aed") for c in cats_saida],
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value:,.2f}<extra></extra>",
            ))
            fig_ring.update_layout(**plotly_cfg(), height=210, showlegend=True,
                legend=dict(font=dict(size=11, color="rgba(255,255,255,0.65)"), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(
                    text=f"<b>{fmt(saidas)}</b>", x=0.5, y=0.5,
                    font=dict(size=13, color="white", family="Space Grotesk"), showarrow=False
                )])
            st.plotly_chart(fig_ring, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma despesa lançada.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mv:
        st.markdown('<div class="panel"><div class="panel-title">🎯 Metas do Mês</div>', unsafe_allow_html=True)
        for m in metas:
            pct = min(round(m["atual"] / m["total"] * 100), 100) if m["total"] > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;font-size:12px;opacity:.8">
                <span>{m['nome']}</span>
                <span style="color:{m['cor']};font-weight:600">{pct}%</span>
              </div>
              <div class="goal-track">
                <div style="height:100%;width:{pct}%;background:{m['cor']};border-radius:6px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;opacity:.4">
                <span>{fmt(m['atual'])}</span><span>{fmt(m['total'])}</span>
              </div>
            </div>""", unsafe_allow_html=True)
        if not metas:
            st.info("Nenhuma meta cadastrada.")

        # IA Insight
        if saidas > 0 and entradas > 0:
            pct_s = round(saidas / entradas * 100)
            if pct_s > 80:   insight = f"⚠️ Despesas em {pct_s}% da receita — atenção ao orçamento!"
            elif pct_s > 60: insight = f"📊 Despesas em {pct_s}% da receita. Controle aceitável."
            else:             insight = f"✅ Ótimo controle! Despesas em apenas {pct_s}% da receita."
            if cats_saida:
                maior = max(cats_saida, key=cats_saida.get)
                insight += f" Maior custo: {maior}."
        else:
            insight = "Lance suas transações para ativar o Insight de IA. 💡"

        st.markdown(f"""
        <div class="ai-box">
          <div style="font-size:10px;letter-spacing:1.5px;opacity:.5;text-transform:uppercase;margin-bottom:8px">
            ● IA Insight
          </div>
          <div style="font-size:13px;line-height:1.75;opacity:.9">{insight}</div>
        </div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  LANÇAMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_lanc:
    col_form, col_lista = st.columns([1, 1.6])

    with col_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Lançamento</div>', unsafe_allow_html=True)

        tipo  = st.selectbox("Tipo", ["saida", "entrada"],
                    format_func=lambda x: "💸 Saída" if x == "saida" else "💰 Entrada", key="f_tipo")
        nome  = st.text_input("Descrição", placeholder="Ex: Conta de luz", key="f_nome")
        valor = st.number_input("Valor (R$)", min_value=0.01, step=0.01, format="%.2f", key="f_valor")

        cats_op = [c for c in CATS if c != "Salário"] if tipo == "saida" else ["Salário", "Outros"]
        c1, c2  = st.columns(2)
        with c1: cat  = st.selectbox("Categoria", cats_op, key="f_cat")
        with c2: icon = st.selectbox("Ícone", ICONES, key="f_icon")

        data_l = st.date_input("Data", value=date.today(), key="f_data")

        if st.button("✅ Adicionar lançamento", use_container_width=True, key="btn_add_tx"):
            if nome.strip():
                db_add_lancamento(nome.strip(), cat, valor, tipo, icon, data_l)
                st.success(f"'{nome}' salvo!")
                st.rerun()
            else:
                st.error("Digite uma descrição.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_lista:
        st.markdown('<div class="panel"><div class="panel-title">📋 Todos os Lançamentos</div>', unsafe_allow_html=True)
        txs_all = db_get_lancamentos()

        filtro = st.selectbox("🔍 Filtrar por", ["Todos", "Entradas", "Saídas"] + CATS, key="filtro_tx")
        if filtro == "Entradas":  txs_all = [t for t in txs_all if t["tipo"] == "entrada"]
        elif filtro == "Saídas":  txs_all = [t for t in txs_all if t["tipo"] == "saida"]
        elif filtro in CATS:      txs_all = [t for t in txs_all if t["categoria"] == filtro]

        if not txs_all:
            st.info("Nenhum lançamento encontrado.")

        for t in txs_all:
            sinal = "+" if t["tipo"] == "entrada" else "-"
            cls   = "tx-pos" if t["tipo"] == "entrada" else "tx-neg"
            c_i, c_d = st.columns([6, 1])
            with c_i:
                st.markdown(f"""
                <div class="tx-row">
                  <div style="font-size:20px;width:36px;text-align:center">{t['icone']}</div>
                  <div style="flex:1">
                    <div style="font-size:13px;font-weight:500">{t['nome']}</div>
                    <div style="font-size:11px;opacity:.5;margin-top:2px">{t['categoria']} · {t['data'][:10]}</div>
                  </div>
                  <div class="{cls}">{sinal}{fmt(t['valor'])}</div>
                </div>""", unsafe_allow_html=True)
            with c_d:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_tx_{t['id']}"):
                    db_del_lancamento(t["id"])
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INVESTIMENTOS
# ══════════════════════════════════════════════════════════════════════════════
with tab_invest:
    col_inv_form, col_inv_chart = st.columns([1, 1.5])

    with col_inv_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Novo Ativo</div>', unsafe_allow_html=True)
        inv_nome = st.text_input("Nome do ativo", placeholder="Ex: Tesouro Selic 2029", key="inv_nome")
        inv_val  = st.number_input("Valor (R$)", min_value=0.0, step=100.0, format="%.2f", key="inv_val")
        inv_chg  = st.text_input("Variação", placeholder="Ex: +5.2%", key="inv_chg")
        inv_cor  = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c, c), key="inv_cor")

        if st.button("✅ Adicionar ativo", use_container_width=True, key="btn_add_inv"):
            if inv_nome.strip():
                db_add_investimento(inv_nome.strip(), inv_val, inv_chg or "0%", inv_cor)
                st.success(f"'{inv_nome}' adicionado!")
                st.rerun()
            else:
                st.error("Digite o nome do ativo.")
        st.markdown("</div>", unsafe_allow_html=True)

        invs_list = db_get_investimentos()
        total_port = sum(i["valor"] for i in invs_list)

        st.markdown('<div class="panel"><div class="panel-title">🏦 Seus Ativos</div>', unsafe_allow_html=True)
        for inv in invs_list:
            pct = round(inv["valor"] / total_port * 100) if total_port > 0 else 0
            chg_color = "#4ade80" if str(inv["variacao"]).startswith("+") else "#f87171"
            c_i, c_d  = st.columns([5, 1])
            with c_i:
                st.markdown(f"""
                <div class="tx-row">
                  <div style="width:10px;height:10px;border-radius:50%;background:{inv['cor']};flex-shrink:0"></div>
                  <div style="flex:1;margin-left:10px">
                    <div style="font-size:13px;font-weight:500">{inv['nome']}</div>
                    <div style="font-size:11px;opacity:.5">{pct}% do portfolio</div>
                  </div>
                  <div style="text-align:right">
                    <div style="font-size:13px;font-weight:600">{fmt(inv['valor'])}</div>
                    <div style="font-size:11px;color:{chg_color}">{inv['variacao']}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with c_d:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_inv_{inv['id']}"):
                    db_del_investimento(inv["id"])
                    st.rerun()
        if not invs_list:
            st.info("Nenhum ativo cadastrado.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_inv_chart:
        st.markdown('<div class="panel"><div class="panel-title">📊 Portfolio</div>', unsafe_allow_html=True)
        invs_list2 = db_get_investimentos()
        if invs_list2:
            total_p2 = sum(i["valor"] for i in invs_list2)
            fig_port  = go.Figure(go.Pie(
                labels=[i["nome"] for i in invs_list2],
                values=[i["valor"] for i in invs_list2],
                hole=0.68,
                marker_colors=[i["cor"] for i in invs_list2],
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>%{value:,.2f}<extra></extra>",
            ))
            fig_port.update_layout(**plotly_cfg(), height=400, showlegend=True,
                legend=dict(font=dict(color="rgba(255,255,255,0.65)", size=12), bgcolor="rgba(0,0,0,0)"),
                annotations=[dict(
                    text=f"<b>{fmt(total_p2)}</b>", x=0.38, y=0.5,
                    font=dict(size=15, color="white", family="Space Grotesk"), showarrow=False
                )])
            st.plotly_chart(fig_port, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Adicione ativos para ver o gráfico de portfolio.")
        st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  METAS
# ══════════════════════════════════════════════════════════════════════════════
with tab_metas:
    col_meta_form, col_meta_list = st.columns([1, 1.5])

    with col_meta_form:
        st.markdown('<div class="form-box"><div class="form-title">➕ Nova Meta</div>', unsafe_allow_html=True)
        meta_nome  = st.text_input("Nome da meta", placeholder="Ex: Fundo de emergência", key="meta_nome")
        meta_atual = st.number_input("Valor atual (R$)", min_value=0.0, step=100.0, format="%.2f", key="meta_atual")
        meta_total = st.number_input("Valor da meta (R$)", min_value=1.0, step=100.0, format="%.2f", key="meta_total", value=1000.0)
        meta_cor   = st.selectbox("Cor", CORES, format_func=lambda c: COR_LABEL.get(c, c), key="meta_cor")

        if st.button("✅ Adicionar meta", use_container_width=True, key="btn_add_meta"):
            if meta_nome.strip():
                db_add_meta(meta_nome.strip(), meta_atual, meta_total, meta_cor)
                st.success(f"Meta '{meta_nome}' criada!")
                st.rerun()
            else:
                st.error("Digite o nome da meta.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_meta_list:
        st.markdown('<div class="panel"><div class="panel-title">🏆 Suas Metas</div>', unsafe_allow_html=True)
        metas_list = db_get_metas()

        if not metas_list:
            st.info("Nenhuma meta cadastrada ainda.")

        for m in metas_list:
            pct = min(round(m["atual"] / m["total"] * 100), 100) if m["total"] > 0 else 0
            st.markdown(f"""
            <div style="margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:500">
                <span>{m['nome']}</span>
                <span style="color:{m['cor']};font-weight:700">{pct}%</span>
              </div>
              <div class="goal-track">
                <div style="height:100%;width:{pct}%;background:{m['cor']};border-radius:6px"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:10px;opacity:.4;margin-bottom:10px">
                <span>Atual: {fmt(m['atual'])}</span><span>Meta: {fmt(m['total'])}</span>
              </div>
            </div>""", unsafe_allow_html=True)

            c_upd, c_del_m = st.columns([4, 1])
            with c_upd:
                novo_a = st.number_input(
                    f"upd_{m['id']}", value=float(m["atual"]),
                    min_value=0.0, step=100.0, format="%.2f",
                    key=f"upd_meta_{m['id']}", label_visibility="collapsed"
                )
                if st.button("💾 Atualizar", key=f"save_meta_{m['id']}"):
                    db_update_meta(m["id"], novo_a)
                    st.rerun()
            with c_del_m:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️", key=f"del_meta_{m['id']}"):
                    db_del_meta(m["id"])
                    st.rerun()
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
