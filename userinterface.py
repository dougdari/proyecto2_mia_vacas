from flask import Flask, render_template,request,redirect
import LoginLogic
import analizadorEntrada
import gestor
import requests
import comandos_bucket_server
import json
import stringify

app = Flask(__name__)

@app.route('/app', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        usuario = request.form.get('username')
        contrasenia = request.form.get('password')
        if(LoginLogic.comprobacion_usuario(usuario,contrasenia)):
            return redirect('/app')
    return render_template('auth/login.html')

@app.route('/', methods=['GET', 'POST'])
def app_view():

    if request.method == 'POST':
        #Lecutra comando individual

        comando_env = ''
        comando_env = request.form.get('comando_escrito')
        analizadorEntrada.comandos = []

        contenido_archivo = ''

        resultado = analizadorEntrada.parser.parse(str(comando_env), lexer=analizadorEntrada.lexer)
        for comando in analizadorEntrada.comandos:
            print(comando)

        file = request.files['myfile']
        if file.filename != '':
            # Guardar el archivo en el sistema de archivos
            file.save(file.filename)
            
            # Leer el contenido del archivo
            with open(file.filename, 'r') as f:

                contenido_archivo = f.read()
            analizadorEntrada.comandos = []
            resultado = analizadorEntrada.parser.parse(str(contenido_archivo), lexer=analizadorEntrada.lexer)
            gestor.ejecutar_comandos(analizadorEntrada.comandos)

        
        #en esta parte se van consumir todos los endpoints

        if len(str(comando_env)) > 0 :
            print('comando ingresado por linea')
            print(comando_env)

            if len(analizadorEntrada.comandos) > 0:
                print(analizadorEntrada.comandos[0])

            
    return render_template('interfaz.html')

@app.route('/recovery/<type>/<filename>')
def recover_json(type,filename):
    if type == "bucket":
        data = comandos_bucket_server.json_backup_bucket('/Archivos/',filename)
    elif type == "server":
       data = comandos_bucket_server.json_backup_local('.Archivos/',filename)
    return data

@app.route('/backup/<type>')
def backup_json(type,filename):
    if type == "bucket":
        #data = comandos_bucket_server.json_backup_bucket('/Archivos/',filename)
        data = ''
        print('backup','bucket')
    elif type == "server":
        #data = comandos_bucket_server.json_backup_local('.Archivos/',filename)
        print('backup','server')
        data = ''
    return data
        

@app.route('/open/<type>/<filename>')
def open_json(type,filename):
    if type == "bucket":
        #data = comandos_bucket_server.json_backup_bucket('/Archivos/',filename)
        print('open','bucket')
        data = ''
    elif type == "server":
        #data = comandos_bucket_server.json_backup_local('.Archivos/',filename)
        print('open','server')
        data = ''
    return data

    

if __name__ == '__main__':
    app.run()

