#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import threading
import itertools

if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

C_RESET  = "\033[0m"
C_BOLD   = "\033[1m"
C_NEON_CYAN   = "\033[38;5;51m"
C_NEON_MAGENTA = "\033[38;5;198m"
C_NEON_GREEN   = "\033[38;5;82m"
C_DARK_GRAY    = "\033[38;5;237m"
C_RED          = "\033[38;5;196m"
C_HIDE_CURSOR  = "\033[?25l"
C_SHOW_CURSOR  = "\033[?25h"

def get_venv_python(windowed=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    exe = "pythonw.exe" if (windowed and os.name == 'nt') else "python.exe"
    if os.name != 'nt': exe = "python" # En Linux/Mac suele ser el mismo
    
    if os.name == 'nt': 
        return os.path.normpath(os.path.join(base_dir, "venv", "Scripts", exe))
    return os.path.join(base_dir, "venv", "bin", "python")

def is_running_in_venv():
    return "venv" in sys.executable.lower()

class SmoothDashboard:
    def __init__(self):
        self.tasks = [
            {"id": "env",  "desc": "CORPUS: Entorno Virtual", "status": "pending", "curr_pct": 0, "target_pct": 0},
            {"id": "pip",  "desc": "CORE: Optimizador de Paquetes", "status": "pending", "curr_pct": 0, "target_pct": 0},
            {"id": "libs", "desc": "NEURAL: Librerías Gráficas", "status": "pending", "curr_pct": 0, "target_pct": 0},
            {"id": "gui",  "desc": "INTERFACE: Motor Gráfico", "status": "pending", "curr_pct": 0, "target_pct": 0}
        ]
        self.spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        self.stop_event = False
        self.lock = threading.Lock()

    def set_target(self, task_id, status=None, pct=None):
        with self.lock:
            for t in self.tasks:
                if t["id"] == task_id:
                    if status: t["status"] = status
                    if pct is not None: t["target_pct"] = pct
                    if status == "done": t["target_pct"] = 100

    def draw(self):
        sys.stdout.write(C_HIDE_CURSOR)
        for _ in self.tasks: sys.stdout.write("\n")
        while not self.stop_event:
            sys.stdout.write(f"\033[{len(self.tasks)}F")
            with self.lock:
                s = next(self.spinner)
                for t in self.tasks:
                    if t["curr_pct"] < t["target_pct"]: t["curr_pct"] += 2
                    if t["curr_pct"] > 100: t["curr_pct"] = 100
                    if t["status"] == "done" and t["curr_pct"] == 100: icon = f"{C_NEON_GREEN}✔{C_RESET}"
                    elif t["status"] == "running": icon = f"{C_NEON_MAGENTA}{s}{C_RESET}"
                    else: icon = f"{C_DARK_GRAY}○{C_RESET}"
                    bar_len = 25
                    filled = int(bar_len * t["curr_pct"] / 100)
                    bar = f"{C_NEON_CYAN}{'━' * filled}{C_DARK_GRAY}{'─' * (bar_len - filled)}{C_RESET}"
                    sys.stdout.write(f"\033[K {icon} {t['desc']:35} {C_NEON_MAGENTA}{t['curr_pct']:3}%{C_RESET} {bar}\n")
            sys.stdout.flush()
            time.sleep(0.01)

    def stop(self):
        time.sleep(0.5)
        self.stop_event = True
        sys.stdout.write(C_SHOW_CURSOR + "\n")
        sys.stdout.flush()

def bootstrap():
    venv_dir = os.path.join(os.path.dirname(__file__), "venv")
    # Para la instalación usamos python.exe normal (necesitamos ver la consola)
    venv_python = get_venv_python(windowed=False)
    
    print(f"\n{C_BOLD}{C_NEON_MAGENTA}⚡ SYSTEM BOOT: PROTOCOLO DE ENTRENAMIENTO{C_RESET}")
    print(f"{C_NEON_CYAN}{'━'*65}{C_RESET}\n")
    dash = SmoothDashboard()
    t = threading.Thread(target=dash.draw, daemon=True)
    t.start()

    dash.set_target("env", status="running", pct=30)
    if not os.path.exists(venv_dir):
        subprocess.check_call([sys.executable, "-m", "venv", "venv"], stdout=subprocess.DEVNULL)
    dash.set_target("env", status="done")

    dash.set_target("pip", status="running", pct=50)
    subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dash.set_target("pip", status="done")

    dash.set_target("libs", status="running", pct=30)
    subprocess.check_call([venv_python, "-m", "pip", "install", "customtkinter"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dash.set_target("libs", status="done")

    dash.set_target("gui", status="running", pct=100)
    dash.set_target("gui", status="done")
    dash.stop()
    
    venv_pythonw = get_venv_python(windowed=True)
    
    if os.name == 'nt':
        subprocess.Popen([venv_pythonw, os.path.abspath(__file__)], 
                         creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS)
    else:
        subprocess.Popen([venv_python, os.path.abspath(__file__)])
        
    sys.exit(0)

if __name__ == "__main__":
    if not is_running_in_venv():
        bootstrap()
    else:
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
            sys.exit(1)