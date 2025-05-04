from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pymongo import MongoClient
import random

# Configurações do MongoDB Atlas
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# Função para gerar um registro de venda aleatório
def gerar_venda():
    modelos_motos = ["Yamaha MT-07", "Honda CB 500X", "Kawasaki Ninja 400", "Suzuki GSX-S750", "BMW F 800 GS"]
    modalidades = ["Consócio", "Financiamento", "À vista"]
    cidades = ["Fortaleza", "Caucaia", "Juazeiro do Norte", "Sobral", "Crato"]
    estado = "Ceará"
    data_venda = (datetime.now() - timedelta(days=random.randint(0, 120))).strftime("%Y-%m-%d")
    cidade = random.choice(cidades)
    moto_mais_vendida = random.choice(modelos_motos)
    quantidade_moto_mais_vendida = random.randint(2, 5)
    preco_unitario = round(random.uniform(12000.00, 25000.00), 2)
    preco_total = round(quantidade_moto_mais_vendida * preco_unitario, 2)
    total_vendas = random.randint(15, 35)
    total_faturado = round(total_vendas * random.uniform(10000.00, 25000.00), 2)
    modalidade = random.choice(modalidades)

    return {
        "data_venda": data_venda,
        "total_vendas": total_vendas,
        "total_faturado": total_faturado,
        "moto_mais_vendida": moto_mais_vendida,
        "quantidade_moto_mais_vendida": quantidade_moto_mais_vendida,
        "preco_total": preco_total,
        "cidade": cidade,
        "estado": estado,
        "modalidade": modalidade
    }

# Função que será chamada pela DAG
def gerar_registros(**context):
    try:
        registros = [gerar_venda() for _ in range(2)]
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        collection.insert_many(registros)
        print(f"{len(registros)} registros inseridos com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir dados no MongoDB: {e}")
        raise

# Definição da DAG
dag = DAG(
    dag_id="generate_data_mongo",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",  # Ajuste para o agendamento desejado
    catchup=False,
    tags=["dataops"]
)

# Tarefa PythonOperator
gerar_dados_task = PythonOperator(
    task_id="gerar_dados_mongodb",
    python_callable=gerar_registros,
    dag=dag
)

# Definindo a ordem de execução
gerar_dados_task
