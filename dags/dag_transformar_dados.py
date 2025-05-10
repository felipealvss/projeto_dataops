from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

SCRIPT_ANO_MES = "/opt/airflow/src/python/vendas_ano_mes.py"
SCRIPT_ESTADO = "/opt/airflow/src/python/vendas_estado.py"
SCRIPT_MODALIDADE = "/opt/airflow/src/python/vendas_modalidade.py"

with DAG(
    dag_id="transformar_json_csv",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["dataops", "transform"]
) as dag:

    transformar_task = BashOperator(
        task_id="transformar_json_em_csv_ano_mes",
        bash_command=f"python3 {SCRIPT_ANO_MES}"
    )

    transformar_estado_task = BashOperator(
        task_id="transformar_json_em_csv_estado",
        bash_command=f"python3 {SCRIPT_ESTADO}"
    )

    transformar_modalidade_task = BashOperator(
        task_id="transformar_json_em_csv_modalidade",
        bash_command=f"python3 {SCRIPT_MODALIDADE}"
    )
