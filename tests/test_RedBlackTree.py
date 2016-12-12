import sys
import os
from pytest import raises
import unittest
import numpy as np
from cs207rbtree import RedBlackTree 

class RedBlackTreeTest(unittest.TestCase):

    def test_smoke(self):
        "Smoke test to make sure unbalanced tree is working"
        db = RedBlackTree.connect("/tmp/test1.dbdb")
        db.set("rahul", "aged")
        db.set("pavlos", "aged")
        db.set("kobe", "stillyoung")
        assert db.get("pavlos")=="aged"
        db.commit()
        db.close()
        newdb = RedBlackTree.connect("/tmp/test1.dbdb")
        assert newdb.get("pavlos")=="aged"
        newdb.close()
        os.remove('/tmp/test1.dbdb')

    def test_inits(self):
        "Test init methods."
        db = RedBlackTree.connect("/tmp/test2.dbdb")
        db.close()
        os.remove('/tmp/test2.dbdb')

    def test_set_get(self):
        "Test that we can set a value and then retrieve it with get()."
        db = RedBlackTree.connect("/tmp/test3.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test3.dbdb')

    def test_set_commit_get(self):
        "Test that we can set a value then retrieve it after committing."
        db = RedBlackTree.connect("/tmp/test4.dbdb")
        db.set("pavlos", "aged")
        db.commit()
        db.close()
        db = RedBlackTree.connect("/tmp/test4.dbdb")
        assert db.get("pavlos") == "aged"
        db.close()
        os.remove('/tmp/test4.dbdb')

    def test_set_no_commit(self):
        "Test that getting after setting without committing will raise a KeyError."
        db = RedBlackTree.connect("/tmp/test5.dbdb")
        db.set("pavlos", "aged")
        db.close()
        db = RedBlackTree.connect("/tmp/test5.dbdb")
        with raises(KeyError):
            db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test5.dbdb')

    def test_get_multiple(self):
        "Test that we can set multiple values."
        db = RedBlackTree.connect("/tmp/test6.dbdb")
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

    def test_close(self):
        "Test that we can close a file."
        db = RedBlackTree.connect("/tmp/test8.dbdb")
        db.close()
        with raises(ValueError):
            db._assert_not_closed()
        os.remove('/tmp/test8.dbdb')

    def test_set_set_commit(self):
        """
        Test that we can set a value, replace it with a new value,
        and the new value will be there post-commit.
        """
        db = RedBlackTree.connect("/tmp/test8.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos") == "aged"
        db.set("pavlos", "young")
        assert db.get("pavlos") == "young"
        db.commit()
        db.close()
        db = RedBlackTree.connect("/tmp/test8.dbdb")
        assert db.get("pavlos") == "young"
        db.close()
        os.remove('/tmp/test8.dbdb')

    def test_set_set(self):
        "Test that we can set a value and then replace it with a new value."
        db = RedBlackTree.connect("/tmp/test9.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos") == "aged"
        db.set("pavlos", "young")
        assert db.get("pavlos") == "young"
        db.close()
        os.remove('/tmp/test9.dbdb')

    def test_nonexistantKey(self):
        "Test that we can correctly reject nonexistant keys."
        db = RedBlackTree.connect("/tmp/test11.dbdb")
        db.set("rahul", "veryyoung")
        db.set("pavlos", "stillyoung")
        db.commit()
        with raises(KeyError):
            db.get("kobe")
        db.close()
        os.remove('/tmp/test11.dbdb')        

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
