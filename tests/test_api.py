import httpx

BASE_URL = "http://localhost:8000"

endpoints = {
    "modalidade": "/vendas/modalidade",
    "cidade": "/vendas/cidade",
    "ano_mes": "/vendas/ano-mes"
}

for nome, rota in endpoints.items():
    try:
        response = httpx.get(BASE_URL + rota)
        print(f"\n✅ Endpoint: {rota}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"\n❌ Erro ao acessar {rota}: {e}")
