import streamlit as st
import requests
import pymongo
from datetime import datetime
import pytz

fuso_local = pytz.timezone("America/Fortaleza")

# ====== CONFIGURAÇÕES GERAIS ======
st.set_page_config(page_title="Monitoramento API de Vendas - (Z111) DataOPS Unifor", layout="wide")
st.title("📊 Monitoramento API de Vendas - (Z111) DataOPS Unifor")

# ====== CONFIGURAÇÃO MONGODB ATLAS ======
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# ====== CONFIGURAÇÃO API FASTAPI ======
API_URL = "http://host.docker.internal:8000/vendas"

# ====== FUNÇÃO PARA OBTER DADOS DO MONGODB ======
@st.cache_data(ttl=60)  # atualiza a cada 60 segundos
def get_mongo_stats():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    total = collection.count_documents({})
    last_doc = collection.find_one(sort=[("_id", -1)])
    last_updated = last_doc["timestamp"].astimezone(fuso_local) if last_doc and "timestamp" in last_doc else datetime.now(fuso_local)
    return total, last_updated

# ====== EXIBIÇÃO DE DADOS DO MONGO ======
st.subheader("📦 Dados MongoDB (Gerados pela DAG)")
total, last_updated = get_mongo_stats()

col1, col2, col3 = st.columns([1, 1, 1])
col1.metric("Total de registros", total)
col2.metric("Última atualização", last_updated.strftime("%d/%m/%Y %H:%M:%S"))

# 👉 Botão de atualização manual ao lado direito
with col3:
    if st.button("🔄 Atualizar agora"):
        st.cache_data.clear()
        st.rerun()

st.divider()

# ====== BOTÕES PARA CONSULTA AOS ENDPOINTS FASTAPI ======
st.subheader("🔁 Consultar Endpoints da API")

def consultar_endpoint(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"erro": str(e)}

col1, col2, col3 = st.columns(3)

if col1.button("📍 Vendas por Modalidade"):
    resultado = consultar_endpoint("modalidade")
    if isinstance(resultado, list):
        st.dataframe(resultado)
    else:
        st.json(resultado)

if col2.button("🌆 Vendas por Cidade"):
    resultado = consultar_endpoint("cidade")
    if isinstance(resultado, list):
        st.dataframe(resultado)
    else:
        st.json(resultado)

if col3.button("📅 Vendas por Ano/Mês"):
    resultado = consultar_endpoint("ano-mes")
    if isinstance(resultado, list):
        st.dataframe(resultado)
    else:
        st.json(resultado)