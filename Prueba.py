import os
import os.path
from shutil import rmtree
import regex as re

dir_origen = "./Archivos"
#------------------------------------------------------------FUNCIONES DE COMANDOS---------------------------------------------------------
def fun_crear(nombre_archivo,contenido_archivo,ruta_archivo,tipo_accion):
    tipo = tipo_accion.lower()
    #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
    if(tipo == "server"):
        ruta_archivo_limpia = limpiar_ruta(ruta_archivo)
        #Se crean las carpetas necesarias
        crear_carpeta(ruta_archivo_limpia)
        #Creacion de archivo
        if os.path.exists(ruta_archivo_limpia+nombre_archivo):
            nombre_archivo = nombre_archivo+"(1)"
        f = open(ruta_archivo_limpia+nombre_archivo,"x")
        f.write(contenido_archivo)
        f.close()
    #CODIGO EN CASO DE QUE SE EJECUTE EN BUCKET

def fun_eliminar(ruta_archivo,nombre_archivo,tipo_accion):
    tipo = tipo_accion.lower()
    #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
    if(tipo == "server"):
        ruta_archivo_limpia = limpiar_ruta(ruta_archivo)
        ruta_eliminar = ruta_archivo_limpia+nombre_archivo
        if os.path.exists(ruta_eliminar):
            if os.path.isfile(ruta_eliminar):
                os.remove(ruta_eliminar)
            else:
                rmtree(ruta_eliminar)
    #CODIGO EN CASO DE QUE SE EJECUTE EN BUCKET
#-----------------------------------------------------------FUNCIONES COMPLEMENTARIAS---------------------------------------------------------
def limpiar_ruta(ruta_archivo):
    partes = ruta_archivo.split("/")
    nuevas_partes = [x for x in partes if x != '']
    ruta_limpia = dir_origen+"/"
    for x in nuevas_partes:
        if "\"" in x:
            x = x.replace('\"','')
        if not re.search(".*\.txt",x):
            ruta_limpia = ruta_limpia+x+"/"
        else:
            ruta_limpia = ruta_limpia+x
    return ruta_limpia

def crear_carpeta(ruta):
    partes = ruta.split("/")
    nueva_partes = [x for x in partes if x != '']
    rta = ""
    for x in nueva_partes:
        rta=rta+x+"/"
        if not os.path.exists(rta) and not re.search(".*\.txt",x):
            os.makedirs(rta)

#fun_crear("archivo_n.txt","contenido_archivo","/carpeta1","server")
fun_eliminar("/carpeta1","","server")