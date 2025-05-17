# agents/strategy_agent.py

import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate
from agents.fetch_standings import fetch_standings

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CAMPEONATO_ID   = 10  # ID fixo do Brasileirão Série A

# ─── Prompt template ─────────────────────────────────────────────────────────
template = """
Você é um analista tático para Cartola FC.

– Resumo estatístico dos jogadores (pontos e custo-benefício):
{metrics_summary}

– Classificação atual do campeonato (top {top_n}):
{standings}

Regras:
- Orçamento máximo: R${budget}
- Esquema tático: {formation}

Com base nesses dados, elabore:
1. Critérios de seleção de jogadores (incluindo posição na tabela).
2. Justificativas táticas.
3. Pontos de atenção para as próximas rodadas.
"""
prompt = PromptTemplate(
    input_variables=["metrics_summary", "standings", "budget", "formation", "top_n"],
    template=template
)

# ─── Configura LLM ───────────────────────────────────────────────────────────
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)
strategy_chain = LLMChain(llm=llm, prompt=prompt)


def generate_strategy(
    metrics_df,
    budget: float,
    formation: str,
    top_n: int = 5
) -> str:
    """
    Retorna uma estratégia textual para montagem do time, combinando:
     - Resumo estatístico das métricas dos jogadores.
     - Classificação atual do campeonato (top N posições).
     - Orçamento e formação desejada.

    :param metrics_df: DataFrame com métricas de jogadores
                       (colunas 'avg_points', 'cost_benefit', etc.)
    :param budget: teto de gastos no Cartola
    :param formation: formação tática, ex: '4-3-3'
    :param top_n: quantas posições de tabela incluir no prompt
    :return: texto com recomendações táticas
    """
    # 1) Resumo estatístico
    stats = metrics_df[['avg_points', 'cost_benefit']].describe().to_dict()
    metrics_summary = f"{stats}"

    # 2) Classificação atual (top N)
    standings_df = fetch_standings(CAMPEONATO_ID).head(top_n)
    standings = standings_df.to_json(orient="records")

    # 3) Executa a cadeia LLM
    return strategy_chain.run(
        metrics_summary=metrics_summary,
        standings=standings,
        budget=budget,
        formation=formation,
        top_n=top_n
    )
