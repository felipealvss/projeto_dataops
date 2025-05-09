import streamlit as st
import requests
import pymongo
import psycopg2
from datetime import datetime, timedelta, timezone
import pytz

# Fuso horário
fuso_local = pytz.timezone("America/Fortaleza")

# Configs
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
API_URL = "http://host.docker.internal:8000/vendas"
POSTGRES_CONF = {
    "dbname": "airflow",
    "user": "airflow",
    "password": "airflow",
    "host": "postgres",
    "port": 5432
}

# Verificação de status dos serviços
def check_mongo_status():
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command("ping")
        return "🟢 OK"
    except:
        return "🔴 Falha"

def check_fastapi_status():
    try:
        r = requests.get(f"{API_URL}/modalidade", timeout=2)
        return "🟢 OK" if r.status_code == 200 else "🟡 Parcial"
    except:
        return "🔴 Falha"

def check_postgres_status():
    try:
        conn = psycopg2.connect(**POSTGRES_CONF, connect_timeout=2)
        conn.close()
        return "🟢 OK"
    except:
        return "🔴 Falha"

def checar_airflow():
    try:
        response = requests.get("http://host.docker.internal:8080/health", timeout=2)
        return "🟢 OK" if response.status_code == 200 else "🟡 Parcial"
    except:
        return "🔴 Falha"

# Informações da DAG
def obter_info_dag(dag_id="generate_data_mongo"):
    try:
        conn = psycopg2.connect(**POSTGRES_CONF)
        cur = conn.cursor()
        cur.execute(f'''
            SELECT execution_date, end_date, start_date, run_type
            FROM dag_run
            WHERE dag_id = %s
            ORDER BY execution_date DESC
            LIMIT 5
        ''', (dag_id,))
        registros = cur.fetchall()
        conn.close()

        if not registros:
            return "Sem execuções", 0, "N/A"

        ultima_execucao = registros[0][0].strftime("%d/%m/%Y %H:%M:%S")
        tipo_ultima = registros[0][3]
        execucoes_24h = [r for r in registros if r[0] > (datetime.now(timezone.utc) - timedelta(hours=24))]
        tempos = [(r[1] - r[2]).total_seconds() for r in registros if r[1] and r[2]]
        tempo_medio = sum(tempos) / len(tempos) if tempos else 0
        tempo_formatado = f"{int(tempo_medio//60)}m{int(tempo_medio%60)}s"

        return ultima_execucao, len(execucoes_24h), tempo_formatado, tipo_ultima

    except Exception as e:
        return f"Erro: {str(e)}", "-", "-", "-"

# Página Diagnóstico
def pagina_diagnostico():
    st.subheader("🚦 Diagnóstico do Ambiente")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MongoDB Atlas", check_mongo_status())
    col2.metric("FastAPI", check_fastapi_status())
    col3.metric("PostgreSQL", check_postgres_status())
    col4.metric("Airflow", checar_airflow())

    st.divider()
    st.subheader("📅 Indicadores de Saúde da DAG `generate_data_mongo`")

    ultima_execucao, execucoes, tempo_medio, tipo_execucao = obter_info_dag()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Última execução", ultima_execucao)
    col2.metric("Execuções últimas 24h", execucoes)
    col3.metric("Tempo médio de execução", tempo_medio)
    col4.metric("Tipo da execução", tipo_execucao.capitalize())
