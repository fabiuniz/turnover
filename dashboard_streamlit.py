import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar dados
data = {
    "idade": np.random.randint(22, 60, 500),
    "salario": np.random.randint(3000, 20000, 500),
    "tempo_empresa": np.random.randint(1, 15, 500),
    "avaliacao": np.random.uniform(1, 5, 500),
    "turnover": np.random.randint(0, 2, 500)
}
df = pd.DataFrame(data)

# Título
st.title("Dashboard de Análise de Turnover")

# Visualizações
st.subheader("Distribuição Salarial")
fig = px.histogram(df, x="salario", nbins=30, title="Distribuição Salarial")
st.plotly_chart(fig)

st.subheader("Salário vs Avaliação")
fig2 = px.scatter(df, x="avaliacao", y="salario", color="turnover", title="Salário vs Avaliação")
st.plotly_chart(fig2)

# Formulário de previsão
st.subheader("Previsão de Turnover")
idade = st.number_input("Idade", min_value=18, max_value=100, value=35)
salario = st.number_input("Salário", min_value=1000, max_value=50000, value=8500)
tempo = st.number_input("Tempo na Empresa (anos)", min_value=0, max_value=50, value=5)
avaliacao = st.number_input("Avaliação (1 a 5)", min_value=1.0, max_value=5.0, value=4.2, step=0.1)

if st.button("Prever"):
    payload = {"idade": idade, "salario": salario, "tempo_empresa": tempo, "avaliacao": avaliacao}
    response = requests.post("http://vmlinuxd:8000/predict/", json=payload)
    if response.status_code == 200:
        result = response.json()
        st.write(f"Chance de Turnover: {result['chance_turnover']}")
    else:
        st.write("Erro ao fazer a previsão")