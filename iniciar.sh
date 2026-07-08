#!/bin/bash

# Nos movemos a la carpeta donde está el script
cd "$(dirname "$0")"

# 1. Comprobar si existe el entorno virtual, si no, crearlo
if [ ! -d "venv" ]; then
    echo "Configurando por primera vez..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

# 2. Ejecutar la aplicación usando el python del entorno virtual
./venv/bin/python3 iniciar.py
