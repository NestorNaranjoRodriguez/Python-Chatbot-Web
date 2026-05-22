# Chat demo — Chatbot sobre serpientes

Instrucciones rápidas para ejecutar la app localmente.

1. Ejecutar la aplicación:

```powershell
python Chatbot.py
```

2. Comandos a ejecutar:

---

## Comandos Generales (Independientes del tema)

Estos comandos funcionan en cualquier temática seleccionada.

| Función          | Español       | English   | 中文   | Descripción                                      |
|------------------|---------------|-----------|--------|--------------------------------------------------|
| Salir            | `salir`       | `exit`    | `退出` | Finaliza la sesión o muestra mensaje de despedida|
| Ayuda            | `ayuda`       | `help`    | `帮助` | Muestra esta guía de comandos                    |
| Ver Historial    | `historial`   | `history` | `历史` | Muestra las últimas 10 interacciones             |
| Limpiar Historial| `borrar`      | `clear`   | `清除` | Vacía la memoria de conversación                 |
| Dato Aleatorio   | `aleatorio`   | `random`  | `随机` | Devuelve una frase aleatoria del contexto actual |
| Créditos         | `credito`, `autor` | `credit`, `author` | `版权` | Muestra información del proyecto                 |
| Cambiar Tema     | `tema <valor>`| `topic <value>` | `主题 <值>` | Cambia la temática activa (ver tabla inferior)   |
| Cambiar Idioma   | `idioma <valor>` | `language <value>` | `语言 <值>` | Cambia el idioma de respuesta (ver tabla inferior) |

### Valores válidos para parámetros

| Parámetro | Español        | English        | 中文           |
|-----------|----------------|----------------|----------------|
| **Tema**  | `informatica`, `serpientes`, `coches` | `it`, `snakes`, `cars` | `计算机`, `蛇`, `汽车` |
| **Idioma**| `es`, `español`| `en`, `english`| `zh`, `中文`   |

---

## Tema: Informática / IT / 计算机

Palabras clave técnicas para hardware, software y desarrollo web.

| Categoría          | Español    | English | 中文   | Ejemplo de respuesta (ES)                                  |
|--------------------|------------|---------|--------|------------------------------------------------------------|
| Saludo             | `hola`     | `hello` | `你好` | Asistente técnico listo para ayudar                        |
| Lenguaje Python    | `python`   | `python`| `python` | Lenguaje interpretado, multiparadigma, tipado dinámico     |
| Estructura Web     | `html`     | `html`  | `html` | Define la estructura semántica de páginas web              |
| Memoria Volátil    | `ram`      | `ram`   | `ram`  | Almacena datos activos mientras el sistema está encendido  |
| Procesador         | `cpu`      | `cpu`   | `cpu`  | Ejecuta instrucciones del software (medida en GHz)         |
| Control Versiones  | `git`      | `git`   | `git`  | Sistema distribuido para seguimiento de cambios            |
| Interfaces         | `api`      | `api`   | `api`  | Protocolo estándar de comunicación entre softwares         |
| Bases de Datos     | `sql`      | `sql`   | `sql`  | Lenguaje estándar para gestionar bases relacionales        |

---

## Tema: Serpientes / Snakes / 蛇

Palabras clave sobre biología, anatomía y comportamiento reptil.

| Categoría          | Español      | English  | 中文     | Ejemplo de respuesta (ES)                                  |
|--------------------|--------------|----------|----------|------------------------------------------------------------|
| Saludo             | `hola`       | `hello`  | `你好`   | Enfoque en herpetología, anatomía y ecología               |
| Sustancia Tóxica   | `veneno`     | `venom`  | `毒液`   | Neurotóxico, hemotóxico o citotóxico                       |
| Renovación Piel    | `muda`       | `shed`   | `蜕皮`   | Ecdisis periódica para permitir el crecimiento             |
| Especie Real       | `cobra`      | `cobra`  | `眼镜蛇` | Serpiente venenosa más larga (hasta 5.5 m)                 |
| Constrictoras      | `boa`        | `boa`    | `蟒蛇`   | Subyugan presas por enrollamiento, sin veneno              |
| Percepción         | `sentidos`   | `senses` | `感官`   | Vibraciones del suelo y calor mediante fosetas loreales    |
| Estado Invernal    | `hibernacion`| `hibernation` | `冬眠` | Brumación para conservación energética                     |

---

## Tema: Coches / Cars / 汽车

Palabras clave sobre mecánica automotriz, seguridad e historia.

| Categoría          | Español      | English  | 中文     | Ejemplo de respuesta (ES)                                  |
|--------------------|--------------|----------|----------|------------------------------------------------------------|
| Saludo             | `hola`       | `hello`  | `你好`   | Información técnica o histórica disponible                 |
| Propulsión         | `motor`      | `engine` | `发动机` | Conversión de energía química a mecánica por ciclos        |
| Frenado Seguro     | `abs`        | `abs`    | `abs`    | Modula presión para evitar bloqueo de ruedas               |
| Admisión Forzada   | `turbo`      | `turbo`  | `涡轮`   | Compresión de aire usando gases de escape                  |
| Propulsión Mixta   | `hibrido`    | `hybrid` | `混合动力`| Combina motor térmico y eléctrico                          |
| Estructura         | `chasis`     | `chassis`| `底盘`   | Define rigidez, seguridad y comportamiento dinámico        |
| Contacto Suelo     | `neumatico`  | `tire`   | `轮胎`   | Presión correcta esencial para adherencia y desgaste       |
| Propulsión Limpia  | `electrico`  | `electric`| `电动`  | Baterías de ion-litio, cero emisiones directas             |

---

## Orden de Procesamiento (Prioridad)

1. **Comandos exactos**: `salir`, `ayuda` → Ejecución inmediata.
2. **Comandos con parámetros**: `tema X`, `idioma Y` → Cambio de configuración.
3. **Comandos de gestión**: `historial`, `borrar`, `aleatorio` → Acciones sobre memoria/contexto.
4. **Palabras clave del tema**: Búsqueda exacta o contención en las reglas activas.
5. **Similitud léxica**: Comparación con frases de contexto (umbral `≥ 0.6`).
6. **Fallback**: Respuesta por defecto si no hay coincidencias.

---

## Ejemplos de Interacción

### Español (Tema: Informática)
```text
Tu: hola
IA: Hola. Soy tu asistente técnico. ¿En qué área necesitas ayuda?
Tu: ¿qué es python?
IA: Python es un lenguaje interpretado, multiparadigma y de tipado dinámico...
Tu: tema serpientes
IA: Tema cambiado a Serpientes.
IA: Bienvenido al área de Serpientes. Consulta sobre especies...

```
La app quedará disponible en http://127.0.0.1:5000/ y la ruta del chatbot en `/chatbot`.