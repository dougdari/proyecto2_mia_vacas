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

# p_port: SEPARADOR PORT FLECHA_DIRECTORIO NUMERO_PUERTO

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
    'DIRECTORIO_CON_ARCHIVO_COMILLAS',
    'NOMBRE_ARCHIVO',
    'NOMBRE_ARCHIVO_COMILLAS',
    'SOLO_DIRECTORIO',
    'SOLO_DIRECTORIO_COMILLAS',
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

t_DIRECTORIO_CON_ARCHIVO = r'[\/]([a-zA-Z0-9_-]+[\/])*[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
t_DIRECTORIO_CON_ARCHIVO_COMILLAS = r'\"[\/]([a-zA-Z0-9_ -]+[\/])*[a-zA-Z0-9_ -]+\.[a-zA-Z0-9_-]+\"'

t_NOMBRE_ARCHIVO = r'[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+'
t_NOMBRE_ARCHIVO_COMILLAS = r'\"[a-zA-Z0-9 _-]+\.[a-zA-Z0-9_-]+\"'

t_SOLO_DIRECTORIO = r'[\/]([a-zA-Z0-9_-]+[\/])*'
t_SOLO_DIRECTORIO_COMILLAS = r'\"[\/]([a-zA-Z0-9 _-]+[\/])*\"'

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

    print(comandos)

def p_l_comando(p):

    '''
    l_comando : l_comando comando
            | comando
    '''

    if len(p) > 2:
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
            | c_modify
            | c_backup
            | c_recovery
            | c_delete_all
            | c_open
    '''
    
    p[0] = p[1]

def p_parametro_name(p):
    '''
        parametro_name : SEPARADOR NAME FLECHA name_parametos
    '''

def p_name_parametos(p):
    '''
        name_parametros : NOMBRE_ARCHIVO
                        | NOMBRE_ARCHIVO_COMILLAS
                        | CADENA                        
    '''

    p[0] = ['nombre_archivo',str(p[1])]

def p_parametro_body(p):
    '''
        parametro_body : SEPARADOR BODY FLECHA CADENA
    '''

#############################################################################################################################





def p_error(p):
    print("Error sintactico")



parser = yacc.yacc()
 
entrada = ""

resultado = parser.parse(entrada, lexer=lexer)

print("Resultado: {}".format(resultado))