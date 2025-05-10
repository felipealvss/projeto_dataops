import pandas as pd
import json
import os
import logging

INPUT_PATH = "/opt/airflow/data/extract/mongo_export.json"
EXPORT_PATH = "/opt/airflow/data/transform/data_transform_estado.csv"

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transformar_por_estado_para_csv():
    try:
        if not os.path.exists(INPUT_PATH):
            raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_PATH}")

        with open(INPUT_PATH, "r") as f:
            dados = json.load(f)

        df = pd.DataFrame(dados)

        if df.empty:
            raise ValueError("O DataFrame está vazio.")

        df_grouped = df.groupby(["cidade", "estado"]).agg({
            "total_vendas": "sum",
            "total_faturado": "sum",
            "quantidade_moto_mais_vendida": "sum"
        }).reset_index()

        df_grouped.rename(columns={
            "quantidade_moto_mais_vendida": "quantidade_motos_vendidas"
        }, inplace=True)

        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

        df_grouped.to_csv(EXPORT_PATH, index=False)

        logger.info(f"Arquivo CSV gerado com sucesso: {EXPORT_PATH}")
    except Exception as e:
        logger.error(f"Erro ao transformar os dados: {e}")
        raise
