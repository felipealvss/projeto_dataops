from pydantic import BaseModel

class VendaPorModalidade(BaseModel):
    modalidade: str
    total_vendas: int
    total_faturado: float
    quantidade_motos_vendidas: int

class VendaPorCidade(BaseModel):
    cidade: str
    estado: str
    total_vendas: int
    total_faturado: float
    quantidade_motos_vendidas: int

class VendaPorAnoMes(BaseModel):
    ano_mes: str
    total_vendas: int
    total_faturado: float
    quantidade_motos_vendidas: int
