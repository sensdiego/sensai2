import os
import glob
import pandas as pd

def fetch_all_cartola_csvs(dir_path: str = None) -> pd.DataFrame:
    base    = dir_path or os.path.join("data", "raw", "cartola", "rodadas")
    pattern = os.path.join(base, "rodada_*.csv")
    files   = sorted(glob.glob(pattern))
    if not files:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {base}")

    all_dfs = []
    for file in files:
        # pular arquivos vazios
        if os.path.getsize(file) == 0:
            print(f"Atenção: pulando CSV vazio → {file}")
            continue

        try:
            df = pd.read_csv(file)
        except pd.errors.EmptyDataError:
            print(f"Atenção: pandas não conseguiu ler (vazio?) → {file}")
            continue

        # remova colunas irrelevantes
        df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")

        # renomeie colunas principais
        mapping = {}
        if "atletas.atleta_id" in df:   mapping["atletas.atleta_id"] = "player_id"
        if "atletas.preco_num"   in df: mapping["atletas.preco_num"]   = "price"
        if "atletas.pontos_num"  in df: mapping["atletas.pontos_num"]  = "points"
        if "atletas.rodada_id"   in df: mapping["atletas.rodada_id"]   = "rodada"

        df.rename(columns=mapping, inplace=True)

        # converter tipos numéricos
        for col in ("price", "points", "rodada"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        all_dfs.append(df)

    if not all_dfs:
        raise RuntimeError("Todos os CSVs estavam vazios ou ilegíveis.")

    return pd.concat(all_dfs, ignore_index=True)
