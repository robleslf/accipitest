@echo off
setlocal
cd /d "%~dp0"
echo ====================================================
echo   CREADOR DE EJECUTABLE ACCIPITEST
echo ====================================================
if not exist "venv\" (
    echo [1/4] Creando entorno virtual...
    python -m venv venv
)
echo [2/4] Instalando librerias...
"venv\Scripts\python.exe" -m pip install --upgrade pip
"venv\Scripts\python.exe" -m pip install customtkinter pyinstaller
if exist "dist\" rmdir /s /q "dist"
if exist "build\" rmdir /s /q "build"
echo [3/4] Empaquetando...
"venv\Scripts\python.exe" -m PyInstaller --noconsole --name "AccipiTest" --icon="ico.ico" --add-data "preguntas;preguntas" --add-data "ico.ico;." --collect-all customtkinter iniciar.py
echo [4/4] COMPROBANDO...
if exist "dist\AccipiTest\AccipiTest.exe" (
    echo EXITO: dist\AccipiTest\AccipiTest.exe
) else (
    echo ERROR en el empaquetado.
)
pause