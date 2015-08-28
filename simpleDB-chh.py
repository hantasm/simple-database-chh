# simpleDB developed by Chenghu He

import sys

# record of transaction to recovery
class simpleRecovery():

    def __init__(self):
        # record of the keys which was NULL
        self.toNull = set()
        # record of the keys which had value
        self.toValue = dict()

# database object
class simpleDB:

    def __init__(self):
        self.db = dict()
        self.trans = []

    def checkTran(self, key):
        if len(self.trans) > 0:
            # if there is an active transaction, record the recovery key and value
            if (key not in self.trans[-1].toNull) and (key not in self.trans[-1].toValue):
                if key in self.db:
                    self.trans[-1].toValue[key] = self.db[key]
                else:
                    self.trans[-1].toNull.add(key)

    def setValue(self, key, value):
        self.checkTran(key)
        self.db[key] = value

    def getValue(self, key):
        return self.db[key] if key in self.db else 'NULL'

    def unsetKey(self, key):
        self.checkTran(key)
        if key in self.db: del self.db[key]

    def numOfValue(self, inValue):
        return sum(value == inValue for value in self.db.values())

    def beginTran(self):
        rec = simpleRecovery()
        self.trans.append(rec)

    def rollbackTran(self):
        if len(self.trans) < 1: return 'NO TRANSACTON'
        # reset all the keys that were NULL
        for key in self.trans[-1].toNull:
            if key in self.db: del self.db[key]
        # reset all the keys that had values
        for key, value in self.trans[-1].toValue.items():
            self.db[key] = value
        self.trans.pop() 

    def commitTran(self):
        # write data to disk in real system
        self.trans = []

# main
sdb = simpleDB()
for line in sys.stdin:
    if line == None: break
    args = line[:-1].split(' ')
    argNum = len(args)
    if argNum == 3:
        if args[0] == 'SET':
            sdb.setValue(args[1], args[2])
    elif argNum == 2:
        if args[0] == 'GET':
            val = sdb.getValue(args[1])
            print(val)
        elif args[0] == 'UNSET':
            sdb.unsetKey(args[1])
        elif args[0] == 'NUMEQUALTO':
            val = sdb.numOfValue(args[1])
            print(val)
    elif argNum == 1:
        if args[0] == 'BEGIN':
            sdb.beginTran()
        elif args[0] == 'ROLLBACK':
            val = sdb.rollbackTran()
            if val != None: print(val)
        elif args[0] == 'COMMIT':
            sdb.commitTran()
        elif args[0] == 'END':
            break
 
