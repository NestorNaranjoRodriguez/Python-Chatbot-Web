from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('index.html')


@app.route('/chatbot')
def chatbot():
    # Aquí integrarás tu chatbot existente
    return render_template('chatbot.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
