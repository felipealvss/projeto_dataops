from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
import subprocess

SCRIPT_PATH = "/opt/airflow/src/python/extrair_dados.py"

# Configuração de logging
logging.basicConfig(level=logging.INFO)

# Executando via subprocess
def executar_script_python():
    subprocess.run(["python3", SCRIPT_PATH], check=True)

with DAG(
    dag_id="extrair_dados_mongo",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dataops", "extract"]
) as dag:

    exportar_task = PythonOperator(
        task_id="exportar_para_json",
        python_callable=executar_script_python
    )
