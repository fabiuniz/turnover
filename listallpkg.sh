#!/bin/bash

# Nome do arquivo de requisitos original
REQUIREMENTS_FILE="requirements.txt"
# Nome do novo arquivo com as versões
DEST_DIR="/home/userlnx/docker/script_docker/relay/"
REQUIREMENTS_VERSION_FILE=$DEST_DIR"requirements_version.txt"

# Verifica se o arquivo de requisitos original existe
if [ ! -f "$REQUIREMENTS_FILE" ]; then
  echo "Error: File '$REQUIREMENTS_FILE' not found."
  exit 1
fi

# Limpa o conteúdo do arquivo de versões, caso ele já exista
> "$REQUIREMENTS_VERSION_FILE"

while IFS= read -r line; do
  # Ignora comentários e linhas vazias
  if [[ ! "$line" =~ ^# ]] && [[ -n "$line" ]]; then
    # Extrai o nome do pacote
    package=$(echo "$line" | cut -d '=' -f 1 | tr -d ' ')
    # Obtém a versão do pacote e adiciona ao novo arquivo
    version=$(pip show "$package" 2>/dev/null | grep "^Version:" | awk '{print $2}')
    if [[ -n "$version" ]]; then
      echo "$package==$version" >> "$REQUIREMENTS_VERSION_FILE"
      echo $package==$version
    else
      echo "Warning: Could not find version for package '$package'" >> "$REQUIREMENTS_VERSION_FILE"
      echo "Warning: Could not find version for package '$package'"
    fi
  fi
done < "$REQUIREMENTS_FILE"

echo "Arquivo '$REQUIREMENTS_VERSION_FILE' criado com as versões dos pacotes."