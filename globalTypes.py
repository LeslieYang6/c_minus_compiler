from enum import Enum


class TokenType(Enum):
    NUM = 1
    ID = 2
    SLASH = 3
    COMMENT = 4
    COMMENT = 5
    COMMENT = 6
    COMMENT = 7
    ASTERISC = 8
    SMALLER = 9
    SMALLTHAN = 90
    BIGGER = 11
    BIGTHAN = 110
    EQUALS = 13
    EQEQ = 130
    EXC = 15
    NOTEQ = 150
    O_CURLY = 18
    C_CURLY = 17
    O_BRACKET = 20
    C_BRACKET = 19
    O_PAR = 22
    C_PAR = 21
    SEMICOLON = 24
    COMA = 23
    MINUS = 25
    POINT = 107
    PLUS = 26
    ENDFILE = 100
    SPACE = 0
    ELSE = 101
    IF = 102
    INT = 103
    RETURN = 104
    VOID = 105
    WHILE = 106


#***********   Syntax tree for parsing ************

class NodeKind(Enum):
    program = 1
    declaration_list = 2
    declaration = 3
    var_dec = 4
    type = 5
    func_dec = 6
    params = 7
    paramList = 8
    param = 9
    compound_stmt = 10
    local = 11
    statement_list = 12
    stmt = 13
    exp_stmt = 14
    if_stmt = 15
    loop_stmt = 16
    return_stmt = 17
    exp = 18
    var = 19
    simple_exp = 20
    rel_op = 21
    add_exp = 22
    add_op = 23
    term = 24
    mul_op = 25
    factor = 26
    call = 27
    args = 28
    args_list = 29
    closingP = 30
    new_else = 31
    assign = 32



# Maximo numero de hijos por nodo (3 para el if)
MAXCHILDREN = 3


class TreeNode:
    def __init__(self):
        # MAXCHILDREN = 3 esta en globalTypes
        self.child = [None] * MAXCHILDREN  # tipo treeNode
        self.sibling = None                # tipo treeNode
        self.lineno = 0                    # tipo int
        self.node_kind = None              # tipo NodeKind, en globalTypes

        # en realidad los dos siguientes deberian ser uno solo (kind)
        # siendo la  union { StmtKind stmt; ExpKind exp;}
        self.stmt = None                  # tipo StmtKind
        self.exp = None                   # tipo ExpKind

        # en realidad los tres siguientes deberian ser uno solo (attr)
        # siendo la  union { TokenType op; int val; char * name;}
        self.op = None                    # tipo TokenType
        self.val = None                   # tipo int
        self.name = None                  # tipo String

        # for type checking of exps
        self.type = None                  # de tipo ExpType