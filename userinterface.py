from flask import Flask, render_template,request,redirect,Response
import LoginLogic
import analizadorEntrada
import gestor
import requests
import comandos_bucket_server
import json
import stringify

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
            
    return render_template('interfaz.html')

@app.route('/recovery/<type>/<filename>')
def recover_json(type,filename):
    if type == "bucket":
        data = comandos_bucket_server.json_backup_bucket('Archivos/',filename)
    elif type == "server":
       data = comandos_bucket_server.json_backup_local('./Archivos/',filename)
    return data

@app.route('/backup/<type>',methods=['POST'])
def backup_json(type):
    if request.method == 'POST':
        if type == "server":
            info = request.get_json()
            if info:
                comandos_bucket_server.leer_json_a_local(info,'./Archivos')
            else:
                print("NO HAY NADA QUE ESCRIBIR")
        else:
            info = request.get_json()
            if info:
                comandos_bucket_server.leer_json_a_bucket(info,'Archivos')
            else:
                print("NO HAY NADA QUE ESCRIBIR")
    
        

@app.route('/open/<type>/<filename>')
def open_json(type,filename):
    if type == "bucket":
        data = comandos_bucket_server.json_open_bucket(filename)
    elif type == "server":
        data = comandos_bucket_server.json_open_local(filename)
    return data

    

if __name__ == '__main__':
    app.run()

