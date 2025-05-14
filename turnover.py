# Importação das bibliotecas necessárias
import os # Importe o módulo os para manipulação de caminhos
from fastapi import FastAPI  # FastAPI é um framework leve e rápido para criação de APIs
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import pandas as pd  # Biblioteca para manipulação de dados tabulares
import numpy as np  # Biblioteca para operações numéricas e criação de arrays
import tensorflow as tf  # Biblioteca para machine learning e redes neurais
import matplotlib.pyplot as plt  # Biblioteca para geração de gráficos
import requests
from fastapi.responses import HTMLResponse, FileResponse
import seaborn as sns  # Biblioteca para visualização de dados estatísticos
from sklearn.model_selection import train_test_split  # Função para dividir os dados em treino e teste
from sklearn.preprocessing import StandardScaler  # Normalização dos dados para melhor desempenho da rede neural
from tensorflow.keras.models import Sequential  # Criação de modelos sequenciais de rede neural
from tensorflow.keras.layers import Dense, Dropout  # Camadas da rede neural, incluindo densas e dropout
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import matplotlib.pyplot as plt
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import asyncio

# adicionar registro aleatorio de forma dinamica cosiderando quantidade de colunas
def defaultvalue ():
    novo_funcionario_lista = []
    for col in X.columns:
        if col == "avaliacao":
            # Para 'avaliacao', gerar um valor float aleatório na mesma faixa
            novo_funcionario_lista.append(np.random.uniform(df[col].min(), df[col].max()))
        else:
            # Para outras colunas (inteiras), gerar um inteiro aleatório na mesma faixa
            novo_funcionario_lista.append(np.random.randint(df[col].min(), df[col].max() + 1))
    return np.array([novo_funcionario_lista])

# Carregar dados fictícios
data = {
    "id": np.random.randint(22, 60, 500),
    "nome": np.random.randint(22, 60, 500),
    "cargo": np.random.randint(22, 60, 500),
    "departamento": np.random.randint(22, 60, 500),
    "idade": np.random.randint(22, 60, 500),
    "salario": np.random.randint(3000, 20000, 500),
    "tempo_empresa": np.random.randint(1, 15, 500),
    "avaliacao": np.random.uniform(1, 5, 500),
    "turnover": np.random.randint(0, 2, 500)  # 1 = funcionário saiu, 0 = permaneceu 
}
data = {
    "idade": np.random.randint(22, 60, 500),
    "salario": np.random.randint(3000, 20000, 500),
    "tempo_empresa": np.random.randint(1, 15, 500),
    "avaliacao": np.random.uniform(1, 5, 500),
    "turnover": np.random.randint(0, 2, 500)  # 1 = funcionário saiu, 0 = permaneceu
}

df = pd.DataFrame(data)
# Carregar dados (exemplo fictício)
df = pd.read_csv("static/dados_funcionarios.csv", sep=";", encoding="utf-8")


# Limpeza de dados
df.dropna(inplace=True)
df["idade"] = df["idade"].astype(int)

# Visualizar os primeiros registros
print(df.head())

# Visualização de padrões
sns.histplot(df["salario"], kde=True)
plt.title("Distribuição Salarial")
plt.show()

# Separação de dados
X = df.drop(columns=["turnover"])
y = df["turnover"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalização dos dados
scaler = StandardScaler()
scaler.fit(X_train)
X_train_df = pd.DataFrame(X_train, columns=X.columns)  # Mantém nomes das colunas
X_train_scaled = scaler.fit_transform(X_train_df)

# Construção do modelo de rede neural
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(32, activation="relu"),
    Dropout(0.2),
    Dense(1, activation="sigmoid")
])

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Treinamento
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Avaliação do modelo
loss, acc = model.evaluate(X_test, y_test)
print(f"Acurácia do modelo: {acc:.2f}")

# Plotando a curva de aprendizado
plt.plot(history.history['accuracy'], label='Treino')
plt.plot(history.history['val_accuracy'], label='Validação')
plt.xlabel('Épocas')
plt.ylabel('Acurácia')
plt.legend()
plt.title("Curva de Aprendizado")
plt.show()

# Predição em novos dados


#novo_funcionario = np.array([data[col] for col in X.columns])
#novo_funcionario = scaler.transform(novo_funcionario.reshape(1, -1)) # Reshape para (1, num_features)
#novo_funcionario = np.array([[35, 8500, 5, 4.2]])
novo_funcionario = defaultvalue()
novo_funcionario = scaler.transform(novo_funcionario)

predicao = model.predict(novo_funcionario)
print(f"Chance de Turnover: {predicao[0][0] * 100:.2f}%")

#-----------------------------------------------------------------------
# Inicializa a API
app = FastAPI()  # Cria uma instância da aplicação FastAPI
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite requisições de qualquer origem
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definição do modelo de entrada esperado no request
class FuncionarioInput(BaseModel):
    idade: int
    salario: float
    tempo_empresa: int
    avaliacao: float

# Criando modelo de rede neural
model = Sequential([
    Dense(64, activation="relu", input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(32, activation="relu"),
    Dropout(0.2),
    Dense(1, activation="sigmoid")
])

# Compilando modelo
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# Treinando modelo
model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test))

# Salvando modelo treinado
model.save("modelo_turnover.h5")

# Carrega o modelo treinado
model = tf.keras.models.load_model("modelo_turnover.h5")

# Criando um objeto de normalização (ajuste conforme necessário)
scaler = StandardScaler()
dummy_data = np.array([[35, 8500, 5, 4.2]])  
scaler.fit(dummy_data) 

# Carrega o HTML ao acessar a página inicial
@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse(os.path.join("static", "index.html"))

@app.post("/predict/")
def predict(funcionario: FuncionarioInput):
    """Recebe dados do funcionário via JSON e retorna a probabilidade de turnover"""


    arrai = defaultvalue()
    #arrai[0,4]= funcionario.idade 
    #arrai[0,5]= funcionario.salario
    #arrai[0,6]= funcionario.tempo_empresa 
    #arrai[0,7]= funcionario.avaliacao

    print(arrai)

    # Transforma os dados de entrada para um DataFrame compatível
    entrada_df = pd.DataFrame(arrai, columns=X_train.columns)  # Mantém estrutura idêntica ao treinamento
    entrada_df = entrada_df[X_train.columns]  # Mantém apenas as colunas usadas no treinamento
    
    # Normaliza os dados para que estejam compatíveis com o modelo
    entrada_scaled = scaler.transform(entrada_df.values) # Converte para numpy sem colunas nomeadas

    # Fazendo a previsão
    predicao = model.predict(entrada_scaled)
    chance_turnover = float(predicao[0][0]) * 100  # Converte para porcentagem

    return {
        "idade": funcionario.idade,
        "salario": funcionario.salario,
        "tempo_empresa": funcionario.tempo_empresa,
        "avaliacao": funcionario.avaliacao,
        "chance_turnover": f"{chance_turnover:.2f}%"
    }

# Novo endpoint para executar o dashboard Dash
@app.post("/dashboard/")
async def run_dashboard():
    try:
        # Executa o dashboard.py em um processo separado
        process = subprocess.Popen(["python3", "dashboard.py"])
        return {"message": "Dashboard (Dash) iniciado com sucesso! Acesse http://vmlinuxd:8050"}
    except Exception as e:
        return {"message": f"Erro ao iniciar o dashboard: {str(e)}"}

# Novo endpoint para executar o dashboard Streamlit
@app.post("/streamlit/")
async def run_streamlit():
    try:
        # Executa o dashboard_streamlit.py em um processo separado
        process = subprocess.Popen(["streamlit", "run", "dashboard_streamlit.py"])
        return {"message": "Dashboard (Streamlit) iniciado com sucesso! Acesse http://vmlinuxd:8501"}
    except Exception as e:
        return {"message": f"Erro ao iniciar o Streamlit: {str(e)}"}

#Resumo: ✔ Este código simula um modelo de machine learning que prevê a probabilidade de um funcionário sair de uma empresa baseado em suas características. ✔ Utiliza TensorFlow para treinar uma rede neural, Pandas para manipulação de dados, Seaborn para visualizações e Sklearn para dividir e normalizar os dados. ✔ A rede neural aprende padrões no histórico de funcionários para prever futuras saídas (turnover). ✔ Inclui um gráfico mostrando como a acurácia do modelo evolui ao longo das épocas.
#🚀 Esse código pode ser aprimorado com mais features, tuning dos hiperparâmetros, experimentação com outros algoritmos e mais visualizações de dados! Me avise se precisar de ajustes! 💡
