import streamlit as st
from dotenv import load_dotenv
import os

from agents.fetch_data import fetch_raw_data
from agents.analyze_data import compute_player_metrics
from agents.strategy_agent import generate_strategy
from agents.team_builder import build_optimal_team
from utils.helpers import save_df

load_dotenv()

def main():
    st.title("SENSAI2 – Análise Cartola FC")

    # Parâmetros da rodada
    budget = st.number_input("Orçamento", value=100.0)
    formation_input = st.text_input("Formação (ex: 4-3-3)", value="4-3-3")
    formation = dict(zip(["G","D","M","A"], map(int, formation_input.split("-"))))

    # 1. Ingestão
    raw_df = fetch_raw_data("/v1/players", params={"round": 1})
    st.write("Dados brutos:", raw_df.head())

    # 2. Análise
    metrics_df = compute_player_metrics(raw_df)
    st.write("Métricas:", metrics_df.head())

    # 3. Estratégia
    strategy = generate_strategy(metrics_df, budget, formation_input)
    st.markdown("**Estratégia:**\n\n" + strategy)

    # 4. Escalação
    team_df = build_optimal_team(metrics_df, budget, formation)
    st.write("Escalação sugerida:", team_df)

    # 5. Salvar resultados
    if st.button("Salvar Métricas"):
        save_df(metrics_df, "players", "metrics.csv")
        st.success("Métricas salvas em data/processed/players/metrics.csv")

if __name__ == "__main__":
    main()
