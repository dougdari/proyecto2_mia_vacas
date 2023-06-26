import boto3
import boto3
import Encriptador
lista_usuarios = []

AWS_ACCESS_KEY_ID = 'AKIARESZ4WKTWMJAX5ZO'
AWS_SECRET_ACCESS_KEY = '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'
nombre_bucket_s3 = 'proyecto-2-mia'

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
s3_resource = session.resource('s3')

def contenido_usuarios():
    try:
        s3_object = s3_resource.Object(
            bucket_name='proyecto-2-mia', 
            key='usuarios.txt'
        )
        s3_response = s3_object.get()
        s3_object_body = s3_response.get('Body')
        global content_str 
        content_str = s3_object_body.read().decode()

    except s3_resource.meta.client.exceptions.NoSuchBucket as e:
        print('NO EXISTE ESE BUCKET')
        print(e)

    except s3_resource.meta.client.exceptions.NoSuchKey as e:
        print('NO EXISTE EL ARCHIVO USUARIOS.TXT')
        print(e)

def comprobacion_usuario(usuario, contrasenia):
    contenido_usuarios()
    for linea in content_str.splitlines():
        lista_usuarios.append(linea)
    pass
    flagC = False
    size = len(lista_usuarios)
    i = 0
    while(i+1<size):
        if(usuario == lista_usuarios[i].replace("\n","") and contrasenia == Encriptador.desencriptar(lista_usuarios[i+1].replace("\n",""),"miaproyecto12345").decode("utf-8","ignore")):
            flagC = True
            break
        i=i+2
    return flagC
    


comprobacion_usuario("","")