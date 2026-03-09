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
* Ve a la sección de [**Releases**](https://github.com/tu-usuario/AccipiTest/releases).
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

# 🎯 Modos de Juego

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

# ✨ Cómo añadir preguntas nuevas ✍️

Basta con crear un archivo `.py` dentro de la carpeta `preguntas/`. El programa lo detectará automáticamente al arrancar.

<details>
<summary><b>Click aquí para ver la plantilla de preguntas 📝</b></summary>

```python
# -*- coding: utf-8 -*-
titulo = "Mi Nuevo Examen"

banco_de_preguntas = [
    {
        "pregunta": "¿Ejemplo de pregunta única?",
        "opciones": {"A": "Sí", "B": "No"},
        "tipo": "única",
        "respuesta_correcta": "A",
        "explicacion": {"general": "Info...", "opciones": {"A": "Bien", "B": "Mal"}}
    },
    {
        "pregunta": "¿Gigantes gaseosos? (Selecciona dos)",
        "opciones": {"A": "Júpiter", "B": "Marte", "C": "Saturno", "D": "Tierra"},
        "tipo": "múltiple",
        "respuesta_correcta": "AC",
        "explicacion": {"general": "Info...", "opciones": {}}
    },
    {
        "pregunta": "Escribe la capital de España:",
        "opciones": {},
        "tipo": "rellenar",
        "respuesta_correcta": ["Madrid"],
        "explicacion": {"general": "Info...", "opciones": {}}
    }
]
```
</details>

## 🛠️ Tecnologías utilizadas

- **Python 3.12** 🐍
- **CustomTkinter** 🎨
- **PyInstaller** 📦
- **JSON & AppData Integration** 🛡️

## ⚖️ Licencia

Este proyecto está bajo la **Licencia MIT**.
