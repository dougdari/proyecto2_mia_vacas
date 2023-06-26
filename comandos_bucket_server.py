import os
import shutil
import boto3

nombre_bucket_s3 = 'proyecto-2-mia'

objeto_s3 = boto3.client('s3')

def crear_directorio_archivo(nombre,destino,contenido):

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


def eliminar_direcotrio_archivo(nombre,origen):

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

    if tipo_from == 'bucket':
        if tipo_to == 'bucket':

            #server server

            tipo1, verificacion1 = verificar_archivo_con_ruta_bucket(origen)
            tipo2, verificacion2 = verificar_archivo_con_ruta_bucket(destino)

            print('bucket - bucket',tipo1,verificacion1,tipo2,verificacion2)

            if tipo2 == 'Carpeta':    

                if tipo1 != '':

                    print('copiar')

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

                        origen = origen.replace('"','')
                        if origen[0] == '/':
                            origen = origen[ 1:len(origen)]
                        
                        destino = destino.replace('"','')
                        if destino[0] == '/':
                            destino = destino[ 1:len(destino)]

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
                    print('copiar')
                    ##//llamar ala funcioncion solo copia local------------------------------------------> sustituir aca
                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')

           
def transfer_archivos_carpetas(origen,destino,tipo_from,tipo_to):   

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

                        objeto_s3.delete_object(Bucket=nombre_bucket_s3, Key=origen)
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
                    print('transferir')


                    ##//llamar ala funcioncion solo copia local------------------------------------------> sustituir aca
                else:
                    #reportar error---> ruta destino en el comando copiar no es valida
                    print('la ruta origen no es valida')
            else:
                 #reportar error---> ruta destino en el comando copiar no es valida
                 print('ruta destino no es valida')

        
def cambiar_nombre_archivo_carpeta_bucket(nombre, ruta):


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


def modificar_archivo_bucket(ruta,body):

    if verificar_directorio(ruta):

        ruta = ruta.replace('"','')

        if ruta.startswith('/'):
            ruta = ruta[1:]
    
        if ruta.endswith('/'):
            ruta = ruta[:-1]

        objeto_s3.put_object(Bucket=nombre_bucket_s3, Key=ruta, Body=body)

    else:
        print("La ruta del archivo o carpeta para MODIFICAR no se pudo verificar")

def eliminar_todo_el_contenido_bucket():

    aux_s3 = boto3.resource('s3')
    bucket = aux_s3.Bucket(nombre_bucket_s3)

    for objeto in bucket.objects.all():
        objeto.delete()

    print("CONTENIDO DEL BUCKET ELIMINADO")






#modificar_archivo_bucket('/en_la_raiz.txt','Nuevo contenido 7777')

#eliminar_todo_el_contenido_bucket()












#print(verificar_archivo_con_ruta_bucket('/"carpeta 2"/destinoArchivo/otro_archivo.txt'))
#copiar_archivos_carpetas('/"carpeta 2"/destinoArchivo/otro_archivo.txt','/"carpeta 2"/destinoArchivo/otro_archivo.txt','server','server')
#copiar_archivos_carpetas('C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/Texto 1.txt','C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/','bucket','bucket')

#crear_directorio_archivo('otro_archivo1.txt','/"carpeta 2"/destinoArchivo/','Este es el contenido del archivo')
#print(verificar_archivo_dentro_directorio('otro_archivo.txt','/"carpeta 2"/destinoArchivo/'))
#print(verificar_directorio('/"carpeta 2"/destinoArchivo/'))

#eliminar_direcotrio_archivo('','/"carpeta 3"')

#copiar_archivos_carpetas('/carpeta 2/destinoArchivo/','C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/','bucket','server')

#eliminar_direcotrio_archivo_bucket('','carpeta 2/')
#crear_directorio_archivo('otro.txt','/"carpeta 6"/','Este es el contenido del archivo')


#eliminar_direcotrio_archivo_bucket('','carpeta 2/')
#transfer_archivos_carpetas('/"carpeta 4"/','/"carpeta 1"/','bucket','bucket')
#cambiar_nombre_archivo_carpeta_bucket('\"carpeta 77 nueva\"','/\"carpeta 5\"/')





#print(verificar_archivo_con_ruta_bucket('/"carpeta 2"/destinoArchivo/otro_archivo.txt'))
#copiar_archivos_carpetas('/"carpeta 2"/destinoArchivo/otro_archivo.txt','/"carpeta 2"/destinoArchivo/otro_archivo.txt','server','server')
#copiar_archivos_carpetas('C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/Texto 1.txt','C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/','bucket','bucket')

#crear_directorio_archivo('otro_archivo1.txt','/"carpeta 2"/destinoArchivo/','Este es el contenido del archivo')
#print(verificar_archivo_dentro_directorio('otro_archivo.txt','/"carpeta 2"/destinoArchivo/'))
#print(verificar_directorio('/"carpeta 2"/destinoArchivo/'))

#eliminar_direcotrio_archivo('','/"carpeta 3"')

#copiar_archivos_carpetas('/carpeta 2/destinoArchivo/','C:/Users/Douglas/Desktop/pruebaCarpeta/carpeta1/','bucket','server')


#crear_directorio_archivo('ultimo.txt','/carpeta 3/subcarpeta 3/','Este es el contenido del archivo')

copiar_archivos_carpetas('C:/Users/Douglas/Desktop/vayne.jpg','/carpeta 1/','server','bucket')










