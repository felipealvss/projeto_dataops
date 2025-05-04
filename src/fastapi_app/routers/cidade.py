from fastapi import APIRouter
from fastapi_app.database import get_connection
from fastapi_app.models import VendaPorCidade

router = APIRouter()

@router.get("/vendas/cidade", response_model=list[VendaPorCidade])
def get_vendas_cidade():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendas_por_cidade")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        VendaPorCidade(
            cidade=row[0],
            estado=row[1],
            total_vendas=row[2],
            total_faturado=row[3],
            quantidade_motos_vendidas=row[4],
        )
        for row in rows
    ]
