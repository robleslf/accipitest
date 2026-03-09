# -*- coding: utf-8 -*-

titulo = "Software Wine: Compatibilidad Linux"

banco_de_preguntas = [
    {
        "pregunta": "¿Qué significa el acrónimo recursivo WINE?",
        "opciones": {
            "A": "Windows Internet Networking Engine",
            "B": "Wine Is Not an Emulator",
            "C": "Web Integrated Native Environment",
            "D": "Windows Integration Next Era"
        },
        "tipo": "única",
        "respuesta_correcta": "B",
        "explicacion": {
            "general": "WINE es un acrónimo recursivo que enfatiza que no es un emulador de hardware.",
            "opciones": {
                "A": "Incorrecto.",
                "B": "Correcto. Wine traduce las llamadas de la API de Windows a llamadas POSIX al vuelo.",
                "C": "Incorrecto.",
                "D": "Incorrecto."
            }
        }
    },
    {
        "pregunta": "¿Cuáles de los siguientes son componentes o características de Wine? (Selecciona DOS)",
        "opciones": {
            "A": "Winelib (para compilar código de Windows en Unix)",
            "B": "Un kernel de Windows 10 completo embebido",
            "C": "WineServer (gestión de procesos y sincronización)",
            "D": "Emulación de procesadores ARM en sistemas x86"
        },
        "tipo": "múltiple",
        "respuesta_correcta": "AC",
        "explicacion": {
            "general": "Wine se compone de varias bibliotecas y un servidor de soporte.",
            "opciones": {
                "A": "Correcto. Winelib permite a los desarrolladores portar aplicaciones de Windows.",
                "B": "Falso. Wine no usa código del kernel de Microsoft.",
                "C": "Correcto. WineServer maneja la comunicación entre procesos y registros.",
                "D": "Falso. Wine no emula la CPU; las instrucciones se ejecutan nativamente."
            }
        }
    },
    {
        "pregunta": "¿Cuál es el comando que se utiliza para abrir la interfaz gráfica de configuración de Wine?",
        "opciones": {},
        "tipo": "rellenar",
        "respuesta_correcta": ["winecfg"],
        "explicacion": {
            "general": "El comando 'winecfg' abre una ventana donde puedes configurar la versión de Windows a imitar, los drivers de audio y las bibliotecas (overrides).",
            "opciones": {}
        }
    },
    {
        "pregunta": "De forma predeterminada, ¿en qué subdirectorio de la carpeta del usuario se encuentra la unidad virtual C: de Wine?",
        "opciones": {},
        "tipo": "rellenar",
        "respuesta_correcta": [".wine/drive_c", "~/.wine/drive_c"],
        "explicacion": {
            "general": "Wine crea un 'prefijo' oculto en el home del usuario llamado '.wine', que simula la jerarquía de archivos de Windows.",
            "opciones": {}
        }
    }
]