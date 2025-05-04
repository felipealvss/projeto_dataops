from fastapi import FastAPI
from fastapi_app.routers import modalidade, cidade, ano_mes

app = FastAPI(title="API de Vendas - (Z111) DataOPS Unifor")

app.include_router(modalidade.router)
app.include_router(cidade.router)
app.include_router(ano_mes.router)
