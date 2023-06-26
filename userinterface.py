from flask import Flask, render_template,request,redirect
import LoginLogic 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form.get('username')
        contrasenia = request.form.get('password')
        if(LoginLogic.comprobacion_usuario(usuario,contrasenia)):
            return redirect('/app')
    return render_template('auth/login.html')

@app.route('/app', methods=['GET', 'POST'])
def app_view():
    if request.method == 'POST':
        comando_env = request.form.get('comando_escrito')
        print('El comando enviado es '+comando_env) 
    return render_template('interfaz.html')