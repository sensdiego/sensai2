import pandas as pd

def build_optimal_team(metrics_df: pd.DataFrame, budget: float, formation: dict) -> pd.DataFrame:
    """
    Monta a escalação ideal via método heurístico simples.

    :param metrics_df: DataFrame com colunas de métricas e posições
    :param budget: valor máximo disponível
    :param formation: dict com número de jogadores por posição
                      ex: {"G":1, "D":4, "M":3, "A":3}
    :return: DataFrame com os jogadores selecionados
    """
    # Ordena por custo-benefício
    sorted_df = metrics_df.sort_values("cost_benefit", ascending=False)
    team = []
    remaining_budget = budget

    for pos, count in formation.items():
        candidates = sorted_df[sorted_df["position"] == pos]
        selected = candidates[candidates["price"] <= remaining_budget].head(count)
        team.append(selected)
        remaining_budget -= selected["price"].sum()

    return pd.concat(team).reset_index(drop=True)
