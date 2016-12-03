import os
import numpy as np
import pickle
import struct
import portalocker

"""
Uses CS207 Lab 10 as a foundation for
a Database class DBDB that implements a simple key/value database.
It lets you associate a key with a value, and store that association
on disk for later retrieval.

Lab 10 uses a simple unbalanced Binary Tree

Additions to DBDB from Lab10:
get_All_LTE(key) which returns two lists
LTE_Keys : List of Keys less than or equal to key
LTE_Vals : List of Vals with corresponding Keys less than or equal to key


"""


class ValueRef(object):
    " a reference to a string value on disk"

    def __init__(self, referent=None, address=0):
        """Initialize with either or both the object to be stored
        and its disk address"""
        self._referent = referent  # value to store
        self._address = address  # address to store at

    @property
    def address(self):
        """Return the disk address of the object"""
        return self._address

    def prepare_to_store(self, storage):
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """Encode string value as utf-8"""
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(in_bytes):
        """Decode bytes to string value"""
        return in_bytes.decode('utf-8')

    def get(self, storage):
        "read bytes for value from disk"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        # called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))


class BinaryNodeRef(ValueRef):
    "reference to a btree node on disk"

    # calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "use pickle to convert node to bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )


class BinaryNode(object):
    @classmethod
    def from_node(cls, node, **kwargs):
        "clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        """Initialize a node with key, value, left and right children, and color"""
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        # calls BinaryNodeRef.store. which calls
        # BinaryNodeRef.prepate_to_store
        # which calls this again and recursively stores
        # the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)


class BinaryTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"

    def __init__(self, storage):
        """Initialize tree with disk storage and tree node if it already exists"""
        self._storage = storage
        self._refresh_tree_ref()
        self._tree_ref = None

    def commit(self):
        "changes are final only when committed"
        # triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        # make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "get value for a key"
        # if tree is not locked by another writer
        # refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        # get the top level node
        node = self._follow(self._tree_ref)
        # traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key:
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def get_All_LTE(self, key):
        "get all keys and values with keys less than or equal to passed key"
        "Returns a list of Keys and a corresponding list of Values"
        "Where all Keys are less than passed key"
        "Calls recursive function follow_LTE to find such"

        # if tree is not locked by another writer
        # refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()

        # get the top level node
        node = self._follow(self._tree_ref)

        # Initial Key and Val List set to empty
        LTE_Keys = []
        LTE_Vals = []

        # Recursively find Keys and Values where Key is Less Than or Equal to key
        LTE_Keys, LTE_Vals = self.follow_LTE(key, node, LTE_Keys, LTE_Vals)
        return LTE_Keys, LTE_Vals

    def follow_LTE(self, key, node, LTE_Keys, LTE_Vals):
        "Recursive function to add Keys and Values"
        "to lists, where Keys are less than or equal to key"

        # If node is None, stop and return lists
        if node is None:
            return LTE_Keys, LTE_Vals
        # If node's Key is <= key, add Key and Value to list
        elif key >= node.key:
            LTE_Keys.append(node.key)
            LTE_Vals.append(self._follow(node.value_ref))
            rightNode = self._follow(node.right_ref)
            self.follow_LTE(key, rightNode, LTE_Keys, LTE_Vals)

        # Always move left if current node is not None
        leftNode = self._follow(node.left_ref)
        self.follow_LTE(key, leftNode, LTE_Keys, LTE_Vals)

        # After checking left and right nodes, return lists
        return LTE_Keys, LTE_Vals

    def set(self, key, value):
        "set a new value in the tree. will cause a new tree"
        # try to lock the tree. If we succeed make sure
        # we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)

    def _insert(self, node, key, value_ref):
        "insert a new node creating a new path from root"
        # create a tree ifnthere was none so far
        if node is None:
            new_node = BinaryNode(
                BinaryNodeRef(), key, value_ref, BinaryNodeRef())
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._insert(
                    self._follow(node.left_ref), key, value_ref))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._insert(
                    self._follow(node.right_ref), key, value_ref))
        else:  # create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "delete node with key, creating new tree and path"
        if self._storage.lock():
            self._refresh_tree_ref()
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)

    def _delete(self, node, key):
        "underlying delete implementation"
        if node is None:
            raise KeyError
        elif key < node.key:
            new_node = BinaryNode.from_node(
                node,
                left_ref=self._delete(
                    self._follow(node.left_ref), key))
        elif key > node.key:
            new_node = BinaryNode.from_node(
                node,
                right_ref=self._delete(
                    self._follow(node.right_ref), key))
        else:
            left = self._follow(node.left_ref)
            right = self._follow(node.right_ref)
            if left and right:
                replacement = self._find_max(left)
                left_ref = self._delete(
                    self._follow(node.left_ref), replacement.key)
                new_node = BinaryNode(
                    left_ref,
                    replacement.key,
                    replacement.value_ref,
                    node.right_ref,
                )
            elif left:
                return node.left_ref
            else:
                return node.right_ref
        return BinaryNodeRef(referent=new_node)

    def _follow(self, ref):
        "get a node from a reference"
        # calls BinaryNodeRef.get
        return ref.get(self._storage)

    def _find_max(self, node):
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node


class Storage(object):
    """Class to manage writing to file in consecutive blocks with locking"""
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        """Initialize Storage block, Set Lock to False"""
        self._f = f
        self.locked = False
        # we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        "guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "if not locked, lock the file for writing"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        """Unlock the file if it is currently locked"""
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        """Seek pointer to the end of the block"""
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        """Convert bytes to integer format"""
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        """Convert integers to byte format"""
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        """Read an integer from file"""
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        """Write an integer to file"""
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "write data to disk, returning the adress at which you wrote it"
        # first lock, get to end, get address to return, write size
        # write data, unlock <==WRONG, dont want to unlock here
        # your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        """Read data from address on disk"""
        self._f.seek(address)
        length = self._read_integer()
        data = self._f.read(length)
        return data

    def commit_root_address(self, root_address):
        """Write the root address at position 0 of the superblock"""
        self.lock()
        self._f.flush()
        # make sure you write root address at position 0
        self._seek_superblock()
        # write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address)
        self._f.flush()
        self.unlock()

    def get_root_address(self):
        """Read in the root"""
        # read the first integer in the file
        # your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        """Close the storage file"""
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        """Check if file is closed"""
        return self._f.closed


class DBDB(object):
    """A Database that implements a simple key/value database.
    It lets you associate a key with a value, and store that association
    on disk for later retrieval."""

    def __init__(self, f):
        """Initialize the storage file and structure for the database"""
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        """Check if the storage file is closed"""
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        """Close the storage file"""
        self._storage.close()

    def commit(self):
        """Check if the storage file is closed. If not, write database to file"""
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        """Retrieve the value associated with a key"""
        self._assert_not_closed()
        return self._tree.get(key)

    def get_All_LTE(self, key):
        "get all Keys and Values with keys less than or equal to passed key"
        "Returns two lists: first list is of Keys, second lists is of Vals"
        "where Keys is less than or equal to key"
        "Uses recursion to find such"
        self._assert_not_closed()
        return self._tree.get_All_LTE(key)

    def set(self, key, value):
        """Set the value associated with a key"""
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        """Delete a key, value pair from the Database"""
        self._assert_not_closed()
        return self._tree.delete(key)


def connect(dbname):
    """Connect to Database dbname"""
    try:
        f = open(dbname, 'r+b')
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, 'r+b')
    return DBDB(f)
