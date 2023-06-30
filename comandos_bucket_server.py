import os
import shutil
import boto3
import regex as re
from shutil import rmtree
import shutil
import json


nombre_bucket_s3 = 'proyecto-2-mia'
dir_origen = "./Archivos"
objeto_s3 = boto3.client('s3')
session = boto3.Session()
s3_resource = session.resource('s3')

def crear_directorio_archivo(nombre,destino,contenido,tipo):
    tipo_accion = tipo.lower()
    if tipo_accion == "bucket":
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

    if directorio.endswith('/'):
                directorio = directorio[:-1]

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

                        numero_copia = 1

                        for obj in bucket.objects.filter(Prefix=origen):

                            if numero_copia != 1:

                                print(obj.key)

                                ruta_origen = obj.key
                                ruta_destino = destino + ruta_origen
                                bucket.copy({'Bucket': nombre_bucket_s3, 'Key': ruta_origen}, ruta_destino)
                            
                            numero_copia = numero_copia + 1
                    
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
                        
                        destino = limpiar_ruta(destino)
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        if origen.endswith("/"):
                            origen = origen[:-1]
                            
                        if destino.endswith("/"):
                            destino = destino[:-1]

                        print(origen)

                        def copiar_bucket_a_carpeta_local(bucket, ruta, destino):
                            objetos = objeto_s3.list_objects_v2(Bucket=bucket, Prefix=ruta)['Contents']

                            for objeto in objetos:
                                ruta_objeto = objeto['Key']
                                ruta_relativa = os.path.relpath(ruta_objeto, ruta)
                                destino_local = os.path.join(destino, ruta_relativa)
                                destino_local = destino_local.replace("\\", "/") 

                                print(destino_local)
                                if ruta_objeto.endswith('/'):
                                    os.makedirs(destino_local, exist_ok=True)
                                    
                                else:
                                    objeto_s3.download_file(bucket, ruta_objeto, destino_local)
                                    
                                                                            
                        copiar_bucket_a_carpeta_local(nombre_bucket_s3,origen,destino)
                            
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

                    origen = limpiar_ruta(origen)
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

                origen = limpiar_ruta(origen)
                destino = limpiar_ruta(destino)
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
                        
                        destino = limpiar_ruta(destino)
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

                        if origen.endswith("/"):
                            origen = origen[:-1]
                            
                        if destino.endswith("/"):
                            destino = destino[:-1]

                        def copiar_bucket_a_carpeta_local(bucket, carpeta, destino):
                            print('entra')
                            objetos = objeto_s3.list_objects_v2(Bucket=bucket, Prefix=carpeta)['Contents']

                            for objeto in objetos:
                                ruta_objeto = objeto['Key']
                                ruta_relativa = os.path.relpath(ruta_objeto, carpeta)
                                destino_local = os.path.join(destino, ruta_relativa)

                                if not os.path.exists(os.path.dirname(destino_local)):
                                    os.makedirs(os.path.dirname(destino_local))

                                if not ruta_objeto.endswith('/'):
                                    objeto_s3.download_file(bucket, ruta_objeto, destino_local)

                                if ruta_objeto.endswith('/') and not os.path.exists(destino_local):
                                    os.makedirs(destino_local)

                                if ruta_objeto.endswith('/') and not ruta_relativa.endswith('/'):
                                    # Copia el contenido de las subcarpetas
                                    copiar_bucket_a_carpeta_local(bucket, ruta_objeto, destino)
                                                    
                        copiar_bucket_a_carpeta_local(nombre_bucket_s3,origen,destino)

                        peticion = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen)

                        if 'Contents' in peticion:
                        
                            objetos_a_eliminar = [{'Key': objeto['Key']} for objeto in peticion['Contents']]
                            objeto_s3.delete_objects(Bucket=nombre_bucket_s3, Delete={'Objects': objetos_a_eliminar})
                        else:                
                            print('Algun error')

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

                        objeto_s3.delete_object(Bucket=nombre_bucket_s3, Key=origen)                          

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

                    origen = limpiar_ruta(origen)
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
                    origen = limpiar_ruta(origen)
                    destino = limpiar_ruta(destino)
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
        #Se reestructura la ruta para el nuevo nombred
        ruta = limpiar_ruta(ruta)
        partes = ruta.split("/")
        nueva_partes = [x for x in partes if x != '']
        rta = ""
        dir_carpeta = ""
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
            if dir_carpeta != "":
                for x in os.listdir(dir_carpeta):
                    if(x == nombre):
                        continuar = False
                        break
                if continuar:
                    rta = limpiar_ruta(rta)
                    os.rename(ruta,rta)
                else:
                    print("Imposible Renombrar, Existe un Archivo con el mismo nombre")
            else:
                if ruta == rta:
                    partes = rta.split('/')
                    rta_nueva = [x for x in partes if x != '']
                    rta_generada = ""
                    i = 0
                    while(i < len(rta_nueva)-1):
                        rta_generada = rta_nueva[i]+"/"
                        i+=1
                    rta_generada += nombre.replace('"',"")+"/"
                os.rename(ruta,rta_generada)
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
        ruta = limpiar_ruta(ruta)
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
        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key='Archivos/'+name_copy.replace('"','')+"/")
        destino = 'Archivos/'+name_copy.replace('"','')+"/"
        origen = './Archivos/'
    else:
        if not os.path.exists('./Archivos/'+name_copy.replace('"','')):
            os.mkdir('./Archivos/'+name_copy.replace('"',''))
        destino = './Archivos/'+name_copy.replace('"','')
        origen = 'Archivos/'
    
    if(ip == '' and port == ''):
        copiar_archivos_carpetas(origen,destino,tipo_from,tipo_to)

def crear_recovery(tipo_to,tipo_from,ip,port,name_copy):
    if tipo_from == 'server':
        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key='Archivos/'+name_copy.replace('"','')+"_recovered/")
        destino = 'Archivos/'+name_copy.replace('"','')+"_recovered/"
        origen = './Archivos/'+name_copy.replace('"','')
    else:
        if not os.path.exists('./Archivos/'+name_copy.replace('"','')):
            os.mkdir('./Archivos/'+name_copy.replace('"','')+"_recovered/")
        destino = './Archivos/'+name_copy.replace('"','')+"_recovered/"
        origen = 'Archivos/'+name_copy.replace('"','')
    
    if(ip == '' and port == ''):
        copiar_archivos_carpetas(origen,destino,tipo_from,tipo_to)

def open_archivo(tipo,ip,port,name_file):
    if tipo == "bucket":
        rutab = generar_ruta_bucket(name_file)
        try:
            s3_object = s3_resource.Object(
                bucket_name='proyecto-2-mia', 
                key=rutab
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
        ruta = generar_ruta_local("./Archivos",name_file)
        f = open(ruta)
        print(f.read())

def limpiar_ruta(ruta_archivo):
    partes = ruta_archivo.split("/")
    nuevas_partes = [x for x in partes if x != '']
    ruta_limpia = ""
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

def generar_estructura_carpeta_bucket_jason(origen):
 
    objetos = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3, Prefix=origen)['Contents']

    json_object = {
        'Carpeta': os.path.basename(origen[:-1]),
        'Archivos': []
    }

    for objeto_ in objetos:
        ruta_archivo = objeto_['Key']
        if ruta_archivo != origen:
            if ruta_archivo.startswith(origen):
                sub_ruta = ruta_archivo[len(origen):]
                if '/' not in sub_ruta:

                    nombre_archivo = os.path.basename(ruta_archivo)
                    contenido_archivo = objeto_s3.get_object(Bucket=nombre_bucket_s3, Key=ruta_archivo)['Body'].read().decode('utf-8')
                    json_object['Archivos'].append({
                        'Nombre': nombre_archivo,
                        'Contenido': contenido_archivo
                    })
                else:

                    carpetas = sub_ruta.split('/')
                    if carpetas[0] not in [elem['Carpeta'] for elem in json_object['Archivos']]:

                        sub_json_object = {
                            'Carpeta': carpetas[0],
                            'Archivos': generar_estructura_carpeta_bucket_jason(origen + carpetas[0] + '/')
                        }

                        if len(sub_json_object['Archivos']['Archivos']) > 0:
                            print('tiene algo')
                        else:
                            print('no tiene nada')
                            sub_json_object['Archivos'].pop('Archivos')
                        
                        json_object['Archivos'].append(sub_json_object)    

    return json_object

def json_backup_bucket(origen,nombre):

    origen = origen.replace('"','')

    if origen.startswith('/'):
        origen = origen[1:]

    if origen.endswith('/'):
        print('Origen valido')
    else:
        origen = origen + '/'

    json_backup = generar_estructura_carpeta_bucket_jason(origen)

    #json_backup['Raiz'] = json_backup.pop('Carpeta')
    #json_backup['Raiz'] = nombre

    json_nuevo = {
        'Raiz': os.path.basename(origen),
        'Archivos': []
    }
    
    json_nuevo['Raiz'] = json_backup['Carpeta']
    json_nuevo['Archivos'] = json_backup['Archivos']

    print(json_nuevo)
    
    
    return json.dumps(json_nuevo)

def generar_json_carpeta(ruta):
    jason_objeto = {
        'Carpeta': os.path.basename(ruta),
        'Archivos': []
    }

    for item in os.listdir(ruta):
        item_ruta = os.path.join(ruta, item)
        if os.path.isdir(item_ruta):
            jason_objeto['Archivos'].append(generar_json_carpeta(item_ruta))
        else:
            with open(item_ruta, 'r') as archivo:
                contenido = archivo.read()
            jason_objeto['Archivos'].append({
                'Nombre': item,
                'Contenido': contenido
            })

    if len(jason_objeto['Archivos']) > 0:
            print('tiene algo')
    else:
        print('no tiene nada')
        jason_objeto.pop('Archivos')

    return jason_objeto

def json_backup_local(origen,nombre):
    
    origen = origen.replace('"','')
    if origen.endswith('/'):
        print('Origen valido')
    else:
        origen = origen + '/'

    json_backup = generar_json_carpeta(origen)

    #son_backup['Raiz'] = json_backup.pop('Carpeta')
    #json_backup['Raiz'] = nombre

    json_nuevo = {
        'Raiz': os.path.basename(origen),
        'Archivos': []
    }
  
    json_nuevo['Raiz'] = json_backup['Carpeta']
    json_nuevo['Archivos'] = json_backup['Archivos']

    return json.dumps(json_nuevo)

def json_open_local(nombre_ruta):
    ruta = generar_ruta_local("./Archivos",nombre_ruta)
    ruta=ruta.replace('"','')
    print(ruta)
    if os.path.exists(ruta):
        f = open(ruta,"r")
        texto = f.read()
        partes = ruta.split('/')
        for x in partes:
            if re.search(".*\.txt",x):
                nombre_arch = x
                break
        json_op_local = {
            "Contenido":texto,
            "Nombre":nombre_arch
        }
        
        return json.dumps(json_op_local)

def generar_ruta_local(ruta,nombre_archivo):
    for x in os.listdir(ruta):
        if not re.search(".*\.txt",x):
            ruta = generar_ruta_local(ruta+"/"+x,nombre_archivo)
        else:
            ruta = ruta+"/"+nombre_archivo
        return ruta

def generar_ruta_bucket(nombre_archivo):
    # Obtener la lista de objetos en el bucket
    response = objeto_s3.list_objects_v2(Bucket=nombre_bucket_s3)
    # Buscar el archivo en la lista de objetos
    for obj in response['Contents']:
        key = obj['Key']
        if key.split('/')[-1] == nombre_archivo:
            return f"{key}"
    # Si el archivo no se encuentra
    return None

def json_open_bucket(nombre_ruta):
    ruta = generar_ruta_bucket(nombre_ruta)
    partes = ruta.split('/')
    global content_str
    for x in partes:
        if re.search(".*\.txt",x):
            nombre_arch = x
            break
    if ruta.endswith('/'):
        ruta = ruta[:-1]

    if ruta.startswith('/'):
        ruta = ruta[1:]

    try:
        s3_object = s3_resource.Object(
            bucket_name='proyecto-2-mia', 
            key=ruta
        )
        s3_response = s3_object.get()
        s3_object_body = s3_response.get('Body')
        content_str = s3_object_body.read().decode()
    except s3_resource.meta.client.exceptions.NoSuchBucket as e:
        print('NO EXISTE EL BUCKET INDICADO')
        print(e)

    except s3_resource.meta.client.exceptions.NoSuchKey as e:
        print('NO EXISTE EL ARCHIVO QUE SE DESEA LEER')
        print(e)
    
    json_op_bucket = {
            "Contenido":content_str,
            "Nombre":nombre_arch
        }
        
    return json.dumps(json_op_bucket)

def leer_json_a_local(entradajson,root_inicial=''):
    for item in entradajson['Archivos']:
        if 'Carpeta' in item:
            nombre_crp = item['Carpeta']
            crp_ruta = os.path.join(root_inicial,nombre_crp)
            ruta_crp = os.path.join("./Archivos",crp_ruta)
            os.makedirs(ruta_crp,exist_ok=True)
            if 'Archivos' in item:
                leer_json_a_local(item,root_inicial=crp_ruta)
        else:
            nombre_arch = item['Nombre']
            contenido_arch = item['Contenido']
            rta = os.path.join(root_inicial,nombre_arch)
            rta_final = os.path.join('./Archivos',rta)
            with open(rta_final,'w') as file:
                file.write(contenido_arch)

def leer_json_a_bucket(entradajson,root_inicial=''):
    for item in entradajson['Archivos']:
        if 'Carpeta' in item:
            nombre_crp = item['Carpeta']
            ruta_crp = os.path.join(root_inicial,nombre_crp)
            if 'Archivos' in item:
                leer_json_a_bucket(item,root_inicial=ruta_crp)
        else:
            nombre_arch = item['Nombre']
            content_arch = item['Contenido']
            rta = os.path.join(root_inicial,nombre_arch)
            rta_final = os.path.join("Archivos",rta)
            objeto_s3.put_object(
                Body = content_arch,
                Bucket = nombre_bucket_s3,
                Key = rta_final
            )

#json_open_local("calificacion1.txt")     
#json_open_bucket("/calificacion bucket 1/calificacion1.txt")
#json_backup_bucket('Archivos/calificacion bucket 1/','miBackup')



#Copia desde la carpeta anterior, es decir que incluye la carpeta Archivos en la copia
#copiar_archivos_carpetas("/Archivos/sub_carpeta1/","/Archivos/sub_carpeta2/","bucket","bucket")


#copiar_archivos_carpetas("/Archivos/carpeta_tc/","./Archivos/sub_carpeta2/","bucket","server")



#Transfiere desde la carpeta anterior, es decir que incluye la carpeta Archivos en la transferencia
#transfer_archivos_carpetas("/Archivos/carpeta_tc/","/Archivos/sub_carpeta2/","bucket","bucket")
#transfer_archivos_carpetas("/Archivos/carpeta_tc/","./Archivos/sub_carpeta2/","bucket","server")










#Se descarga el archivo, pero no se elimina del bucket, con lo cual es una copia y no una transferencia
#copiar_archivos_carpetas("/Archivos/","./Archivos/","bucket","server")

#print(verificar_archivo_con_ruta_bucket("/Archivos/sub_carpeta2/sub_carpeta1/"))