import pandas as pd

def build_optimal_team(
    metrics_df: pd.DataFrame,
    budget: float,
    formation: dict
) -> pd.DataFrame:
    """
    Monta a escalação ideal respeitando orçamento e formação.

    Mudanças:
      1. Remove entradas duplicadas de um mesmo jogador, mantendo só
         a linha de maior cost_benefit.
      2. Garante coluna 'position' a partir de 'atletas.posicao_id'.
      3. Seleciona exatamente formation['G'] goleiros, formation['D'] defensores, etc.

    :param metrics_df: DataFrame com colunas
                       ['player_id','price','cost_benefit', …,
                        'atletas.posicao_id' ou 'position']
    :param budget: valor máximo disponível
    :param formation: dict com número de jogadores por posição
                      ex: {"G":1, "D":4, "M":3, "A":3}
    :return: DataFrame com os jogadores selecionados (sem repetir player_id)
    """
    # 0) Copia o DataFrame
    df = metrics_df.copy()

    # 1) Se houver múltiplas linhas por player_id, mantenha a melhor
    df = (
        df
        .sort_values("cost_benefit", ascending=False)
        .drop_duplicates(subset="player_id", keep="first")
    )

    # 2) Garantir coluna 'position'
    if 'position' not in df.columns:
        if 'atletas.posicao_id' in df.columns:
            id_to_sigla = {1: 'G', 2: 'D', 3: 'M', 4: 'A'}
            df['position'] = df['atletas.posicao_id'].map(id_to_sigla)
        else:
            raise KeyError(
                "Nenhuma coluna de posição encontrada "
                "(esperava 'position' ou 'atletas.posicao_id')"
            )

    # 3) Ordena por cost_benefit já foi feito no dedupe, mas útil reforçar para seleção
    sorted_df = df.sort_values("cost_benefit", ascending=False)

    team = []
    remaining_budget = budget

    # 4) Seleciona por posição conforme formação
    for pos, count in formation.items():
        # filtra candidatos daquela posição
        candidates = sorted_df[sorted_df["position"] == pos]
        # escolhe os 'count' primeiros que cabem no orçamento
        picked = []
        for _, player in candidates.iterrows():
            if len(picked) >= count:
                break
            if player["price"] <= remaining_budget:
                picked.append(player)
                remaining_budget -= player["price"]
        team.append(pd.DataFrame(picked))

    # 5) Concatena e retorna
    result = pd.concat(team, ignore_index=True)
    return result
