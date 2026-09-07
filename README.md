# 🌤️ Weather ETL Pipeline — São Paulo

Pipeline ETL automatizado para coleta, transformação e armazenamento de dados meteorológicos em tempo real da cidade de São Paulo, orquestrado via Apache Airflow.

---

## 🛠️ Stack Tecnológica

### Core
* **Python 3.14+** — Linguagem principal
* **Apache Airflow 3.1.7** — Orquestração do pipeline
* **PostgreSQL 14** — Banco de dados relacional
* **Docker & Docker Compose** — Containerização do ambiente

### Bibliotecas Python
* **pandas** — Manipulação e transformação de dados
* **requests** — Requisições HTTP para a API
* **SQLAlchemy** — ORM para interação com o banco de dados
* **psycopg2** — Driver PostgreSQL
* **python-dotenv** — Gerenciamento de variáveis de ambiente

### Outras Ferramentas
* **Redis** — Message broker para Celery
* **Jupyter Notebook** — Análise exploratória de dados
* **UV** — Gerenciador de pacotes Python de alta performance

---

## 🔄 Arquitetura do Pipeline

```text
[ OpenWeather API ] ──(Extract)──> [ weather_data.json ] ──(Transform)──> [ Pandas DataFrame ] ──(Load)──> [ PostgreSQL ]

---
## 🔄 Arquitetura do Pipeline

### 📥 ETAPA 1: EXTRACT
**Arquivo:** `src/extract_data.py`

* Faz uma requisição HTTP GET para a API do OpenWeatherMap.
* Valida o status code da resposta (`200 OK`).
* Salva os dados brutos em formato JSON em `data/weather_data.json`.

**Métricas Coletadas:**
* Temperatura atual, mínima, máxima e sensação térmica
* Umidade e pressão atmosférica
* Velocidade e direção do vento
* Cobertura de nuvens
* Horários de nascer e pôr do sol
* Coordenadas geográficas

---

### 🔄 ETAPA 2: TRANSFORM
**Arquivo:** `src/transform_data.py`

* **Criação do DataFrame:** Lê o JSON bruto e o converte utilizando `pd.json_normalize()`.
* **Normalização de Estruturas Aninhadas:** Extrai os campos `weather_id`, `weather_main` e `weather_description` do objeto `weather`.
* **Limpeza de Dados:** Remove colunas desnecessárias (`weather`, `weather_icon`, `sys.type`).
* **Padronização:** Renomeia as colunas para padrão técnico em inglês (ex: `main.temp` $\rightarrow$ `temperature`, `coord.lon` $\rightarrow$ `longitude`).
* **Tratamento Temporal:** Converte timestamps Unix para `datetime` com o fuso horário de São Paulo (`America/Sao_Paulo`):

```python
df[col] = pd.to_datetime(df[col], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
---

# 💾 ETAPA 3: LOAD

Arquivo: `src/load_data.py`

---

## 📌 O que faz

### 3.1 Conexão com o banco de dados
Estabelece a conexão com o PostgreSQL via SQLAlchemy utilizando o driver **psycopg2**:

```python
engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@{host}:5432/{database}"
)

3.2 Inserção dos dados
Insere o DataFrame limpo na tabela sp_weather em modo append:
df.to_sql(
    name='sp_weather',
    con=engine,
    if_exists='append',  # Adiciona novos registros
    index=False
)
3.3 Validação
Executa um SELECT COUNT(*) para verificar o total de registros

Loga o resultado para auditoria







Projeto desenvolvido com base no tutorial e repositório da [@vbluuiza](https://github.com/vbluuiza/pipeline_etl_weather_data_tutorial_youtube).
