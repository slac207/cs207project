from pytest import raises
import unittest
import numpy as np
from RedBlackTree import *
import os

class RedBlackTreeTest(unittest.TestCase):

    def test_smoke(self):
        "smoke test to make sure unbalanced tree is working"
        def connect(dbname):
            try:
                f = open(dbname, 'r+b')
            except IOError:
                fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
                f = os.fdopen(fd, 'r+b')
            return DBDB(f)
        db = connect("/tmp/test2.dbdb")
        db.set("rahul", "aged")
        db.set("pavlos", "aged")
        db.set("kobe", "stillyoung")
        assert db.get("pavlos")=="aged"
        db.commit()
        db.close()
        newdb = connect("/tmp/test2.dbdb")
        assert newdb.get("pavlos")=="aged"
        newdb.close()
        os.remove('/tmp/test2.dbdb')

    def test_inits(self):
        "test init methods"
        dbname = "/tmp/test2.dbdb"
        try:
            f = open(dbname, 'r+b')
        except IOError:
            fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        storage = Storage(f)
        binaryTree = BinaryTree(storage)
        db = DBDB(f)
        db.close()
        os.remove('/tmp/test2.dbdb')

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
