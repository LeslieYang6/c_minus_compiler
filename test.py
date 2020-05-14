from globalTypes import *
from Parser import *

f = open('example.txt','r')             # lee todo el archivo a compilar
programa = f.read()
progLong = len(programa)                # longitud original del programa
programa = programa + '$'               # agregar un caracter $ que represente EOF
posicion = 0                            # posicion del caracter actual del string

# funcion para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)

#token, tokenString = getToken(True)
#while (token is not TokenType.ENDFILE):
    #token, tokenString = getToken(True)

AST = parser(True)