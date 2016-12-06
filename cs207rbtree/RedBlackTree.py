import pickle # for BinaryNodeRef class
import os # for storage class
import struct # for storage class
import portalocker # for storage class

class ValueRef(object):
    "A reference to a string value on disk"
    def __init__(self, referent=None, address=0):
        self._referent = referent # value to store
        self._address = address # address to store at

    @property
    def address(self):
        "get the address"
        return self._address

    def prepare_to_store(self, storage):
        # Not implemented
        pass

    @staticmethod
    def referent_to_bytes(referent):
        "convert the string to utf-8 encoding"
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        "convert utf-8 encoding to a string"
        return bytes.decode('utf-8')

    def get(self, storage):
        "read bytes for value from disk and assign string to referent property"
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        "store bytes for value to disk"
        #called by BinaryNode.store_refs
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))

class BinaryNodeRef(ValueRef):
    "Reference to a btree node on disk"

    #calls the BinaryNode's store_refs
    def prepare_to_store(self, storage):
        "Have a node store its refs"
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        "Use pickle to convert node to dictionary of bytes"
        return pickle.dumps({
            'left': referent.left_ref.address,
            'key': referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        "Unpickle bytes to get a node object"
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )

class BinaryNode(object):
    """
    Class that points to one node of a Binary Tree and stores references
    to its children nodes.
    """
    @classmethod
    def from_node(cls, node, **kwargs):
        "Clone a node with some changes from another one"
        return cls(
            left_ref=kwargs.get('left_ref', node.left_ref),
            key=kwargs.get('key', node.key),
            value_ref=kwargs.get('value_ref', node.value_ref),
            right_ref=kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        "Stores key and references to the value, left node, and right node"
        self.left_ref = left_ref
        self.key = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        "method for a node to store all of its stuff"
        self.value_ref.store(storage)
        #calls BinaryNodeRef.store. which calls
        #BinaryNodeRef.prepate_to_store
        #which calls this again and recursively stores
        #the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)

class BinaryTree(object):
    "Immutable Binary Tree class. Constructs new tree on changes"
    def __init__(self, storage):
        "Sets storage object as property and refreshes reference to tree"
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        "Changes are final only when committed"
        #triggers BinaryNodeRef.store
        self._tree_ref.store(self._storage)
        #make sure address of new tree is stored
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        "Get reference to new tree if it has changed"
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        "Get value for a key"
        #your code here
        #if tree is not locked by another writer
        #refresh the references and get new tree if needed
        if not self._storage.locked:
            self._refresh_tree_ref()
        #get the top level node
        node = self._follow(self._tree_ref)
        #traverse until you find appropriate node
        while node is not None:
            if key < node.key:
                node = self._follow(node.left_ref)
            elif key > node.key: # this was a bug!
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value): # Have questions about this one
        "Set a new value in the tree. Will cause a new tree"
        #try to lock the tree. If we succeed make sure
        #we dont lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        #get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        #insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)


    def _insert(self, node, key, value_ref):
        "Insert a new node creating a new path from root"
        #create a tree if there was none so far
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
        else: #create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        "Delete node with key, creating new tree and path"
        if self._storage.lock(): # returns true if it was unlocked
            self._refresh_tree_ref() # pragma: no cover
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)

    def _delete(self, node, key):
        "Underlying delete implementation"
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
        "Get a node from a reference"
        #calls BinaryNodeRef.get
        return ref.get(self._storage)

    def _find_max(self, node):
        "Get the node that represents the maximum"
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node

class Storage(object):
    """
    Storage class to interact with the file on disk.
    Manages writing to file, locking/unlocking for editing, and closing the file."
    """
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT = "!Q"
    INTEGER_LENGTH = 8

    def __init__(self, f):
        "Stores f, sets state to unlocked, and ensures we start in sector boundary"
        self._f = f
        self.locked = False
        #we ensure that we start in a sector boundary
        self._ensure_superblock()

    def _ensure_superblock(self):
        "Guarantee that the next write will start on a sector boundary"
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "If not locked, lock the file for writing and return True"
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def unlock(self):
        "If locked, flush and unlock the file"
        if self.locked:
            self._f.flush()
            portalocker.unlock(self._f)
            self.locked = False

    def _seek_end(self):
        "Move pointer to the end of the file"
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "Go to beginning of file which is on sec boundary"
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        "Use struct to unpack bytes into an integer"
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        "Use struct to pack an integer into bytes"
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        "Read the next 8 bytes and return the unpacked integer"
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        "Lock the file and write integer to file"
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "Write data to disk, returning the address at which you wrote it"
        #first lock, get to end, get address to return, write size
        #write data, unlock <==WRONG, dont want to unlock here
        #your code here
        self.lock()
        self._seek_end()
        object_address = self._f.tell()
        self._write_integer(len(data))
        self._f.write(data)
        return object_address

    def read(self, address):
        "Read data from given address in file"
        self._f.seek(address) # Move pointer in file
        length = self._read_integer() # Get the next integer from the file
        data = self._f.read(length) #
        return data

    def commit_root_address(self, root_address):
        """
        Atomically commit changes by writing the new root address to beginning
        of the next superblock and unlocking the file.
        """
        self.lock() # Lock self
        self._f.flush() # finish off sector
        #make sure you write root address at position 0
        self._seek_superblock() # move pointer to next superblock
        #write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address) # write the root address to file
        self._f.flush() # finish off sector
        self.unlock() # unlock the file for writing

    def get_root_address(self):
        "Get the root address from the beginning of the file"
        #read the first integer in the file
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        "Unlock and close the file"
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        "Returns true if database is closed"
        return self._f.closed

class DBDB(object):
    """
    Database class to manage Storage and BinaryTree operations.

    Attributes:
    ----------
    _storage: Storage object to manage file writes/reads
    _tree: BinaryTree object to manage a Red Black Tree

    Example:
    --------
    >>> import os
    >>> fd = os.open("/tmp/test.dbdb", os.O_RDWR | os.O_CREAT)
    >>> f  = open(fd, 'r+b')
    >>> db = DBDB(f)
    >>> db.set("rahul", "aged")
    >>> db.set("kobe", "stillyoung")
    >>> db.get("rahul")
    'aged'
    >>> db.commit()
    >>> db.close()
    """

    def __init__(self, f):
        "Creates storage and tree properties"
        self._storage = Storage(f)
        self._tree = BinaryTree(self._storage)

    def _assert_not_closed(self):
        "Confirm the storage database is closed"
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        "Close the storage object"
        self._storage.close()

    def commit(self):
        "Confirm storage is closed and commit"
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        "Confirm storage is open and get a value for a key"
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        "Confirm storage is open and set a value for a key"
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        "Confirm storage is open and delete node with key"
        self._assert_not_closed()
        return self._tree.delete(key)