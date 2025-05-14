#!/bin/bash
DEST_DIR="/home/userlnx/docker/script_docker/relay/"
REQUIREMENTS_FILE="requirements.txt"
# Passo 1: Criar o diretório de destino se não existir
mkdir -p "$DEST_DIR"
echo "Diretório de destino criado: $DEST_DIR"
# Passo 2: Iterar sobre os pacotes instalados e baixar apenas se não existir
pip freeze | while IFS= read -r package_line; do
  package_with_version=$(echo "$package_line")
  package=$(echo "$package_with_version" | cut -d'=' -f1)
  if [[ -n "$package" ]]; then
    # Tentar encontrar um arquivo .whl para o pacote no diretório de destino
    wheel_file=$(find "$DEST_DIR" -maxdepth 1 -name "$package-*.whl" -print0 | head -z -n 1)
    if [[ -z "$wheel_file" ]]; then
      echo "Arquivo .whl para $package não encontrado. Baixando para $DEST_DIR"
      pip download "$package_with_version" -d "$DEST_DIR"
    else
      echo "Arquivo .whl para $package já existe em $DEST_DIR. Ignorando download."
    fi
  fi
done
echo "Processo de backup completo."
pip freeze > "$DEST_DIR$REQUIREMENTS_FILE"
echo "Arquivo $DEST_DIR$REQUIREMENTS_FILE criado com a lista dos pacotes instalados."
echo "Processo de download concluído."