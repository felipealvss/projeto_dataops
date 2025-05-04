import json
from airflow import DAG
from airflow.operators.python import PythonOperator
from pymongo import MongoClient
import psycopg2
from datetime import datetime
import pandas as pd

# Configurações do MongoDB Atlas
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# Configurações do PostgreSQL
POSTGRES_HOST = "postgres"
POSTGRES_PORT = "5432"
POSTGRES_USER = "airflow"
POSTGRES_PASSWORD = "airflow"
POSTGRES_DB = "airflow"

POSTGRES_TABLE = "vendas_por_modalidade"

def consultar_e_agrupar_vendas(**context):
    try:

        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]

        pipeline = [
            {
                "$group": {
                    "_id": "$modalidade",
                    "total_vendas": {"$sum": "$total_vendas"},
                    "total_faturado": {"$sum": "$total_faturado"},
                    "quantidade_motos_vendidas": {"$sum": "$quantidade_moto_mais_vendida"}
                }
            },
            {
                "$sort": {"total_vendas": -1}  # Ordenar por total_vendas
            }
        ]

        resultado = list(collection.aggregate(pipeline))
        if resultado:

            df = pd.DataFrame(resultado)

            df = df.rename(columns={
                "_id": "modalidade",
                "total_vendas": "total_vendas",
                "total_faturado": "total_faturado",
                "quantidade_motos_vendidas": "quantidade_motos_vendidas"
            })
            df['modalidade'] = df['modalidade'].astype(str)  # Garantir que modalidade é string
            
            return json.dumps(df.to_dict(orient="records"))  # Converte para lista de dicionários e serializa como JSON
        else:
            raise Exception("Nenhum dado encontrado.")

    except Exception as e:
        print(f"Erro ao consultar ou agrupar dados do MongoDB: {e}")
        raise

def inserir_dados_no_postgres(df, **context):
    try:

        df = json.loads(df)  # Desserializa o JSON de volta para a lista de dicionários
        
        if isinstance(df, list) and all(isinstance(item, dict) for item in df):

            df = pd.DataFrame(df)
        else:
            raise ValueError(f"O tipo de 'df' não é uma lista de dicionários. Tipo atual: {type(df)}")

        # Conectar ao PostgreSQL com psycopg2
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB
        )
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas_por_modalidade (
                modalidade VARCHAR(255),
                total_vendas INT,
                total_faturado DOUBLE PRECISION,
                quantidade_motos_vendidas INT
            );
        """)

        cursor.execute(f"TRUNCATE TABLE {POSTGRES_TABLE};")

        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO vendas_por_modalidade (modalidade, total_vendas, total_faturado, quantidade_motos_vendidas)
                VALUES (%s, %s, %s, %s)
                """, (row['modalidade'], row['total_vendas'], row['total_faturado'], row['quantidade_motos_vendidas']))
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{len(df)} registros inseridos com sucesso.")
    
    except Exception as e:
        print(f"Erro ao inserir dados no PostgreSQL: {e}")
        raise

dag = DAG(
    dag_id="vendas_por_modalidade",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # Ajuste para o agendamento desejado
    catchup=False,
    tags=["dataops"]
)

consultar_e_agrupar_task = PythonOperator(
    task_id="consultar_e_agrupar_vendas",
    python_callable=consultar_e_agrupar_vendas,
    provide_context=True,
    dag=dag
)

inserir_dados_task = PythonOperator(
    task_id="inserir_dados_postgres",
    python_callable=inserir_dados_no_postgres,
    provide_context=True,
    op_args=['{{ task_instance.xcom_pull(task_ids="consultar_e_agrupar_vendas") }}'],  # Passa os dados para a próxima tarefa
    dag=dag
)

consultar_e_agrupar_task >> inserir_dados_task
