import pandas as pd

def compute_player_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajusta nomes de colunas e calcula:
      - avg_points: média de pontos por jogador
      - cost_benefit: avg_points / price

    Espera as colunas originais como:
      * atleta_id  ou  player_id
      * pontuacao  ou  pontos  (ou dentro de estatisticas)
      * preco      ou  valor   (ou dentro de estatisticas)
    """
    df = df.copy()

    # 1) Renomear ID do atleta
    if 'atleta_id' in df.columns:
        df.rename(columns={'atleta_id': 'player_id'}, inplace=True)

    # 2) Renomear coluna de pontos
    if 'pontuacao' in df.columns:
        df.rename(columns={'pontuacao': 'points'}, inplace=True)
    elif 'pontos' in df.columns:
        df.rename(columns={'pontos': 'points'}, inplace=True)
    # Se veio como estatisticas.pontos (json_normalize), extraia:
    elif 'estatisticas.pontos' in df.columns:
        df['points'] = df['estatisticas.pontos']

    # 3) Renomear coluna de preço
    if 'preco' in df.columns:
        df.rename(columns={'preco': 'price'}, inplace=True)
    elif 'valor' in df.columns:
        df.rename(columns={'valor': 'price'}, inplace=True)
    elif 'estatisticas.preco' in df.columns:
        df['price'] = df['estatisticas.preco']

    # 4) Verificar colunas obrigatórias
    required = ['player_id', 'points', 'price']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Colunas obrigatórias ausentes: {missing}")

    # 5) Cálculo das métricas
    df['avg_points'] = df.groupby('player_id')['points'].transform('mean')
    df['cost_benefit'] = df['avg_points'] / df['price']

    return df
