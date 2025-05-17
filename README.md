# sensai2 – análise Cartola FC

Este projeto fornece uma série de agentes para coletar e analisar dados do Cartola FC e montar times automaticamente.

## Requisitos

- Python 3.11 ou superior

## Instalação

```bash
pip install -r requirements.txt
```

É recomendável utilizar um ambiente virtual (venv, conda etc.).

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do repositório contendo:

```
API_FUTEBOL_KEY=chave_da_api
OPENAI_API_KEY=chave_openai
```

Estas chaves são utilizadas respectivamente para acessar a API Futebol e o modelo da OpenAI.

## Executando o Streamlit

Após instalar as dependências e definir as variáveis de ambiente, execute:

```bash
streamlit run streamlit_app.py
```

A aplicação será iniciada em `http://localhost:8501/`.