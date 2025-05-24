import streamlit as st
import pandas as pd
import numpy as np # Mantido caso precise para algo futuro, mas não para carregar dados
import requests
import plotly.express as px
import seaborn as sns # Mantido caso precise para algo futuro, mas plotly é preferido no Streamlit
import matplotlib.pyplot as plt # Mantido caso precise para algo futuro, mas plotly é preferido no Streamlit

# --- Carregar Dados Reais ---
# Certifique-se de que o arquivo 'dados_funcionarios.csv' está na pasta 'static'
try:
    df = pd.read_csv("static/dados_funcionarios.csv", sep=";", encoding="utf-8")
    st.success("Dados de funcionários carregados com sucesso!")
    
    # Limpeza de dados (se necessário, replique do seu turnover.py)
    # df.dropna(inplace=True)
    # df["idade"] = df["idade"].astype(int)

except FileNotFoundError:
    st.error("Erro: O arquivo 'static/dados_funcionarios.csv' não foi encontrado. Verifique o caminho.")
    st.stop() # Para o script se o arquivo não for encontrado
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}. Verifique o formato do CSV.")
    st.stop()

# Título
st.title("Dashboard de Análise de Turnover")

# Visualizações - Agora usando o 'df' carregado do CSV
st.subheader("Distribuição Salarial")
st.write("A distribuição salarial abaixo é baseada nos dados reais carregados de 'dados_funcionarios.csv'.")
fig = px.histogram(df, x="salario", nbins=30, title="Distribuição Salarial")
st.plotly_chart(fig)

st.subheader("Salário vs Avaliação")
st.write("Este gráfico mostra a relação entre salário e avaliação de desempenho, coloridos pela ocorrência de turnover nos dados reais.")
fig2 = px.scatter(df, x="avaliacao", y="salario", color="turnover", title="Salário vs Avaliação")
st.plotly_chart(fig2)

# Formulário de previsão - Permite testar qualquer valor
st.subheader("Previsão de Turnover")
st.write("Insira os dados de um funcionário para prever a chance de turnover. Você pode usar esta seção para testar diferentes cenários.")

idade = st.number_input("Idade", min_value=int(df['idade'].min()), max_value=int(df['idade'].max()), value=int(df['idade'].mean()))
salario = st.number_input("Salário", min_value=int(df['salario'].min()), max_value=int(df['salario'].max()), value=int(df['salario'].mean()))
tempo = st.number_input("Tempo na Empresa (anos)", min_value=int(df['tempo_empresa'].min()), max_value=int(df['tempo_empresa'].max()), value=int(df['tempo_empresa'].mean()))
avaliacao = st.number_input("Avaliação (1 a 5)", min_value=float(df['avaliacao'].min()), max_value=float(df['avaliacao'].max()), value=float(df['avaliacao'].mean()), step=0.1)


if st.button("Prever"):
    # Payload para a API - usa os valores inseridos pelo usuário
    payload = {
        "idade": idade,
        "salario": salario,
        "tempo_empresa": tempo, # O nome da chave deve ser 'tempo_empresa' para a API
        "avaliacao": avaliacao
    }
    
    try:
        # URL da sua API FastAPI
        # Certifique-se de que esta URL está correta e acessível
        response = requests.post("http://vmlinuxd:8000/predict/", json=payload)
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Chance de Turnover: {result['chance_turnover']}")
        else:
            st.error(f"Erro ao fazer a previsão: Status {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão: Certifique-se de que o backend FastAPI está rodando em 'http://vmlinuxd:8000'.")
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")