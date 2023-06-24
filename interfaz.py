import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os.path
import os

coordenada_x = 0
coordenada_y = 0

usuario_nombre_logueado = ""
usuario_contrasenia_logueado = ""
global llave_enc
llave_enc = ""
#PARAMETROS QUE ALMACENARÁN LOS VALORES DE LA OP CONFIG

def generar_pantalla_login():
    
    pantalla1.withdraw()
    pantallaLogin = tk.Tk()    
    pantallaLogin.title("Proyecto MIA 1 login")
    pantallaLogin.resizable(False,False)
    ancho_monitor_login = pantalla1.winfo_screenwidth()
    alto_monitor_login = pantalla1.winfo_screenheight()
    coordenada_x_login = (ancho_monitor_login - 500) // 2
    coordenada_y_login = (alto_monitor_login - 320) // 2  
    pantallaLogin.geometry(f"{500}x{320}+{coordenada_x_login}+{coordenada_y_login}")       

    etiqueta_titulo = tk.Label(pantallaLogin, text="Ingrese un usuario y password valido!")
    etiqueta_titulo.place(x=50, y=45)

    etiqueta_campo_usuario = tk.Label(pantallaLogin, text="Usuario:")
    etiqueta_campo_usuario.place(x=50, y=115)

    campo_usuario = tk.Entry(pantallaLogin, width=55)
    campo_usuario.place(x=110, y=115)
    #campo_usuario.grid(row=2, column=3)
    #campo_usuario.pack()

    etiqueta_campo_contrasenia = tk.Label(pantallaLogin, text="Password:")
    etiqueta_campo_contrasenia.place(x=50, y=165)

    campo_contrasenia = tk.Entry(pantallaLogin, show="*", width=55)
    campo_contrasenia.place(x=110, y=165)
    #campo_contrasenia.grid(row=4, column=3)
    #campo_contrasenia.pack()

    #print("cadena para analizar")
    #entrada = "exec -path->/home/Desktop/calificacion.mia modify -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\" add -path->/carpeta1/prueba1.txt -body->\" este es el nuevo contenido del archivo\""
    #resultado = analizadorEntrada.parser.parse(entrada, lexer=analizadorEntrada.lexer)
    #print("Resultado: {}".format(resultado))

    def ir_a_pantalla_principal():
        pantallaLogin.destroy()
        pantalla1.deiconify()  
            

        

    boton = tk.Button(pantallaLogin, text="Ir a pantalla principal", command=ir_a_pantalla_principal, width=55)
    boton.place(x=50, y=215)
    #boton.grid(row=6, column=3)
    #boton.pack()


    pantalla_comando_delete = tk.Toplevel(pantalla1)
    pantalla_comando_delete.title("Comando \"Delete\"")
    pantalla_comando_delete.resizable(False,False)
    ancho_monitor_comando = pantalla1.winfo_screenwidth() 
    alto_monitor_comando = pantalla1.winfo_screenheight()
    coordenada_x_comando = (ancho_monitor_comando - 500) // 2
    coordenada_y_comando = (alto_monitor_comando - 320) // 2  
    pantalla_comando_delete.geometry(f"{500}x{320}+{coordenada_x_comando}+{coordenada_y_comando}")   

    etiqueta_titulo = tk.Label(pantalla_comando_delete, text="Ingrese los parametros para el comando \"Delete\"")
    etiqueta_titulo.place(x=50, y=15)    

    etiqueta_campo_path = tk.Label(pantalla_comando_delete, text="-path (*)")
    etiqueta_campo_path.place(x=50, y=55)

    campo_path = tk.Entry(pantalla_comando_delete, width=45)
    campo_path.place(x=155, y=55)

    etiqueta_campo_name = tk.Label(pantalla_comando_delete, text="-name")
    etiqueta_campo_name.place(x=50, y=105)

    campo_name = tk.Entry(pantalla_comando_delete, width=45)
    campo_name.place(x=155, y=105)
    
def generar_pantalla_principal():

    pantalla  = tk.Tk()
    pantalla.title("Proyecto MIA 1")
    pantalla.geometry("1000x600")
    pantalla.resizable(False,False)  

    etiqueta_entrada = tk.Label(pantalla, text="Ingrese un comando:")
    etiqueta_entrada.place(x=45, y=10)

    entrada = tk.Entry(pantalla, width=90)
    entrada.place(x=47, y=30)
    entrada.focus() 

    def ejetular_linea_entrada():
        pass

    boton_ejecutar = tk.Button(pantalla, command=generar_pantalla_login, text="Ejecutar", width=30)
    boton_ejecutar.place(x = 625, y = 25)

    boton_generar_reporte = tk.Button(pantalla, command=generar_pantalla_login, text="Cargar", width=30)
    boton_generar_reporte.place(x = 625, y = 75)

    boton_cargar_archivo = tk.Button(pantalla, command=generar_pantalla_login, text="Reporte", width=30)
    boton_cargar_archivo.place(x = 625, y = 125)


    boton_cerrar_secion = tk.Button(pantalla, command=generar_pantalla_login, text="Cerrar sesion", width=30)
    boton_cerrar_secion.place(x = 625, y = 545)

    return pantalla

pantalla1 = generar_pantalla_principal()
ancho_monitor = pantalla1.winfo_screenwidth()
alto_monitor = pantalla1.winfo_screenheight()
coordenada_x = (ancho_monitor - 872) // 2
coordenada_y = (alto_monitor - 600) // 2
pantalla1.geometry(f"{872}x{600}+{coordenada_x}+{coordenada_y}")

area_de_inputs = tk.Text(pantalla1, height=15, width=68)
area_de_inputs.config(state="disabled")
area_de_inputs.place(x=45, y=75)
area_de_inputs['state'] = 'normal'

area_de_respuestas = tk.Text(pantalla1, height=15, width=68)
area_de_respuestas.config(state="disabled")
area_de_respuestas.place(x=45, y=325)
area_de_respuestas['state'] = 'normal'

def main():  
    #generar_pantalla_login()
    pantalla1.mainloop()
main()