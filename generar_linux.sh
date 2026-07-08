#!/bin/bash

# Ir a la carpeta del script
cd "$(dirname "$0")"

# Crear venv si no existe para limpiar el empaquetado
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Instalar dependencias
./venv/bin/pip install customtkinter pyinstaller

# Empaquetar
# OJO: En Linux, el separador de --add-data es ":" (dos puntos), no ";" (punto y coma)
./venv/bin/python3 -m PyInstaller --noconsole \
    --name "AccipiTest" \
    --icon="ico.png" \
    --add-data "preguntas:preguntas" \
    --add-data "ico.png:." \
    iniciar.py

echo "¡Listo! El ejecutable está en dist/AccipiTest/AccipiTest"