import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import requests
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Carregar os dados (mesmo dataset do seu código)
data = {
    "idade": np.random.randint(22, 60, 500),
    "salario": np.random.randint(3000, 20000, 500),
    "tempo_empresa": np.random.randint(1, 15, 500),
    "avaliacao": np.random.uniform(1, 5, 500),
    "turnover": np.random.randint(0, 2, 500)
}
df = pd.DataFrame(data)

# Função para gerar gráficos Matplotlib como imagem base64
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

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análise de Turnover"),
    
    # Seção de visualizações
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
    
    # Seção de métricas do modelo
    html.H2("Métricas do Modelo"),
    html.Img(id="curva-aprendizado", src=f"data:image/png;base64,{plot_to_base64()}"),
    
    # Seção de previsão
    html.H2("Previsão de Turnover"),
    html.Div([
        html.Label("Idade:"),
        dcc.Input(id="input-idade", type="number", value=35),
        html.Label("Salário:"),
        dcc.Input(id="input-salario", type="number", value=8500),
        html.Label("Tempo na Empresa (anos):"),
        dcc.Input(id="input-tempo", type="number", value=5),
        html.Label("Avaliação (1 a 5):"),
        dcc.Input(id="input-avaliacao", type="number", value=4.2, step=0.1),
        html.Button("Prever", id="predict-button"),
        html.H3(id="resultado-predicao", children="Aguardando previsão...")
    ])
])

# Callback para atualizar a previsão
@app.callback(
    Output("resultado-predicao", "children"),
    [Input("predict-button", "n_clicks")],
    [
        Input("input-idade", "value"),
        Input("input-salario", "value"),
        Input("input-tempo", "value"),
        Input("input-avaliacao", "value")
    ]
)
def update_prediction(n_clicks, idade, salario, tempo, avaliacao):
    if n_clicks is None:
        return "Aguardando previsão..."
    if None in (idade, salario, tempo, avaliacao):
        return "Por favor, preencha todos os campos com valores válidos."
    try:
        idade = int(idade)
        salario = int(salario)
        tempo = int(tempo)
        avaliacao = float(avaliacao)
    except (ValueError, TypeError):
        return "Erro: Insira valores numéricos válidos."
    
    # Continuar com a requisição
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
            return f"Erro ao fazer a previsão: Status {response.status_code}"
    except Exception as e:
        return f"Erro: {str(e)}"

# Rodar o servidor Dash
if __name__ == "__main__":    
    app.run(debug=True, port=8050, host='0.0.0.0')