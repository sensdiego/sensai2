import streamlit as st
from dotenv import load_dotenv
import os

# ─── Carrega variáveis do .env ───────────────────────────────────────────────
load_dotenv()

# ─── Imports dos agentes ────────────────────────────────────────────────────
from agents.load_cartola_csv import fetch_all_cartola_csvs
from agents.analyze_data     import compute_player_metrics
from agents.strategy_agent   import generate_strategy
from agents.team_builder     import build_optimal_team

def main():
    st.title("Cartola FC Analytics")
    st.write("É os guri não tem jeito.")

    # ─── Inputs do usuário ─────────────────────────────────────────────────
    budget    = st.number_input("Orçamento (R$)", min_value=0.0, value=150.0, step=0.5)
    formation = st.text_input("Formação D-M-A (ex: 4-3-3)", value="4-3-3")

    # ─── Parse da formação D-M-A ───────────────────────────────────────────
    try:
        parts = list(map(int, formation.split("-")))
        formation_dict = {"D": parts[0], "M": parts[1], "A": parts[2]}
    except Exception:
        st.error("Formação inválida. Use o formato 'D-M-A', ex: '4-3-3'.")
        return

    # ─── Pipeline de dados ───────────────────────────────────────────────────
    cartola_df  = fetch_all_cartola_csvs()
    metrics_df  = compute_player_metrics(cartola_df)

    # ─── Estratégia baseada em LLM ───────────────────────────────────────────
    strategy = generate_strategy(metrics_df, budget, formation)
    st.subheader("🔍 Estratégia")
    st.markdown(strategy)

    # ─── Montagem do time D-M-A ─────────────────────────────────────────────
    team_df = build_optimal_team(metrics_df, budget, formation_dict)

    # ─── Renomeia coluna de nome para exibição ─────────────────────────────
    if "atletas.apelido" in team_df.columns:
        team_df = team_df.rename(columns={"atletas.apelido": "player_name"})
    elif "atletas.nome" in team_df.columns:
        team_df = team_df.rename(columns={"atletas.nome": "player_name"})
    else:
        # fallback para exibir algo, se não houver coluna de nome
        team_df["player_name"] = team_df["player_id"].astype(str)

    # ─── Exibição da tabela com nome em vez de ID ─────────────────────────
    st.subheader("⚽ Escalação D-M-A")
    st.table(team_df[["player_name", "position", "price", "cost_benefit"]])

if __name__ == "__main__":
    main()
