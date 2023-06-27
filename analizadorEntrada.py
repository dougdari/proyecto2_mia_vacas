import ply.lex as lex
import ply.yacc as yacc


#(C|c)(R|r)(E|e)(A|a)(T|t)(E|e) - (N|n)(A|a)(M|m)(E|e) -> T_NOMBRE_ARCHIVO - (P|p)(A|a)(T|t)(H|h) -> T_RUTA_DIRECTORIO  - (B|b)(O|o)(D|d)(Y|y) -> CADENA_CONTENIDO - (T|t)(Y|y)(P|p)(E|e) -> T_ALMANENAMIENTO
#(D|d)(E|e)(L|l)(E|e)(T|t)(E|e) - (P|p)(A|a)(T|t)(H|h) -> T_RUTA_DIRECTORIO - (N|n)(A|a)(M|m)(E|e) -> T_NOMBRE_ARCHIVO - (T|t)(Y|y)(P|p)(E|e) -> T_ALMANENAMIENTO
#(C|c)(O|o)(P|p)(Y|y) - (F|f)(R|r)(O|o)(M|m) -> T_RUTA_DIRECTORIO_ARCHIVO - (T|t)(O|o) -> T_RUTA_DIRECTORIO - (T|t)(Y|y)(P|p)(E|e)_(T|t)(O|o) -> T_ALMANENAMIENTO - (T|t)(Y|y)(P|p)(E|e)_(F|f)(R|r)(O|o)(M|m) -> T_ALMANENAMIENTO
#(T|t)(R|r)(A|a)(N|n)(S|s)(F|f)(E|e)(R|r) -(F|f)(R|r)(O|o)(M|m)-> T_RUTA_DIRECTORIO_ARCHIVO -(T|t)(O|o) -> T_RUTA_DIRECTORIO - (T|t)(Y|y)(P|p)(E|e)_(T|t)(O|o) -> T_ALMANENAMIENTO -(T|t)(Y|y)(P|p)(E|e)_(F|f)(R|r)(O|o)(M|m) -> T_ALMANENAMIENTO
#(R|r)(E|e)(N|n)(A|a)(M|m)(E|e) -(P|p)(A|a)(T|t)(H|h) -> T_RUTA_DIRECTORIO_ARCHIVO -(N|n)(A|a)(M|m)(E|e) -> T_NOMBRE_ARCHIVO - (T|t)(Y|y)(P|p)(E|e) -> T_ALMANENAMIENTO
#(M|m)(O|o)(D|d)(I|i)(F|f)(Y|y) -(P|p)(A|a)(T|t)(H|h) -> T_RUTA_DIRECTORIO_ARCHIVO - (B|b)(O|o)(D|d)(Y|y) -> CADENA_CONTENIDO - (T|t)(Y|y)(P|p)(E|e) -> T_ALMANENAMIENTO
#(B|b)(A|a)(C|c)(K|k)(U|u)(P|p) - (T|t)(Y|y)(P|p)(E|e)_(T|t)(O|o) -> T_ALMANENAMIENTO - (T|t)(Y|y)(P|p)(E|e)_(F|f)(R|r)(O|o)(M|m) -> T_ALMANENAMIENTO - (I|i)(P|p)-> T_IP - (P|p)(O|o)(R|r)(T|t)-> NUMERO -(N|n)(A|a)(M|m)(E|e) -> CADENA  
#(R|r)(E|e)(C|c)(O|o)(V|v)(E|e)(R|r)(Y|y)  -(T|t)(Y|y)(P|p)(E|e)_(T|t)(O|o)-> T_ALMANENAMIENTO -(T|t)(Y|y)(P|p)(E|e)_(F|f)(R|r)(O|o)(M|m) -> T_ALMANENAMIENTO -(I|i)(P|p) -> T_IP -(P|p)(O|o)(R|r)(T|t) -> NUMERO -(N|n)(A|a)(M|m)(E|e)-> CADENA    
#(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)_(A|a)(L|l)(L|l) - (T|t)(Y|y)(P|p)(E|e) -> T_ALMANENAMIENTO 
#(O|o)(P|p)(E|e)(N|n) - (T|t)(Y|y)(P|p)(E|e)-> T_ALMANENAMIENTO - (I|i)(P|p)-> T_IP -(P|p)(O|o)(R|r)(T|t) -> NUMERO -(N|n)(A|a)(M|m)(E|e) ->  CADENA   


# p_name        -name         ----------- (NOMBRE_ARCHIVO|NOMBRE_ARCHIVO_COMILLAS|CADENA)
# p_body        -body         ----------- CADENA
# p_path        -path         ----------- (SOLO_DIRECTORIO|SOLO_DIRECTORIO_COMILLAS|DIRECTORIO_CON_ARCHIVO| DIRECTORIO_CON_ARCHIVO_COMILLAS)
# p_type        -type         ----------- TIPO_ALMACENAMIENTO
# p_from        -from         ----------- (SOLO_DIRECTORIO|SOLO_DIRECTORIO_COMILLAS|DIRECTORIO_CON_ARCHIVO| DIRECTORIO_CON_ARCHIVO_COMILLAS)
# p_to          -to           ----------- (SOLO_DIRECTORIO|SOLO_DIRECTORIO_COMILLAS)
# p_type_to     -type_to      ----------- TIPO_ALMACENAMIENTO
# p_type_from   -type_from    ----------- TIPO_ALMACENAMIENTO
# p_ip          -ip           ----------- DIRECCION_IP
# p_port        -port         ----------- NUMERO_PUERTO

# p_name : SEPARADOR NAME FLECHA p_name_parametros
# p_name_paramtros : NOMBRE_ARCHIVO | NOMBRE_ARCHIVO_COMILLAS | CADENA

# p_body : SEPARADOR BODY FLECHA CADENA

# p_path : SEPARADOR PATH FLECHA p_rutas_parametros
# p_rutas_parametros :  DIRECTORIO_CON_ARCHIVO | DIRECTORIO_CON_ARCHIVO_COMILLAS | p_rutas_solo_directorios

# p_type : SEPARADOR TYPE FLECHA TIPO_ALMACENAMIENTO

# p_from : SEPARADOR FROM FLECHA p_rutas_parametros

# p_to :   SEPARADOR TO FLECHA p_rutas_solo_directorios
# p_rutas_solo_directorios : SOLO_DIRECTORIO | SOLO_DIRECTORIO_COMILLAS

# p_type_to : SEPARADOR TYPE_TO FLECHA TIPO_ALMACENAMIENTO

# p_type_from : SEPARADOR TYPE_FROM FLECHA TIPO_ALMACENAMIENTO

# p_ip : SEPARADOR IP FLECHA DIRECCION_IP

# p_port: SEPARADOR PORT FLECHA_ NUMERO_PUERTO

#################################################################################################################################################################

# c_create : CREATE p_posible_parametro_create p_posible_parametro_create p_posible_parametro_create p_posible_parametro_create p_posible_parametro_create

# p_posible_parametro_create : p_name | p_path | p_body | p_type



tokens = (

    'CREATE',
    'NAME',
    'TIPO_ALMACENAMIENTO',
    'PATH',
    'BODY',
    'TYPE',
    'DELETE_ALL',
    'DELETE',
    'COPY',
    'FROM',
    'TO',
    'TYPE_TO',
    'TYPE_FROM',
    'TRANSFER',
    'RENAME',
    'MODIFY',
    'BACKUP',
    'IP',
    'PORT',
    'RECOVERY',
    'DIRECCION_IP',
    'NUMERO_PUERTO',
    'OPEN',   
    'DIRECTORIO_CON_ARCHIVO',
    'NOMBRE_ARCHIVO',
    'NOMBRE_ARCHIVO_COMILLAS',
    'SOLO_DIRECTORIO',
    'FLECHA',
    'SEPARADOR',   
    'CADENA',
)

t_CREATE = r'(C|c)(R|r)(E|e)(A|a)(T|t)(E|e)'
t_TIPO_ALMACENAMIENTO = r'((S|s)(E|e)(R|r)(V|v)(E|e)(R|r))|((B|b)(U|u)(C|c)(K|k)(E|e)(T|t))|(\"(S|s)(E|e)(R|r)(V|v)(E|e)(R|r)\")|(\"(B|b)(U|u)(C|c)(K|k)(E|e)(T|t)\")'
t_NAME = r'(N|n)(A|a)(M|m)(E|e)'
t_PATH = r'(P|p)(A|a)(T|t)(H|h)'
t_BODY = r'(B|b)(O|o)(D|d)(Y|y)'
t_TYPE = r'(T|t)(Y|y)(P|p)(E|e)'
t_DELETE_ALL = r'(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)_(A|a)(L|l)(L|l)'
t_DELETE = r'(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)'
t_COPY = r'(C|c)(O|o)(P|p)(Y|y)'
t_FROM = r'(F|f)(R|r)(O|o)(M|m)'
t_TO = r'(T|t)(O|o)'
t_TYPE_TO = r'(T|t)(Y|y)(P|p)(E|e)_(T|t)(O|o)'
t_TYPE_FROM = r'(T|t)(Y|y)(P|p)(E|e)_(F|f)(R|r)(O|o)(M|m)'
t_TRANSFER = r'(T|t)(R|r)(A|a)(N|n)(S|s)(F|f)(E|e)(R|r)'
t_RENAME = r'(R|r)(E|e)(N|n)(A|a)(M|m)(E|e)'
t_MODIFY = r'(M|m)(O|o)(D|d)(I|i)(F|f)(Y|y)'
t_BACKUP = r'(B|b)(A|a)(C|c)(K|k)(U|u)(P|p)'
t_IP = r'(I|i)(P|p)'
t_PORT = r'(P|p)(O|o)(R|r)(T|t)'
t_RECOVERY = r'(R|r)(E|e)(C|c)(O|o)(V|v)(E|e)(R|r)(Y|y)'
t_OPEN = r'(O|o)(P|p)(E|e)(N|n)'

t_DIRECCION_IP = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
t_NUMERO_PUERTO = r'\b(?:[0-9]{1,4})\b'

t_DIRECTORIO_CON_ARCHIVO = r'[\/](([a-zA-Z0-9_-]+|\"[a-zA-Z0-9_ -]+\")[\/])*(([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)|(\"[a-zA-Z0-9_ -]+\.[a-zA-Z0-9_-]+\"))'

t_NOMBRE_ARCHIVO = r'[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
t_NOMBRE_ARCHIVO_COMILLAS = r'\"[a-zA-Z0-9 _-]+\.[a-zA-Z0-9_-]+\"'

t_SOLO_DIRECTORIO = r'[\/]((([a-zA-Z0-9_-]+)|(\"[a-zA-Z0-9_ -]+\"))[\/])*'


t_FLECHA = r'(-|–)>'
t_SEPARADOR = r'(-|–)'

t_CADENA = r'\"[^\"]*\"'

t_ignore = ' \t\n'



def t_error(t):
    print("Error lexico: {}".format(t.value[0]))
    t.lexer.skip(1)

lexer = lex.lex()
comandos = []

def p_inicio(p):
    '''
        inicio : l_comando
    '''

    #print(comandos)

def p_l_comando(p):

    '''
    l_comando : l_comando comando
            | comando
    '''

    if len(p) == 3:
        comandos.append(p[2])
    else:
        comandos.append(p[1]) 

def p_comando(p): 
    '''
    comando : c_create
            | c_delete
            | c_copy
            | c_transfer
            | c_rename
            | c_modify
            | c_backup
            | c_recovery
            | c_delete_all
            | c_open
    '''
    
    p[0] = p[1]

def p_parametro_name(p):
    '''
        parametro_name : SEPARADOR NAME FLECHA name_parametros
    '''
    
    p[0] = ['name', p[4]]

def p_name_parametos(p):
    '''
        name_parametros : NOMBRE_ARCHIVO
                        | NOMBRE_ARCHIVO_COMILLAS
                        | DIRECTORIO_CON_ARCHIVO
                        | CADENA                        
    '''

    if p.slice[1].type == 'NOMBRE_ARCHIVO':
        p[0] = ['nombre_archivo', p[1]]
    elif p.slice[1].type == 'NOMBRE_ARCHIVO_COMILLAS':
        p[0] = ['nombre_archivo', p[1]]
    elif p.slice[1].type == 'DIRECTORIO_CON_ARCHIVO':
        p[0] = ['directorio_con_archivo', p[1]]
    else:
        p[0] = ['cadena', p[1]]

    p[0] = p[1]

def p_parametro_body(p):
    '''
        parametro_body : SEPARADOR BODY FLECHA CADENA
    '''
    p[0] = ['body', p[4]]

def p_parametro_path(p):
    '''
        parametro_path : SEPARADOR PATH FLECHA path_parametros
    '''   

    p[0] = ['path', p[4]]

def p_path_parametros(p):
    '''
        path_parametros : DIRECTORIO_CON_ARCHIVO
                        | rutas_solo_directorios
    '''

    if p.slice[1].type != 'rutas_solo_directorios':
        p[0] = ['directorio_con_archivo',str(p[1])]
    else:
        p[0] = p[1]
   
    p[0] = p[1]

def p_rutas_solo_directorios(p):
    '''
        rutas_solo_directorios : SOLO_DIRECTORIO 
    '''

    p[0] = ['directorio',str(p[1])]
    p[0] = p[1]

def p_parametro_type(p):
    '''
        parametro_type : SEPARADOR TYPE FLECHA TIPO_ALMACENAMIENTO
    '''

    p[0] = ['type',str(p[4]).lower().replace('"', '')]

def p_parametro_from(p): 
    '''
        parametro_from : SEPARADOR FROM FLECHA path_parametros
    '''
    p[0] = ['from',p[4]]

def p_parametro_to(p):
    '''
        parametro_to : SEPARADOR TO FLECHA rutas_solo_directorios
    '''

    p[0] = ['to', p[4]]

def p_parametro_type_to(p):
    '''
        parametro_type_to : SEPARADOR TYPE_TO FLECHA TIPO_ALMACENAMIENTO
    '''
    
    p[0] = ['type_to',str(p[4]).lower().replace('"', '')]

def p_parametro_type_from(p):
    '''
        parametro_type_from : SEPARADOR TYPE_FROM FLECHA TIPO_ALMACENAMIENTO
    '''

    p[0] = ['type',str(p[4]).lower().replace('"', '')]

def p_parametro_ip(p):
    '''
        parametro_ip : SEPARADOR IP FLECHA DIRECCION_IP
    '''

    p[0] = ['ip',str(p[4])]

def p_parametro_port(p):
    '''
        parametro_port : SEPARADOR PORT FLECHA NUMERO_PUERTO
    '''

    p[0] = ['port',str(p[4])]

def p_posible_parametro_create(p):
    '''
        posible_parametro_create : parametro_name
                                 | parametro_path
                                 | parametro_body
                                 | parametro_type
    '''

    p[0] = p[1]

def p_c_create(p):
    '''
        c_create : CREATE posible_parametro_create posible_parametro_create posible_parametro_create posible_parametro_create
    '''

    p[0] = ['create',p[2],p[3],p[4],p[5]]

def p_posible_parametro_delete(p):
    '''
        posible_parametro_delete : parametro_path
                                 | parametro_name
                                 | parametro_type
    '''

    p[0] = p[1]

def p_c_delete(p):
    '''
        c_delete : DELETE posible_parametro_delete posible_parametro_delete posible_parametro_delete
                 | DELETE posible_parametro_delete posible_parametro_delete
    '''

    
    

    if len(p) == 5:
        p[0] = ['delete',p[2],p[3],p[4]]
    elif len(p) == 4:
        p[0] = ['delete',p[2],p[3]]

def p_posible_parametro_copy(p):
    '''
        posible_parametro_copy : parametro_from
                               | parametro_to
                               | parametro_type_to
                               | parametro_type_from
    '''

    p[0] = p[1]

def p_c_copy(p):
    '''
        c_copy : COPY posible_parametro_copy posible_parametro_copy posible_parametro_copy posible_parametro_copy
    '''

    p[0] = ['copy',p[2],p[3],p[4],p[5]]

def p_posible_parametro_transfer(p):
    '''
        posible_parametro_transfer : parametro_from
                                   | parametro_to
                                   | parametro_type_to
                                   | parametro_type_from
    '''

    p[0] = p[1]

def p_c_transfer(p):
    '''
        c_transfer : TRANSFER posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer
    '''

    p[0] = ['transfer',p[2],p[3],p[4],p[5]]

def p_posible_parametro_rename(p):
    '''
        posible_parametro_rename : parametro_path
                                 | parametro_name
                                 | parametro_type
    '''

    p[0] = p[1]

def p_c_rename(p):
    '''
        c_rename : RENAME posible_parametro_rename posible_parametro_rename posible_parametro_rename
    '''

    p[0] = ['rename',p[2],p[3],p[4]]

def p_posible_parametro_modify(p):
    '''
        posible_parametro_modify : parametro_path
                                 | parametro_body
                                 | parametro_type
    '''

    p[0] = p[1]

def p_c_modify(p):
    '''
        c_modify : MODIFY posible_parametro_modify posible_parametro_modify posible_parametro_modify
    '''

    p[0] = ['modify',p[2],p[3],p[4]]

def p_posible_parametro_backup(p):
    '''
        posible_parametro_backup : parametro_type_to
                                 | parametro_type_from
                                 | parametro_ip
                                 | parametro_port
                                 | parametro_name
    '''

    p[0] = p[1]

def p_c_backup(p):
    '''
        c_backup : BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup
                 | BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup
                 | BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup
    '''

    if len(p) == 7:
        p[0] = ['backup',p[2],p[3],p[4],p[5],p[6]]
    elif len(p) == 6:
        p[0] = ['backup',p[2],p[3].p[4],p[5]]
    else:
        p[0] = ['backup',p[2],p[3],p[4]]


def p_posible_parametro_recovery(p):
    '''
        posible_parametro_recovery : parametro_type_to
                                   | parametro_type_from
                                   | parametro_ip
                                   | parametro_port
                                   | parametro_name
    '''

    p[0] = p[1]

def p_c_recovery(p):
    '''
        c_recovery : RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery
                   | RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery
                   | RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery
    '''

    if len(p) == 7:
        p[0] = ['recovery',p[2],p[3],p[4],p[5],p[6]]
    elif len(p) == 6:
        p[0] = ['recovery',p[2],p[3].p[4],p[5]]
    else:
        p[0] = ['recovery',p[2],p[3],p[4]]

def p_c_delete_all(p):
    '''
        c_delete_all : DELETE_ALL parametro_type 
    '''

    p[0] = ['delete_all',p[2]]

def p_posible_parametro_open(p):
    '''
        posible_parametro_open : parametro_type
                               | parametro_ip
                               | parametro_port
                               | parametro_name
    '''

    p[0] = p[1]

def p_c_open(p):
    '''
        c_open : OPEN posible_parametro_open posible_parametro_open posible_parametro_open posible_parametro_open
               | OPEN posible_parametro_open posible_parametro_open posible_parametro_open
               | OPEN posible_parametro_open posible_parametro_open
    '''

    if len(p) == 6:
        p[0] = ['open',p[2],p[3],p[4],p[5]]
    elif len(p) == 5:
        p[0] = ['open',p[2],p[3],p[4]]
    else:
        p[0] = ['open',p[2],p[3]]

def p_error(p):
    print("Error sintactico")



parser = yacc.yacc()
#entrada = "delete -path->/\"carpeta 2\"/ -type->bucket open -type->\"bUcKet\"  -port->3000  -ip->3.144.137.114  -name->/\"Mi carpeta\"/\"archivo1.txt\"  create -name->prueba1.txt -path->/carpeta1/ -body->\"Este es el contenido del archivo 1\" -type->server"

entrada = 'MoDIFY -path->/"carpeta ejemplo"/ejemplo1/calificacion3.txt -Type->server -body->"Contenido del archivo calificacion3 carpeta ejemplo ejemplo1" modifY -path->/"carpeta ejemplo"/ejemplo1/calificacion4.txt -Type->server -body->"Contenido del archivo calificacion4 carpeta ejemplo ejemplo1" rename -path->/carpeta_calificacion1/calificacion1.txt -type->bucket -Name->"calificacion bucket 1" rename -path->/carpeta_calificacion1/calificacion2.txt -type->bucket -Name->"calificacion bucket 2" rename -path->/carpeta_calificacion1/calificacion1.txt -type->server -Name->"calificacion server 1" DELETE -TYPE->bucket -paTh->/carpeta_calificacion1/calificacion4.txt creatE -name->calificacion1.txt -path->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo3/ -bodY->"Contenido del archivo calificacion1 carpeta ejemplo" -type->bucket Create -name->calificacion2.txt -path->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo3/ -body->"Contenido del archivo calificacion2 carpeta ejemplo" -Type->bucket Create -namE->calificacion3.txt -path->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo4/ -body->"Contenido del archivo calificacion3 carpeta ejemplo" -Type->bucket Create -namE->calificacion4.txt -path->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo4/ -body->"Contenido del archivo calificacion4 carpeta ejemplo" -Type->bucket copy -from->/"carpeta ejemplo"/ejemplo2 -type_from->server -type_to->server -to->/"carpeta ejemplo"/ copy -from->/"carpeta ejemplo"/ejemplo2 -to->/"carpeta ejemplo"/ejemplo1 -type_from->server -type_to->server copy -from->/"carpeta ejemplo"/ejemplo2 -to->/carpeta_calificacion1/"carpeta ejemplo"/ -type_from->server -type_to->bucket copy -from->/"carpeta ejemplo"/ejemplo2 -to->/carpeta_calificacion1/"carpeta ejemplo"/ -type_from->server -type_to->bucket copy -to->/"carpeta ejemplo"/ejemplo2 -from->/carpeta_calificacion1/"calificacion bucket 1.txt" -type_from->bucket -type_to->server copy -to->/carpeta_calificacion1/"carpeta ejemplo"  -from->/carpeta_calificacion1/"calificacion bucket 1.txt" -type_from->bucket -type_to->bucket Transfer -from->/carpeta_calificacion_1/"calificacion server 1.txt" -type_from->server -type_to->server -to->/"carpeta ejemplo"/ Transfer -to->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo3 -from->/carpeta_calificacion1/"calificacion bucket 1.txt" -type_from->bucket -type_to->bucket Transfer -from->/carpeta_calificacion1/"carpeta ejemplo"/ejemplo3/calificacion1.txt -to->/"carpeta ejemplo"/ -type_from->bucket -type_to->server' 
resultado = parser.parse(entrada, lexer=lexer)


print("Resultado: {}".format(resultado))

for indice, elemento in enumerate(comandos):
    print(elemento)