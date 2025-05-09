# monitoramento.py

import streamlit as st
import requests
import pymongo
from datetime import datetime
import pytz

# Fuso horário
fuso_local = pytz.timezone("America/Fortaleza")

# Configurações MongoDB Atlas
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# Configuração da API FastAPI
API_URL = "http://host.docker.internal:8000/vendas"

# Consulta dados no MongoDB
@st.cache_data(ttl=60)
def get_mongo_stats():
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    total = collection.count_documents({})
    last_doc = collection.find_one(sort=[("_id", -1)])
    last_updated = last_doc["timestamp"].astimezone(fuso_local) if last_doc and "timestamp" in last_doc else datetime.now(fuso_local)
    return total, last_updated

# Consulta endpoints da API
def consultar_endpoint(endpoint):
    try:
        response = requests.get(f"{API_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"erro": str(e)}

# Página de Monitoramento
def pagina_monitoramento():
    st.subheader("📦 Dados MongoDB (Gerados pela DAG)")
    total, last_updated = get_mongo_stats()

    col1, col2, col3 = st.columns([1, 1, 1])
    col1.metric("Total de registros", total)
    col2.metric("Última atualização", last_updated.strftime("%d/%m/%Y %H:%M:%S"))

    # Botão de atualização manual
    with col3:
        if st.button("🔄 Atualizar agora"):
            st.cache_data.clear()
            st.rerun()

    st.divider()
    st.subheader("🔁 Consultar Endpoints da API")

    col1, col2, col3 = st.columns(3)

    if col1.button("📍 Vendas por Modalidade"):
        resultado = consultar_endpoint("modalidade")
        st.dataframe(resultado) if isinstance(resultado, list) else st.json(resultado)

    if col2.button("🌆 Vendas por Cidade"):
        resultado = consultar_endpoint("cidade")
        st.dataframe(resultado) if isinstance(resultado, list) else st.json(resultado)

    if col3.button("📅 Vendas por Ano/Mês"):
        resultado = consultar_endpoint("ano-mes")
        st.dataframe(resultado) if isinstance(resultado, list) else st.json(resultado)
