from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import logging
import os


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parents[2] / 'config' / '.env'
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
# host = 'host.docker.internal'
host = os.getenv('DB_HOST', 'postgres')


def get_engine():
    if not password:
        raise ValueError(
            "A variável 'password' não foi encontrada no arquivo .env!")
    logging.info(f"Conectando em {host}:5432/{database}")
    safe_password = quote_plus(str(password))
    return create_engine(
        f"postgresql+psycopg2://{user}:{safe_password}@{host}:5432/{database}"
    )


engine = get_engine()


def load_weather_data(table_name: str, df):
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False
    )

    logging.info(f"Dados carregados com sucesso!\n")

    df_check = pd.read_sql(f'SELECT * FROM {table_name}', con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}\n")
