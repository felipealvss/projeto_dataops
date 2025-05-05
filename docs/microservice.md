# 🧩 Microserviço FastAPI

## 📌 O que é um Microserviço?

Um **microserviço** é um estilo de arquitetura de software em que um sistema é dividido em pequenas aplicações independentes que se comunicam entre si, geralmente via APIs. Cada microserviço é responsável por uma funcionalidade específica do sistema e pode ser desenvolvido, implantado e escalado de forma independente.

### ✳️ Características principais:

* **Independência**: cada serviço funciona isoladamente.
* **Escalabilidade**: serviços podem ser escalados individualmente.
* **Desenvolvimento Desacoplado**: diferentes times podem trabalhar em diferentes microserviços.
* **Facilidade de Manutenção**: atualizações são feitas localmente sem afetar o sistema todo.
* **Tecnologias Diversas**: cada microserviço pode ser desenvolvido com a linguagem e tecnologia mais adequadas à sua função.

---

## ⚙️ Microserviço no Projeto: FastAPI

No contexto deste projeto, o componente FastAPI é responsável por disponibilizar rotas RESTful para consulta de dados armazenados no banco **PostgreSQL**, que são processados e atualizados pelas DAGs do **Apache Airflow**.

Ele pode ser considerado um microserviço porque:

* Está isolado em seu próprio **container Docker**;
* Expõe uma API específica e bem definida;
* Pode ser escalado ou modificado sem interferir nos outros componentes (Airflow, Streamlit, etc);
* Serve exclusivamente para **consultar e entregar dados**;
* Comunicação com outros serviços é feita via **HTTP requests**.

---

## 📈 Relação com outros Componentes


<img src="docs/images/FasAPIMermaidChart-2025-05-05-05.png" alt="Microserviço"/>

---
