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

# Configurações do PostgreSQL diretamente no código
POSTGRES_HOST = "postgres"  # Endereço do seu contêiner do PostgreSQL (local ou outro host)
POSTGRES_PORT = "5432"      # A porta padrão do PostgreSQL
POSTGRES_USER = "airflow"   # Usuário do PostgreSQL
POSTGRES_PASSWORD = "airflow"  # Senha do PostgreSQL
POSTGRES_DB = "airflow"  # Banco de dados

POSTGRES_TABLE = "vendas_por_ano_mes"  # Novo nome da tabela

# Função para consultar dados do MongoDB e agrupar por ano e mês
def consultar_e_agrupar_vendas_por_ano_mes(**context):
    try:
        # Conectar ao MongoDB
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        
        # Consultar todos os dados
        pipeline = [
            {
                "$addFields": {
                    "ano_mes": {
                        "$dateToString": {"format": "%Y-%m", "date": {"$dateFromString": {"dateString": "$data_venda"}}}
                    }
                }
            },
            {
                "$group": {
                    "_id": "$ano_mes",
                    "total_vendas": {"$sum": "$total_vendas"},
                    "total_faturado": {"$sum": "$total_faturado"},
                    "quantidade_motos_vendidas": {"$sum": "$quantidade_moto_mais_vendida"}
                }
            },
            {
                "$sort": {"_id": 1}  # Ordenar por ano e mês
            }
        ]
        
        resultado = list(collection.aggregate(pipeline))
        if resultado:
            # Transformar o resultado em um DataFrame
            df = pd.DataFrame(resultado)
            # Ajustar o formato para o PostgreSQL
            df = df.rename(columns={
                "_id": "ano_mes",
                "total_vendas": "total_vendas",
                "total_faturado": "total_faturado",
                "quantidade_motos_vendidas": "quantidade_motos_vendidas"
            })
            
            # Retornar os dados como uma lista de dicionários (formato serializável)
            return json.dumps(df.to_dict(orient="records"))  # Converte para lista de dicionários e serializa como JSON
        else:
            raise Exception("Nenhum dado encontrado.")
    
    except Exception as e:
        print(f"Erro ao consultar ou agrupar dados do MongoDB: {e}")
        raise

# Função para inserir os dados agrupados no PostgreSQL
def inserir_dados_no_postgres(df, **context):
    try:
        # Desserializar os dados do XCom (converter de volta para lista de dicionários)
        df = json.loads(df)  # Desserializa o JSON de volta para a lista de dicionários
        
        # Verificar se df é uma lista de dicionários antes de tentar convertê-la em um DataFrame
        if isinstance(df, list) and all(isinstance(item, dict) for item in df):
            # Converte a lista de dicionários em DataFrame
            df = pd.DataFrame(df)
        else:
            raise ValueError(f"O tipo de 'df' não é uma lista de dicionários. Tipo atual: {type(df)}")

        # Conectar ao PostgreSQL diretamente com psycopg2
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            dbname=POSTGRES_DB
        )
        cursor = conn.cursor()
        
        # Verificar se a tabela existe e criar, caso não exista
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vendas_por_ano_mes (
                ano_mes VARCHAR(7),  -- No formato YYYY-MM
                total_vendas INT,
                total_faturado DOUBLE PRECISION,
                quantidade_motos_vendidas INT
            );
        """)

        # Truncar a tabela antes de inserir novos dados
        cursor.execute(f"TRUNCATE TABLE {POSTGRES_TABLE};")

        # Inserir os dados no PostgreSQL
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO vendas_por_ano_mes (ano_mes, total_vendas, total_faturado, quantidade_motos_vendidas)
                VALUES (%s, %s, %s, %s)
                """, (row['ano_mes'], row['total_vendas'], row['total_faturado'], row['quantidade_motos_vendidas']))
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"{len(df)} registros inseridos com sucesso.")
    
    except Exception as e:
        print(f"Erro ao inserir dados no PostgreSQL: {e}")
        raise

# Definição da DAG
dag = DAG(
    dag_id="vendas_por_ano_mes",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # Ajuste para o agendamento desejado
    catchup=False,
    tags=["dataops"]
)

# Tarefa para consultar e agrupar dados do MongoDB por ano e mês
consultar_e_agrupar_task = PythonOperator(
    task_id="consultar_e_agrupar_vendas_por_ano_mes",
    python_callable=consultar_e_agrupar_vendas_por_ano_mes,
    provide_context=True,
    dag=dag
)

# Tarefa para inserir os dados no PostgreSQL
inserir_dados_task = PythonOperator(
    task_id="inserir_dados_postgres",
    python_callable=inserir_dados_no_postgres,
    provide_context=True,
    op_args=['{{ task_instance.xcom_pull(task_ids="consultar_e_agrupar_vendas_por_ano_mes") }}'],  # Passa os dados para a próxima tarefa
    dag=dag
)

# Definindo a ordem de execução
consultar_e_agrupar_task >> inserir_dados_task
