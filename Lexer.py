from globalTypes import TokenType

with open('matrix.txt') as f:
    fil, col = [int(x) for x in next(f).split()]
    simbolos = next(f).split('|')
    M = [[int(x) for x in line.split()] for line in f]

mapa = {}
for i in range(len(simbolos)):
    for c in simbolos[i]:
        mapa[c] = i


global linea
linea = ''

def setLineaGlobal(linea):
    global line
    line = linea

def getLineaGlobal():
    global linea
    return linea


def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    programa = prog
    posicion = pos
    progLong = long+1

global lineNumber
imprime = True
lineNumber = 0

def getToken(imprime):
    global posicion
    global estado
    global lineNumber
    global linea

    token = ''
    estado = 0

    while (posicion < progLong):
        c = programa[posicion]
        #print(c)
        if (c != ' ' or c != '\n'):
            estado = M[estado][mapa[c]]

            if(c == '\n'):
                lineNumber += 1
                #print(linea)
                linea = ''
            else:
                linea += c

            # EOF
            if (estado == 100):
                tipo = getTokenType(estado)
                if imprime:
                    print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                return tipo, token, lineNumber

            ## COMMENTS
            if (estado == 3):
                token += c
                n2 = programa[posicion + 1]
                estAux2 = M[estado][mapa[n2]]

                if (estAux2 == 4):
                    posicion += 1
                    c = programa[posicion]
                    token += c
                    posicion += 1
                    c = programa[posicion]
                    token += c
                    estadoComment = 4

                    #FORMA EL TOKEN CON UN WHILE QUE VA SUMANDO CHARS WHILE estado != 7 (NO SE CIERRE EL COMENTARIO)
                    while(estadoComment != 7):
                        posicion += 1
                        c = programa[posicion]
                        token += c
                        estadoComment = M[estadoComment][mapa[c]]

                    tipo = getTokenType(7)
                    if imprime:
                        print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                    posicion += 1
                    return tipo, token, lineNumber

                else:
                    tipo = getTokenType(estado)
                    posicion += 1
                    if imprime:
                        print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                    return tipo, token, lineNumber


            ## ID, NUMS & DOUBLECHARS
            if (estado == 1 or estado == 2 or estado == 8 or estado == 9 or estado == 11 or estado == 13 or estado == 15 or estado == 130):
                token += c
                n = programa[posicion + 1]
                posicion += 1
                estAux = M[estado][mapa[n]]

                if (estAux != estado):
                    if(token == "else"):
                        tipo = getTokenType(101)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    elif (token == "if"):
                        tipo = getTokenType(102)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    elif(token == "int"):
                        tipo = getTokenType(103)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    elif (token == "return"):
                        tipo = getTokenType(104)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    elif (token == "void"):
                        tipo = getTokenType(105)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    elif (token == "while"):
                        tipo = getTokenType(106)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber
                    else:
                        tipo = getTokenType(estado)
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber

            ## SINGLE CHARS
            else:
                if(c == ' ' or c == '\n'):
                    posicion += 1
                else:
                    if(estado != 3 or estado != 4 or estado != 5 or estado != 6 or estado != 7):
                        token = c
                        tipo = getTokenType(estado)
                        posicion += 1
                        if imprime:
                            print("Tipo: ", tipo.name, "Valor: ", token, "Linea: ", lineNumber)
                        return tipo, token, lineNumber


def getTokenType(estado):
    global respuesta
    respuesta = TokenType(estado)
    return respuesta


#while(posicion < progLong):
    #getToken(True)