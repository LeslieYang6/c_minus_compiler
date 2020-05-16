from globalTypes import *
from Lexer import *
from symbolsTable import *
from semantica import *

token = None  # holds current token
tokenString = None  # holds the token string value
Error = False
SintaxTree = None
imprimeScanner = False
scopeAux = 0

def syntax_error(message):
    global Error
    l = getLineaGlobal()
    print("")
    print(">>> Syntax error at line " + str(lineNumber + 1) + ": " + message)
    print(">>> " + l + " <<<")
    print("    " + " " * len(l) + "^")
    Error = True


def print_token(token, tokenString):
    if token in {TokenType.IF, TokenType.ELSE, TokenType.WHILE, TokenType.INT, TokenType.RETURN, TokenType.VOID}:
        print("Reserved word: " + tokenString)
    elif token == TokenType.NUM:
        print("Number: " + tokenString)
    elif token == TokenType.ID:
        print("ID: " + tokenString)
    elif token == TokenType.COMMENT:
        print("Comment: " + tokenString)
    elif token == TokenType.SLASH:
        print("/")
    elif token == TokenType.ASTERISC:
        print("*")
    elif token == TokenType.SMALLER:
        print("<")
    elif token == TokenType.BIGGER:
        print(">")
    elif token == TokenType.EQUALS:
        print("=")
    elif token == TokenType.EXC:
        print("!")
    elif token == TokenType.O_CURLY:
        print("{")
    elif token == TokenType.C_CURLY:
        print("}")
    elif token == TokenType.O_BRACKET:
        print("[")
    elif token == TokenType.C_BRACKET:
        print("]")
    elif token == TokenType.O_PAR:
        print("(")
    elif token == TokenType.C_PAR:
        print(")")
    elif token == TokenType.SEMICOLON:
        print(";")
    elif token == TokenType.COMA:
        print(",")
    elif token == TokenType.POINT:
        print(".")
    elif token == TokenType.PLUS:
        print("+")
    elif token == TokenType.ENDFILE:
        print("EOF")
    else:  # should never happen
        print("Unknown token: " + tokenString)


# Variable usada para desplegar Match por Match
global printMatch
printMatch = False


def match(expected):
    global token, tokenString, lineNumber

    if token == expected:
        if printMatch is True:
            print("MATCH! --> " + tokenString + " == " + expected.name)
        token, tokenString, lineNumber = getToken(imprimeScanner)
        return True
    else:
        syntax_error("@match() unexpected token -> ")
        return False


def ignore_comment():
    global token, tokenString, lineNumber
    token, tokenString, lineNumber = getToken(imprimeScanner)


def program():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.program)

    t.child[0] = declaration_list()

    return t


def declaration_list():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.declaration_list)
    t.child[0] = declaration()

    p = t
    while token is not TokenType.ENDFILE:
        print
        q = declaration()
        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    return t


def declaration():
    global token, tokenString, lineNumber, scopeAux
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.declaration)
    t.child[0] = type()

    aux = tokenString
    match(TokenType.ID)

    if token is TokenType.SEMICOLON or token is TokenType.O_BRACKET:
        # Create new Var-Declaration Node
        t.child[1] = var_dec()
        t.child[1].node_type = NodeType.StmtK
        t.child[1].stmt = StmtKind.AssignK

        t.child[1].val = aux
        t.child[1].name = aux
        t.child[1].type = t.child[0].type

    elif token is TokenType.O_PAR:
        t.child[1] = func_dec()
        t.child[1].node_type = NodeType.StmtK
        t.child[1].stmt = StmtKind.AssignK

        t.child[1].val = aux
        t.child[1].name = aux
        t.child[1].type = t.child[0].type

        t.child[1].scope = scopeAux + 1

    else:
        syntax_error("@declaration() unexpected token -> ")
        token, tokenString, lineNumber = getToken(imprimeScanner)

    return t


def var_dec():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.var_dec)
    t.lineno = lineNumber

    if token is TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)

    elif token is TokenType.O_BRACKET:
        match(TokenType.O_BRACKET)

        match(TokenType.NUM)

        match(TokenType.C_BRACKET)

        # Check if it has Semicolon to close variable declaration
        match(TokenType.SEMICOLON)

    return t


def type():
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.type)

    if token == TokenType.INT:
        t.val = tokenString
        t.type = TokenType.INT
        match(TokenType.INT)
        return t

    elif token == TokenType.VOID:
        t.val = tokenString
        t.type = TokenType.VOID
        match(TokenType.VOID)
        return t

    return


def func_dec():
    global token, tokenString, lineNumber, scopeAux

    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.func_dec)
    t.lineno = lineNumber

    if token == TokenType.O_PAR:
        match(TokenType.O_PAR)

        t.child[0] = params()

        match(TokenType.C_PAR)

        t.child[1] = compound_stmt()

    return t


def params():
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.params)

    if token == TokenType.VOID:
        t.val = tokenString
        match(TokenType.VOID)
    else:
        t.child[0] = params_list()

    return t


def params_list():
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.paramList)

    if token == TokenType.C_PAR:
        syntax_error("@params_list() expected parameter -> ")

    if token == TokenType.INT:
        t.child[0] = param()

        if token == TokenType.COMA:
            match(TokenType.COMA)
            t.child[1] = param()

            if token == TokenType.COMA:
                match(TokenType.COMA)
                t.child[2] = param()

    return t


def param():
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.param)

    if token is TokenType.INT:
        t.child[0] = type()

        t.val = tokenString
        t.name = tokenString
        t.lineno = lineNumber

        t.node_type = NodeType.StmtK
        t.stmt = StmtKind.AssignK
        t.type = t.child[0].type

        match(TokenType.ID)

        if token is TokenType.O_BRACKET:
            match(TokenType.O_BRACKET)
            x = match(TokenType.C_BRACKET)

            if x is False:
                syntax_error("@param() expected Closing Bracket ")
                # print_token(token,tokenString)

    return t


def compound_stmt():
    global inout
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.compound_stmt)

    if token == TokenType.O_CURLY:
        match(TokenType.O_CURLY)

        inout = True
        if token == TokenType.C_CURLY:
            match(TokenType.C_CURLY)
            inout = False
        else:
            # Check if there is any local variable declaration
            if token == TokenType.INT or token == TokenType.VOID:
                t.child[0] = local()

                t.child[1] = statement_list()
            else:
                # Looks for Statments declaration
                t.child[0] = statement_list()

            match(TokenType.C_CURLY)
            inout = False

    return t


def local():
    global token, tokenString, lineNumber
    if token == TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.local)

    t = declaration()

    if token == TokenType.INT or token == TokenType.VOID:
        t.sibling = declaration()

    return t


def statement_list():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.statement_list)

    t.child[0] = stmt()

    return t


def stmt():
    global token, tokenString, lineNumber, inout
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.stmt)

    if token is TokenType.IF:
        t.child[0] = if_stmt()

        if token is not TokenType.C_CURLY:
            t.sibling = stmt()

    elif token is TokenType.ID or token is TokenType.NUM or token is TokenType.SEMICOLON:
        t.child[0] = exp_stmt()

        if token is not TokenType.C_CURLY:
            t.sibling = stmt()

    elif token is TokenType.O_CURLY:
        t.child[0] = compound_stmt()

        if token is not TokenType.C_CURLY:
            t.sibling = stmt()

    elif token is TokenType.WHILE:
        t.child[0] = loop_stmt()

        if token is not TokenType.C_CURLY:
            t.sibling = stmt()

    elif token is TokenType.RETURN:
        t.child[0] = return_stmt()

        if token is TokenType.COMMENT:
            ignore_comment()

    return t


def exp_stmt():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.exp_stmt)

    if token is TokenType.SEMICOLON:
        match(TokenType.SEMICOLON)
    else:
        t.child[0] = exp()

        match(TokenType.SEMICOLON)

    return t


def if_stmt():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.if_stmt)
    t.node_type = NodeType.StmtK
    t.stmt = StmtKind.IfK

    t.val = tokenString
    t.name = tokenString
    match(TokenType.IF)

    if token is TokenType.O_PAR:
        match(TokenType.O_PAR)

        t.child[0] = exp()

        match(TokenType.C_PAR)

        # Look for statements
        t.child[1] = stmt()

        if token is TokenType.ELSE:
            t.sibling = new_node(NodeKind.new_else)
            t.sibling.val = tokenString

            match(TokenType.ELSE)

            # Look for ELSE statements
            t.sibling.child[0] = stmt()

    return t


def loop_stmt():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.loop_stmt)
    t.node_type = NodeType.StmtK
    t.stmt = StmtKind.RepeatK

    t.val = tokenString
    t.name = tokenString
    match(TokenType.WHILE)

    if token is TokenType.O_PAR:
        match(TokenType.O_PAR)

        t.child[0] = exp()

        match(TokenType.C_PAR)

        # Look for WHILE statements
        t.child[1] = stmt()

    return t


def return_stmt():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.return_stmt)

    if token is TokenType.RETURN:
        t.val = tokenString
        match(TokenType.RETURN)

        if token is not TokenType.SEMICOLON:
            t.child[0] = exp()

            match(TokenType.SEMICOLON)

        else:
            match(TokenType.SEMICOLON)

    return t


def exp():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.exp)

    t.child[0] = simple_exp()

    return t


def var():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.var)

    t.name = tokenString
    t.val = tokenString
    t.lineno = lineNumber

    t.node_type = NodeType.StmtK
    t.stmt = StmtKind.AssignK
    t.type = TokenType.INT

    match(TokenType.ID)

    if token is TokenType.O_BRACKET:
        t.node_type = NodeType.StmtK
        t.stmt = StmtKind.ReadK

        match(TokenType.O_BRACKET)

        t.child[0] = exp()

        match(TokenType.C_BRACKET)

    return t


def simple_exp():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.simple_exp)

    t.child[0] = add_exp()

    if token is TokenType.BIGGER or token is TokenType.SMALLER or token is TokenType.EQUALS or token is TokenType.EXC:
        t.child[1] = rel_op()

        t.child[2] = exp()

    if token == TokenType.SEMICOLON or token is TokenType.C_PAR or token is TokenType.COMA:
        return t
    else:
        t.sibling = simple_exp()

    return t


def rel_op():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.rel_op)


    if token is TokenType.EQUALS:
        match(TokenType.EQUALS)

        if token is not TokenType.EQUALS:
            t.op = '='
            return t

        elif token is TokenType.EQUALS:
            tokenString = '=='
            token = TokenType.EQEQ
            t.op = tokenString
            match(TokenType.EQEQ)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t

    elif token is TokenType.BIGGER:
        token, tokenString, lineNumber = getToken(imprimeScanner)

        if token is not TokenType.EQUALS:
            tokenString = '>'
            token = TokenType.BIGGER
            t.op = tokenString
            match(TokenType.BIGGER)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t

        if token is TokenType.EQUALS:
            tokenString = '>='
            token = TokenType.BIGTHAN
            t.op = tokenString
            match(TokenType.BIGTHAN)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t

    elif token is TokenType.SMALLER:
        token, tokenString, lineNumber = getToken(imprimeScanner)

        if token is not TokenType.EQUALS:
            tokenString = '<'
            token = TokenType.SMALLER
            t.op = tokenString
            match(TokenType.SMALLER)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t

        if token is TokenType.EQUALS:
            tokenString = '<='
            token = TokenType.SMALLTHAN
            t.op = tokenString
            match(TokenType.SMALLTHAN)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t

    elif token is TokenType.EXC:
        token, tokenString, lineNumber = getToken(imprimeScanner)

        if token is not TokenType.EQUALS:
            tokenString = '!'
            token = TokenType.EXC
            syntax_error("--> Expected =")
            return t

        if token is TokenType.EQUALS:
            tokenString = '!='
            token = TokenType.NOTEQ
            t.op = tokenString
            match(TokenType.NOTEQ)

            t.child[0] = new_node(NodeKind.factor)
            t.child[0].val = tokenString

            return t


def add_exp():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.add_exp)

    if token is TokenType.PLUS or token == TokenType.MINUS:
        t.child[0] = add_op()

        t.child[1] = term()

        if token is TokenType.PLUS or token == TokenType.MINUS:
            t.sibling = add_exp()

    else:
        t.child[0] = term()

    return t


def add_op():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.add_op)

    if token is TokenType.PLUS:
        t.op = tokenString
        match(TokenType.PLUS)
    elif token is TokenType.MINUS:
        t.op = tokenString
        match(TokenType.MINUS)

    return t


def term():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.term)

    if token is TokenType.ASTERISC or token is TokenType.SLASH:
        t.child[0] = mul_op()

        t.child[1] = factor()

        if token is TokenType.ASTERISC or token == TokenType.SLASH:
            t.sibling = term()

    else:
        t.child[0] = factor()

    return t


def mul_op():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.mul_op)

    if token == TokenType.ASTERISC:
        t.op = tokenString
        match(TokenType.ASTERISC)
    elif token == TokenType.SLASH:
        t.op = tokenString
        match(TokenType.SLASH)

    return t


def factor():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.factor)

    if token is TokenType.ID:
        aux = tokenString
        t.child[0] = var()

        if token is TokenType.O_PAR:
            t.child[1] = call()

            #t.child[1].node_type = NodeType.ExpK
            #t.child[1].exp = ExpKind.IdK
            #t.child[1].val = aux
            #t.child[1].name = aux
            #t.child[1].lineno = lineNumber

            t.sibling = new_node(NodeKind.closingP)
            t.sibling.val = ')'

            return t

        elif token is TokenType.O_BRACKET:
            t.child[1] = var()

            t.sibling = new_node(NodeKind.closingP)
            t.sibling.val = ']'

            return t

        return t

    elif token is TokenType.O_PAR:
        match(TokenType.O_PAR)

        t.val = tokenString

        t.child[0] = exp()

        match(TokenType.C_PAR)

        return t

    elif token == TokenType.NUM:
        t.val = tokenString
        match(TokenType.NUM)

        if token is TokenType.COMA:
            return t



def call():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.call)

    match(TokenType.O_PAR)

    if token is not TokenType.C_PAR:

        t.child[0] = args()

        if token is TokenType.C_PAR:
            match(TokenType.C_PAR)
    else:
        match(TokenType.C_PAR)

    return t


def args():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.args)

    if token is not TokenType.C_PAR:
        t.child[0] = args_list()

    return t


def args_list():
    global token, tokenString, lineNumber
    if token is TokenType.COMMENT:
        ignore_comment()

    t = new_node(NodeKind.args_list)

    t.val = tokenString

    t.child[0] = exp()

    if token is TokenType.COMA:
        match(TokenType.COMA)

        t.sibling = args_list()

    return t


# Following function creates new Nodes
# for tree based on NodeKind needed
def new_node(kind):
    t = TreeNode()
    if t is None:
        print("Out of memory error at line " + lineNumber)
    else:
        t.node_kind = kind
        t.lineNumber = lineNumber
    return t


# Variable indent_number is used by printTree to
# store current number of spaces to indent
indent_number = 0


# procedure printTree prints a syntax tree to the
# listing file using indentation to indicate subtrees
def print_tree(tree):
    global indent_number
    indent_number += 2  # INDENT
    while tree is not None:

        if tree.node_kind is NodeKind.var_dec:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.type:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.func_dec:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.params:
            if tree.val is not None:
                print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.param:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.var:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.rel_op:
            print(" " * indent_number + tree.op)
        elif tree.node_kind is NodeKind.add_op:
            print(" " * indent_number + tree.op)
        elif tree.node_kind is NodeKind.mul_op:
            print(" " * indent_number + tree.op)
        elif tree.node_kind is NodeKind.factor:
            if tree.val is not None:
                print(" " * indent_number + tree.val)
            elif tree.op is not None:
                print(" " * indent_number + tree.op)
        elif tree.node_kind is NodeKind.if_stmt:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.return_stmt:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.loop_stmt:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.new_else:
            print(" " * indent_number + tree.val)
        elif tree.node_kind is NodeKind.assign:
            print(" " * indent_number + tree.val)

        for i in range(MAXCHILDREN):
            print_tree(tree.child[i])

        tree = tree.sibling
    indent_number -= 2  # UN INDENT


# the primary function of the parser
# Function parse returns the newly
# constructed syntax tree
def parser(imprime):
    global token, tokenString, lineNumber

    token, tokenString, lineNumber = getToken(imprimeScanner)
    t = program()

    if token is not TokenType.ENDFILE:
        syntax_error("Code ends before file\n")

    if imprime is True:
        print
        print(" --- AST ---")
        print
        print_tree(t)

        return t

    return t