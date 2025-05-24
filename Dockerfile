# /home/userlnx/docker/script_docker/turnover/Dockerfile
FROM python:3.9-slim
WORKDIR /app

# 1. Copie APENAS o arquivo requirements.txt
# Esta camada só será invalidada se o requirements.txt mudar.
COPY requirements.txt .

# 2. Copie o diretório 'pacotespip' (se contiver wheels pré-baixados)
# Esta camada só será invalidada se os conteúdos de 'pacotespip' mudarem.
# Se você não usa pacotes offline, pode remover esta linha e o --no-index no pip install.
COPY pacotespip /tmp/relay_packages

# 3. Instale as dependências
# Esta camada só será reconstruída se requirements.txt ou pacotespip (se usado) mudar.
RUN pip install --no-index --find-links=/tmp/relay_packages -r requirements.txt

# 4. Por último, copie o restante do código da sua aplicação
# Esta camada e as subsequentes serão reconstruídas se qualquer arquivo do seu código mudar.
# No entanto, a instalação das dependências (camada 3) permanecerá em cache.
COPY . .

EXPOSE 8000
CMD ["uvicorn", "turnover:app", "--host", "0.0.0.0", "--port", "8000"]