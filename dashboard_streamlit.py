import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# --- Carregar Dados Reais ou Gerar Aleatórios como Fallback ---
try:
    df = pd.read_csv("static/dados_funcionarios.csv", sep=";", encoding="utf-8")
    st.success("Dados de funcionários carregados com sucesso de 'static/dados_funcionarios.csv'!")

except FileNotFoundError:
    st.warning("Arquivo 'static/dados_funcionarios.csv' não encontrado. Carregando dados aleatórios para demonstração.")
    # Gerar dados aleatórios como fallback
    data_fallback = {
        "idade": np.random.randint(22, 60, 500),
        "salario": np.random.randint(3000, 20000, 500), # Ajuste o max_value se quiser salários maiores no fallback
        "tempo_empresa": np.random.randint(1, 15, 500),
        "avaliacao": np.random.uniform(1, 5, 500),
        "turnover": np.random.randint(0, 2, 500)
    }
    df = pd.DataFrame(data_fallback)
except Exception as e:
    st.error(f"Erro ao carregar dados de 'static/dados_funcionarios.csv': {e}. Carregando dados aleatórios.")
    # Gerar dados aleatórios como fallback em caso de outros erros de carregamento
    data_fallback = {
        "idade": np.random.randint(22, 60, 500),
        "salario": np.random.randint(3000, 20000, 500),
        "tempo_empresa": np.random.randint(1, 15, 500),
        "avaliacao": np.random.uniform(1, 5, 500),
        "turnover": np.random.randint(0, 2, 500)
    }
    df = pd.DataFrame(data_fallback)

# Título
st.title("Dashboard de Análise de Turnover")

# Visualizações - Agora usando o 'df' carregado (real ou aleatório)
st.subheader("Distribuição Salarial")
st.write("A distribuição salarial abaixo é baseada nos dados carregados.")
fig = px.histogram(df, x="salario", nbins=30, title="Distribuição Salarial")
st.plotly_chart(fig)

st.subheader("Salário vs Avaliação")
st.write("Este gráfico mostra a relação entre salário e avaliação de desempenho, coloridos pela ocorrência de turnover.")
fig2 = px.scatter(df, x="avaliacao", y="salario", color="turnover", title="Salário vs Avaliação")
st.plotly_chart(fig2)

# Formulário de previsão - Permite testar qualquer valor
st.subheader("Previsão de Turnover")
st.write("Insira os dados de um funcionário para prever a chance de turnover. Você pode usar esta seção para testar diferentes cenários.")

# Define valores padrão e limites com base no DataFrame carregado (real ou aleatório)
min_idade = int(df['idade'].min()) if not df.empty else 18
max_idade = int(df['idade'].max()) if not df.empty else 100
mean_idade = int(df['idade'].mean()) if not df.empty else 35

min_salario = int(df['salario'].min()) if not df.empty else 1000
max_salario = int(df['salario'].max()) if not df.empty else 50000
mean_salario = int(df['salario'].mean()) if not df.empty else 8500

min_tempo = int(df['tempo_empresa'].min()) if not df.empty else 0
max_tempo = int(df['tempo_empresa'].max()) if not df.empty else 50
mean_tempo = int(df['tempo_empresa'].mean()) if not df.empty else 5

min_avaliacao = float(df['avaliacao'].min()) if not df.empty else 1.0
max_avaliacao = float(df['avaliacao'].max()) if not df.empty else 5.0
mean_avaliacao = float(df['avaliacao'].mean()) if not df.empty else 4.2


idade = st.number_input("Idade", min_value=min_idade, max_value=max_idade, value=mean_idade)
salario = st.number_input("Salário", min_value=min_salario, max_value=max_salario, value=mean_salario)
tempo = st.number_input("Tempo na Empresa (anos)", min_value=min_tempo, max_value=max_tempo, value=mean_tempo)
avaliacao = st.number_input("Avaliação (1 a 5)", min_value=min_avaliacao, max_value=max_avaliacao, value=mean_avaliacao, step=0.1)


if st.button("Prever"):
    payload = {
        "idade": idade,
        "salario": salario,
        "tempo_empresa": tempo,
        "avaliacao": avaliacao
    }
    
    try:
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
