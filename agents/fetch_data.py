import os
import requests
import pandas as pd
from dotenv import load_dotenv, find_dotenv

# Carrega variáveis do .env na raiz do sensai2
load_dotenv(find_dotenv())

API_FUTEBOL_KEY = os.getenv("API_FUTEBOL_KEY")
BASE_URL = "https://api.api-futebol.com.br/v1"

def fetch_raw_data(endpoint: str, params: dict = None) -> pd.DataFrame:
    """
    Busca dados brutos da API Futebol e retorna um DataFrame.

    :param endpoint: caminho do recurso sem barras extras,
                     ex: "atletas/564" ou "partidas/1234"
    :param params: dicionário de parâmetros de query
    :return: pandas.DataFrame com os dados normalizados
    """
    # Garante apenas um slash entre BASE_URL e endpoint
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"
    headers = {"Authorization": f"Bearer {API_FUTEBOL_KEY}"}

    try:
        response = requests.get(url, headers=headers, params=params or {})
        response.raise_for_status()
    except requests.HTTPError as http_err:
        # Exibe status e corpo da resposta para debug
        raise RuntimeError(f"HTTP {response.status_code} – {response.text}") from http_err
    except requests.RequestException as req_err:
        raise RuntimeError(f"Falha na requisição: {req_err}") from req_err

    data = response.json()
    # Ajuste aqui caso o JSON retorne um nível extra, ex: data["atletas"]
    df = pd.json_normalize(data)
    return df
