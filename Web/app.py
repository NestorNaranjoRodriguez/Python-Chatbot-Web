# /Web/app.py
from flask import Flask, render_template, request, jsonify
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Chatbot'))
from chatbot_engine import ChatbotEngine

app = Flask(__name__, static_folder='public', static_url_path='/public')

bot_engine = ChatbotEngine(base_path=os.path.join(os.path.dirname(__file__), '..', 'Chatbot'))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/chatbot')
def pagina_chatbot():
    return render_template('chatbot.html')

@app.route('/saludo')
def saludo():
    return 'Hola'

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    mensaje = data.get('mensaje', '')
    
    resultado = bot_engine.procesar_mensaje(mensaje)
    
    if resultado.get('tipo') != 'salida':
        bot_engine.historial.append(f"Tu: {mensaje}")
        bot_engine.historial.append(f"IA: {resultado.get('respuesta', '')}")
    
    return jsonify(resultado)

@app.route('/api/config', methods=['GET'])
def api_get_config():
    return jsonify({
        "idioma": bot_engine.idioma,
        "tema": bot_engine.tema,
        "traducciones": bot_engine.traducciones.get(bot_engine.idioma, {})
    })

@app.route('/api/config', methods=['POST'])
def api_set_config():
    data = request.get_json()
    if 'idioma' in data:
        bot_engine.cambiar_idioma(data['idioma'])
    if 'tema' in data:
        bot_engine.cambiar_tema(data['tema'])
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)