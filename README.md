<p align="center">
  <img src="ico.png" width="200" alt="AccipiTest Logo">
</p>

<h1 align="center">AccipiTest</h1>

<p align="center">
  <strong>Plataforma interactiva para la realización y creación de tests personalizados.</strong>
</p>

---

AccipiTest es un programa portable escrito en Python diseñado para proveer al usuario de una herramienta interactiva de estudio. Permite gestionar diferentes perfiles, guardar progresos y ampliar el contenido simplemente añadiendo nuevos archivos de preguntas.

## 🏁 Cómo empezar

### 🪟 Uso en Windows
Tienes dos formas de utilizar AccipiTest en Windows:

**1. Versión Portable (Recomendado):**
* Ve a la sección de [**Releases**](https://github.com/robleslf/accipitest/releases).
* Descarga el archivo `AccipiTest.zip`.
* Descomprime y ejecuta `AccipiTest.exe`. No requiere instalación.

**2. Ejecución desde el código fuente:**
* Instala [Python 3.12](https://www.python.org/).
* En una terminal, instala las dependencias: `pip install -r requirements.txt`.
* Ejecuta el programa con: `python iniciar.py`.

---

### 🐧 Uso en Linux
En Linux, el programa se ejecuta directamente desde el código fuente:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/AccipiTest.git
   cd AccipiTest
   ```
2. **Crear entorno virtual y activar:**
   ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instalar dependencias y ejecutar:**
   ```bash
    pip install -r requirements.txt
    python3 iniciar.py
    ```

---

# 🎯 Modos

## 📖 Modo Estudio
Sistema guiado de aprendizaje.  
El objetivo es completar series de 10 tests por cada tema.  
Al finalizar, el sistema permite repasar exclusivamente las preguntas falladas hasta que no quede ningún error.

## 🎯 Práctica Libre
Permite configurar un test al gusto, seleccionando múltiples temas a la vez y el número de preguntas.

# 💾 Perfiles y Guardado

- **Perfiles:** Permite crear diferentes usuarios con progresos independientes.  
- **Guardado:** Puedes pausar cualquier test y retomarlo en otro momento.  
- **Persistencia:** En Windows, los datos se almacenan en `%APPDATA%/AccipiTest`, por lo que puedes mover la carpeta del programa sin perder tu progreso.

---

# ✨ Cómo añadir preguntas nuevas ✍️

Basta con crear un archivo `.py` dentro de la carpeta `preguntas/`. El programa lo detectará automáticamente al arrancar.

<details>
<summary><b>Click aquí para ver la plantilla de preguntas 📝</b></summary>

```python
# -*- coding: utf-8 -*-

# =============================================================================
# TÍTULO DEL PACK
# Nombre que aparecerá en el menú de AccipiTest
# =============================================================================
titulo = "Mi Nuevo Examen Personalizado"

# =============================================================================
# BANCO DE PREGUNTAS
# Soporta 3 tipos: única, múltiple y rellenar.
# =============================================================================
banco_de_preguntas = [
    
    # --- TIPO 1: SELECCIÓN ÚNICA ---
    {
        "pregunta": "¿Cuál es la función principal del comando 'mdadm'?",
        "opciones": {
            "A": "Configurar la red inalámbrica.",
            "B": "Gestionar dispositivos RAID por software.",
            "C": "Formatear particiones en formato NTFS.",
            "D": "Monitorizar la temperatura de la CPU."
        },
        "tipo": "única",
        "respuesta_correcta": "B", 
        "explicacion": {
            "general": "mdadm (Multiple Device Admin) es la herramienta estándar para RAID en Linux.",
            "opciones": {
                "A": "Incorrecto. Se usa nmcli o iw para redes.",
                "B": "¡Correcto! Permite crear, gestionar y monitorizar arrays RAID.",
                "C": "Incorrecto. Se usaría mkfs.ntfs.",
                "D": "Incorrecto. Para eso se usa lm-sensors."
            }
        }
    },

    # --- TIPO 2: SELECCIÓN MÚLTIPLE ---
    # El usuario debe marcar todas las correctas para acertar.
    {
        "pregunta": "¿Qué protocolos utiliza keepalived para gestionar alta disponibilidad? (Selecciona DOS)",
        "opciones": {
            "A": "VRRP",
            "B": "HTTP",
            "C": "LVS (IPVS)",
            "D": "FTP"
        },
        "tipo": "múltiple",
        "respuesta_correcta": "AC", # Letras juntas en orden alfabético
        "explicacion": {
            "general": "Keepalived combina VRRP para redundancia y LVS para balanceo de carga.",
            "opciones": {
                "A": "Correcto. Virtual Router Redundancy Protocol.",
                "B": "Incorrecto. Es un protocolo de aplicación.",
                "C": "Correcto. Linux Virtual Server integrado en el kernel.",
                "D": "Incorrecto. Es para transferencia de archivos."
            }
        }
    },

    # --- TIPO 3: RELLENAR ---
    # El usuario escribe la respuesta. No distingue entre mayúsculas y minúsculas.
    {
        "pregunta": "¿Cómo se llama el mecanismo para aislar nodos fallidos en un cluster (Fencing)?",
        "opciones": {}, # Vacío
        "tipo": "rellenar",
        "respuesta_correcta": ["STONITH", "stonith admin"], # Lista de respuestas aceptadas
        "explicacion": {
            "general": "STONITH significa 'Shoot The Other Node In The Head'.",
            "opciones": {} # Vacío
        }
    }

]
```
</details>

---

# 🛠️ Tecnologías utilizadas

- **Python 3.12** 🐍
- **CustomTkinter** 🎨
- **PyInstaller** 📦
- **JSON & AppData Integration** 🛡️

---

# ⚖️ Licencia

Este proyecto está bajo la **Licencia GPL-3.0**.
