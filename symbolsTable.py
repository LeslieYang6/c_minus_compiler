from globalTypes import *

# the hash table
BucketList = {}

# the stack
ScopeStack = []

pos = 0
scopeSwitch = False


class Scope:
    def __init__(self):
        self.scope_number = 0
        self.bucket_list = None


def st_insert(name, lineno, loc, tipo, scope):
    global pos

    switch = False

    if len(BucketList.items()) is 0:
        BucketList[pos] = {}
        BucketList[pos]['name'] = name
        BucketList[pos]['type'] = tipo
        BucketList[pos]['location'] = loc
        BucketList[pos]['scope'] = scope.scope_number
        BucketList[pos]['lineno'] = str(lineno+1)
        pos = pos + 1

        return

    for node_id, node_info in BucketList.items():
        if name == node_info['name']:
            switch = True
            auxPos = node_id

    if switch is True:
        BucketList[auxPos]['lineno'] = str(BucketList[auxPos]['lineno']) + "   " + str(lineno+1)

    else:
        BucketList[pos] = {}
        BucketList[pos]['name'] = name
        BucketList[pos]['type'] = tipo
        BucketList[pos]['location'] = loc
        BucketList[pos]['scope'] = scope.scope_number
        BucketList[pos]['lineno'] = str(lineno+1)
        pos = pos + 1


def st_lookup(name):
    switch = False
    for node_id, node_info in BucketList.items():

        c = node_info['name']
        if name is c:
            switch = True
            auxPos = node_id

    if switch is True:
        return BucketList[auxPos]['name']
    else:
        return -1


def printSymTab():
    print("Variable Name  Type           Location  Scope  Line Numbers")
    print("-------------  -------------  --------  -----  ------------")

    for node_id, node_info in BucketList.items():

        print '{0:14}'.format(node_info['name']),
        print '{0:14}'.format(node_info['type']),
        print '{0:8d}'.format(node_info['location']),
        print '{0:6}'.format(node_info['scope']),
        print '  {0:20}'.format(node_info['lineno']),
        print