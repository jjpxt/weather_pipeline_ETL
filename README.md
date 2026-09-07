# 🌤️ Weather ETL Pipeline — São Paulo

Pipeline ETL automatizado para coleta, transformação e armazenamento de dados meteorológicos em tempo real da cidade de São Paulo, orquestrado via **Apache Airflow**.

---

## 🛠️ Stack Tecnológica

### Core
- **Python 3.14+** — Linguagem principal
- **Apache Airflow 3.1.7** — Orquestração do pipeline
- **PostgreSQL 14** — Banco de dados relacional
- **Docker & Docker Compose** — Containerização do ambiente

### Bibliotecas Python
- **pandas** — Manipulação e transformação de dados
- **requests** — Requisições HTTP para a API
- **SQLAlchemy** — ORM para interação com o banco de dados
- **psycopg2** — Driver PostgreSQL
- **python-dotenv** — Gerenciamento de variáveis de ambiente

### Outras Ferramentas
- **Redis** — Message broker para Celery
- **Jupyter Notebook** — Análise exploratória de dados
- **UV** — Gerenciador de pacotes Python de alta performance

---

## 🔄 Arquitetura do Pipeline

```text
[ OpenWeather API ] ──(Extract)──> [ weather_data.json ] ──(Transform)──> [ Pandas DataFrame ] ──(Load)──> [ PostgreSQL ]

# 📥 ETAPA 1: EXTRACT

**Arquivo:** `src/extract_data.py`

---

## 📌 O que faz

- Faz uma requisição **HTTP GET** para a API do **OpenWeatherMap**  
- Valida o status code da resposta (`200 OK`)  
- Salva os dados brutos em formato **JSON** em `data/weather_data.json`  

---

## 🌡️ Métricas Coletadas

- Temperatura atual, mínima, máxima e sensação térmica  
- Umidade e pressão atmosférica  
- Velocidade e direção do vento  
- Cobertura de nuvens  
- Horários de nascer e pôr do sol  
- Coordenadas geográficas  

---
# 🧮 ETAPA 2: TRANSFORM

**Arquivo:** `src/transform_data.py`

---

## 📌 O que faz

### 2.1 Criação do DataFrame
- Lê o arquivo JSON  
- Converte para DataFrame Pandas  
- Normaliza dados aninhados usando `pd.json_normalize()`  

### 2.2 Normalização da coluna `weather`
- A coluna `weather` vem como lista de dicionários  
- Extrai: `weather_id`, `weather_main`, `weather_description`, `weather_icon`  
- Concatena com o DataFrame principal  

### 2.3 Remoção de colunas desnecessárias
```python
columns_to_drop = ['weather', 'weather_icon', 'sys.type']


# 💾 ETAPA 3: LOAD

**Arquivo:** `src/load_data.py`

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

# 🌀 Fluxo da DAG no Airflow

**Arquivo:** `dags/weather_dag.py`

---

## 📌 Configuração da DAG

```python
@dag(
    dag_id='youtube_weather_pipeline',
    schedule='0 */1 * * *',  # Executa a cada 1 hora
    start_date=datetime(2020, 2, 7),
    catchup=False,  # Não executa datas passadas
    tags=['weather', 'etl', 'se inscreve no canal!']
)
📥 Tasks Definidas

@task
def extract():
    extract_weather_data(url)

@task
def transform():
    df = data_transformations()
    df.to_parquet('/opt/airflow/data/temp_data.parquet')

@task
def load():
    df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
    load_weather_data('sp_weather', df)

# Dependências
extract() >> transform() >> load()

