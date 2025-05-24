import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# --- Carregar Dados Reais ou Gerar Aleatórios como Fallback ---
try:
    df = pd.read_csv("static/dados_funcionarios.csv", sep=";", encoding="utf-8")
    print("Dados de funcionários carregados com sucesso de 'static/dados_funcionarios.csv'!")
    data_source_message = "Os gráficos abaixo são baseados nos dados reais carregados de 'dados_funcionarios.csv'."
except FileNotFoundError:
    print("Arquivo 'static/dados_funcionarios.csv' não encontrado. Carregando dados aleatórios para demonstração.")
    data_source_message = "Arquivo 'static/dados_funcionarios.csv' não encontrado. Os gráficos abaixo são baseados em dados aleatórios para demonstração."
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
    print(f"Erro ao carregar dados de 'static/dados_funcionarios.csv': {e}. Carregando dados aleatórios.")
    data_source_message = f"Erro ao carregar dados de 'static/dados_funcionarios.csv': {e}. Os gráficos abaixo são baseados em dados aleatórios para demonstração."
    # Gerar dados aleatórios como fallback em caso de outros erros de carregamento
    data_fallback = {
        "idade": np.random.randint(22, 60, 500),
        "salario": np.random.randint(3000, 20000, 500),
        "tempo_empresa": np.random.randint(1, 15, 500),
        "avaliacao": np.random.uniform(1, 5, 500),
        "turnover": np.random.randint(0, 2, 500)
    }
    df = pd.DataFrame(data_fallback)


# Função para gerar gráficos Matplotlib como imagem base64 (se ainda usar)
def plot_to_base64():
    plt.figure(figsize=(6, 4))
    sns.histplot(df["salario"], kde=True)
    plt.title("Distribuição Salarial")
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")

# Inicializar o app Dash
app = dash.Dash(__name__)

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


# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análise de Turnover"),
    
    # Mensagem sobre a fonte dos dados
    html.P(data_source_message, style={'font-style': 'italic', 'color': '#555'}),

    # Seção de visualizações - Agora usando o 'df' carregado (real ou aleatório)
    html.H2("Visualização dos Dados"),
    html.Div([
        dcc.Graph(
            id="hist-salario",
            figure=px.histogram(df, x="salario", nbins=30, title="Distribuição Salarial")
        ),
        dcc.Graph(
            id="hist-idade",
            figure=px.histogram(df, x="idade", nbins=30, title="Distribuição de Idade")
        ),
        dcc.Graph(
            id="scatter-avaliacao",
            figure=px.scatter(df, x="avaliacao", y="salario", color="turnover", 
                             title="Salário vs Avaliação (Colorido por Turnover)")
        ),
    ], style={"display": "flex", "flexWrap": "wrap"}),
    
    # Seção de métricas do modelo (se o gráfico for gerado de Matplotlib)
    html.H2("Métricas do Modelo"),
    html.Img(id="curva-aprendizado", src=f"data:image/png;base64,{plot_to_base64()}"),
    
    # Seção de previsão - Permite testar qualquer valor
    html.H2("Previsão de Turnover"),
    html.P("Insira os dados de um funcionário para obter uma previsão individual da chance de turnover. Você pode usar esta seção para testar diferentes cenários."),
    html.Div([
        html.Label("Idade:"),
        dcc.Input(id="input-idade", type="number", value=mean_idade, min=min_idade, max=max_idade),
        html.Label("Salário:"),
        dcc.Input(id="input-salario", type="number", value=mean_salario, min=min_salario, max=max_salario),
        html.Label("Tempo na Empresa (anos):"),
        dcc.Input(id="input-tempo", type="number", value=mean_tempo, min=min_tempo, max=max_tempo),
        html.Label("Avaliação (1 a 5):"),
        dcc.Input(id="input-avaliacao", type="number", value=mean_avaliacao, step=0.1, min=min_avaliacao, max=max_avaliacao),
        html.Button("Prever", id="predict-button"),
        html.H3(id="resultado-predicao", children="Aguardando previsão...")
    ])
])

# Callback para atualizar a previsão
@app.callback(
    Output("resultado-predicao", "children"),
    [Input("predict-button", "n_clicks")],
    [
        State("input-idade", "value"),
        State("input-salario", "value"),
        State("input-tempo", "value"),
        State("input-avaliacao", "value")
    ]
)
def update_prediction(n_clicks, idade, salario, tempo, avaliacao):
    if n_clicks is None or n_clicks == 0:
        return "Aguardando previsão..."
    
    if None in (idade, salario, tempo, avaliacao):
        return "Por favor, preencha todos os campos com valores válidos."
    
    try:
        idade = int(idade)
        salario = float(salario)
        tempo = int(tempo)
        avaliacao = float(avaliacao)
    except (ValueError, TypeError):
        return "Erro: Insira valores numéricos válidos."
        
    url = "http://vmlinuxd:8000/predict/"
    payload = {
        "idade": idade,
        "salario": salario,
        "tempo_empresa": tempo,
        "avaliacao": avaliacao
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            return f"Chance de Turnover: {result['chance_turnover']}"
        else:
            return f"Erro ao fazer a previsão: Status {response.status_code} - {response.text}"
    except requests.exceptions.ConnectionError:
        return "Erro de conexão: Certifique-se de que o backend FastAPI está rodando em 'http://vmlinuxd:8000'."
    except Exception as e:
        return f"Ocorreu um erro inesperado: {e}"

# Rodar o servidor Dash
if __name__ == "__main__":    
    app.run(debug=True, port=8050, host='0.0.0.0')