import customtkinter as ctk
import random
import re
from tkinter import messagebox
from datetime import datetime
import os
import sys
import ctypes

FONT_NAME = "Roboto"
SIZE_PREGUNTA = 26
SIZE_OPCION = 20
SIZE_EXPLICACION = 18
SIZE_HEADER = 22
SIZE_BTN = 20

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)
        self.controller, self.manager = controller, manager
        ctk.CTkLabel(self, text="ACCIPITEST", font=(FONT_NAME, 32, "bold"), text_color="#3B8ED0").pack(pady=(120, 20))
        frame_box = ctk.CTkFrame(self)
        frame_box.pack(pady=10, padx=20)
        ctk.CTkLabel(frame_box, text="Introduce tu perfil de usuario:", font=(FONT_NAME, SIZE_HEADER)).pack(pady=20, padx=40)
        self.entry = ctk.CTkEntry(frame_box, width=300, height=45, font=(FONT_NAME, 18))
        self.entry.pack(pady=10, padx=30)
        self.entry.bind("<Return>", self.login)
        ctk.CTkButton(self, text="ENTRAR", command=self.login, height=60, width=300, font=(FONT_NAME, SIZE_BTN, "bold")).pack(pady=20)
        ctk.CTkButton(self, text="SALIR", command=self.controller.quit, height=50, width=300, font=(FONT_NAME, 16), fg_color="transparent", border_width=1).pack(pady=10)
        self.entry.focus()

    def login(self, event=None):
        name = self.entry.get().strip()
        if name:
            self.manager.set_user(name)
            self.controller.show_dashboard()

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, manager):
        super().__init__(parent)
        self.controller, self.manager = controller, manager
        header = ctk.CTkFrame(self, height=70, fg_color="#1A1A1A")
        header.pack(fill="x", side="top")
        ctk.CTkLabel(header, text=f"👤 Perfil: {self.manager.current_user}", font=(FONT_NAME, 20, "bold")).pack(side="left", padx=20)
        ctk.CTkButton(header, text="Cerrar Sesión", width=140, height=35, fg_color="transparent", border_width=1, command=self.controller.show_login).pack(side="right", padx=20)
        
        content = ctk.CTkScrollableFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=10)
        
        saved_test = self.manager.load_suspended_test()
        if saved_test:
            resume_f = ctk.CTkFrame(content, fg_color="#3E2723", border_width=2, border_color="#E67E22")
            resume_f.pack(fill="x", padx=40, pady=(10, 20))
            ctk.CTkLabel(resume_f, text=f"⏳ TEST EN PAUSA ({saved_test['mode'].upper()})", font=(FONT_NAME, 16, "bold")).pack(pady=10)
            ctk.CTkButton(resume_f, text="REANUDAR TEST", fg_color="#E67E22", hover_color="#D35400", height=50, command=lambda: self.resume_test(saved_test)).pack(pady=10, padx=20)
            
        grid = ctk.CTkFrame(content, fg_color="transparent")
        grid.pack(fill="both", expand=True)
        grid.grid_columnconfigure((0,1), weight=1)
        
        f_st = ctk.CTkFrame(grid); f_st.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(f_st, text="📖 Modo Estudio", font=(FONT_NAME, 22, "bold"), text_color="#3B8ED0").pack(pady=15)
        p_id, a, p_titulo = self.manager.get_study_recommendation()
        txt = f"Siguiente:\n{p_titulo}\n(Intento {a}/10)" if p_id else "¡Todo completado!"
        ctk.CTkButton(f_st, text=txt, height=80, font=(FONT_NAME, 16), state="normal" if p_id else "disabled", command=lambda: self.launch_study(p_id)).pack(pady=20, padx=20)
        
        f_ra = ctk.CTkFrame(grid); f_ra.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(f_ra, text="🎲 Práctica Libre", font=(FONT_NAME, 22, "bold"), text_color="#27AE60").pack(pady=15)
        self.all_var = ctk.BooleanVar(value=False)
        ctk.CTkSwitch(f_ra, text="Seleccionar todos", variable=self.all_var, command=self.toggle_all).pack()
        
        self.packs_scroll = ctk.CTkScrollableFrame(f_ra, height=200)
        self.packs_scroll.pack(fill="both", expand=True, padx=15, pady=10)
        self.vars = {}
        for pack_info in self.manager.get_available_packs():
            pid = pack_info['id']; titulo = pack_info['titulo']
            v = ctk.BooleanVar(); v.trace_add("write", self.update_counter)
            self.vars[pid] = v
            ctk.CTkCheckBox(self.packs_scroll, text=titulo, variable=v).pack(anchor="w", pady=4)
            
        f_cnt = ctk.CTkFrame(f_ra, fg_color="transparent")
        f_cnt.pack(pady=10)
        self.lbl_available = ctk.CTkLabel(f_cnt, text="Seleccionadas: 0"); self.lbl_available.pack(side="left", padx=10)
        self.entry_num = ctk.CTkEntry(f_cnt, width=60); self.entry_num.pack(side="left"); self.entry_num.insert(0, "20")
        ctk.CTkButton(f_ra, text="GENERAR TEST", fg_color="#27AE60", height=55, font=(FONT_NAME, 18, "bold"), command=self.launch_random).pack(pady=10, padx=20)
        
        num_f = len(self.manager.load_failures())
        ctk.CTkButton(content, text=f"❌ Repasar Errores ({num_f})", fg_color="#C0392B", height=60, font=(FONT_NAME, 18, "bold"), command=self.launch_fails).pack(pady=20, padx=40)
        self.update_counter()

    def resume_test(self, d): self.controller.start_quiz(d['questions'], d['mode'], d.get('pack_id'), resume_data=d)
    def update_counter(self, *args):
        total = sum(len(self.manager.load_questions_from_pack(p)) for p, v in self.vars.items() if v.get())
        self.lbl_available.configure(text=f"Disponibles: {total}")
    def toggle_all(self):
        for v in self.vars.values(): v.set(self.all_var.get())
    def launch_study(self, pid):
        preguntas = self.manager.load_questions_from_pack(pid)
        import random
        random.shuffle(preguntas)
        self.controller.start_quiz(preguntas, "study", pid)
    def launch_random(self):
        pks = [i for i, v in self.vars.items() if v.get()]
        if not pks: return
        qs = []
        for p in pks: qs.extend(self.manager.load_questions_from_pack(p))
        try: num = int(self.entry_num.get())
        except: return
        self.controller.start_quiz(random.sample(qs, min(len(qs), num)), "random")
    def launch_fails(self):
        preguntas = self.manager.load_failures()
        if not preguntas: return
        random.shuffle(preguntas)
        self.controller.start_quiz(preguntas, "review")

class QuizFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, manager, questions, mode, pack_id=None, resume_data=None):
        super().__init__(parent)
        self.controller, self.manager, self.questions, self.mode, self.pack_id = controller, manager, questions, mode, pack_id
        
        if resume_data:
            self.current_idx = resume_data['current_idx']
            self.aciertos = resume_data['aciertos']
            self.nuevos_fallos = resume_data['nuevos_fallos']
            self.acertadas = resume_data['acertadas']
        else:
            self.current_idx, self.aciertos, self.nuevos_fallos, self.acertadas = 0, 0, [], []
            
        self.total = len(questions)
        self.letters = ['A', 'B', 'C', 'D', 'E', 'F']
        self.answered = False
        self.key_map, self.widgets, self.display_order = {}, {}, []
        self.controller.bind("<Key>", self.handle_key)
        
        # UI
        self.head = ctk.CTkFrame(self, height=40)
        self.head.pack(fill="x", padx=10, pady=5)
        self.lbl_mode = ctk.CTkLabel(self.head, text=f"MODO: {mode.upper()}", font=(FONT_NAME, 14, "bold"), text_color="#3B8ED0")
        self.lbl_mode.pack(side="left", padx=15)
        self.lbl_prog = ctk.CTkLabel(self.head, text="", font=(FONT_NAME, 14))
        self.lbl_prog.pack(side="right", padx=15)
        
        self.txt_q = ctk.CTkTextbox(self, height=180, font=(FONT_NAME, SIZE_PREGUNTA), wrap="word")
        self.txt_q.pack(fill="x", padx=10, pady=5)
        
        self.scroll_body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_body.pack(fill="both", expand=True, padx=10, pady=5)
        self.opts_frame = ctk.CTkFrame(self.scroll_body, fg_color="transparent")
        self.opts_frame.pack(fill="x")
        self.lbl_feed = ctk.CTkLabel(self.scroll_body, text="", font=(FONT_NAME, 24, "bold"))
        self.lbl_feed.pack(pady=10)
        self.txt_exp = ctk.CTkTextbox(self.scroll_body, height=250, font=(FONT_NAME, SIZE_EXPLICACION), wrap="word")
        
        self.btns_f = ctk.CTkFrame(self, height=80)
        self.btns_f.pack(fill="x", side="bottom", padx=10, pady=10)
        self.btn_act = ctk.CTkButton(self.btns_f, text="CONFIRMAR", height=60, font=(FONT_NAME, 20, "bold"), command=self.check_or_next)
        self.btn_act.pack(side="left", fill="x", expand=True, padx=5)
        ctk.CTkButton(self.btns_f, text="💾", width=60, height=60, fg_color="#E67E22", command=self.quick_save).pack(side="left", padx=2)
        ctk.CTkButton(self.btns_f, text="SALIR", width=100, height=60, fg_color="#444", command=self.exit_quiz).pack(side="left", padx=2)
        
        self.load_q()

    def handle_key(self, e):
        if self.current_idx >= len(self.questions): return
        q = self.questions[self.current_idx]
        if e.keysym == 'Return': self.check_or_next(); return
        if e.keysym == 'space' and q['tipo'] != 'rellenar': self.check_or_next(); return
        if not self.answered and e.char.lower() in self.key_map:
            k = self.key_map[e.char.lower()]
            self.toggle(k, self.widgets[k], q['tipo'])

    def clean_ansi(self, t): 
        return re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])').sub('', str(t)) if t else ""

    def load_q(self):
        self.answered = False
        self.txt_exp.pack_forget()
        self.lbl_feed.configure(text="")
        self.btn_act.configure(text="CONFIRMAR (Enter)", fg_color="#3B8ED0")
        for w in self.opts_frame.winfo_children(): w.destroy()
        if self.current_idx >= len(self.questions): self.finish(); return
        
        q = self.questions[self.current_idx]
        self.lbl_prog.configure(text=f"Pregunta {self.current_idx+1} de {self.total}")
        self.txt_q.configure(state="normal")
        self.txt_q.delete("0.0", "end")
        self.txt_q.insert("0.0", self.clean_ansi(q['pregunta']))
        self.txt_q.configure(state="disabled")
        self.selected, self.widgets, self.key_map = set(), {}, {}
        
        if q['tipo'] == 'rellenar':
            self.entry = ctk.CTkEntry(self.opts_frame, height=50, font=(FONT_NAME, 20), width=400)
            self.entry.pack(pady=20); self.entry.focus()
        else:
            opts = list(q['opciones'].items())
            random.shuffle(opts)
            self.display_order = opts
            for i, (k, txt) in enumerate(opts):
                l = self.letters[i]
                self.key_map[l.lower()] = k
                btn = ctk.CTkButton(self.opts_frame, text=f"{l}) {self.clean_ansi(txt)}", fg_color="transparent", border_width=1, anchor="w", height=45, font=(FONT_NAME, SIZE_OPCION))
                btn.configure(command=lambda k=k, b=btn: self.toggle(k, b, q['tipo']))
                btn.pack(fill="x", pady=4)
                self.widgets[k] = btn

    def toggle(self, k, btn, t):
        if self.answered: return
        if t == 'única':
            self.selected = {k}
            for w in self.widgets.values(): w.configure(fg_color="transparent", border_color="#555")
            btn.configure(fg_color="#1F6AA5", border_color="#3B8ED0")
        else:
            if k in self.selected: self.selected.remove(k); btn.configure(fg_color="transparent", border_color="#555")
            else: self.selected.add(k); btn.configure(fg_color="#1F6AA5", border_color="#3B8ED0")

    def check_or_next(self):
        if self.answered: self.next()
        else: self.check()

    def check(self):
        q = self.questions[self.current_idx]
        if q['tipo'] == 'rellenar':
            user_ans = self.entry.get().strip().lower()
            ok = any(user_ans == val.lower() for val in q['respuesta_correcta'])
        else:
            if not self.selected: return
            ok = "".join(sorted(list(self.selected))) == "".join(sorted(list(q['respuesta_correcta'])))
        
        self.answered = True
        if q['tipo'] != 'rellenar':
            for k, b in self.widgets.items():
                b.configure(state="disabled")
                if k in q['respuesta_correcta']: b.configure(border_color="#2ECC71", border_width=3)
                if k in self.selected: b.configure(fg_color="#27AE60" if k in q['respuesta_correcta'] else "#C0392B")
        
        if ok:
            self.aciertos += 1; self.acertadas.append(q)
            self.lbl_feed.configure(text="¡EXCELENTE! ✅", text_color="#2ECC71")
            self.btn_act.configure(text="SIGUIENTE ➡", fg_color="#27AE60")
        else:
            self.nuevos_fallos.append(q)
            self.lbl_feed.configure(text="ERROR ❌", text_color="#E74C3C")
            self.btn_act.configure(text="ENTENDIDO ➡", fg_color="#C0392B")
            
        self.txt_exp.configure(state="normal")
        self.txt_exp.delete("0.0", "end")
        gen_exp = q.get('explicacion', {}).get('general', 'No hay explicación.')
        exp_text = f"📝 EXPLICACIÓN:\n{self.clean_ansi(gen_exp)}\n\n"
        if q['tipo'] == 'rellenar':
            exp_text += f"✅ Respuestas válidas: {', '.join(q['respuesta_correcta'])}"
        else:
            for i, (id_o, _) in enumerate(self.display_order):
                sym = "✅" if id_o in q['respuesta_correcta'] else "❌"
                det = q['explicacion']['opciones'].get(id_o, "")
                exp_text += f"{sym} {self.letters[i]}: {self.clean_ansi(det)}\n"
        self.txt_exp.insert("0.0", exp_text)
        self.txt_exp.configure(state="disabled")
        self.txt_exp.pack(fill="x", padx=10, pady=10)

    def next(self):
        self.current_idx += 1
        self.load_q()

    def quick_save(self):
        self.manager.save_suspended_test({"questions": self.questions, "current_idx": self.current_idx, "aciertos": self.aciertos, "nuevos_fallos": self.nuevos_fallos, "acertadas": self.acertadas, "mode": self.mode, "pack_id": self.pack_id})
        messagebox.showinfo("Guardado", "Progreso guardado correctamente.")

    def exit_quiz(self):
        self.quick_save()
        self.controller.unbind("<Key>")
        self.controller.show_dashboard()

    def finish(self):
        self.controller.unbind("<Key>")
        self.manager.delete_suspended_test()
        
        # 1. Los fallos siempre se guardan para que la lista crezca
        if self.nuevos_fallos:
            self.manager.update_failures(self.nuevos_fallos)
            
        # 2. CAMBIO SOLICITADO: Solo en modo 'review' (repasar errores) eliminamos los que ahora están bien
        if self.mode == 'review' and self.acertadas:
            self.manager.remove_correct_from_failures(self.acertadas)
            
        # 3. Guardar progreso de estudio si aplica
        if self.mode == 'study' and self.pack_id:
            st = self.manager.load_state()
            res = {"timestamp": str(datetime.now()), "aciertos": self.aciertos, "total": self.total}
            if self.pack_id not in st["packs_de_preguntas"]:
                st["packs_de_preguntas"][self.pack_id] = {"intentos_completados": 0, "resultados": []}
            st["packs_de_preguntas"][self.pack_id]["resultados"].append(res)
            st["packs_de_preguntas"][self.pack_id]["intentos_completados"] += 1
            self.manager.save_state(st)
            
        messagebox.showinfo("Test Finalizado", f"¡Buen trabajo!\nResultado: {self.aciertos}/{self.total}")
        self.controller.show_dashboard()

class MainApp(ctk.CTk):
    def __init__(self, data_manager):
        super().__init__()
        self.manager = data_manager
        self.title("AccipiTest")
        self.geometry("1150x900")
        if os.name == 'nt':
            try:
                myappid = 'com.felip.accipitest.v1'
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
                ruta_icono = os.path.join(base_path, "ico.ico")
                if os.path.exists(ruta_icono): self.iconbitmap(ruta_icono)
            except: pass
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None
        self.show_login()

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame: self.current_frame.destroy()
        self.current_frame = frame_class(self.container, self, self.manager, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def show_login(self): self.switch_frame(LoginFrame)
    def show_dashboard(self): self.switch_frame(DashboardFrame)
    def start_quiz(self, questions, mode, pack_id=None, resume_data=None):
        self.switch_frame(QuizFrame, questions=questions, mode=mode, pack_id=pack_id, resume_data=resume_data)
