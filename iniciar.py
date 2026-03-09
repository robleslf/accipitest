#!/usr/bin/env python3
import sys
import os
import subprocess
import time

IS_EXE = getattr(sys, 'frozen', False)

def get_venv_python(windowed=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe = "pythonw.exe" if (windowed and os.name == 'nt') else "python.exe"
    if os.name == 'nt': 
        return os.path.normpath(os.path.join(base_dir, "venv", "Scripts", exe))
    return os.path.join(base_dir, "venv", "bin", "python")

def start_app():
    try:
        import backend
        import ui
        app = ui.MainApp(backend.DataManager())
        app.mainloop()
    except Exception as e:
        with open("ERROR_LOG.txt", "w", encoding="utf-8") as f:
            import traceback
            f.write(f"Error fatal:\n{str(e)}\n\n")
            f.write(traceback.format_exc())

if __name__ == "__main__":
    if IS_EXE:
        start_app()
    else:
        venv_dir = os.path.join(os.path.dirname(__file__), "venv")
        if not os.path.exists(venv_dir):
            print("Entorno virtual no encontrado. Por favor, ejecuta el .bat")
            sys.exit(1)
            
        start_app()