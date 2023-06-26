from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        comando_env = request.form.get('comando_escrito')
        print('El comando enviado es '+comando_env)
    return render_template('interfaz.html')