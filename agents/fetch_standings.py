# agents/fetch_standings.py

import pandas as pd
from agents.fetch_data import fetch_raw_data

def fetch_standings(campeonato_id: int) -> pd.DataFrame:
    """
    Retorna o DataFrame com a classificação do campeonato:
    posição, time, pontos, jogos, vitórias, empates, derrotas,
    gols pró (gm), gols contra (gc), saldo (sg), últimas5.
    """
    # 1) Busca o JSON bruto
    df = fetch_raw_data(f"campeonatos/{campeonato_id}/classificacao")
    # 2) Normaliza para um DataFrame
    #    Aqui assumimos que `df` já é DataFrame de registros simples.
    #    Caso venha aninhado, use pd.json_normalize(df.to_dict("records"), ...)
    # 3) Renomeia colunas para nossa convenção
    df = df.rename(columns={
        "posição": "posicao",
        "time.time_id": "time_id",
        "time.nome_popular": "time",
        "pontos": "pontos",
        "jogos": "jogos",
        "vitorias": "vitorias",
        "empates": "empates",
        "derrotas": "derrotas",
        "gols_pro": "gm",
        "gols_contra": "gc",
        "saldo_gols": "sg",
        "ultimas": "ultimas5"
    })
    # 4) Seleciona e ordena as colunas que queremos
    return df[[
        "posicao","time","pontos","jogos","vitorias","empates","derrotas",
        "gm","gc","sg","ultimas5"
    ]].sort_values("posicao").reset_index(drop=True)
