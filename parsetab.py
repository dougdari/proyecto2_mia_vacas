
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'BACKUP BODY CADENA COPY CREATE DELETE DELETE_ALL DIRECCION_IP DIRECTORIO_CON_ARCHIVO FLECHA FROM IP MODIFY NAME NOMBRE_ARCHIVO NOMBRE_ARCHIVO_COMILLAS NUMERO_PUERTO OPEN PATH PORT RECOVERY RENAME SEPARADOR SOLO_DIRECTORIO TIPO_ALMACENAMIENTO TO TRANSFER TYPE TYPE_FROM TYPE_TO\n        inicio : l_comando\n    \n    l_comando : l_comando comando\n            | comando\n    \n    comando : c_create\n            | c_delete\n            | c_copy\n            | c_transfer\n            | c_rename\n            | c_modify\n            | c_backup\n            | c_recovery\n            | c_delete_all\n            | c_open\n    \n        parametro_name : SEPARADOR NAME FLECHA name_parametros\n    \n        name_parametros : NOMBRE_ARCHIVO\n                        | NOMBRE_ARCHIVO_COMILLAS\n                        | CADENA                        \n    \n        parametro_body : SEPARADOR BODY FLECHA CADENA\n    \n        parametro_path : SEPARADOR PATH FLECHA path_parametros\n    \n        path_parametros : DIRECTORIO_CON_ARCHIVO\n                        | rutas_solo_directorios\n    \n        rutas_solo_directorios : SOLO_DIRECTORIO \n    \n        parametro_type : SEPARADOR TYPE FLECHA TIPO_ALMACENAMIENTO\n    \n        parametro_from : SEPARADOR FROM FLECHA path_parametros\n    \n        parametro_to : SEPARADOR TO FLECHA rutas_solo_directorios\n    \n        parametro_type_to : SEPARADOR TYPE_TO FLECHA TIPO_ALMACENAMIENTO\n    \n        parametro_type_from : SEPARADOR TYPE_FROM FLECHA TIPO_ALMACENAMIENTO\n    \n        parametro_ip : SEPARADOR IP FLECHA DIRECCION_IP\n    \n        parametro_port : SEPARADOR PORT FLECHA NUMERO_PUERTO\n    \n        posible_parametro_create : parametro_name\n                                 | parametro_path\n                                 | parametro_body\n                                 | parametro_type\n    \n        c_create : CREATE posible_parametro_create posible_parametro_create posible_parametro_create posible_parametro_create\n    \n        posible_parametro_delete : parametro_path\n                                 | parametro_name\n                                 | parametro_type\n    \n        c_delete : DELETE posible_parametro_delete posible_parametro_delete posible_parametro_delete\n                 | DELETE posible_parametro_delete posible_parametro_delete\n    \n        posible_parametro_copy : parametro_from\n                               | parametro_to\n                               | parametro_type_to\n                               | parametro_type_from\n    \n        c_copy : COPY posible_parametro_copy posible_parametro_copy posible_parametro_copy posible_parametro_copy\n    \n        posible_parametro_transfer : parametro_from\n                                   | parametro_to\n                                   | parametro_type_to\n                                   | parametro_type_from\n    \n        c_transfer : TRANSFER posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer\n    \n        posible_parametro_rename : parametro_path\n                                 | parametro_name\n                                 | parametro_type\n    \n        c_rename : RENAME posible_parametro_rename posible_parametro_rename posible_parametro_rename\n    \n        posible_parametro_modify : parametro_path\n                                 | parametro_body\n                                 | parametro_type\n    \n        c_modify : MODIFY posible_parametro_modify posible_parametro_modify posible_parametro_modify\n    \n        posible_parametro_backup : parametro_type_to\n                                 | parametro_type_from\n                                 | parametro_ip\n                                 | parametro_port\n                                 | parametro_name\n    \n        c_backup : BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup\n                 | BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup\n                 | BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup\n    \n        posible_parametro_recovery : parametro_type_to\n                                   | parametro_type_from\n                                   | parametro_ip\n                                   | parametro_port\n                                   | parametro_name\n    \n        c_recovery : RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery\n                   | RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery\n                   | RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery\n    \n        c_delete_all : DELETE_ALL parametro_type \n    \n        posible_parametro_open : parametro_type\n                               | parametro_ip\n                               | parametro_port\n                               | parametro_name\n    \n        c_open : OPEN posible_parametro_open posible_parametro_open posible_parametro_open posible_parametro_open\n               | OPEN posible_parametro_open posible_parametro_open posible_parametro_open\n               | OPEN posible_parametro_open posible_parametro_open\n    '
    
_lr_action_items = {'CREATE':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[14,14,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'DELETE':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[15,15,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'COPY':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[16,16,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'TRANSFER':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[17,17,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'RENAME':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[18,18,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'MODIFY':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[19,19,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'BACKUP':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[20,20,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'RECOVERY':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[21,21,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'DELETE_ALL':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[22,22,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'OPEN':([0,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[23,23,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,24,26,27,28,29,32,33,34,37,38,39,40,43,44,45,46,48,49,50,52,53,54,57,58,59,60,61,64,65,66,67,68,69,72,73,74,75,82,95,101,108,109,110,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,-2,-30,-31,-32,-33,-35,-36,-37,-40,-41,-42,-43,-45,-46,-47,-48,-50,-51,-52,-54,-55,-56,-58,-59,-60,-61,-62,-66,-67,-68,-69,-70,-74,-75,-76,-77,-78,-39,-81,-38,-53,-57,-65,-73,-80,-34,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-44,-24,-25,-26,-27,-49,-64,-28,-29,-72,-79,-63,-71,]),'SEPARADOR':([14,15,16,17,18,19,20,21,22,23,25,26,27,28,29,31,32,33,34,36,37,38,39,40,42,43,44,45,46,47,48,49,50,51,52,53,54,56,57,58,59,60,61,63,64,65,66,67,68,71,72,73,74,75,77,82,83,88,89,90,91,94,95,96,102,107,110,113,114,116,117,118,119,120,121,122,123,124,125,127,128,129,130,132,133,134,135,],[30,35,41,41,35,55,62,62,70,76,30,-30,-31,-32,-33,35,-35,-36,-37,41,-40,-41,-42,-43,41,-45,-46,-47,-48,35,-50,-51,-52,55,-54,-55,-56,62,-58,-59,-60,-61,-62,62,-66,-67,-68,-69,-70,76,-75,-76,-77,-78,30,35,41,41,35,55,62,62,76,30,41,41,62,62,76,-14,-15,-16,-17,-19,-20,-21,-22,-18,-23,-24,-25,-26,-27,62,-28,-29,62,]),'NAME':([30,35,62,76,],[78,78,78,78,]),'PATH':([30,35,55,],[79,79,79,]),'BODY':([30,55,],[80,80,]),'TYPE':([30,35,55,70,76,],[81,81,81,81,81,]),'FROM':([41,],[84,]),'TO':([41,],[85,]),'TYPE_TO':([41,62,],[86,86,]),'TYPE_FROM':([41,62,],[87,87,]),'IP':([62,76,],[92,92,]),'PORT':([62,76,],[93,93,]),'FLECHA':([78,79,80,81,84,85,86,87,92,93,],[97,98,99,100,103,104,105,106,111,112,]),'NOMBRE_ARCHIVO':([97,],[117,]),'NOMBRE_ARCHIVO_COMILLAS':([97,],[118,]),'CADENA':([97,99,],[119,124,]),'DIRECTORIO_CON_ARCHIVO':([98,103,],[121,121,]),'SOLO_DIRECTORIO':([98,103,104,],[123,123,123,]),'TIPO_ALMACENAMIENTO':([100,105,106,],[125,129,130,]),'DIRECCION_IP':([111,],[133,]),'NUMERO_PUERTO':([112,],[134,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'inicio':([0,],[1,]),'l_comando':([0,],[2,]),'comando':([0,2,],[3,24,]),'c_create':([0,2,],[4,4,]),'c_delete':([0,2,],[5,5,]),'c_copy':([0,2,],[6,6,]),'c_transfer':([0,2,],[7,7,]),'c_rename':([0,2,],[8,8,]),'c_modify':([0,2,],[9,9,]),'c_backup':([0,2,],[10,10,]),'c_recovery':([0,2,],[11,11,]),'c_delete_all':([0,2,],[12,12,]),'c_open':([0,2,],[13,13,]),'posible_parametro_create':([14,25,77,96,],[25,77,96,115,]),'parametro_name':([14,15,18,20,21,23,25,31,47,56,63,71,77,82,89,91,94,95,96,110,113,114,132,135,],[26,33,49,61,68,75,26,33,49,61,68,75,26,33,49,61,68,75,26,61,68,75,61,68,]),'parametro_path':([14,15,18,19,25,31,47,51,77,82,89,90,96,],[27,32,48,52,27,32,48,52,27,32,48,52,27,]),'parametro_body':([14,19,25,51,77,90,96,],[28,53,28,53,28,53,28,]),'parametro_type':([14,15,18,19,22,23,25,31,47,51,71,77,82,89,90,95,96,114,],[29,34,50,54,69,72,29,34,50,54,72,29,34,50,54,72,29,72,]),'posible_parametro_delete':([15,31,82,],[31,82,101,]),'posible_parametro_copy':([16,36,83,102,],[36,83,102,126,]),'parametro_from':([16,17,36,42,83,88,102,107,],[37,43,37,43,37,43,37,43,]),'parametro_to':([16,17,36,42,83,88,102,107,],[38,44,38,44,38,44,38,44,]),'parametro_type_to':([16,17,20,21,36,42,56,63,83,88,91,94,102,107,110,113,132,135,],[39,45,57,64,39,45,57,64,39,45,57,64,39,45,57,64,57,64,]),'parametro_type_from':([16,17,20,21,36,42,56,63,83,88,91,94,102,107,110,113,132,135,],[40,46,58,65,40,46,58,65,40,46,58,65,40,46,58,65,58,65,]),'posible_parametro_transfer':([17,42,88,107,],[42,88,107,131,]),'posible_parametro_rename':([18,47,89,],[47,89,108,]),'posible_parametro_modify':([19,51,90,],[51,90,109,]),'posible_parametro_backup':([20,56,91,110,132,],[56,91,110,132,137,]),'parametro_ip':([20,21,23,56,63,71,91,94,95,110,113,114,132,135,],[59,66,73,59,66,73,59,66,73,59,66,73,59,66,]),'parametro_port':([20,21,23,56,63,71,91,94,95,110,113,114,132,135,],[60,67,74,60,67,74,60,67,74,60,67,74,60,67,]),'posible_parametro_recovery':([21,63,94,113,135,],[63,94,113,135,138,]),'posible_parametro_open':([23,71,95,114,],[71,95,114,136,]),'name_parametros':([97,],[116,]),'path_parametros':([98,103,],[120,127,]),'rutas_solo_directorios':([98,103,104,],[122,122,128,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> inicio","S'",1,None,None,None),
  ('inicio -> l_comando','inicio',1,'p_inicio','parser.py',144),
  ('l_comando -> l_comando comando','l_comando',2,'p_l_comando','parser.py',151),
  ('l_comando -> comando','l_comando',1,'p_l_comando','parser.py',152),
  ('comando -> c_create','comando',1,'p_comando','parser.py',160),
  ('comando -> c_delete','comando',1,'p_comando','parser.py',161),
  ('comando -> c_copy','comando',1,'p_comando','parser.py',162),
  ('comando -> c_transfer','comando',1,'p_comando','parser.py',163),
  ('comando -> c_rename','comando',1,'p_comando','parser.py',164),
  ('comando -> c_modify','comando',1,'p_comando','parser.py',165),
  ('comando -> c_backup','comando',1,'p_comando','parser.py',166),
  ('comando -> c_recovery','comando',1,'p_comando','parser.py',167),
  ('comando -> c_delete_all','comando',1,'p_comando','parser.py',168),
  ('comando -> c_open','comando',1,'p_comando','parser.py',169),
  ('parametro_name -> SEPARADOR NAME FLECHA name_parametros','parametro_name',4,'p_parametro_name','parser.py',176),
  ('name_parametros -> NOMBRE_ARCHIVO','name_parametros',1,'p_name_parametos','parser.py',181),
  ('name_parametros -> NOMBRE_ARCHIVO_COMILLAS','name_parametros',1,'p_name_parametos','parser.py',182),
  ('name_parametros -> CADENA','name_parametros',1,'p_name_parametos','parser.py',183),
  ('parametro_body -> SEPARADOR BODY FLECHA CADENA','parametro_body',4,'p_parametro_body','parser.py',190),
  ('parametro_path -> SEPARADOR PATH FLECHA path_parametros','parametro_path',4,'p_parametro_path','parser.py',196),
  ('path_parametros -> DIRECTORIO_CON_ARCHIVO','path_parametros',1,'p_path_parametros','parser.py',201),
  ('path_parametros -> rutas_solo_directorios','path_parametros',1,'p_path_parametros','parser.py',202),
  ('rutas_solo_directorios -> SOLO_DIRECTORIO','rutas_solo_directorios',1,'p_rutas_solo_directorios','parser.py',211),
  ('parametro_type -> SEPARADOR TYPE FLECHA TIPO_ALMACENAMIENTO','parametro_type',4,'p_parametro_type','parser.py',218),
  ('parametro_from -> SEPARADOR FROM FLECHA path_parametros','parametro_from',4,'p_parametro_from','parser.py',224),
  ('parametro_to -> SEPARADOR TO FLECHA rutas_solo_directorios','parametro_to',4,'p_parametro_to','parser.py',229),
  ('parametro_type_to -> SEPARADOR TYPE_TO FLECHA TIPO_ALMACENAMIENTO','parametro_type_to',4,'p_parametro_type_to','parser.py',234),
  ('parametro_type_from -> SEPARADOR TYPE_FROM FLECHA TIPO_ALMACENAMIENTO','parametro_type_from',4,'p_parametro_type_from','parser.py',241),
  ('parametro_ip -> SEPARADOR IP FLECHA DIRECCION_IP','parametro_ip',4,'p_parametro_ip','parser.py',248),
  ('parametro_port -> SEPARADOR PORT FLECHA NUMERO_PUERTO','parametro_port',4,'p_parametro_port','parser.py',253),
  ('posible_parametro_create -> parametro_name','posible_parametro_create',1,'p_posible_parametro_create','parser.py',258),
  ('posible_parametro_create -> parametro_path','posible_parametro_create',1,'p_posible_parametro_create','parser.py',259),
  ('posible_parametro_create -> parametro_body','posible_parametro_create',1,'p_posible_parametro_create','parser.py',260),
  ('posible_parametro_create -> parametro_type','posible_parametro_create',1,'p_posible_parametro_create','parser.py',261),
  ('c_create -> CREATE posible_parametro_create posible_parametro_create posible_parametro_create posible_parametro_create','c_create',5,'p_c_create','parser.py',268),
  ('posible_parametro_delete -> parametro_path','posible_parametro_delete',1,'p_posible_parametro_delete','parser.py',273),
  ('posible_parametro_delete -> parametro_name','posible_parametro_delete',1,'p_posible_parametro_delete','parser.py',274),
  ('posible_parametro_delete -> parametro_type','posible_parametro_delete',1,'p_posible_parametro_delete','parser.py',275),
  ('c_delete -> DELETE posible_parametro_delete posible_parametro_delete posible_parametro_delete','c_delete',4,'p_c_delete','parser.py',280),
  ('c_delete -> DELETE posible_parametro_delete posible_parametro_delete','c_delete',3,'p_c_delete','parser.py',281),
  ('posible_parametro_copy -> parametro_from','posible_parametro_copy',1,'p_posible_parametro_copy','parser.py',286),
  ('posible_parametro_copy -> parametro_to','posible_parametro_copy',1,'p_posible_parametro_copy','parser.py',287),
  ('posible_parametro_copy -> parametro_type_to','posible_parametro_copy',1,'p_posible_parametro_copy','parser.py',288),
  ('posible_parametro_copy -> parametro_type_from','posible_parametro_copy',1,'p_posible_parametro_copy','parser.py',289),
  ('c_copy -> COPY posible_parametro_copy posible_parametro_copy posible_parametro_copy posible_parametro_copy','c_copy',5,'p_c_copy','parser.py',294),
  ('posible_parametro_transfer -> parametro_from','posible_parametro_transfer',1,'p_posible_parametro_transfer','parser.py',299),
  ('posible_parametro_transfer -> parametro_to','posible_parametro_transfer',1,'p_posible_parametro_transfer','parser.py',300),
  ('posible_parametro_transfer -> parametro_type_to','posible_parametro_transfer',1,'p_posible_parametro_transfer','parser.py',301),
  ('posible_parametro_transfer -> parametro_type_from','posible_parametro_transfer',1,'p_posible_parametro_transfer','parser.py',302),
  ('c_transfer -> TRANSFER posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer posible_parametro_transfer','c_transfer',5,'p_c_transfer','parser.py',307),
  ('posible_parametro_rename -> parametro_path','posible_parametro_rename',1,'p_posible_parametro_rename','parser.py',312),
  ('posible_parametro_rename -> parametro_name','posible_parametro_rename',1,'p_posible_parametro_rename','parser.py',313),
  ('posible_parametro_rename -> parametro_type','posible_parametro_rename',1,'p_posible_parametro_rename','parser.py',314),
  ('c_rename -> RENAME posible_parametro_rename posible_parametro_rename posible_parametro_rename','c_rename',4,'p_c_rename','parser.py',319),
  ('posible_parametro_modify -> parametro_path','posible_parametro_modify',1,'p_posible_parametro_modify','parser.py',324),
  ('posible_parametro_modify -> parametro_body','posible_parametro_modify',1,'p_posible_parametro_modify','parser.py',325),
  ('posible_parametro_modify -> parametro_type','posible_parametro_modify',1,'p_posible_parametro_modify','parser.py',326),
  ('c_modify -> MODIFY posible_parametro_modify posible_parametro_modify posible_parametro_modify','c_modify',4,'p_c_modify','parser.py',331),
  ('posible_parametro_backup -> parametro_type_to','posible_parametro_backup',1,'p_posible_parametro_backup','parser.py',336),
  ('posible_parametro_backup -> parametro_type_from','posible_parametro_backup',1,'p_posible_parametro_backup','parser.py',337),
  ('posible_parametro_backup -> parametro_ip','posible_parametro_backup',1,'p_posible_parametro_backup','parser.py',338),
  ('posible_parametro_backup -> parametro_port','posible_parametro_backup',1,'p_posible_parametro_backup','parser.py',339),
  ('posible_parametro_backup -> parametro_name','posible_parametro_backup',1,'p_posible_parametro_backup','parser.py',340),
  ('c_backup -> BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup','c_backup',6,'p_c_backup','parser.py',345),
  ('c_backup -> BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup posible_parametro_backup','c_backup',5,'p_c_backup','parser.py',346),
  ('c_backup -> BACKUP posible_parametro_backup posible_parametro_backup posible_parametro_backup','c_backup',4,'p_c_backup','parser.py',347),
  ('posible_parametro_recovery -> parametro_type_to','posible_parametro_recovery',1,'p_posible_parametro_recovery','parser.py',352),
  ('posible_parametro_recovery -> parametro_type_from','posible_parametro_recovery',1,'p_posible_parametro_recovery','parser.py',353),
  ('posible_parametro_recovery -> parametro_ip','posible_parametro_recovery',1,'p_posible_parametro_recovery','parser.py',354),
  ('posible_parametro_recovery -> parametro_port','posible_parametro_recovery',1,'p_posible_parametro_recovery','parser.py',355),
  ('posible_parametro_recovery -> parametro_name','posible_parametro_recovery',1,'p_posible_parametro_recovery','parser.py',356),
  ('c_recovery -> RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery','c_recovery',6,'p_c_recovery','parser.py',361),
  ('c_recovery -> RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery','c_recovery',5,'p_c_recovery','parser.py',362),
  ('c_recovery -> RECOVERY posible_parametro_recovery posible_parametro_recovery posible_parametro_recovery','c_recovery',4,'p_c_recovery','parser.py',363),
  ('c_delete_all -> DELETE_ALL parametro_type','c_delete_all',2,'p_c_delete_all','parser.py',368),
  ('posible_parametro_open -> parametro_type','posible_parametro_open',1,'p_posible_parametro_open','parser.py',373),
  ('posible_parametro_open -> parametro_ip','posible_parametro_open',1,'p_posible_parametro_open','parser.py',374),
  ('posible_parametro_open -> parametro_port','posible_parametro_open',1,'p_posible_parametro_open','parser.py',375),
  ('posible_parametro_open -> parametro_name','posible_parametro_open',1,'p_posible_parametro_open','parser.py',376),
  ('c_open -> OPEN posible_parametro_open posible_parametro_open posible_parametro_open posible_parametro_open','c_open',5,'p_c_open','parser.py',381),
  ('c_open -> OPEN posible_parametro_open posible_parametro_open posible_parametro_open','c_open',4,'p_c_open','parser.py',382),
  ('c_open -> OPEN posible_parametro_open posible_parametro_open','c_open',3,'p_c_open','parser.py',383),
]
