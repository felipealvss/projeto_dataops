from fastapi import APIRouter
from fastapi_app.database import get_connection
from fastapi_app.models import VendaPorAnoMes

router = APIRouter()

@router.get("/vendas/ano-mes", response_model=list[VendaPorAnoMes])
def get_vendas_ano_mes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendas_por_ano_mes")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        VendaPorAnoMes(
            ano_mes=row[0],
            total_vendas=row[1],
            total_faturado=row[2],
            quantidade_motos_vendidas=row[3],
        )
        for row in rows
    ]
