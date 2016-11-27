from pytest import raises
import unittest
import numpy as np
from RedBlackTree import *
import os

class RedBlackTreeTest(unittest.TestCase):
    def get_f(self,dbname):
        "Open file with dbname as path"
        try:
            f = open(dbname, 'r+b')
        except IOError:
            fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, 'r+b')
        return f

    def test_smoke(self):
        "Smoke test to make sure unbalanced tree is working"
        f = self.get_f("/tmp/test1.dbdb")
        db = DBDB(f)
        db.set("rahul", "aged")
        db.set("pavlos", "aged")
        db.set("kobe", "stillyoung")
        assert db.get("pavlos")=="aged"
        db.commit()
        db.close()
        f = self.get_f("/tmp/test1.dbdb")
        newdb = DBDB(f)
        assert newdb.get("pavlos")=="aged"
        newdb.close()
        os.remove('/tmp/test1.dbdb')

    def test_inits(self):
        "Test init methods"
        f = self.get_f("/tmp/test2.dbdb")
        storage = Storage(f)
        binaryTree = BinaryTree(storage)
        db = DBDB(f)
        db.close()
        os.remove('/tmp/test2.dbdb')

    def test_set_get(self):
        "Test that we can set a value and then retrieve it with get"
        f = self.get_f("/tmp/test3.dbdb")
        db = DBDB(f)
        db.set("pavlos", "aged")
        assert db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test3.dbdb')

    def test_set_commit_get(self):
        "Test that we can set a value then retrieve it after committing"
        f = self.get_f("/tmp/test4.dbdb")
        db = DBDB(f)
        db.set("pavlos", "aged")
        db.commit()
        db.close()
        f = self.get_f("/tmp/test4.dbdb")
        db = DBDB(f)
        assert db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test4.dbdb')

    def test_set_no_commit(self):
        "Test that getting after setting without committing will raise a key error"
        f = self.get_f("/tmp/test5.dbdb")
        db = DBDB(f)
        db.set("pavlos", "aged")
        db.close()
        f = self.get_f("/tmp/test5.dbdb")
        db = DBDB(f)
        with raises(KeyError):
            db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test5.dbdb')

    def test_get_multiple(self):
        "Test that we can set multiple values"
        f = self.get_f("/tmp/test6.dbdb")
        db = DBDB(f)
        db.set("kobe", "baby")
        db.set("rahul", "veryyoung")
        db.set("pavlos", "stillyoung")
        db.set("andy", "old")
        db.set("lisa", "ancient")
        assert db.get("rahul")=="veryyoung"
        assert db.get("pavlos")=="stillyoung"
        assert db.get("lisa")=="ancient"
        assert db.get("andy")=="old"
        db.close()
        os.remove('/tmp/test6.dbdb')

    def test_delete(self):
        "Test that we can delete a node"
        f = self.get_f("/tmp/test7.dbdb")
        db = DBDB(f)
        db.set("kobe", "baby")
        db.set("allison", "veryyoung")
        db.set("greg", "stillyoung")
        db.set("yi", "old")
        db.set("cathy", "ancient")
        db.delete("greg")
        with raises(KeyError):
            db.get("greg")
        with raises(KeyError):
            db.delete("greg")
        assert db.get("allison")=="veryyoung"
        assert db.get("yi")=="old"
        assert db.get("cathy")=="ancient"
        assert db.get("kobe")=="baby"
        db.close()
        os.remove('/tmp/test7.dbdb')

    def test_close(self):
        "Test that we can delete a node"
        f = self.get_f("/tmp/test8.dbdb")
        db = DBDB(f)
        db.close()
        with raises(ValueError):
            db._assert_not_closed()
        os.remove('/tmp/test8.dbdb')

    def test_delete_root(self):
        "Test that we can delete a root node and have expected behavior"
        f = self.get_f("/tmp/test7.dbdb")
        db = DBDB(f)
        db.set("kobe", "baby")
        db.set("yi", "old")
        db.set("cathy", "ancient")
        db.set("greg", "stillyoung")
        db.set("allison", "veryyoung")
        db.delete("kobe")
        with raises(KeyError):
            db.get("kobe")
        with raises(KeyError):
            db.delete("kobe")
        assert db.get("allison")=="veryyoung"
        assert db.get("yi")=="old"
        assert db.get("cathy")=="ancient"
        assert db.get("greg")=="stillyoung"
        db.close()
        os.remove('/tmp/test7.dbdb')

    def test_set_set(self):
        "Test that we can set a value and then replace it with a new value"
        f = self.get_f("/tmp/test8.dbdb")
        db = DBDB(f)
        db.set("pavlos", "aged")
        assert db.get("pavlos")=="aged"
        db.set("pavlos", "young")
        assert db.get("pavlos")=="young"
        db.commit()
        db.close()
        f = self.get_f("/tmp/test8.dbdb")
        db = DBDB(f)
        assert db.get("pavlos")=="young"
        db.close()
        os.remove('/tmp/test8.dbdb')

    # def test_delete_refresh(self):
    #     "Test that we can delete a node while the storage is unlocked"
    #     f = self.get_f("/tmp/test9.dbdb")
    #     db = DBDB(f)
    #     db.set("kobe", "baby")
    #     db.set("cathy", "ancient")
    #     db.set("allison", "veryyoung")
    #     db._storage.unlock()
    #     db.delete("cathy")
    #     with raises(KeyError):
    #         db.get("cathy")
    #     with raises(KeyError):
    #         db.delete("cathy")
    #     assert db.get("allison")=="veryyoung"
    #     assert db.get("kobe")=="baby"
    #     db.close()
    #     os.remove('/tmp/test9.dbdb')


if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
