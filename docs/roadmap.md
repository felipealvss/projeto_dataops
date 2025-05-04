
## 📌 **Roadmap Técnico – Projeto DataOps Unifor**

### 🔧 1. **Configuração do Ambiente Base**

* **Objetivo**: Preparar o ambiente de desenvolvimento e execução utilizando contêineres.
* **Ações**:

  * Configurar o `docker-compose.yaml` utilizando a imagem oficial do Airflow com CeleryExecutor.
  * Definir serviços para: Airflow (webserver, scheduler, workers), PostgreSQL, FastAPI, e Streamlit.
  * Incluir variáveis no `.env` com URIs, credenciais e caminhos utilizados pelos serviços.
* **Diretórios envolvidos**: `docker`, `.env`, `docker-compose.yaml`, `README.md`.

---

### 🗂️ 2. **Organização da Estrutura do Projeto**

* **Objetivo**: Manter a modularidade e escalabilidade do sistema.
* **Ações**:

  * Estruturar os diretórios conforme seu modelo (ex: `src/`, `dags/`, `config/`, `plugins/`, `tests/`, `docs/`).
  * Usar `pyproject.toml` e `poetry.lock` para o controle de dependências no projeto como um todo.
* **Diretórios envolvidos**: Toda a arquitetura definida.

---

### 📅 3. **Orquestração com Airflow**

* **Objetivo**: Automatizar a geração, transformação e carga de dados.
* **Ações**:

  * Criar a DAG `dag_gerar_dados.py` para gerar e enviar dados simulados para o **MongoDB Atlas**.
  * Implementar as DAGs:

    * `dag_vendas_ano_mes.py`
    * `dag_vendas_estado.py`
    * `dag_vendas_modalidade.py`

    > Todas se conectam ao MongoDB Atlas, realizam transformações específicas e carregam os dados em tabelas PostgreSQL.
* **Diretórios envolvidos**: `dags/`, `config/`, `plugins/`.

---

### 🧩 4. **Modelagem e Acesso aos Dados**

* **Objetivo**: Estruturar e disponibilizar os dados transformados via API.
* **Ações**:

  * Modelar tabelas no PostgreSQL de acordo com os formatos de saída das DAGs.
  * Desenvolver rotas no FastAPI que consultam cada uma dessas tabelas e retornam dados em JSON.
  * Configurar container para o FastAPI dentro de `src/fastapi_app`.
* **Diretórios envolvidos**: `src/fastapi_app`, `docker/`, `tests/`.

---

### 📊 5. **Visualização e Monitoramento com Streamlit**

* **Objetivo**: Permitir a visualização dos dados em tempo real.
* **Ações**:

  * Criar uma interface no `dashboard.py` que consuma:

    * As coleções originais no MongoDB Atlas.
    * As rotas do FastAPI conectadas ao PostgreSQL.
  * Atualizar o dashboard com refresh automático a cada minuto.
  * Manter código em `src/streamlit_dashboard`.
* **Diretórios envolvidos**: `src/streamlit_dashboard`, `docker/`.

---

### 🧪 6. **Testes e Validação**

* **Objetivo**: Garantir a robustez e a qualidade do pipeline.
* **Ações**:

  * Escrever testes unitários para funções críticas (transformações, API).
  * Validar DAGs no Airflow.
  * Garantir que todos os containers iniciem corretamente com `docker-compose up`.
* **Diretórios envolvidos**: `tests/`, `logs/`.

---

### 📚 7. **Documentação e Manutenção**

* **Objetivo**: Garantir a compreensão e continuidade do projeto.
* **Ações**:

  * Documentar o funcionamento das DAGs, API e Streamlit em `docs/`.
  * Atualizar o `README.md` com instruções de uso, variáveis e endpoints.
  * Registrar o roadmap técnico em `docs/roadmap.md`.

---

## 💡 Estratégias e Insights

* **Separação de responsabilidades**: Cada serviço (Airflow, DB, API, Dashboard) é isolado e independente, facilitando o monitoramento e manutenção.
* **Escalabilidade**: O uso do CeleryExecutor no Airflow permite escalar workers conforme a carga.
* **Padronização**: O uso do Poetry e da arquitetura modular garante controle sobre dependências e manutenção do projeto.
* **Observabilidade**: Com Streamlit acessando dados brutos e transformados, é possível validar a integridade dos dados de ponta a ponta.

---
