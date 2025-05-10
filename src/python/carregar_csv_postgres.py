import pandas as pd
import psycopg2
import os
import logging

# Configurações do PostgreSQL
POSTGRES_CONF = {
    "host": "postgres",
    "port": 5432,
    "user": "airflow",
    "password": "airflow",
    "dbname": "airflow"
}

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def carregar_csv_para_postgres(caminho_csv, tabela_destino, colunas, tipos):
    """
    Função para carregar dados de um arquivo CSV para o PostgreSQL.
    """
    try:
        if not os.path.exists(caminho_csv):
            raise FileNotFoundError(f"Arquivo CSV não encontrado: {caminho_csv}")

        df = pd.read_csv(caminho_csv)
        if df.empty:
            raise ValueError("O DataFrame está vazio.")

        conn = psycopg2.connect(**POSTGRES_CONF)
        cur = conn.cursor()

        # Criação da tabela se não existir
        col_def = ", ".join([f"{col} {tipo}" for col, tipo in zip(colunas, tipos)])
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tabela_destino} ({col_def});")

        # Limpeza da tabela antes de inserir os novos dados
        cur.execute(f"TRUNCATE TABLE {tabela_destino};")

        # Carga dos dados no PostgreSQL
        for _, row in df.iterrows():
            values = tuple(row[col] for col in colunas)
            placeholders = ", ".join(["%s"] * len(colunas))
            cur.execute(
                f"INSERT INTO {tabela_destino} ({', '.join(colunas)}) VALUES ({placeholders})",
                values
            )

        conn.commit()
        cur.close()
        conn.close()
        logger.info(f"{len(df)} registros inseridos na tabela '{tabela_destino}' com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar os dados: {e}")
        raise
