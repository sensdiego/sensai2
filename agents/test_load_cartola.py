# test_load_cartola.py

from agents.load_cartola_csv import fetch_all_cartola_csvs

def main():
    df = fetch_all_cartola_csvs()
    print("Total de registros:", len(df))
    print("Colunas encontradas:", df.columns.tolist())
    print(df[["player_id","rodada","price","points"]].head())

if __name__ == "__main__":
    main()
