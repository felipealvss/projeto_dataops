import os
import json
from pymongo import MongoClient
import logging

# Configurações MongoDB
MONGO_URI = "mongodb+srv://felipe:123@unifor.o7sppxt.mongodb.net/?retryWrites=true&w=majority&appName=unifor"
MONGO_DB = "unifor"
MONGO_COLLECTION = "dataops_dados"

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho de diretório local para exportação
EXPORT_PATH = "/opt/airflow/data/extract/mongo_export.json"

def exportar_dados_mongodb():
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]
        dados = list(collection.find({}, {"_id": 0}))

        os.makedirs(os.path.dirname(EXPORT_PATH), exist_ok=True)

        with open(EXPORT_PATH, "w") as f:
            json.dump(dados, f, indent=4)

        logger.info(f"{len(dados)} registros exportados para {EXPORT_PATH}")
    except Exception as e:
        logger.error(f"Erro ao exportar dados: {e}")
        raise
