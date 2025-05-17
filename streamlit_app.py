import os
import sys

# ─── Ajusta o path para permitir imports de 'agents' ─────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from dotenv import load_dotenv
import pandas as pd

# ─── Carrega variáveis do .env ───────────────────────────────────────────────
load_dotenv()

# ─── Imports dos agentes ────────────────────────────────────────────────────
from agents.load_cartola_csv import fetch_all_cartola_csvs
from agents.analyze_data     import compute_player_metrics
from agents.strategy_agent   import generate_strategy
from agents.team_builder     import build_optimal_team
from agents.fetch_matches    import fetch_next_round_matches, fetch_last_results_by_team

CAMPEONATO_ID = 10  # Brasileirão Série A

def main():
    st.title("Cartola FC Analytics")
    st.write("É os guri não tem jeito.")

    # ─── Inputs do usuário ─────────────────────────────────────────────────
    budget      = st.number_input("Orçamento (R$)", min_value=0.0, value=150.0, step=0.5)
    formation   = st.text_input("Formação D-M-A (ex: 4-3-3)", value="4-3-3")
    round_input = st.number_input("Rodada p/ próximos jogos", min_value=1, max_value=38, value=9, step=1)

    # ─── Parse da formação D-M-A ───────────────────────────────────────────
    try:
        parts = list(map(int, formation.split("-")))
        formation_dict = {"D": parts[0], "M": parts[1], "A": parts[2]}
    except Exception:
        st.error("Formação inválida. Use o formato 'D-M-A', ex: '4-3-3'.")
        return

    # ─── Pipeline de dados ───────────────────────────────────────────────────
    cartola_df = fetch_all_cartola_csvs()
    metrics_df = compute_player_metrics(cartola_df)

    # ─── Estratégia baseada em LLM ───────────────────────────────────────────
    strategy = generate_strategy(metrics_df, budget, formation)
    st.subheader("🔍 Estratégia")
    st.markdown(strategy)

    # ─── Montagem do time D-M-A ─────────────────────────────────────────────
    team_df = build_optimal_team(metrics_df, budget, formation_dict)
    if "atletas.apelido" in team_df.columns:
        team_df = team_df.rename(columns={"atletas.apelido": "player_name"})
    elif "atletas.nome" in team_df.columns:
        team_df = team_df.rename(columns={"atletas.nome": "player_name"})
    else:
        team_df["player_name"] = team_df["player_id"].astype(str)

    st.subheader("⚽ Escalação D-M-A")
    st.table(team_df[["player_name", "position", "price", "cost_benefit"]])

    # ─── Próximos confrontos ─────────────────────────────────────────────────
    upcoming = fetch_next_round_matches(CAMPEONATO_ID, round_input)
    st.subheader(f"📅 Próximos jogos – Rodada {round_input}")
    st.table(upcoming[[
        "time_mandante.nome_popular",
        "time_visitante.nome_popular",
        "data_realizacao",
        "hora_realizacao"
    ]])

    # ─── Últimos resultados ─────────────────────────────────────────────────
    first_round = fetch_next_round_matches(CAMPEONATO_ID, 1)
    teams = pd.concat([
        first_round[["time_mandante.time_id","time_mandante.nome_popular"]]
            .rename(columns={"time_mandante.time_id":"id","time_mandante.nome_popular":"nome"}),
        first_round[["time_visitante.time_id","time_visitante.nome_popular"]]
            .rename(columns={"time_visitante.time_id":"id","time_visitante.nome_popular":"nome"})
    ]).drop_duplicates().set_index("nome")["id"].to_dict()

    team_name = st.selectbox("Time p/ últimos resultados", options=list(teams.keys()))
    results_n = st.number_input("Qtd. resultados", min_value=1, max_value=10, value=5, step=1)
    team_id   = teams[team_name]
    recent    = fetch_last_results_by_team(CAMPEONATO_ID, team_id, num_matches=results_n)

    st.subheader(f"🏆 Últimos resultados – {team_name}")
    st.table(recent[[
        "rodada",
        "time_mandante.nome_popular", "placar_oficial_mandante",
        "time_visitante.nome_popular", "placar_oficial_visitante"
    ]])

if __name__ == "__main__":
    main()
