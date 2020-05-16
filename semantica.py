from globalTypes import *
from symbolsTable import *
from Parser import *

Error = False

location = 0
scopeNum = 0
globalScope = None
currentScope = None

def nullProc(t):
    None


def typeError(t, message):
    global Error
    print("Type error at line", t.lineno, ":", message)
    Error = True


def insertNode(treeNode):
    global location, currentScope, globalScope

    if treeNode.node_type is NodeType.StmtK and treeNode.name not in ['input','output']:
        if treeNode.stmt is StmtKind.AssignK or treeNode.stmt is StmtKind.ReadK:
            if st_lookup(treeNode.name) is -1:
                # not yet in table, so treat as new definition
                st_insert(treeNode.name, treeNode.lineno, location, treeNode.type, currentScope)
                location += 1

            else:
                # already in table, so ignore location,
                # add line number of use only
                st_insert(treeNode.name, treeNode.lineno, 0, treeNode.type, currentScope)

    elif treeNode.node_type is NodeType.ExpK and treeNode.name not in ['input','output']:
        if treeNode.exp is ExpKind.IdK:
            if st_lookup(treeNode.name) is -1:
                # not yet in table, so treat as new definition
                st_insert(treeNode.name, treeNode.lineno, location, treeNode.type, currentScope)
                location += 1

            else:
                # already in table, so ignore location,
                # add line number of use only
                st_insert(treeNode.name, treeNode.lineno, 0, treeNode.type, currentScope)


def traverse(tree, preProc, postProc):
    global scopeNum, currentScope, globalScope

    if tree is not None:
        if tree.node_kind is NodeKind.func_dec:
            globalScope = Scope()
            currentScope = globalScope
            ScopeStack.append(globalScope)
            globalScope.scope_number = scopeNum

            scopeNum += 1

        preProc(tree)
        for i in range(MAXCHILDREN):
            traverse(tree.child[i], preProc, postProc)
        postProc(tree)
        traverse(tree.sibling, preProc, postProc)


def buildSymTab(tree, imprime):
    traverse(tree, insertNode, nullProc)
    if imprime:
        print
        print("--------------------[ SYMBOLS TABLE ]----------------------")
        print
        printSymTab()


def tabla(tree, imprime):
    global scopeNum

    buildSymTab(tree, imprime)
    return


def semantica(tree, imprime):
    global scopeNum, globalScope, currentScope, initScope
    globalScope = Scope()
    ScopeStack.append(globalScope)
    globalScope.scope_number = scopeNum
    currentScope = initScope = globalScope
    scopeNum += 1

    tabla(tree, imprime)

    return
