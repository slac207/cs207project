import sys
import os
from pytest import raises
import unittest
import numpy as np
from RedBlackTree import *

class RedBlackTreeTest(unittest.TestCase):

    def test_smoke(self):
        "Smoke test to make sure unbalanced tree is working"
        db = self.get_f("/tmp/test1.dbdb")
        db.set("rahul", "aged")
        db.set("pavlos", "aged")
        db.set("kobe", "stillyoung")
        assert db.get("pavlos")=="aged"
        db.commit()
        db.close()
        newdb = self.get_f("/tmp/test1.dbdb")
        assert newdb.get("pavlos")=="aged"
        newdb.close()
        os.remove('/tmp/test1.dbdb')

    def test_inits(self):
        "Test init methods."
        db = self.get_f("/tmp/test2.dbdb")
        db.close()
        os.remove('/tmp/test2.dbdb')

    def test_set_get(self):
        "Test that we can set a value and then retrieve it with get()."
        db = self.get_f("/tmp/test3.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test3.dbdb')

    def test_set_commit_get(self):
        "Test that we can set a value then retrieve it after committing."
        db = self.get_f("/tmp/test4.dbdb")
        db.set("pavlos", "aged")
        db.commit()
        db.close()
        db = self.get_f("/tmp/test4.dbdb")
        assert db.get("pavlos") == "aged"
        db.close()
        os.remove('/tmp/test4.dbdb')

    def test_set_no_commit(self):
        "Test that getting after setting without committing will raise a KeyError."
        db = self.get_f("/tmp/test5.dbdb")
        db.set("pavlos", "aged")
        db.close()
        db = self.get_f("/tmp/test5.dbdb")
        with raises(KeyError):
            db.get("pavlos")=="aged"
        db.close()
        os.remove('/tmp/test5.dbdb')

    def test_get_multiple(self):
        "Test that we can set multiple values."
        db = self.get_f("/tmp/test6.dbdb")
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
        "Test that we can delete a node."
        db = self.get_f("/tmp/test7.dbdb")
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
        "Test that we can close a file."
        db = self.get_f("/tmp/test8.dbdb")
        db.close()
        with raises(ValueError):
            db._assert_not_closed()
        os.remove('/tmp/test8.dbdb')

    def test_delete_root(self):
        "Test that we can delete a root node and have expected behavior."
        db = self.get_f("/tmp/test7.dbdb")
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

    def test_set_set_commit(self):
        """
        Test that we can set a value, replace it with a new value, 
        and the new value will be there post-commit.
        """
        db = self.get_f("/tmp/test8.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos") == "aged"
        db.set("pavlos", "young")
        assert db.get("pavlos") == "young"
        db.commit()
        db.close()
        db = self.get_f("/tmp/test8.dbdb")
        assert db.get("pavlos") == "young"
        db.close()
        os.remove('/tmp/test8.dbdb')

    def test_set_set(self):
        "Test that we can set a value and then replace it with a new value."
        db = self.get_f("/tmp/test9.dbdb")
        db.set("pavlos", "aged")
        assert db.get("pavlos") == "aged"
        db.set("pavlos", "young")
        assert db.get("pavlos") == "young"
        db.close()
        os.remove('/tmp/test9.dbdb')
        
    def test_getRoot(self):
        "Test that we can correctly recall the root key."
        db = self.get_f("/tmp/test10.dbdb")
        db.set("kobe", "baby")
        db.set("rahul", "veryyoung")
        db.set("pavlos", "stillyoung")
        assert db.rootKey() == "pavlos"
        db.close()
        os.remove('/tmp/test10.dbdb') 
        
    def test_nonexistantKey(self):
        "Test that we can correctly reject nonexistant keys."
        db = self.get_f("/tmp/test11.dbdb")
        db.set("rahul", "veryyoung")
        db.set("pavlos", "stillyoung")
        db.commit()
        with raises(KeyError):
            db.get("kobe")
        os.remove('/tmp/test11.dbdb')   

if __name__=='__main__':
    try:  # pragma: no cover
        unittest.main()  # pragma: no cover
    except SystemExit as inst:  # pragma: no cover
        if inst.args[0] is True:  # pragma: no cover
            raise  # pragma: no cover
