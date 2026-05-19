import os
import sys
import json
import re
import random
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

CONFIG = {
    "archivo_traducciones": "translations.json",
    "archivo_contextos": "contextos.json",
    "umbral_similitud": 0.6,
    "max_historial": 10,
    "idioma_defecto": "es",
    "tema_defecto": "informatica",
    "velocidad_escritura": 25
}

class ChatbotEngine:
    def __init__(self):
        self.idioma = CONFIG["idioma_defecto"]
        self.tema = CONFIG["tema_defecto"]
        self.historial = []
        self.traducciones = self._cargar_json(CONFIG["archivo_traducciones"], self._traducciones_minimas())
        self.contextos = self._cargar_json(CONFIG["archivo_contextos"], self._contextos_minimos())
        self.reglas = self._inicializar_reglas()

    def _cargar_json(self, ruta, fallback):
        if os.path.exists(ruta):
            try:
                with open(ruta, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error cargando {ruta}: {e}")
        return fallback

    def _traducciones_minimas(self):
        return {
            "es": {"welcome": "CHATBOT SERPIENTE", "fallback": "Sin respuesta.", "ui": {}},
            "en": {"welcome": "SNAKE CHATBOT", "fallback": "No response.", "ui": {}},
            "zh": {"welcome": "蛇聊天机器人", "fallback": "无响应。", "ui": {}}
        }

    def _contextos_minimos(self):
        return {
            "informatica": {"es": ["La CPU ejecuta instrucciones."], "en": ["The CPU executes instructions."], "zh": ["CPU执行指令。"]},
            "serpientes": {"es": ["Las serpientes son reptiles."], "en": ["Snakes are reptiles."], "zh": ["蛇是爬行动物。"]},
            "coches": {"es": ["Un coche tiene motor."], "en": ["A car has an engine."], "zh": ["汽车有发动机。"]}
        }

    def _inicializar_reglas(self):
        return {
            "informatica": {
                "es": {
                    "hola": "Hola. Soy tu asistente tecnico. ¿En que area necesitas ayuda?",
                    "python": "Python es un lenguaje interpretado, multiparadigma y de tipado dinamico. Ideal para IA, web y automatizacion.",
                    "html": "HTML define la estructura semantica de una pagina web. Se combina con CSS (estilos) y JS (comportamiento).",
                    "ram": "La RAM es memoria volatil. Almacena datos activos mientras el sistema esta encendido. Se mide en GB.",
                    "cpu": "La CPU (Unidad Central de Procesamiento) ejecuta instrucciones del software. Su velocidad se mide en GHz.",
                    "git": "Git es un sistema de control de versiones distribuido. Permite cambios y colaborar en codigo.",
                    "api": "Una API (Interfaz de Programacion de Aplicaciones) permite que dos softwares se comuniquen mediante protocolos estandar.",
                    "sql": "SQL es el lenguaje estandar para gestionar bases de datos relacionales. Permite consultar, insertar y modificar datos."
                },
                "en": {
                    "hello": "Hello. I am your technical assistant. Which area do you need help with?",
                    "python": "Python is an interpreted, multi-paradigm, dynamically typed language. Ideal for AI, web, and automation.",
                    "html": "HTML defines the semantic structure of a web page. It works with CSS (styles) and JS (behavior).",
                    "ram": "RAM is volatile memory. It stores active data while the system is on. Measured in GB.",
                    "cpu": "The CPU (Central Processing Unit) executes software instructions. Speed is measured in GHz.",
                    "git": "Git is a distributed version control system. It tracks changes and enables code collaboration.",
                    "api": "An API (Application Programming Interface) allows two software systems to communicate via standard protocols.",
                    "sql": "SQL is the standard language for managing relational databases. It allows querying, inserting, and modifying data."
                },
                "zh": {
                    "你好": "你好。我是您的技术助手。您需要哪方面的帮助？",
                    "python": "Python是一种解释型、多范式、动态类型语言。非常适合AI、Web和自动化。",
                    "html": "HTML定义网页的语义结构。它与CSS（样式）和JS（行为）配合使用。",
                    "ram": "RAM是易失性内存。在系统运行时存储活动数据。以GB为单位。",
                    "cpu": "CPU（中央处理器）执行软件指令。速度以GHz衡量。",
                    "git": "Git是一个分布式版本控制系统。它跟踪更改并支持代码协作。",
                    "api": "API（应用程序编程接口）允许两个软件系统通过标准协议进行通信。",
                    "sql": "SQL是管理关系数据库的标准语言。允许查询、插入和修改数据。"
                }
            },
            "serpientes": {
                "es": {
                    "hola": "Hola. ¿Interesado en herpetologia? Puedo hablar sobre anatomia, ecologia o peligrosidad.",
                    "veneno": "El veneno puede ser neurotoxico (afecta sistema nervioso), hemotoxico (sangre) o citotoxico (tejidos).",
                    "muda": "La muda o ecdisis ocurre varias veces al año. La piel vieja se desprende en una sola pieza.",
                    "cobra": "La cobra real es la serpiente venenosa mas larga del mundo. Puede alcanzar 5.5 metros.",
                    "boa": "Las boas y pitones son constrictoras. No tienen veneno, sino que asfixian a sus presas.",
                    "sentidos": "Las serpientes perciben vibraciones por el suelo y calor mediante fosetas loreales.",
                    "hibernacion": "En climas frios, muchas serpientes entran en brumacion para conservar energia."
                },
                "en": {
                    "hello": "Hello. Interested in herpetology? I can discuss anatomy, ecology, or venom toxicity.",
                    "venom": "Venom can be neurotoxic, hemotoxic, or cytotoxic. Not all snakes are venomous; some are constrictors.",
                    "shed": "Shedding (ecdysis) happens several times a year. Old skin comes off in one piece to allow growth.",
                    "cobra": "The king cobra is the longest venomous snake, reaching up to 5.5 meters. It feeds on other snakes.",
                    "boa": "Boas and pythons are constrictors. They lack venom and subdue prey by coiling around it.",
                    "senses": "Snakes detect ground vibrations and heat via loreal pits. Their tongue collects airborne chemical particles.",
                    "hibernation": "In cold climates, many snakes enter brumation to conserve energy during winter months."
                },
                "zh": {
                    "你好": "你好。对爬行动物学感兴趣吗？我可以讨论解剖学、生态学或毒性。",
                    "veneno": "毒液可分为神经毒素、血液毒素或细胞毒素。并非所有蛇都有毒，有些是绞杀型。",
                    "muda": "蜕皮（ecdysis）每年发生多次。旧皮整片脱落以促进生长。",
                    "cobra": "眼镜王蛇是最长的毒蛇，可达5.5米。它以其他蛇类为食。",
                    "boa": "蟒蛇和蚺蛇是绞杀型。它们没有毒液，通过缠绕制服猎物。",
                    "sentidos": "蛇通过地面振动和颊窝感知热量。舌头收集空气中的化学颗粒。",
                    "hibernacion": "在寒冷气候中，许多蛇进入冬眠状态以在冬季保存能量。"
                }
            },
            "coches": {
                "es": {
                    "hola": "Hola. ¿Buscas informacion tecnica o historica sobre automoviles? Estoy listo.",
                    "motor": "El motor de combustion interna transforma energia quimica en mecanica mediante ciclos.",
                    "abs": "El ABS modula la presion de frenado para evitar que las ruedas se bloqueen.",
                    "turbo": "El turbocompresor usa los gases de escape para comprimir aire de admision, aumentando la potencia.",
                    "hibrido": "Un hibrido combina motor termico y electrico. Recupera energia en frenadas.",
                    "chasis": "El chasis es la estructura portante del vehiculo. Determina rigidez y seguridad.",
                    "neumatico": "La presion correcta de los neumaticos es crucial para adherencia y desgaste.",
                    "electrico": "Los vehiculos electricos usan baterias de ion-litio. Cero emisiones directas."
                },
                "en": {
                    "hello": "Hello. Looking for technical or historical car info? I am ready.",
                    "engine": "The internal combustion engine converts chemical energy into mechanical work via intake, compression, power, and exhaust strokes.",
                    "abs": "ABS modulates brake pressure to prevent wheel lockup, maintaining steering control during hard braking.",
                    "turbo": "A turbocharger uses exhaust gases to compress intake air, boosting power without increasing engine displacement.",
                    "hybrid": "A hybrid combines thermal and electric motors. It recovers energy during braking.",
                    "chassis": "The chassis is the vehicle's load-bearing structure. It determines rigidity, safety, and dynamic behavior.",
                    "tire": "Correct tire pressure is crucial for grip, even wear, and energy efficiency.",
                    "electric": "Electric vehicles use lithium-ion batteries and AC motors. Zero direct emissions."
                },
                "zh": {
                    "你好": "你好。寻找汽车技术或历史信息吗？我已准备好。",
                    "motor": "内燃机通过进气、压缩、做功和排气冲程将化学能转化为机械能。",
                    "abs": "ABS调节制动压力以防止车轮抱死，在紧急制动时保持转向控制。",
                    "turbo": "涡轮增压器利用废气压缩进气空气，在不增加排量的情况下提升动力。",
                    "hibrido": "混合动力车结合热力发动机和电动机。制动时回收能量，降低城市油耗。",
                    "chasis": "底盘是车辆的承载结构。决定刚性、安全性和动态性能。",
                    "neumatico": "正确的轮胎压力对抓地力、均匀磨损和能效至关重要。",
                    "electrico": "电动汽车使用锂离子电池和交流电机。零直接排放和瞬时扭矩输出。"
                }
            }
        }

    def cambiar_idioma(self, nuevo_idioma):
        if nuevo_idioma in self.traducciones:
            self.idioma = nuevo_idioma
            return True
        return False

    def cambiar_tema(self, nuevo_tema):
        if nuevo_tema in self.contextos:
            self.tema = nuevo_tema
            return True
        return False

    def _limpiar_texto(self, texto):
        return re.sub(r"[^\w\s]", "", texto.lower().strip())

    # NUEVA LÓGICA DE COMANDOS (Más flexible)
    def procesar_comando(self, entrada):
        texto = self._limpiar_texto(entrada)
        lang = self.idioma
        t = self.traducciones.get(lang, {})
        prefix = t.get("response_prefix", "IA: ")

        # 1. COMANDO: HISTORIAL (Detecta si la palabra "historial" está en el texto)
        if "historial" in texto or "history" in texto or "历史" in texto:
            if not self.historial:
                return f"{prefix}{t.get('history_msg', 'Historial vacio.')}\n{prefix}Aun no hay conversaciones registradas."
            
            hist = f"{prefix}{t.get('history_msg', 'Ultimas interacciones:')}\n"
            # Muestra los últimos 10 mensajes
            for h in self.historial[-CONFIG["max_historial"]:]:
                hist += f"  {h}\n"
            return hist

        # 2. COMANDO: BORRAR (Detecta si "borrar" está en el texto)
        if "borrar" in texto or "clear" in texto or "清除" in texto:
            self.historial.clear()
            return f"{prefix}{t.get('clear_msg', 'Chat limpiado.')}"

        # 3. COMANDO: ALEATORIO
        if "aleatorio" in texto or "random" in texto or "随机" in texto:
            ctx = self.contextos.get(self.tema, {}).get(lang, [])
            if ctx:
                return f"{prefix}{t.get('random_msg', 'Dato aleatorio:')} {random.choice(ctx)}"
            return f"{prefix}No hay datos disponibles para este tema."

        # 4. COMANDO: CRÉDITOS
        if "credito" in texto or "credit" in texto or "autor" in texto or "author" in texto or "版权" in texto:
            return f"{prefix}{t.get('credits_msg', 'Proyecto 2 DAW.')}"

        # 5. COMANDOS CON PARÁMETROS (tema / idioma)
        if texto.startswith("tema ") or texto.startswith("topic ") or texto.startswith("主题 "):
            partes = texto.split()
            if len(partes) >= 2:
                nuevo = partes[1]
                mapa = {"informatica": "informatica", "it": "informatica", "serpientes": "serpientes", "coches": "coches", "cars": "coches", "计算机": "informatica", "蛇": "serpientes", "汽车": "coches"}
                if nuevo in mapa and self.cambiar_tema(mapa[nuevo]):
                    intro = t.get("theme_intros", {}).get(mapa[nuevo], "")
                    return f"{prefix}Tema cambiado a {nuevo.title()}.\n{prefix}{intro}"
                return f"{prefix}Tema no reconocido. Usa: informatica, serpientes, coches."

        if texto.startswith("idioma ") or texto.startswith("language ") or texto.startswith("语言 "):
            partes = texto.split()
            if len(partes) >= 2:
                nuevo = partes[1]
                mapa = {"es": "es", "español": "es", "spanish": "es", "en": "en", "english": "en", "ingles": "en", "zh": "zh", "chinese": "zh", "chino": "zh", "中文": "zh"}
                if nuevo in mapa and self.cambiar_idioma(mapa[nuevo]):
                    return f"{prefix}Idioma cambiado a {nuevo.upper()}."
                return f"{prefix}Idioma no reconocido. Usa: es, en, zh."

        return None  # No es un comando

    def buscar_respuesta(self, entrada):
        texto_norm = self._limpiar_texto(entrada)
        reglas_tema = self.reglas.get(self.tema, {}).get(self.idioma, {})

        for palabra, respuesta in reglas_tema.items():
            if palabra in texto_norm or texto_norm in palabra:
                return respuesta

        contextos = self.contextos.get(self.tema, {}).get(self.idioma, [])
        palabras = [p for p in texto_norm.split() if len(p) > 3]
        if palabras:
            mejor_score, mejor_frase = 0, None
            for frase in contextos:
                coincidencias = sum(1 for p in palabras if p in self._limpiar_texto(frase))
                score = coincidencias / len(palabras)
                if score > mejor_score and score >= CONFIG["umbral_similitud"]:
                    mejor_score, mejor_frase = score, frase
            if mejor_frase:
                return mejor_frase

        t = self.traducciones.get(self.idioma, {})
        return t.get("fallback", "Sin respuesta disponible.")

class ChatbotGUI:
    def __init__(self):
        self.engine = ChatbotEngine()
        self.root = tk.Tk()
        self.root.title("Chatbot Serpiente - 2 DAW")
        self.root.geometry("750x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#f0f2f5")

        self._is_typing = False
        self._snake_anim_id = None
        self._typewriter_id = None
        self._snake_frame_index = 0

        self.snake_frames = [
            ["    ___________", "   /           \\", "  |  O     O    |", "  |      ^      |", "   \\___________/", "      \\   /", "       \\ /", "        O"],
            ["    ___________", "   /           \\", "  |  O     O    |", "  |     ___     |", "   \\___________/", "      \\   /", "       \\ /", "        O"],
            ["    ___________", "   /           \\", "  |  O     O    |", "  |    (  )     |", "   \\___________/", "      \\   /", "       \\ /", "        O"]
        ]

        self._refs = {}
        self._construir_ui()
        self._mostrar_serpiente(0)
        self._actualizar_interfaz()

    def _construir_ui(self):
        frm_top = tk.Frame(self.root, bg="#f0f2f5", pady=10)
        frm_top.pack(fill=tk.X)
        self._refs["header"] = tk.Label(frm_top, text="CARGANDO...", font=("Segoe UI", 14, "bold"), bg="#f0f2f5")
        self._refs["header"].pack()

        frm_ctrl = tk.Frame(self.root, bg="#ffffff", padx=15, pady=8, relief=tk.RAISED, bd=1)
        frm_ctrl.pack(fill=tk.X, padx=10, pady=5)

        self._refs["lbl_idioma"] = tk.Label(frm_ctrl, text="Idioma:", bg="#ffffff")
        self._refs["lbl_idioma"].grid(row=0, column=0, padx=5)
        self.var_idioma = tk.StringVar()
        self.cbo_idioma = ttk.Combobox(frm_ctrl, textvariable=self.var_idioma, width=12, state="readonly")
        self.cbo_idioma.grid(row=0, column=1, padx=5)
        self.cbo_idioma.bind("<<ComboboxSelected>>", lambda e: self._cambiar_idioma_ui())

        self._refs["lbl_tema"] = tk.Label(frm_ctrl, text="Tema:", bg="#ffffff")
        self._refs["lbl_tema"].grid(row=0, column=2, padx=5)
        self.var_tema = tk.StringVar()
        self.cbo_tema = ttk.Combobox(frm_ctrl, textvariable=self.var_tema, width=12, state="readonly")
        self.cbo_tema.grid(row=0, column=3, padx=5)
        self.cbo_tema.bind("<<ComboboxSelected>>", lambda e: self._cambiar_tema_ui())

        self._refs["btn_ayuda"] = tk.Button(frm_ctrl, text="Ayuda", command=self._mostrar_ayuda, bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self._refs["btn_ayuda"].grid(row=0, column=4, padx=5)

        frm_bottom = tk.Frame(self.root, bg="#ffffff", padx=10, pady=8, bd=1, relief=tk.RAISED)
        frm_bottom.pack(fill=tk.X, side=tk.BOTTOM)

        self.var_entrada = tk.StringVar()
        self.ent_entrada = tk.Entry(frm_bottom, textvariable=self.var_entrada, font=("Segoe UI", 11), relief=tk.FLAT)
        self.ent_entrada.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.ent_entrada.bind("<Return>", lambda e: self._enviar())

        self._refs["btn_enviar"] = tk.Button(frm_bottom, text="Enviar", command=self._enviar, bg="#2980b9", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self._refs["btn_enviar"].pack(side=tk.RIGHT, padx=5)

        frm_main = tk.Frame(self.root, bg="#f0f2f5", pady=10)
        frm_main.pack(fill=tk.BOTH, expand=True, padx=10)

        frm_snake = tk.Frame(frm_main, bg="#2c3e50", width=180, height=300, bd=2, relief=tk.GROOVE)
        frm_snake.pack(side=tk.LEFT, padx=(0, 10), fill=tk.Y)
        frm_snake.pack_propagate(False)

        self.lbl_snake = tk.Label(frm_snake, text="", font=("Courier", 10), fg="#00ff00", bg="#2c3e50", justify=tk.LEFT)
        self.lbl_snake.pack(expand=True, pady=20)

        frm_respuesta = tk.Frame(frm_main, bg="#ffffff", bd=2, relief=tk.GROOVE)
        frm_respuesta.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.txt_respuesta = scrolledtext.ScrolledText(frm_respuesta, font=("Consolas", 11), state="disabled", wrap=tk.WORD, bg="#fafafa")
        self.txt_respuesta.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.root.after(200, lambda: self.ent_entrada.focus_set())

    def _mostrar_serpiente(self, frame_idx):
        self.lbl_snake.config(text="\n".join(self.snake_frames[frame_idx]))

    def _animar_serpiente(self):
        if self._is_typing:
            self._snake_frame_index = (self._snake_frame_index + 1) % len(self.snake_frames)
            self._mostrar_serpiente(self._snake_frame_index)
            self._snake_anim_id = self.root.after(250, self._animar_serpiente)

    def _detener_animacion(self):
        if self._snake_anim_id: self.root.after_cancel(self._snake_anim_id); self._snake_anim_id = None
        if self._typewriter_id: self.root.after_cancel(self._typewriter_id); self._typewriter_id = None
        self._is_typing = False
        self._mostrar_serpiente(0)

    def _actualizar_interfaz(self):
        lang = self.engine.idioma
        t = self.engine.traducciones.get(lang, {})
        ui = t.get("ui", {})
        langs = t.get("languages", {})
        topics = t.get("topics", {})

        self.root.title(ui.get("window_title", "Chatbot"))
        self._refs["header"].config(text=ui.get("header", "Chatbot"))
        self._refs["lbl_idioma"].config(text=ui.get("lang_label", "Idioma:"))
        self._refs["lbl_tema"].config(text=ui.get("topic_label", "Tema:"))
        self._refs["btn_enviar"].config(text=ui.get("send_btn", "Enviar"))
        self._refs["btn_ayuda"].config(text=ui.get("help_btn", "Ayuda"))

        self.cbo_idioma["values"] = ui.get("lang_options", [])
        self.cbo_tema["values"] = ui.get("topic_options", [])

        self.var_idioma.set(langs.get(lang, self.var_idioma.get()))
        self.var_tema.set(topics.get(self.engine.tema, self.var_tema.get()))

    def _cambiar_idioma_ui(self):
        sel = self.var_idioma.get()
        lang_map = {v: k for k, v in self.engine.traducciones[self.engine.idioma].get("languages", {}).items()}
        nuevo = lang_map.get(sel, "es")
        self.engine.cambiar_idioma(nuevo)
        self._actualizar_interfaz()
        self._escribir_en_chat(f"[Idioma cambiado a {sel}]\n")

    def _cambiar_tema_ui(self):
        sel = self.var_tema.get()
        tema_map = {v: k for k, v in self.engine.traducciones[self.engine.idioma].get("topics", {}).items()}
        nuevo = tema_map.get(sel, "informatica")
        self.engine.cambiar_tema(nuevo)
        self._actualizar_interfaz()
        self._escribir_en_chat(f"[Tema cambiado a {sel}]\n")
        intro = self.engine.traducciones.get(self.engine.idioma, {}).get("theme_intros", {}).get(nuevo, "")
        if intro:
            prefix = self.engine.traducciones.get(self.engine.idioma, {}).get("response_prefix", "IA: ")
            self._detener_animacion()
            self._is_typing = True
            self._animar_serpiente()
            self._tipo_maquina(f"{prefix}{intro}\n")

    def _mostrar_ayuda(self):
        lang = self.engine.idioma
        t = self.engine.traducciones.get(lang, {})
        prefix = t.get("response_prefix", "IA: ")
        txt = f"{prefix}{t.get('help_title', 'AYUDA')}\n{t.get('commands_list', '')}\n\n"
        self._escribir_en_chat(txt)

    def _get_prefix(self):
        return self.engine.traducciones.get(self.engine.idioma, {}).get("response_prefix", "IA: ")

    def _enviar(self):
        entrada = self.var_entrada.get().strip()
        if not entrada: return

        self.var_entrada.set("")
        user_pref = self.engine.traducciones.get(self.engine.idioma, {}).get("prompt", "Tu: ")
        self._escribir_en_chat(f"{user_pref}{entrada}\n")

        # 1. Comandos de Salida/Ayuda (Exactos)
        lower = entrada.lower()
        if lower in ["salir", "exit", "退出"]:
            self._detener_animacion()
            self._escribir_en_chat(f"{self._get_prefix()}Hasta pronto.\n")
            self.root.after(1000, self.root.destroy)
            return
        elif lower in ["ayuda", "help", "帮助"]:
            self._mostrar_ayuda()
            self.engine.historial.append(f"Tu: {entrada}")
            self.engine.historial.append(f"{self._get_prefix()}Ayuda")
            return

        # 2. Comandos Lógicos (Historial, Borrar, Aleatorio, etc.)
        # ¡CORRECCIÓN AQUÍ! Se procesan antes de guardar en historial para evitar loops
        respuesta_cmd = self.engine.procesar_comando(entrada)
        if respuesta_cmd:
            self._escribir_en_chat(f"{respuesta_cmd}\n")
            self.engine.historial.append(f"Tu: {entrada}")
            self.engine.historial.append(f"{self._get_prefix()}{respuesta_cmd.strip()}")
            return

        # 3. Búsqueda Normal (IA)
        respuesta = self.engine.buscar_respuesta(entrada)
        self._detener_animacion()
        self._is_typing = True
        self._animar_serpiente()
        self._tipo_maquina(f"{self._get_prefix()}{respuesta}\n")
        
        # Guardar en historial al final
        self.engine.historial.append(f"Tu: {entrada}")
        self.engine.historial.append(f"{self._get_prefix()}{respuesta}")

    def _escribir_en_chat(self, texto):
        self.txt_respuesta.config(state="normal")
        self.txt_respuesta.insert(tk.END, texto)
        self.txt_respuesta.see(tk.END)
        self.txt_respuesta.config(state="disabled")

    def _tipo_maquina(self, texto, delay=None, idx=0):
        if delay is None: delay = CONFIG["velocidad_escritura"]
        if idx < len(texto):
            self.txt_respuesta.config(state="normal")
            self.txt_respuesta.insert(tk.END, texto[idx])
            self.txt_respuesta.see(tk.END)
            self.txt_respuesta.config(state="disabled")
            self._typewriter_id = self.root.after(delay, self._tipo_maquina, texto, delay, idx + 1)
        else:
            self._detener_animacion()
            self.ent_entrada.focus_set()

    def ejecutar(self):
        t = self.engine.traducciones.get(self.engine.idioma, {})
        self._escribir_en_chat(f"{t.get('welcome', 'CHATBOT')}\n")
        self._escribir_en_chat(f"{t.get('prompt', 'Tu: ')}Escribe tu pregunta o un comando.\n")
        self._escribir_en_chat(f"{t.get('response_prefix', 'IA: ')}Usa 'ayuda' para ver todas las opciones.\n\n")
        self.root.mainloop()


if __name__ == "__main__":
    try:
        app = ChatbotGUI()
        app.ejecutar()
    except Exception as e:
        print(f"Error critico: {e}")
        input("Pulsa Enter para salir...")