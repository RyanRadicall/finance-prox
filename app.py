import streamlit as st
import plotly.graph_objects as go
from datetime import date
from supabase import create_client, Client

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Finance PRO X",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Configure SUPABASE_URL e SUPABASE_ANON_KEY no secrets.toml")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ── Session init ──────────────────────────────────────────────────────────────
if "logado" not in st.session_state:
    st.session_state["logado"] = False
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_user_id():
    return st.session_state.get("user_id")


def fmt(v):
    return f"R$ {v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

# ── DB SAFETY WRAPPER ────────────────────────────────────────────────────────
def safe_select(table, filters=None):
    uid = get_user_id()
    if not uid:
        return []

    query = supabase.table(table).select("*").eq("user_id", uid)

    if filters:
        for k, v in filters.items():
            query = query.eq(k, v)

    return query.execute().data or []

# ── AUTH ─────────────────────────────────────────────────────────────────────

def login_screen():
    st.title("Finance PRO X 💜")

    tab1, tab2 = st.tabs(["Entrar", "Criar conta"])

    with tab1:
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_pass")

        if st.button("Entrar"):
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": senha
                })

                st.session_state["user_id"] = res.user.id
                st.session_state["user_email"] = res.user.email
                st.session_state["logado"] = True

                st.rerun()

            except Exception as e:
                st.error(f"Erro login: {e}")

    with tab2:
        email = st.text_input("Email cadastro", key="reg_email")
        senha = st.text_input("Senha cadastro", type="password", key="reg_pass")

        if st.button("Criar conta"):
            try:
                res = supabase.auth.sign_up({
                    "email": email,
                    "password": senha
                })
                st.success("Conta criada! Confirme o email se necessário.")
            except Exception as e:
                st.error(f"Erro cadastro: {e}")


# ── SESSION GUARD ────────────────────────────────────────────────────────────
if not st.session_state["logado"] or not get_user_id():
    login_screen()
    st.stop()

# ── DATA FUNCTIONS ────────────────────────────────────────────────────────────

def get_lancamentos():
    return safe_select("lancamentos")


def add_lancamento(nome, cat, val, tipo, icone, dt):
    supabase.table("lancamentos").insert({
        "user_id": get_user_id(),
        "nome": nome,
        "categoria": cat,
        "valor": val,
        "tipo": tipo,
        "icone": icone,
        "data": str(dt)
    }).execute()


def del_lancamento(rid):
    supabase.table("lancamentos").delete().eq("id", rid).execute()

# ── APP ───────────────────────────────────────────────────────────────────────

st.markdown("## Dashboard Finance PRO X")

lanc = get_lancamentos()

entradas = sum(x["valor"] for x in lanc if x["tipo"] == "entrada")
saidas = sum(x["valor"] for x in lanc if x["tipo"] == "saida")
saldo = entradas - saidas

col1, col2, col3 = st.columns(3)
col1.metric("Entradas", fmt(entradas))
col2.metric("Saídas", fmt(saidas))
col3.metric("Saldo", fmt(saldo))

st.divider()

st.subheader("Lançamentos")

for t in lanc:
    colA, colB, colC = st.columns([4,2,1])

    with colA:
        st.write(f"{t['icone']} {t['nome']} - {t['categoria']}")

    with colB:
        st.write(fmt(t['valor']))

    with colC:
        if st.button("🗑️", key=f"del_{t['id']}"):
            del_lancamento(t['id'])
            st.rerun()

st.divider()

st.subheader("Adicionar lançamento")

nome = st.text_input("Nome")
cat = st.text_input("Categoria")
val = st.number_input("Valor", min_value=0.0)
tipo = st.selectbox("Tipo", ["entrada","saida"])
ico = st.text_input("Ícone", "💰")
data = st.date_input("Data", date.today())

if st.button("Adicionar"):
    add_lancamento(nome, cat, val, tipo, ico, data)
    st.rerun()
