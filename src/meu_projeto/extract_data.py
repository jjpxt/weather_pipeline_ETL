from pathlib import Path
import requests
import logging
import json

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def extract_weather_data(url: str) -> dict:
    response = requests.get(url)

    if response.status_code != 200:
        logging.error(f"Erro na requisição: {response.status_code}")
        return {}

    data = response.json()

    if not data:
        logging.warning("Nenhum dado retornado")
        return {}

    output_path = Path('/opt/airflow/data/weather_data.json')
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logging.info(f'Arquivo salvo com sucesso em {output_path}')
    return data
