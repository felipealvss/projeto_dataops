import streamlit as st
import pytz
from monitoramento import pagina_monitoramento
from diagnostico import pagina_diagnostico

# ====== CONFIGURAÇÕES GERAIS ======
st.set_page_config(page_title="Monitoramento API de Vendas - (Z111) DataOPS Unifor", layout="wide")
st.title("📊 Monitoramento API de Vendas - (Z111) DataOPS Unifor")

pagina = st.sidebar.radio("🧭 Navegação", ["📊 Monitoramento", "🛠 Diagnóstico"])

# ====== ROTEAMENTO DAS PÁGINAS ======
if pagina == "📊 Monitoramento":
    pagina_monitoramento()

elif pagina == "🛠 Diagnóstico":
    pagina_diagnostico()
