from carregar_csv_postgres import carregar_csv_para_postgres

# Definindo os parâmetros para a carga
CAMINHO_CSV = "/opt/airflow/data/transform/data_transform_ano_mes.csv"
TABELA_DESTINO = "vendas_por_ano_mes"
COLUNAS = ["ano_mes", "total_vendas", "total_faturado", "quantidade_motos_vendidas"]
TIPOS = ["VARCHAR(7)", "INT", "DOUBLE PRECISION", "INT"]

# Chama a função de carga
carregar_csv_para_postgres(CAMINHO_CSV, TABELA_DESTINO, COLUNAS, TIPOS)
