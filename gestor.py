import comandos_bucket_server
import requests

def ejecutar_comandos(lista_comandos):
    pos = 0
    while(pos < len(lista_comandos)):
        if(lista_comandos[pos] != None):
            identificar_ejecutar(lista_comandos[pos])
        pos+=1

def identificar_ejecutar(comando):
    #La primera i indica el tipo de comando a ejecutar
    if(str(comando[0]).lower() == "create"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_crear = "./Archivos"
        #PARAMETROS PARA EL MÉTODO CREAR
        nombre_crear = ""
        body_crear = ""
        ruta_crear = ""
        tipo_crear = ""
        #RECORRO EL ARREGLO DE COMANDO PARA OBTENER EL VALOR DE PARAMETROS
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="name":
                nombre_crear = comando[i][1]
            elif str(comando[i][0]).lower()=="body":
                body_crear = comando[i][1]
            elif str(comando[i][0]).lower()=="path":
                ruta_crear = comando[i][1]
            elif str(comando[i][0]).lower()=="type":
                tipo_crear = comando[i][1]
            i+=1
        if tipo_crear == 'bucket':
            irta_crear = "Archivos"
        comandos_bucket_server.crear_directorio_archivo(nombre_crear,irta_crear+ruta_crear,body_crear,tipo_crear)
    elif(str(comando[0]).lower() == "delete"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_eliminar = "./Archivos"
        #DEFINICION DE PARAMETROS DEL MÉTODO ELIMINAR
        ruta_eliminar = ""
        nombre_eliminar = ""
        tipo_eliminar = ""
        #RECORRIDO DE ARREGLO PARA DETERMINAR PARAMETROS
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="path":
                ruta_eliminar = comando[i][1]
            elif str(comando[i][0]).lower()=="name":
                nombre_eliminar = comando[i][1]
            elif str(comando[i][0]).lower()=="type":
                tipo_eliminar = comando[i][1]
            i+=1
        if tipo_eliminar == "bucket":
            irta_eliminar = "Archivos"
        comandos_bucket_server.eliminar_direcotrio_archivo(nombre_eliminar,irta_eliminar+ruta_eliminar,tipo_eliminar)
    elif(str(comando[0]).lower() == "copy"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_copy_origen = "./Archivos"
        irta_copy_destino = "./Archivos"
        #DEFINICION DE PARAMETROS DEL MÉTODO ELIMINAR
        ruta_origen_copiar = ""
        ruta_destino_copiar = ""
        tipo_origen_copiar = ""
        tipo_destino_copiar = ""
        #RECORRIDO DE ARREGLO PARA DETERMINAR PARAMETROS
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="from":
                ruta_origen_copiar = comando[i][1]
            elif str(comando[i][0]).lower()=="to":
                ruta_destino_copiar = comando[i][1]
            elif str(comando[i][0]).lower()=="type_to":
                tipo_origen_copiar = comando[i][1]
            elif str(comando[i][0]).lower()=="type_from":
                tipo_destino_copiar = comando[i][1]
            i+=1
        if irta_copy_origen == "bucket":
            irta_copy_origen = "Archivos"
        if irta_copy_destino == "bucket":
            irta_copy_destino = "Archivos"
        comandos_bucket_server.copiar_archivos_carpetas(irta_copy_origen+ruta_origen_copiar,irta_copy_destino+ruta_destino_copiar,tipo_origen_copiar,tipo_destino_copiar)
    elif(str(comando[0]).lower() == "transfer"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_transfer_origen = "./Archivos"
        irta_transfer_destino = "./Archivos"
        #DEFINICION DE PARAMETROS DEL MÉTODO ELIMINAR
        ruta_origen_transfer = ""
        ruta_destino_transfer = ""
        tipo_origen_transfer = ""
        tipo_destino_transfer = ""
        #RECORRIDO DE ARREGLO PARA DETERMINAR PARAMETROS
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="from":
                ruta_origen_transfer = comando[i][1]
            elif str(comando[i][0]).lower()=="to":
                ruta_destino_transfer = comando[i][1]
            elif str(comando[i][0]).lower()=="type_to":
                tipo_origen_transfer = comando[i][1]
            elif str(comando[i][0]).lower()=="type_from":
                tipo_destino_transfer = comando[i][1]
            i+=1
        if irta_transfer_origen == "bucket":
            irta_transfer_origen = "Archivos"
        if irta_transfer_destino == "bucket":
            irta_transfer_destino = "Archivos"
        comandos_bucket_server.transfer_archivos_carpetas(irta_transfer_origen+ruta_origen_transfer,irta_transfer_destino+ruta_destino_transfer,tipo_origen_transfer,tipo_destino_transfer)
    elif(str(comando[0]).lower() == "rename"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_rename = "./Archivos"
        #PARAMETROS PARA EL MÉTODO CREAR
        ruta_rename = ""
        nombre_rename = ""
        tipo_rename = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="path":
                ruta_rename = comando[i][1]
            elif str(comando[i][0]).lower()=="name":
                nombre_rename = comando[i][1]
            elif str(comando[i][0]).lower()=="type":
                tipo_rename = comando[i][1]
            i+=1
        if tipo_rename == "bucket":
            irta_rename = "Archivos"
        comandos_bucket_server.cambiar_nombre_archivo_carpeta_bucket(nombre_rename,irta_rename+ruta_rename,tipo_rename) 
    elif(str(comando[0]).lower() == "modify"):
        #VARIABLE DE CONCATENACION CON CARPETA ARCHIVOS
        irta_modify = "./Archivos"
        #PARAMETROS PARA EL MÉTODO CREAR
        ruta_modify = ""
        body_modify = ""
        tipo_modify = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="path":
                ruta_modify = comando[i][1]
            elif str(comando[i][0]).lower()=="body":
                body_modify = comando[i][1]
            elif str(comando[i][0]).lower()=="type":
                tipo_modify = comando[i][1]
            i+=1
        if tipo_modify == "bucket":
            irta_modify = "Archivos"
        comandos_bucket_server.modificar_archivo_bucket(irta_modify+ruta_modify,body_modify,tipo_modify)
    elif(str(comando[0]).lower() == "backup"):
        #PARAMETROS PARA EL MÉTODO CREAR
        tipo_to_backup = ""
        tipo_from_backup = ""
        ip_backup = ""
        port_backup = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="type_to":
                tipo_to_backup = comando[i][1]
            elif str(comando[i][0]).lower()=="type_from":
                tipo_from_backup = comando[i][1]
            elif str(comando[i][0]).lower()=="ip":
                ip_backup = comando[i][1]
            elif str(comando[i][0]).lower()=="port":
                port_backup = comando[i][1]
            i+=1

        if len(ip_backup):
            #consumir api rivaldo
            print('hola')

            url = 'http:/34.224.123.209/backup/' + tipo_from_backup
            json_rivaldo = requests.get(url)

            print(json_rivaldo)

            if tipo_to_backup == 'server':

                #implementar el metodo aca de json a server
                print('copiar al server')
            elif tipo_to_backup == 'bucket':

                #implementar el metodo aca de json a bucket
                print('copiar al bucket')

        else:
            #backup normal
            print('backup normal')
            comandos_bucket_server.crear_backup(tipo_to_backup,tipo_from_backup,ip_backup,port_backup)

    elif(str(comando[0]).lower() == "recovery"):
        #PARAMETROS PARA EL MÉTODO CREAR
        tipo_to_recovery= ""
        tipo_from_recovery = ""
        ip_recovery = ""
        port_recovery = ""
        name_recovery = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="type_to":
                tipo_to_recovery = comando[i][1]
            elif str(comando[i][0]).lower()=="type_from":
                tipo_from_recovery = comando[i][1]
            elif str(comando[i][0]).lower()=="ip":
                ip_recovery = comando[i][1]
            elif str(comando[i][0]).lower()=="port":
                port_recovery = comando[i][1]
            elif str(comando[i][0]).lower()=="name":
                name_recovery = comando[i][1]
            i+=1
        comandos_bucket_server.crear_recovery(tipo_to_recovery,tipo_from_recovery,ip_recovery,port_recovery,name_recovery)
    elif(str(comando[0]).lower() == "delete_all"):
        #PARAMETROS PARA EL MÉTODO CREAR
        tipo_eliminar_todo = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="type":
                tipo_eliminar_todo = comando[i][1]
            i+=1
        comandos_bucket_server.eliminar_todo_el_contenido_bucket(tipo_eliminar_todo)
    elif(str(comando[0]).lower() == "open"):
        #PARAMETROS PARA EL MÉTODO CREAR
        tipo_open= ""
        ip_open = ""
        port_open = ""
        name_open = ""
        i = 1
        while(i < len(comando)):
            if str(comando[i][0]).lower()=="type_to":
                tipo_open = comando[i][1]
            elif str(comando[i][0]).lower()=="ip":
                ip_open = comando[i][1]
            elif str(comando[i][0]).lower()=="port":
                port_open = comando[i][1]
            elif str(comando[i][0]).lower()=="name":
                name_open = comando[i][1]
            i+=1
        comandos_bucket_server.open_archivo(tipo_open,ip_open,port_open,name_open)
