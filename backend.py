import os
import json
import importlib.util
import sys
import re
from datetime import datetime

class DataManager:
    def __init__(self):
        self.current_user = None

        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        app_name = "EntrenadorPro"
        self.app_data_dir = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), app_name)
        self.users_dir = os.path.join(self.app_data_dir, 'users')

        # --- RUTA DE PREGUNTAS (Lectura) ---
        self.preguntas_dir = os.path.join(self.base_path, 'preguntas')

        # Crear carpetas si no existen
        os.makedirs(self.users_dir, exist_ok=True)
        if not os.path.exists(self.preguntas_dir):
            os.makedirs(self.preguntas_dir, exist_ok=True)

        if self.preguntas_dir not in sys.path:
            sys.path.append(self.preguntas_dir)

    def set_user(self, username):
        self.current_user = username
        safe_name = "".join(c for c in username if c.isalnum() or c in (' ', '_', '-')).strip()
        if not safe_name: safe_name = "default"
        
        self.state_file = os.path.join(self.users_dir, f"{safe_name}_estado.json")
        self.fails_file = os.path.join(self.users_dir, f"{safe_name}_fallos.json")
        self.suspended_file = os.path.join(self.users_dir, f"{safe_name}_suspendido.json")
        self.sync_packs()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return {"packs_de_preguntas": {}, "objetivo_intentos": 10}

    def save_state(self, state):
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, indent=2)

    def load_failures(self):
        if os.path.exists(self.fails_file):
            try:
                with open(self.fails_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return []
        return []

    def save_failures(self, failures):
        with open(self.fails_file, 'w', encoding='utf-8') as f:
            json.dump(failures, f, indent=2)

    def update_failures(self, new_failures_list):
        existing = self.load_failures()
        existing_texts = {q['pregunta'] for q in existing}
        for fail in new_failures_list:
            if fail['pregunta'] not in existing_texts:
                existing.append(fail)
                existing_texts.add(fail['pregunta'])
        self.save_failures(existing)

    def remove_correct_from_failures(self, correct_questions):
        if not correct_questions: return
        current_fails = self.load_failures()
        correct_texts = {q['pregunta'] for q in correct_questions}
        remaining_fails = [q for q in current_fails if q['pregunta'] not in correct_texts]
        self.save_failures(remaining_fails)

    def get_available_packs(self):
        packs = []
        if not os.path.exists(self.preguntas_dir): return []
        
        for f in os.listdir(self.preguntas_dir):
            if f.endswith('.py') and not f.startswith('__'):
                module_name = f[:-3]
                try:
                    # Importación dinámica para leer la variable 'titulo'
                    spec = importlib.util.spec_from_file_location(module_name, os.path.join(self.preguntas_dir, f))
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    titulo = getattr(module, "titulo", module_name)
                    packs.append({"id": module_name, "titulo": titulo})
                except Exception as e:
                    print(f"Error al identificar pack {f}: {e}")
        return sorted(packs, key=lambda x: x['titulo'])

    def sync_packs(self):
        state = self.load_state()
        packs = self.get_available_packs()
        for p in packs:
            p_id = p['id']
            if p_id not in state["packs_de_preguntas"]:
                state["packs_de_preguntas"][p_id] = {"intentos_completados": 0, "resultados": []}
        self.save_state(state)

    def load_questions_from_pack(self, pack_id):
        try:
            if pack_id in sys.modules:
                module = importlib.reload(sys.modules[pack_id])
            else:
                module = importlib.import_module(pack_id)
            return module.banco_de_preguntas
        except Exception as e:
            print(f"Error cargando preguntas de {pack_id}: {e}")
            return []

    def get_study_recommendation(self):
        state = self.load_state()
        available = self.get_available_packs()
        for p in available:
            p_id = p['id']
            data = state["packs_de_preguntas"].get(p_id, {"intentos_completados": 0})
            if data["intentos_completados"] < state.get("objetivo_intentos", 10):
                return p_id, data["intentos_completados"] + 1, p['titulo']
        return None, None, None

    def save_suspended_test(self, test_data):
        with open(self.suspended_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2)

    def load_suspended_test(self):
        if os.path.exists(self.suspended_file):
            try:
                with open(self.suspended_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: pass
        return None

    def delete_suspended_test(self):
        if os.path.exists(self.suspended_file):
            try:
                os.remove(self.suspended_file)
            except: pass