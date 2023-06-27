import os
import shutil
import boto3
import regex as re
from shutil import rmtree
import shutil

nombre_bucket_s3 = 'proyecto-2-mia'
dir_origen = "./Archivos"
objeto_s3 = boto3.client('s3')
session = boto3.Session()
s3_resource = session.resource('s3')

def crear_directorio_archivo(nombre,destino,contenido,tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
        destino = "/Archivos"+destino
        destino = destino.replace('"','')
        directorios = destino.split('/')
        ruta_directorio = ''

        for directorio in directorios:
            if directorio:
                ruta_directorio += directorio + '/'
                objeto_s3.put_object(Bucket=nombre_bucket_s3, Key=ruta_directorio)

        ruta_archivo = ruta_directorio + nombre
        objeto_s3.put_object(Body=contenido, Bucket=nombre_bucket_s3, Key=ruta_archivo)

        print("nuevo archivo creado ",nombre)
    else:
        #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
        ruta_archivo_limpia = limpiar_ruta(destino)
        #Se crean las carpetas necesarias
        crear_carpeta(ruta_archivo_limpia)
        #Creacion de archivo
        if os.path.exists(ruta_archivo_limpia+nombre):
            nombre = nombre+"(1)"
        f = open(ruta_archivo_limpia+nombre,"x")
        f.write(contenido)
        f.close()

def verificar_directorio(directorio):

    directorio = directorio.replace('"','')
    if directorio[0] == '/':
            directorio = directorio[ 1:len(directorio)]

    peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=directorio, MaxKeys=1)
    comprobacion = 'Contents' in peticion

    return comprobacion

def verificar_archivo_dentro_directorio(archivo, directorio):

    directorio = directorio.replace('"','')
    if directorio[0] == '/':
            directorio = directorio[ 1:len(directorio)]

    peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=directorio) 
    encontrado = False

    for contenido in peticion.get('Contents', []):
        ruta_contenido = contenido['Key']

        if ruta_contenido == directorio + archivo:

        
            encontrado = True
            break

    return encontrado        

def eliminar_direcotrio_archivo(nombre,origen,tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
        origen = "Archivos"+origen
        origen = origen.replace('"','')
        if origen[0] == '/':
            origen = origen[ 1:len(origen)]

        if verificar_directorio(origen):

            if nombre == "":
                print('proceder a eliminar toda la carpeta')

                peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen)

                # Verificar si la carpeta está vacía
                if 'Contents' in peticion:
                    # Recorrer y eliminar los objetos dentro de la carpeta
                    objetos_a_eliminar = [{'Key': objeto['Key']} for objeto in peticion['Contents']]
                    objeto_s3.delete_objects(Bucket=nombre_bucket_s3, Delete={'Objects': objetos_a_eliminar})
                else:                
                    print('Algun error')
                    #### reportar error

            else:
                if verificar_archivo_dentro_directorio(nombre,origen):
                    print("proceder a eliminar solo el archivo") 

                    print(str(origen)+str(nombre))
                    rutan_nombre = str(origen)+str(nombre)
                    objeto_s3.delete_object(Bucket=nombre_bucket_s3, Key=rutan_nombre)
                else:
                    print("El archivo no existe")
                    ####### reportar error
        else:
            print("La ruta no existe")
            ####### reportar error
    else:
        #CODIGO EN CASO DE QUE SE EJECUTE EN SERVIDOR
        ruta_archivo_limpia = limpiar_ruta(origen)
        ruta_eliminar = ruta_archivo_limpia+nombre
        if os.path.exists(ruta_eliminar):
            if os.path.isfile(ruta_eliminar):
                os.remove(ruta_eliminar)
            else:
                rmtree(ruta_eliminar)
    
def verificar_archivo_carpeta(directorio):

    directorio = directorio.replace('"','')

    if os.path.isfile(directorio):
        return 'Archivo', True
    elif os.path.isdir(directorio):
        return 'Carpeta', True
    else:
        return '', False
    
def verificar_archivo_con_ruta_bucket(directorio):
    # Verificar si la ruta es un archivo

    directorio = directorio.replace('"','')
    tipo_ruta = ""

    if directorio[0] == '/':
        directorio = directorio[ 1:len(directorio)]

    if directorio.find('.') != -1:
        tipo_ruta = 'Archivo'
    else:
        tipo_ruta = 'Carpeta'
    try:
        objeto_s3.head_object(Bucket=nombre_bucket_s3, Key=directorio)       
        return tipo_ruta, True  
    except:
        pass

    response = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=directorio + '/')
    if 'Contents' in response or 'CommonPrefixes' in response:
        return tipo_ruta, True
    else:
        return '', False 
    
def copiar_archivos_carpetas(origen,destino,tipo_from,tipo_to):   

    origen = origen.replace('"','')
    destino = destino.replace('"','')

    if tipo_from == 'bucket':
        if tipo_to == 'bucket':

            #server server

            tipo1, verificacion1 = verificar_archivo_con_ruta_bucket(origen)
            tipo2, verificacion2 = verificar_archivo_con_ruta_bucket(destino)

            print('bucket - bucket',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':    

                if tipo1 != '':

                    print('copiar')

                    if tipo1 == 'Carpeta':

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        ob_s3 = boto3.resource('s3')
                        bucket = ob_s3.Bucket(nombre_bucket_s3)

                        for obj in bucket.objects.filter(Prefix=origen):
                            ruta_origen = obj.key
                            ruta_destino = destino + ruta_origen
                            bucket.copy({'Bucket': nombre_bucket_s3, 'Key': ruta_origen}, ruta_destino)
                    
                    elif tipo1 == 'Archivo': 

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        nombre_archivo = nombre_archivo_descargado = os.path.basename(origen)
                        objeto_s3.copy_object(Bucket=nombre_bucket_s3, CopySource=f'{nombre_bucket_s3}/{origen}', Key=f'{destino}{nombre_archivo}')

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')

        else:
            #server local
            tipo1, verificacion1 = verificar_archivo_con_ruta_bucket(origen)
            tipo2, verificacion2 = verificar_archivo_carpeta(destino)

            print('bucket - server',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':

                if tipo1 != '':
                    print('copiar')

                    if tipo1 == 'Carpeta':

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        def descarga_recursiva(ruta_origen, ruta_destino):
                            objeto_s3.download_file( nombre_bucket_s3, ruta_origen, ruta_destino)

                        def copiar_carpeta(origen_, destino_):
                            contenido = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen_)['Contents']

                            for archivo_carpeta in contenido:
                                ruta_nuevo_origen = archivo_carpeta['Key']
                                ruta_nuevo_destino = os.path.join(destino_, ruta_nuevo_origen)

                                if ruta_nuevo_origen.endswith('/'):  
                                    os.makedirs(ruta_nuevo_destino, exist_ok=True)
                                else:  
                                    descarga_recursiva(ruta_nuevo_origen, ruta_nuevo_destino)

                        copiar_carpeta(origen, destino)

                    elif tipo1 == 'Archivo':

                        print(destino)

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        print(destino,origen)
                        os.makedirs(destino, exist_ok=True)                      
                        nombre_archivo_descargado = os.path.basename(origen)
                        objeto_s3.download_file(nombre_bucket_s3, origen, destino + nombre_archivo_descargado)

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')
            
    else:
        if tipo_to == 'bucket':

            #local server

            tipo1, verificacion1 = verificar_archivo_carpeta(origen)
            tipo2, verificacion2 = verificar_archivo_con_ruta_bucket(destino)

            print('server - bucket',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':

                if tipo1 != '':
                    print('copiar')

                    origen = origen.replace('"','')
                    if origen[0] == '/':
                        origen = origen[ 1:len(origen)]
                    
                    destino = destino.replace('"','')
                    if destino[0] == '/':
                        destino = destino[ 1:len(destino)]


                    if(tipo1 == 'Carpeta'):

                        solo_carpeta_nombre = origen

                        if solo_carpeta_nombre.endswith("/"):
                            solo_carpeta_nombre = solo_carpeta_nombre[:-1]

                        solo_carpeta_nombre = os.path.basename(solo_carpeta_nombre)

                        print('Origen', origen)
                        print('Carpeta a copiar', solo_carpeta_nombre)
                        print('Carpeta a donde', destino)

                        nueva_ruta_destino = destino

                        if nueva_ruta_destino.endswith("/"):
                            nueva_ruta_destino = nueva_ruta_destino + solo_carpeta_nombre + '/'
                        else:
                            nueva_ruta_destino = nueva_ruta_destino + '/' + solo_carpeta_nombre + '/'

                        print('ruta Nueva carpeta', nueva_ruta_destino)
                        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key = nueva_ruta_destino) 

                        destino = nueva_ruta_destino

                        for root, dirs, files in os.walk(origen):
                            for file in files:
                                
                                if os.path.basename(file) != 'desktop.ini':
                                    ruta_archivo_local = os.path.join(root, file)
                                    ruta_archivo_s3 = os.path.join(destino, os.path.relpath(ruta_archivo_local, origen))
                                    ruta_archivo_s3 = ruta_archivo_s3.replace('\\','/')
                                    objeto_s3.upload_file(ruta_archivo_local, nombre_bucket_s3, ruta_archivo_s3)                                
                                
                            for dir in dirs:
                                ruta_carpeta_local = os.path.join(root, dir)
                                ruta_carpeta_s3 = os.path.join(destino, os.path.relpath(ruta_carpeta_local, origen))
                                ruta_carpeta_s3 = ruta_carpeta_s3.replace('\\','/')
                                objeto_s3.put_object(Bucket=nombre_bucket_s3, Key=ruta_carpeta_s3 + '/')                                


                    elif(tipo1 == 'Archivo'):

                        objeto_s3.upload_file(origen, nombre_bucket_s3, destino + os.path.basename(origen))

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                #reportar error---> ruta destino en el comando copiar no es valida
                print('ruta destino no es valida')
        else:

            #local local
            tipo1, verificacion1 = verificar_archivo_carpeta(origen)
            tipo2, verificacion2 = verificar_archivo_carpeta(destino)

            print('server - server',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':

                
                if tipo1 != '':
                    if os.path.exists(origen) and os.path.exists(destino):
                        #Se determina si la ruta de origen corresponde a la de un archivo o carpeta
                        if os.path.isfile(origen):
                            #Se obiene el nombre del archivo
                            partes = origen.split("/")
                            nueva_partes = [x for x in partes if x != '']
                            for x in nueva_partes:
                                if re.search(".*\.txt",x):
                                    nombre_archivo = x
                                    break
                            shutil.copyfile(origen,destino+nombre_archivo)
                        else:
                            copiar_archivos_directorio(origen,destino)
                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')

def transfer_archivos_carpetas(origen,destino,tipo_from,tipo_to):   
    origen = origen.replace('"','')
    destino = destino.replace('"','')

    if tipo_from == 'bucket':
        if tipo_to == 'bucket':

            #server server

            tipo1, verificacion1 = verificar_archivo_con_ruta_bucket(origen)
            tipo2, verificacion2 = verificar_archivo_con_ruta_bucket(destino)

            print('bucket - bucket',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':    

                if tipo1 != '': 

                    print('transferir')

                    if tipo1 == 'Carpeta':

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        ob_s3 = boto3.resource('s3')
                        bucket = ob_s3.Bucket(nombre_bucket_s3)

                        for obj in bucket.objects.filter(Prefix=origen):
                            ruta_origen = obj.key
                            ruta_destino = destino + ruta_origen
                            bucket.copy({'Bucket': nombre_bucket_s3, 'Key': ruta_origen}, ruta_destino)

                        print(origen)

                        peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen)

                        if 'Contents' in peticion:
                        
                            objetos_a_eliminar = [{'Key': objeto['Key']} for objeto in peticion['Contents']]
                            objeto_s3.delete_objects(Bucket=nombre_bucket_s3, Delete={'Objects': objetos_a_eliminar})
                        else:                
                            print('Algun error')
                            #### reportar error


                    elif tipo1 == 'Archivo':

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        nombre_archivo = nombre_archivo_descargado = os.path.basename(origen)
                        objeto_s3.copy_object(Bucket=nombre_bucket_s3, CopySource=f'{nombre_bucket_s3}/{origen}', Key=f'{destino}{nombre_archivo}')

                        print(origen)
                        objeto_s3.delete_object(Bucket=nombre_bucket_s3, Key=origen)


                    #

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')

        else:
            #server local
            tipo1, verificacion1 = verificar_archivo_con_ruta_bucket(origen)
            tipo2, verificacion2 = verificar_archivo_carpeta(destino)

            print('bucket - server',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':

                if tipo1 != '':
                    print('transferir')

                    if tipo1 == 'Carpeta':

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        def descarga_recursiva(ruta_origen, ruta_destino):
                            objeto_s3.download_file( nombre_bucket_s3, ruta_origen, ruta_destino)

                        def copiar_carpeta(origen_, destino_):
                            contenido = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen_)['Contents']

                            for archivo_carpeta in contenido:
                                ruta_nuevo_origen = archivo_carpeta['Key']
                                ruta_nuevo_destino = os.path.join(destino_, ruta_nuevo_origen)

                                if ruta_nuevo_origen.endswith('/'):  
                                    os.makedirs(ruta_nuevo_destino, exist_ok=True)
                                else:  
                                    descarga_recursiva(ruta_nuevo_origen, ruta_nuevo_destino)

                        copiar_carpeta(origen,destino)

                        shutil.rmtree(origen)

                    elif tipo1 == 'Archivo':

                        print(destino)

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        print(destino,origen)
                        os.makedirs(destino, exist_ok=True)                      
                        nombre_archivo_descargado = os.path.basename(origen)
                        objeto_s3.download_file(nombre_bucket_s3, origen, destino + nombre_archivo_descargado)

                          

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')
            
    else:
        if tipo_to == 'bucket':

            #local server

            tipo1, verificacion1 = verificar_archivo_carpeta(origen)
            tipo2, verificacion2 = verificar_archivo_con_ruta_bucket(destino)

            print('server - bucket',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':

                solo_carpeta_nombre = origen

                if solo_carpeta_nombre.endswith("/"):
                    solo_carpeta_nombre = solo_carpeta_nombre[:-1]

                solo_carpeta_nombre = os.path.basename(solo_carpeta_nombre)

                print('Origen', origen)
                print('Carpeta a copiar', solo_carpeta_nombre)
                print('Carpeta a donde', destino)

                nueva_ruta_destino = destino

                if nueva_ruta_destino.endswith("/"):
                    nueva_ruta_destino = nueva_ruta_destino + solo_carpeta_nombre + '/'
                else:
                    nueva_ruta_destino = nueva_ruta_destino + '/' + solo_carpeta_nombre + '/'

                print('ruta Nueva carpeta', nueva_ruta_destino)
                objeto_s3.put_object(Bucket=nombre_bucket_s3, Key = nueva_ruta_destino) 

                destino = nueva_ruta_destino

                if tipo1 != '':
                    print('transferir')

                    origen = origen.replace('"','')
                    if origen[0] == '/':
                        origen = origen[ 1:len(origen)]
                    
                    destino = destino.replace('"','')
                    if destino[0] == '/':
                        destino = destino[ 1:len(destino)]

                    if(tipo1 == 'Carpeta'):

                        for root, dirs, files in os.walk(origen):
                            for file in files:
                                
                                if os.path.basename(file) != 'desktop.ini':
                                    ruta_archivo_local = os.path.join(root, file)
                                    ruta_archivo_s3 = os.path.join(destino, os.path.relpath(ruta_archivo_local, origen))
                                    ruta_archivo_s3 = ruta_archivo_s3.replace('\\','/')
                                    objeto_s3.upload_file(ruta_archivo_local, nombre_bucket_s3, ruta_archivo_s3)                                
                                
                            for dir in dirs:
                                ruta_carpeta_local = os.path.join(root, dir)
                                ruta_carpeta_s3 = os.path.join(destino, os.path.relpath(ruta_carpeta_local, origen))
                                ruta_carpeta_s3 = ruta_carpeta_s3.replace('\\','/')
                                objeto_s3.put_object(Bucket=nombre_bucket_s3, Key=ruta_carpeta_s3 + '/')  

                        shutil.rmtree(origen)                        

                    elif(tipo1 == 'Archivo'):

                        objeto_s3.upload_file(origen, nombre_bucket_s3, destino + os.path.basename(origen))                        
                        os.remove(origen) 

                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                #reportar error---> ruta destino en el comando copiar no es valida
                print('ruta destino no es valida')
        else:

            #local local
            tipo1, verificacion1 = verificar_archivo_carpeta(origen)
            tipo2, verificacion2 = verificar_archivo_carpeta(destino)

            print('server - server',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':
                if tipo1 != '':
                    nombre_archivo = ""
                    if os.path.exists(origen) and os.path.exists(destino):
                        #Se determina si la ruta de origen corresponde a la de un archivo o carpeta
                        if os.path.isfile(origen):
                            #Se obiene el nombre del archivo
                            partes = origen.split("/")
                            nueva_partes = [x for x in partes if x != '']
                            for x in nueva_partes:
                                if re.search(".*\.txt",x):
                                    nombre_archivo = x
                                    break 
                        shutil.move(origen,destino+nombre_archivo)
                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')
   
def cambiar_nombre_archivo_carpeta_bucket(nombre, ruta,tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
        if verificar_directorio(ruta):

            nombre = nombre.replace('"','')
        
            if ruta.endswith('/'):
                ruta = ruta[:-1]

            if ruta.startswith('/'):
                ruta = ruta[1:]

            ruta = ruta.replace('"','')

            solo_ruta = os.path.dirname(ruta)

            solo_nombre_viejo = os.path.basename(ruta)

            print(solo_nombre_viejo)

            print(solo_ruta)

            if len(solo_ruta) > 0 :
                solo_ruta = solo_ruta + '/'

            print(solo_ruta + nombre,' , ',ruta)


            peticion = objeto_s3.list_objects(Bucket=nombre_bucket_s3, Prefix=ruta)
            for content in peticion.get('Contents', []):
                key = content['Key']
                new_key = key.replace(ruta, solo_ruta + nombre)
                objeto_s3.copy_object(Bucket=nombre_bucket_s3, CopySource={'Bucket': nombre_bucket_s3, 'Key': key},
                            Key=new_key)



            peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=ruta)

            if 'Contents' in peticion:
            
                objetos_a_eliminar = [{'Key': objeto['Key']} for objeto in peticion['Contents']]
                objeto_s3.delete_objects(Bucket=nombre_bucket_s3, Delete={'Objects': objetos_a_eliminar})
            else:                
                print('Algun error')
                #### reportar error

        else:
            print("La ruta del archivo o carpeta para renombrar no se pudo verificar")
    else:
        #Se reestructura la ruta para el nuevo nombre
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rta = ""
        for x in nueva_partes:
            if not re.search(".*\.txt",x):
                rta=rta+x+"/"
            else:
                dir_carpeta = rta
                rta+=nombre
                break
        continuar = True
        if os.path.exists(ruta):
            #Se compara archivo existentes para verificar si no se repiten
            for x in os.listdir(dir_carpeta):
                if(x == nombre):
                    continuar = False
                    break
            if continuar:
                os.rename(ruta,rta)
            else:
                print("Imposible Renombrar, Existe un Archivo con el mismo nombre")
        else:
            print("Imposible de Renombrar, El Directorio o Archivo No Existe")

def modificar_archivo_bucket(ruta,body,tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
        if verificar_directorio(ruta):

            ruta = ruta.replace('"','')

            if ruta.startswith('/'):
                ruta = ruta[1:]
        
            if ruta.endswith('/'):
                ruta = ruta[:-1]

            objeto_s3.put_object(Bucket=nombre_bucket_s3, Key=ruta, Body=body)

        else:
            print("La ruta del archivo o carpeta para MODIFICAR no se pudo verificar")
    else:
        print(ruta)
        if os.path.exists(ruta):
            f = open(ruta,"w")
            f.write(body)
            f.close()
        else:
            print("El Directorio o Archivo No Existe")

def eliminar_todo_el_contenido_bucket(tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
        aux_s3 = boto3.resource('s3')
        bucket = aux_s3.Bucket(nombre_bucket_s3)

        for objeto in bucket.objects.all():
            objeto.delete()

        print("CONTENIDO DEL BUCKET ELIMINADO")
    else:
        for filename in os.listdir(dir_origen+"/"):
            rta = os.path.join(dir_origen+"/",filename)
            try:
                if os.path.isfile(rta) or os.path.islink(rta):
                    os.unlink(rta)
                elif os.path.isdir(rta):
                    rmtree(rta)
            except Exception as e:
                print("Error "+e)

def crear_backup(tipo_to,tipo_from,ip,port,name_copy):
    if tipo_from == 'server':
        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key='Archivos/'+name_copy+"/")
        destino = '/Archivos/'+name_copy
        origen = './Archivos/'
    else:
        if not os.path.exists('./Archivos/'+name_copy):
            os.mkdir('./Archivos/'+name_copy)
        destino = './Archivos/'+name_copy
        origen = '/Archivos/'
    
    if(ip == '' and port == ''):
        copiar_archivos_carpetas(origen,destino,tipo_from,tipo_to)

def crear_recovery(tipo_to,tipo_from,ip,port,name_copy):
    if tipo_from == 'server':
        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key='Archivos/'+name_copy+"_recovered/")
        destino = '/Archivos/'+name_copy+"_recovered/"
        origen = './Archivos/'+name_copy
    else:
        if not os.path.exists('./Archivos/'+name_copy):
            os.mkdir('./Archivos/'+name_copy+"_recovered/")
        destino = './Archivos/'+name_copy+"_recovered/"
        origen = '/Archivos/'+name_copy
    
    if(ip == '' and port == ''):
        copiar_archivos_carpetas(origen,destino,tipo_from,tipo_to)

def open_archivo(tipo,ip,port,name_file):
    if name_file.endswith('/'):
        name_file = name_file[:-1]

    if name_file.startswith('/'):
        name_file = name_file[1:]

    if tipo == "bucket":
        try:
            s3_object = s3_resource.Object(
                bucket_name='proyecto-2-mia', 
                key=name_file
            )
            s3_response = s3_object.get()
            s3_object_body = s3_response.get('Body')
            global content_str 
            content_str = s3_object_body.read().decode()
            print(content_str)
        except s3_resource.meta.client.exceptions.NoSuchBucket as e:
            print('NO EXISTE EL BUCKET INDICADO')
            print(e)

        except s3_resource.meta.client.exceptions.NoSuchKey as e:
            print('NO EXISTE EL ARCHIVO QUE SE DESEA LEER')
            print(e)
    else:
        nombre = "./"+name_file
        f = open(nombre)
        print(f.read())

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

def copiar_archivos_directorio(origen, destino):
    if os.path.isdir(origen):

        if os.path.isdir(destino):

            print('entra')

            nombre_carpeta = os.path.basename(os.path.dirname(origen))
            ruta_nueva = str(destino) + str(nombre_carpeta)
                    
            if os.path.exists(ruta_nueva):

                print('entra')

                contador = 1
                nombre_carpeta_original = os.path.basename(os.path.dirname(origen))
                nuevo_nombre_carpeta = nombre_carpeta_original + "(" + str(contador) + ")"
                extencion_archivo = os.path.splitext(os.path.basename(origen))[1]

                print(str(destino) + str(nuevo_nombre_carpeta))
            
                while os.path.exists(str(destino) + str(nuevo_nombre_carpeta)):

                    contador = contador + 1
                    nuevo_nombre_carpeta = str(nombre_carpeta_original) + "(" + str(contador) + ")"

                nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nuevo_nombre_carpeta)
                shutil.copytree(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)

            else:

                print('entra2')
                print("Copiando carpeta")
                print(origen)
                print(destino)
                shutil.copytree(origen, str(destino) + nombre_carpeta)

        else:
            print("Ruta destino no existe")

    elif os.path.isfile(origen):

        if os.path.isdir(destino):

            if os.path.exists(origen):            

                nombre_archivo = os.path.basename(origen)

                #print(str(destino) + str(nombre_archivo))
        
                if os.path.exists(str(destino) + str(nombre_archivo)):

                    print("El archivo existe")

                    contador = 1

                    nombre_archivo_original = os.path.splitext(os.path.basename(origen))[0]
                    nuevo_nombre_archivo = nombre_archivo_original + "(" + str(contador) + ")"
                    extencion_archivo = os.path.splitext(os.path.basename(origen))[1]

                    print(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo))
                

                    while os.path.exists(str(destino) + str(nuevo_nombre_archivo)  + str(extencion_archivo)):

                        contador = contador + 1
                        nuevo_nombre_archivo = str(nombre_archivo_original) + "(" + str(contador) + ")"
                    

                    nuevo_nombre_archivo = nuevo_nombre_archivo + extencion_archivo
                    
                    destino = os.path.join(destino, nuevo_nombre_archivo)
                    shutil.copy2(origen, destino)

                else:
    
                    nueva_ruta_nombre_y_ruta_nuevo_archivo = os.path.join(destino, nombre_archivo)
                    shutil.copy2(origen, nueva_ruta_nombre_y_ruta_nuevo_archivo)
        
            else:
                output_bt = "El archivo o directorio a copiar no existe"
        else:
            output_bt = "La ruta destino no existe"
    else:
        output_bt = "No se encontró nada en el directorio: "+origen+"para mover a: "+destino

#Copia desde la carpeta anterior, es decir que incluye la carpeta Archivos en la copia
#copiar_archivos_carpetas("/Archivos/carpeta_tc/","/Archivos/sub_carpeta2/","bucket","bucket")
#copiar_archivos_carpetas("/Archivos/carpeta_tc/","./Archivos/sub_carpeta2/","bucket","server")

#No sube la carpeta del server a la carpeta del bucket
#copiar_archivos_carpetas("./Archivos/carpeta_tcs/","/Archivos/sub_carpeta2/","server","bucket")

#---------------
#No sube la carpeta del server a la carpeta del bucket
#Transfiere desde la carpeta anterior, es decir que incluye la carpeta Archivos en la transferencia
#transfer_archivos_carpetas("/Archivos/carpeta_tc/","/Archivos/sub_carpeta2/","bucket","bucket")
#transfer_archivos_carpetas("/Archivos/carpeta_tc/","./Archivos/sub_carpeta2/","bucket","server")






#------------------------------------------------------------------------------------
#No sube la carpeta
#transfer_archivos_carpetas("./Archivos/sub_carpeta1/","/Archivos/sub_carpeta2/","server","bucket")



#Se descarga el archivo, pero no se elimina del bucket, con lo cual es una copia y no una transferencia
transfer_archivos_carpetas("/Archivos/sub_carpeta1/Archivo.txt","./Archivos/sub_carpeta2/","bucket","server")