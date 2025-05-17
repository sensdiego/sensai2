# agents/fetch_matches.py

import re
import pandas as pd
from agents.fetch_data import fetch_raw_data

def fetch_next_round_matches(campeonato_id: int, next_round: int) -> pd.DataFrame:
    """
    Retorna um DataFrame com todos os jogos da rodada `next_round`
    do campeonato `campeonato_id`.
    """
    df = fetch_raw_data(f"campeonatos/{campeonato_id}/partidas")
    col = f"partidas.fase-unica.{next_round}a-rodada"
    if col not in df.columns:
        raise KeyError(f"Coluna esperada não encontrada: {col}")
    jogos = df[col].iloc[0]  # lista de dicts
    return pd.json_normalize(jogos)


def fetch_last_results_by_team(
    campeonato_id: int,
    team_id: int,
    num_matches: int = 5
) -> pd.DataFrame:
    """
    Retorna um DataFrame com as últimas `num_matches` partidas
    de um time específico, incluindo os gols oficiais.
    """

    # 1) Puxa todas as rodadas (cronograma completo)
    df = fetch_raw_data(f"campeonatos/{campeonato_id}/partidas")

    # 2) Identifica colunas de rodada
    rodada_cols = [
        c for c in df.columns
        if c.startswith("partidas.fase-unica.") and c.endswith("a-rodada")
    ]
    if not rodada_cols:
        raise KeyError("Nenhuma coluna de rodada encontrada no DataFrame.")

    # 3) Flatten de todas as rodadas num DF único
    all_games = []
    for col in rodada_cols:
        m = re.search(r"(\d+)a-rodada$", col)
        rodada = int(m.group(1)) if m else None
        jogos = df[col].iloc[0]        # lista de dicts
        temp = pd.json_normalize(jogos)
        temp["rodada"] = rodada
        all_games.append(temp)
    all_games_df = pd.concat(all_games, ignore_index=True)

    # 4) Filtra só os jogos do time (mandante ou visitante)
    home_col = "time_mandante.time_id"
    away_col = "time_visitante.time_id"
    mask = (
        all_games_df.get(home_col) == team_id
    ) | (
        all_games_df.get(away_col) == team_id
    )
    schedule_games = all_games_df[mask].sort_values("rodada", ascending=False)

    # 5) Para cada partida, busca o placar via detalhes e só registra
    results = []
    for _, row in schedule_games.iterrows():
        if len(results) >= num_matches:
            break
        pid = row["partida_id"]
        detail = fetch_raw_data(f"partidas/{pid}")
        cols = detail.columns.tolist()

        # detecta dinamicamente os campos de placar
        mand_col = next((c for c in cols if "mandante" in c.lower() and "placar" in c.lower()), None)
        vis_col  = next((c for c in cols if "visitante" in c.lower() and "placar" in c.lower()), None)
        if not mand_col or not vis_col:
            continue  # pula se não houver placar

        home_goals = detail[mand_col].iloc[0]
        # se for None/NaN, significa jogo ainda não ocorreu
        if pd.isna(home_goals):
            continue

        away_goals = detail[vis_col].iloc[0]
        # monta o dict de saída, mantendo colunas originais + placares
        data = row.to_dict()
        data["placar_oficial_mandante"]   = home_goals
        data["placar_oficial_visitante"]  = away_goals
        results.append(data)

    # 6) Constrói o DataFrame final
    if not results:
        # se nenhuma partida retornou placar, retorna vazio mas com colunas previstas
        cols = list(schedule_games.columns) + ["placar_oficial_mandante", "placar_oficial_visitante"]
        return pd.DataFrame(columns=cols)

    return pd.DataFrame(results).reset_index(drop=True)
