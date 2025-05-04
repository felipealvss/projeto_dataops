import streamlit as st
import requests
import pymongo
from datetime import datetime
import time

# ====== CONFIGURAÇÕES GERAIS ======
st.set_page_config(page_title="Monitoramento API de Vendas - (Z111) DataOPS Unifor", layout="wide")
st.title("📊 Monitoramento API de Vendas - (Z111) DataOPS Unifor")

# ====== CONFIGURAÇÃO MONGODB ATLAS ======
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# ====== CONFIGURAÇÃO API FASTAPI ======
API_URL = "http://host.docker.internal:8000/vendas"  # para acessar serviço da FastAPI via Docker

# ====== FUNÇÃO PARA OBTER DADOS DO MONGODB ======
@st.cache_data(ttl=60)  # atualiza a cada 60 segundos
def get_mongo_stats():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    total = collection.count_documents({})
    last_doc = collection.find_one(sort=[("_id", -1)])
    last_updated = last_doc["timestamp"] if last_doc and "timestamp" in last_doc else datetime.utcnow()
    return total, last_updated

# ====== EXIBIÇÃO DE DADOS DO MONGO ======
st.subheader("📦 Dados MongoDB (Gerados pela DAG)")
total, last_updated = get_mongo_stats()

col1, col2 = st.columns(2)
col1.metric("Total de registros", total)
col2.metric("Última atualização", last_updated.strftime("%d/%m/%Y %H:%M:%S"))

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
    st.json(consultar_endpoint("modalidade"))

if col2.button("🌆 Vendas por Cidade"):
    st.json(consultar_endpoint("cidade"))

if col3.button("📅 Vendas por Ano/Mês"):
    st.json(consultar_endpoint("ano-mes"))
