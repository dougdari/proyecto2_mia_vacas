from flask import Flask, render_template,request,redirect
import LoginLogic
import analizadorEntrada
import gestor

app = Flask(__name__)

@app.route('/s', methods=['GET', 'POST'])
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
        #comando_env = request.form.get('comando_escrito')
        #analizadorEntrada.comandos = []
        #resultado = analizadorEntrada.parser.parse(str(comando_env), lexer=analizadorEntrada.lexer)
        #for comando in analizadorEntrada.comandos:
            #print(comando)
        #Lectura archivo
        file = request.files['myfile']
        if file.filename != '':
            # Guardar el archivo en el sistema de archivos
            file.save(file.filename)
            
            # Leer el contenido del archivo
            with open(file.filename, 'r') as f:
                contenido = f.read()
            analizadorEntrada.comandos = []
            resultado = analizadorEntrada.parser.parse(str(contenido), lexer=analizadorEntrada.lexer)
            gestor.ejecutar_comandos(analizadorEntrada.comandos)

    return render_template('interfaz.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=22)