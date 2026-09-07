from datetime import datetime, timedelta
from pathlib import Path
import os

from airflow.decorators import dag, task  # type: ignore
from dotenv import load_dotenv

from src.meu_projeto.extract_data import extract_weather_data
from src.meu_projeto.load_data import load_weather_data
from src.meu_projeto.transform_data import data_transformations

ROOT_PATH = Path(__file__).resolve().parent.parent
env_path = ROOT_PATH / 'config' / '.env'
load_dotenv(env_path)

API_KEY = os.getenv('API_KEY')
url = f'https://api.openweathermap.org/data/2.5/weather?q=Sao Paulo,BR&units=metric&appid={API_KEY}'


@dag(
    dag_id='youtube_weather_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Clima SP',
    schedule='0 */1 * * *',
    start_date=datetime(2026, 2, 7),
    catchup=False,
    tags=['weather', 'etl', 'se inscreve no canal!']
)
def weather_pipeline():

    @task
    def extract():
        extract_weather_data(url)
        return True

    @task
    def transform(setup_done: bool):
        df = data_transformations()
        file_path = '/opt/airflow/data/temp_data.parquet'
        df.to_parquet(file_path, index=False)
        return file_path

    @task
    def load(file_path: str):
        import pandas as pd
        df = pd.read_parquet(file_path)
        load_weather_data('sp_weather', df)

    status_extract = extract()
    path_parquet = transform(status_extract)
    load(path_parquet)


weather_pipeline()
