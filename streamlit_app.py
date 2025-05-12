import streamlit as st

st.title("Cartola")
st.write(
    "É os guri não tem jeito.)."
)
from dotenv import load_dotenv
import os

load_dotenv()  # lê sensai2/.env

API_FUTEBOL_KEY = os.getenv("API_FUTEBOL_KEY")
OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY")
