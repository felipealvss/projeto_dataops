from fastapi import APIRouter
from fastapi_app.database import get_connection
from fastapi_app.models import VendaPorModalidade

router = APIRouter()

@router.get("/vendas/modalidade", response_model=list[VendaPorModalidade])
def get_vendas_modalidade():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendas_por_modalidade")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        VendaPorModalidade(
            modalidade=row[0],
            total_vendas=row[1],
            total_faturado=row[2],
            quantidade_motos_vendidas=row[3],
        )
        for row in rows
    ]
