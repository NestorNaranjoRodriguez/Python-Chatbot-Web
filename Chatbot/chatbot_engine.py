import os
import json
import re
import random

CONFIG = {
    "archivo_traducciones": "translations.json",
    "archivo_contextos": "contextos.json",
    "umbral_similitud": 0.6,
    "max_historial": 10,
    "idioma_defecto": "es",
    "tema_defecto": "informatica",
}

class ChatbotEngine:
    def __init__(self, base_path="."):
        self.base_path = base_path
        self.idioma = CONFIG["idioma_defecto"]
        self.tema = CONFIG["tema_defecto"]
        self.historial = []
        self.traducciones = self._cargar_json(CONFIG["archivo_traducciones"], self._traducciones_minimas())
        self.contextos = self._cargar_json(CONFIG["archivo_contextos"], self._contextos_minimos())
        self.reglas = self._inicializar_reglas()

    def _cargar_json(self, ruta, fallback):
        ruta_completa = os.path.join(self.base_path, ruta)
        if os.path.exists(ruta_completa):
            try:
                with open(ruta_completa, "r", encoding="utf-8") as f:
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
                    "python": "Python es un lenguaje interpretado, multiparadigma y de tipado dinamico.",
                    "html": "HTML define la estructura semantica de una pagina web.",
                    "ram": "La RAM es memoria volatil. Almacena datos activos mientras el sistema esta encendido.",
                    "cpu": "La CPU ejecuta instrucciones del software. Su velocidad se mide en GHz.",
                    "git": "Git es un sistema de control de versiones distribuido.",
                    "api": "Una API permite que dos softwares se comuniquen mediante protocolos estandar.",
                    "sql": "SQL es el lenguaje estandar para gestionar bases de datos relacionales."
                },
                "en": {
                    "hello": "Hello. I am your technical assistant. Which area do you need help with?",
                    "python": "Python is an interpreted, multi-paradigm, dynamically typed language.",
                    "html": "HTML defines the semantic structure of a web page.",
                    "ram": "RAM is volatile memory. It stores active data while the system is on.",
                    "cpu": "The CPU executes software instructions. Speed is measured in GHz.",
                    "git": "Git is a distributed version control system.",
                    "api": "An API allows two software systems to communicate via standard protocols.",
                    "sql": "SQL is the standard language for managing relational databases."
                },
                "zh": {
                    "你好": "你好。我是您的技术助手。您需要哪方面的帮助？",
                    "python": "Python是一种解释型、多范式、动态类型语言。",
                    "html": "HTML定义网页的语义结构。",
                    "ram": "RAM是易失性内存。在系统运行时存储活动数据。",
                    "cpu": "CPU执行软件指令。速度以GHz衡量。",
                    "git": "Git是一个分布式版本控制系统。",
                    "api": "API允许两个软件系统通过标准协议进行通信。",
                    "sql": "SQL是管理关系数据库的标准语言。"
                }
            },
            "serpientes": {
                "es": {
                    "hola": "Hola. ¿Interesado en herpetologia? Puedo hablar sobre anatomia, ecologia o peligrosidad.",
                    "veneno": "El veneno puede ser neurotoxico, hemotoxico o citotoxico.",
                    "muda": "La muda ocurre varias veces al año. La piel vieja se desprende en una sola pieza.",
                    "cobra": "La cobra real es la serpiente venenosa mas larga del mundo.",
                    "boa": "Las boas y pitones son constrictoras. No tienen veneno.",
                    "sentidos": "Las serpientes perciben vibraciones y calor mediante fosetas loreales.",
                    "hibernacion": "En climas frios, muchas serpientes entran en brumacion."
                },
                "en": {
                    "hello": "Hello. Interested in herpetology? I can discuss anatomy, ecology, or venom.",
                    "venom": "Venom can be neurotoxic, hemotoxic, or cytotoxic.",
                    "shed": "Shedding happens several times a year. Old skin comes off in one piece.",
                    "cobra": "The king cobra is the longest venomous snake.",
                    "boa": "Boas and pythons are constrictors. They lack venom.",
                    "senses": "Snakes detect vibrations and heat via loreal pits.",
                    "hibernation": "In cold climates, many snakes enter brumation."
                },
                "zh": {
                    "你好": "你好。对爬行动物学感兴趣吗？我可以讨论解剖学、生态学或毒性。",
                    "veneno": "毒液可分为神经毒素、血液毒素或细胞毒素。",
                    "muda": "蜕皮每年发生多次。旧皮整片脱落。",
                    "cobra": "眼镜王蛇是最长的毒蛇。",
                    "boa": "蟒蛇和蚺蛇是绞杀型。它们没有毒液。",
                    "sentidos": "蛇通过地面振动和颊窝感知热量。",
                    "hibernacion": "在寒冷气候中，许多蛇进入冬眠状态。"
                }
            },
            "coches": {
                "es": {
                    "hola": "Hola. ¿Buscas informacion tecnica o historica sobre automoviles?",
                    "motor": "El motor transforma energia quimica en mecanica mediante ciclos.",
                    "abs": "El ABS modula la presion de frenado para evitar que las ruedas se bloqueen.",
                    "turbo": "El turbocompresor usa gases de escape para comprimir aire de admision.",
                    "hibrido": "Un hibrido combina motor termico y electrico.",
                    "chasis": "El chasis es la estructura portante del vehiculo.",
                    "neumatico": "La presion correcta de los neumaticos es crucial para adherencia.",
                    "electrico": "Los vehiculos electricos usan baterias de ion-litio."
                },
                "en": {
                    "hello": "Hello. Looking for technical or historical car info?",
                    "engine": "The engine converts chemical energy into mechanical work.",
                    "abs": "ABS modulates brake pressure to prevent wheel lockup.",
                    "turbo": "A turbocharger uses exhaust gases to compress intake air.",
                    "hybrid": "A hybrid combines thermal and electric motors.",
                    "chassis": "The chassis is the vehicle's load-bearing structure.",
                    "tire": "Correct tire pressure is crucial for grip.",
                    "electric": "Electric vehicles use lithium-ion batteries."
                },
                "zh": {
                    "你好": "你好。寻找汽车技术或历史信息吗？",
                    "motor": "内燃机将化学能转化为机械能。",
                    "abs": "ABS调节制动压力以防止车轮抱死。",
                    "turbo": "涡轮增压器利用废气压缩进气空气。",
                    "hibrido": "混合动力车结合热力发动机和电动机。",
                    "chasis": "底盘是车辆的承载结构。",
                    "neumatico": "正确的轮胎压力对抓地力至关重要。",
                    "electrico": "电动汽车使用锂离子电池。"
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

    def procesar_comando(self, entrada):
        texto = self._limpiar_texto(entrada)
        lang = self.idioma
        t = self.traducciones.get(lang, {})
        prefix = t.get("response_prefix", "IA: ")

        if "historial" in texto or "history" in texto or "历史" in texto:
            if not self.historial:
                return f"{prefix}{t.get('history_msg', 'Historial vacio.')}\n{prefix}Aun no hay conversaciones registradas."
            hist = f"{prefix}{t.get('history_msg', 'Ultimas interacciones:')}\n"
            for h in self.historial[-CONFIG["max_historial"]:]:
                hist += f"  {h}\n"
            return hist

        if "borrar" in texto or "clear" in texto or "清除" in texto:
            self.historial.clear()
            return f"{prefix}{t.get('clear_msg', 'Chat limpiado.')}"

        if "aleatorio" in texto or "random" in texto or "随机" in texto:
            ctx = self.contextos.get(self.tema, {}).get(lang, [])
            if ctx:
                return f"{prefix}{t.get('random_msg', 'Dato aleatorio:')} {random.choice(ctx)}"
            return f"{prefix}No hay datos disponibles para este tema."

        if "credito" in texto or "credit" in texto or "autor" in texto or "author" in texto or "版权" in texto:
            return f"{prefix}{t.get('credits_msg', 'Proyecto 2 DAW.')}"

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

        return None

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

    def procesar_mensaje(self, entrada):
        entrada = entrada.strip()
        if not entrada:
            return {"error": "Entrada vacía"}

        lower = entrada.lower()
        if lower in ["salir", "exit", "退出"]:
            return {"respuesta": "Hasta pronto.", "tipo": "salida"}
        elif lower in ["ayuda", "help", "帮助"]:
            lang = self.idioma
            t = self.traducciones.get(lang, {})
            return {"respuesta": f"{t.get('help_title', 'AYUDA')}\n{t.get('commands_list', '')}", "tipo": "ayuda"}

        respuesta_cmd = self.procesar_comando(entrada)
        if respuesta_cmd:
            return {"respuesta": respuesta_cmd, "tipo": "comando"}

        respuesta = self.buscar_respuesta(entrada)
        return {"respuesta": respuesta, "tipo": "respuesta"}