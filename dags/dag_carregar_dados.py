from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

SCRIPT_CARGA_ANO_MES = "/opt/airflow/src/python/carga_vendas_ano_mes.py"
SCRIPT_CARGA_ESTADO = "/opt/airflow/src/python/carga_vendas_estado.py"
SCRIPT_CARGA_MODALIDADE = "/opt/airflow/src/python/carga_vendas_modalidade.py"

# Definindo a DAG principal
with DAG(
    dag_id="carga_dados_postgres",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # Executa a DAG diariamente
    catchup=False,
    tags=["dataops", "load"]
) as dag:

    # Tarefa para carregar vendas por ano e mês
    carga_ano_mes = BashOperator(
        task_id="carga_vendas_por_ano_mes",
        bash_command=f"python3 {SCRIPT_CARGA_ANO_MES}"
    )

    # Tarefa para carregar vendas por estado
    carga_estado = BashOperator(
        task_id="carga_vendas_por_estado",
        bash_command=f"python3 {SCRIPT_CARGA_ESTADO}"
    )

    # Tarefa para carregar vendas por modalidade
    carga_modalidade = BashOperator(
        task_id="carga_vendas_por_modalidade",
        bash_command=f"python3 {SCRIPT_CARGA_MODALIDADE}"
    )
