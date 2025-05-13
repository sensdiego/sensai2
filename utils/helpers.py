import pandas as pd
import os

def save_df(df: pd.DataFrame, path: str, filename: str):
    """
    Salva o DataFrame em CSV dentro de data/processed.

    :param df: DataFrame a salvar
    :param path: subpasta em data/processed (ex: 'players')
    :param filename: nome do arquivo (ex: 'metrics.csv')
    """
    full_path = os.path.join("data", "processed", path)
    os.makedirs(full_path, exist_ok=True)
    df.to_csv(os.path.join(full_path, filename), index=False)
