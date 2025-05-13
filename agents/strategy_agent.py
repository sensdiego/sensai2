import os
from dotenv import load_dotenv
from langchain import OpenAI, LLMChain, PromptTemplate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

template = """
Você é um analista tático para Cartola FC.
Com base nos dados agregados, sugira critérios de escolha e justifique.
Dados: {metrics}
Regras: orçamento máximo {budget}, esquema tático {formation}
"""
prompt = PromptTemplate(input_variables=["metrics", "budget", "formation"], template=template)
llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.7)
strategy_chain = LLMChain(llm=llm, prompt=prompt)

def generate_strategy(
    metrics_df,
    budget: float,
    formation: str
) -> str:
    """
    Retorna uma estratégia textual para montagem do time, enviando ao GPT
    apenas um resumo estatístico das métricas, para não exceder o limite
    de tokens.

    :param metrics_df: DataFrame com métricas de jogadores (colunas 
                       'player_id', 'points', 'avg_points', 'cost_benefit', etc.)
    :param budget: teto de gastos no Cartola
    :param formation: string com formação (ex: '4-3-3')
    :return: texto com recomendações táticas
    """
    # 1. Calcular resumo estatístico das duas métricas principais
    summary_stats = metrics_df[['avg_points', 'cost_benefit']].describe().to_dict()

    # 2. Transformar em string legível
    #    Exemplo de saída: 
    #    {
    #      'avg_points': {'mean': 4.2, 'std': 1.3, ...},
    #      'cost_benefit': {'mean': 0.35, 'std': 0.12, ...}
    #    }
    metrics_summary = f"Resumo estatístico:\n{summary_stats}"

    # 3. Chamar o LLM apenas com o summary, budget e formation
    return strategy_chain.run(
        metrics=metrics_summary,
        budget=budget,
        formation=formation
    )