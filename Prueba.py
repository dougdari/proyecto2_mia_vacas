import os
import os.path
from shutil import rmtree
import shutil
import regex as re

dir_origen = "./Archivos"
#------------------------------------------------------------FUNCIONES DE COMANDOS---------------------------------------------------------
def fun_crear(nombre_archivo,contenido_archivo,ruta_archivo,):
    #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
    ruta_archivo_limpia = limpiar_ruta(ruta_archivo)
    #Se crean las carpetas necesarias
    crear_carpeta(ruta_archivo_limpia)
    #Creacion de archivo
    if os.path.exists(ruta_archivo_limpia+nombre_archivo):
        nombre_archivo = nombre_archivo+"(1)"
    f = open(ruta_archivo_limpia+nombre_archivo,"x")
    f.write(contenido_archivo)
    f.close()

def fun_eliminar(ruta_archivo,nombre_archivo):
    #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
    ruta_archivo_limpia = limpiar_ruta(ruta_archivo)
    ruta_eliminar = ruta_archivo_limpia+nombre_archivo
    if os.path.exists(ruta_eliminar):
        if os.path.isfile(ruta_eliminar):
            os.remove(ruta_eliminar)
        else:
            rmtree(ruta_eliminar)

def fun_copiar(ruta_origen,ruta_destino,tipo_destino):
    tipo = tipo_destino.lower()
    ruta_origen_limpia = limpiar_ruta(ruta_origen)
    ruta_destino_limpia = limpiar_ruta(ruta_destino)
    if tipo == "server":
        if os.path.exists(ruta_origen_limpia) and os.path.exists(ruta_destino_limpia):
            #Se determina si la ruta de origen corresponde a la de un archivo o carpeta
            if os.path.isfile(ruta_origen_limpia):
                #Se obiene el nombre del archivo
                partes = ruta_origen_limpia.split("/")
                nueva_partes = [x for x in partes if x != '']
                for x in nueva_partes:
                    if re.search(".*\.txt",x):
                        nombre_archivo = x
                        break
                shutil.copyfile(ruta_origen_limpia,ruta_destino_limpia+nombre_archivo)
            else:
                shutil.copytree(ruta_origen_limpia,ruta_destino_limpia)

def fun_transferir(ruta_origen,ruta_destino,tipo_destino):
    tipo = tipo_destino.lower()
    nombre_archivo = ""
    ruta_origen_limpia = limpiar_ruta(ruta_origen)
    ruta_destino_limpia = limpiar_ruta(ruta_destino)
    if tipo == "server":
        if os.path.exists(ruta_origen_limpia) and os.path.exists(ruta_destino_limpia):
            #Se determina si la ruta de origen corresponde a la de un archivo o carpeta
            if os.path.isfile(ruta_origen_limpia):
                #Se obiene el nombre del archivo
                partes = ruta_origen_limpia.split("/")
                nueva_partes = [x for x in partes if x != '']
                for x in nueva_partes:
                    if re.search(".*\.txt",x):
                        nombre_archivo = x
                        break
            shutil.move(ruta_origen_limpia,ruta_destino_limpia+nombre_archivo)

def fun_renombrar(ruta,nuevo_nombre):
    #Se limpia la ruta en caso alguna parte tenga doble comilla
    nueva_ruta = limpiar_ruta(ruta)
    #Se reestructura la ruta para el nuevo nombre
    partes = nueva_ruta.split("/")
    nueva_partes = [x for x in partes if x != '']
    rta = ""
    for x in nueva_partes:
        if not re.search(".*\.txt",x):
            rta=rta+x+"/"
        else:
            dir_carpeta = rta
            rta+=nuevo_nombre
            break
    continuar = True
    if os.path.exists(nueva_ruta):
        #Se compara archivo existentes para verificar si no se repiten
        for x in os.listdir(dir_carpeta):
            if(x == nuevo_nombre):
                continuar = False
                break
        if continuar:
            os.rename(nueva_ruta,rta)
        else:
            print("Imposible Renombrar, Existe un Archivo con el mismo nombre")
    else:
        print("Imposible de Renombrar, El Directorio o Archivo No Existe")

def fun_modificar(ruta,nuevo_contenido):
    #Se limpia la ruta en caso alguna parte tenga doble comilla
    nueva_ruta = limpiar_ruta(ruta)
    if os.path.exists(nueva_ruta):
        f = open(nueva_ruta,"w")
        f.write(nuevo_contenido)
        f.close()
    else:
        print("El Directorio o Archivo No Existe")

def fun_eliminar_todo():
    for filename in os.listdir(dir_origen+"/"):
        ruta = os.path.join(dir_origen+"/",filename)
        try:
            if os.path.isfile(ruta) or os.path.islink(ruta):
                os.unlink(ruta)
            elif os.path.isdir(ruta):
                rmtree(ruta)
        except Exception as e:
            print("Error "+e)

#-----------------------------------------------------------FUNCIONES COMPLEMENTARIAS-----  ----------------------------------------------------
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

#fun_transferir("/carpeta1","/carpeta2","server")
#fun_crear("archivo_n.txt","contenido_archivo","/carpeta1")
#fun_eliminar("/carpeta1","")
#fun_renombrar("/carpeta1/archivo_n.txt","archivo_renombre.txt")
#fun_modificar("/carpeta1/archivo_renombre.txt","Nuevo contenido")
#fun_eliminar_todo()