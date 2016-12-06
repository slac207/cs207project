import pickle      # for BinaryNodeRef class
import os          # for Storage class
import struct      # for Storage class
import portalocker # for Storage class


class Color(object):
    """
    Class that defines the coloring of our red-black tree, and 
    the corresponding underlying values.
    """
    RED = 0
    BLACK = 1

    
class ValueRef(object):
    """
    A ValueRef object is a reference to a string value on disk.
    """
    
    def __init__(self, referent=None, address=0):
        """
        Class constructor. 
        
        Args
        ----
          referent: value (a string) to store on disk [optional]
          address : integer indicating where to store `_referent`
                    (number of bytes from beginning of file)
        """
        self._referent = referent # value to store
        self._address  = address  # address to store at

    @property
    def address(self):
        return self._address

    def prepare_to_store(self, storage):
        # Not implemented
        pass

    @staticmethod
    def referent_to_bytes(referent):
        """
        Converts `referent` to bytes, in preparation for disk storage.
        
        Args
        ----
          referent: value (a string) to be encoded
          
        Returns
        -------
          A bytes representation of the Unicode string, 
            encoded in UTF-8.
        """
        return referent.encode('utf-8')

    @staticmethod
    def bytes_to_referent(bytes):
        """
        Converts `bytes` to a string, typically after reading `bytes` 
          from disk.
        
        Args
        ----
          referent: value (a string) to be encoded
          
        Returns
        -------
          A bytes representation of the Unicode string, 
            encoded in UTF-8.
        """
        return bytes.decode('utf-8')

    def get(self, storage):
        """
        Reads whatever bytes are at the `_address` attribute,
           converts to a string,
           saves this string as `_referent`, and and returns it.
           
        Args
        ----
          storage: a Storage object
                   (our Python representation of our data on disk)
                   
        Returns
        -------
          The string located at the `_address` attribute in `storage`.
        """
        if self._referent is None and self._address:
            self._referent = self.bytes_to_referent(storage.read(self._address))
        return self._referent

    def store(self, storage):
        """
        Converts whatever value is contained in the `_referent`
          attribute to bytes, saves it to disk within `storage`, 
          and records the storage address.`, and and returns it.
           
        Args
        ----
          storage: a Storage object
                   (our Python representation of our data on disk)
                   
        Returns
        -------
          None.
          
        Notes
        -----
        This method is called by BinaryNode.store_refs() 
        """        
        if self._referent is not None and not self._address:
            self.prepare_to_store(storage)
            self._address = storage.write(self.referent_to_bytes(self._referent))

            
class BinaryNodeRef(ValueRef):
    """
    A BinaryNodeRef object is a reference to a binary tree node on disk.
    Inherits from ValueRef.
    """
    
    def prepare_to_store(self, storage):
        """
        Stores the node contents to disk within `storage`.
           
        Args
        ----
          storage: a Storage object
                   (our Python representation of our data on disk)
                   
        Returns
        -------
          None.
          
        Notes
        -----
        This method calls BinaryNode.store_refs() 
        """
        if self._referent:
            self._referent.store_refs(storage)

    @staticmethod
    def referent_to_bytes(referent):
        """
        Serializes the tree node (i.e., pickles the tree node) 
          in preparation for disk storage.
           
        Args
        ----
          referent: node to be encoded
                   
        Returns
        -------
          A serialized tree node (e.g., a serialized BinaryNode object).
        """
        return pickle.dumps({
            'left' : referent.left_ref.address,
            'key'  : referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Deserializes the tree node (i.e., unpickles the tree node) 
          typically after disk retrieval.
           
        Args
        ----
          string: value to be reconstituted
                   
        Returns
        -------
          A reconstituted BinaryNode object.
        """        
        d = pickle.loads(string)
        return BinaryNode(
            BinaryNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            BinaryNodeRef(address=d['right']),
        )
    
    
class RedBlackNodeRef(BinaryNodeRef):
    """
    A RedBlackNodeRef object is a reference to a red-black 
      binary tree node on disk.
    Inherits from ValueRef.
    """
    
    @staticmethod
    def referent_to_bytes(referent):
        """
        Serializes the tree node (i.e., pickles the tree node) 
          in preparation for disk storage.
           
        Args
        ----
          referent: node to be encoded
                   
        Returns
        -------
          A serialized tree node (e.g., a serialized BinaryNode object).
        """
        return pickle.dumps({
            'left' : referent.left_ref.address,
            'key'  : referent.key,
            'value': referent.value_ref.address,
            'right': referent.right_ref.address,
            'color': referent.color
        })

    @staticmethod
    def bytes_to_referent(string):
        """
        Deserializes the tree node (i.e., unpickles the tree node) 
          typically after disk retrieval.
           
        Args
        ----
          string: value to be reconstituted
                   
        Returns
        -------
          A reconstituted RedBlackNode object.
        """        
        d = pickle.loads(string)
        return RedBlackNode(
            RedBlackNodeRef(address=d['left']),
            d['key'],
            ValueRef(address=d['value']),
            RedBlackNodeRef(address=d['right']),
            d['color']
        )    

    
class BinaryNode(object):
    """
    A BinaryNode object contains the data of a single node in a 
      binary tree, and stores references to the data and its two
      child nodes.
    """
    
    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Clones a node, but with updates as specified by addtional arguments.
           
        Args
        ----
          node:     tree node to be cloned
          **kwargs: tree node attributes to be updated
                   
        Returns
        -------
          An updated BinaryNode object.
        """           
        return cls(
            left_ref  = kwargs.get('left_ref', node.left_ref),
            key       = kwargs.get('key', node.key),
            value_ref = kwargs.get('value_ref', node.value_ref),
            right_ref = kwargs.get('right_ref', node.right_ref),
        )

    def __init__(self, left_ref, key, value_ref, right_ref):
        """
        Class constructor.
        A BinaryNode object consists of its data value, its address, 
          and the addresses of its two children.
           
        Args
        ----
          left_ref:  address of left child (e.g., number of bytes from  
                     start of file on disk, or ValueRef object)
          key:       string associated with the data value stored
                     in the tree.
          value_ref: address of data value stored in this node
          right_ref: address of right child                   
        """
        self.left_ref  = left_ref
        self.key       = key
        self.value_ref = value_ref
        self.right_ref = right_ref

    def store_refs(self, storage):
        """
        Method for BinaryNode object to save its contents to disk.
        Recursively stores the entire tree to disk.
           
        Args
        ----
          storage: a Storage object
                   (our Python representation of our data on disk)                  
        """        
        self.value_ref.store(storage)
        # code below: 
        #  calls BinaryNodeRef.store() which
        #  calls BinaryNodeRef.prepare_to_store() which
        #  calls BinaryNode.store_refs() on ???
        #  thus recursively stores the whole tree
        self.left_ref.store(storage)
        self.right_ref.store(storage)
        
        
class RedBlackNode(BinaryNode):
    """
    A RedBlackNode object contains the data of a single node in a 
      binary tree, and stores references to the data and its two
      child nodes.
    """
    
    @classmethod
    def from_node(cls, node, **kwargs):
        """
        Clones a node, but with updates as specified by addtional arguments.
           
        Args
        ----
          node:     tree node to be cloned
          **kwargs: tree node attributes to be updated
                   
        Returns
        -------
          An updated RedBlackNode object.
        """           
        return cls(
            left_ref  = kwargs.get('left_ref', node.left_ref),
            key       = kwargs.get('key', node.key),
            value_ref = kwargs.get('value_ref', node.value_ref),
            right_ref = kwargs.get('right_ref', node.right_ref),
            color     = kwargs.get('color', node.color),
        )

    def __init__(self, left_ref, key, value_ref, right_ref, color=Color.RED):
        """
        Class constructor.
        A BinaryNode object consists of its data value, its address, 
          and the addresses of its two children.
           
        Args
        ----
          left_ref:  address of left child (e.g., number of bytes from  
                     start of file on disk, or ValueRef object)
          key:       string associated with the data value stored
                     in the tree.
          value_ref: address of data value stored in this node
          right_ref: address of right child 
          color:     color of the node (default color is red).
        """
        self.left_ref  = left_ref
        self.key       = key
        self.value_ref = value_ref
        self.right_ref = right_ref
        self.color     = color    
        
        
class BinaryTree(object):
    """
    Immutable Binary Tree class. Constructs new tree on changes.
    """
    
    def __init__(self, storage):
        """
        Class constructor.
        The disk storage is set as a property of a BinaryTree object,
          then all tree node references are refreshed.
           
        Args
        ----
          storage: a Storage object
                   (our Python representation of our data on disk)                   
        """        
        self._storage = storage
        self._refresh_tree_ref()

    def commit(self):
        """
        Commits tree changes to disk (within `_storage`).
        Changes are final only when committed.                 
        """                
        # triggers BinaryNodeRef.store()
        self._tree_ref.store(self._storage)
        # make sure address of new tree is stored()
        self._storage.commit_root_address(self._tree_ref.address)

    def _refresh_tree_ref(self):
        """
        Gets reference to new tree if it has changed.
        """
        self._tree_ref = BinaryNodeRef(
            address=self._storage.get_root_address())

    def get(self, key):
        """
        Retrieves the value associated with the specified key.
        
        Args
        ----
        key: indexes the value that we want to retrieve
        
        Returns
        -------
        The string value associated with `key`.
        """
        # your code here
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
            elif key > node.key: # this was a bug!
                node = self._follow(node.right_ref)
            else:
                return self._follow(node.value_ref)
        raise KeyError

    def set(self, key, value): # Have questions about this one
        """
        Sets a new value in the tree, causing a new tree to be created
        (b/c of immutability).
        
        Args
        ----
        key:   indexes the value that we want to store
        value: the data we want to store, under `key`
        """
        # try to lock the tree. If we succeed make sure
        # we don't lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)


    def _insert(self, node, key, value_ref):
        """
        Insert a new node creating a new path from tree root.
        
        Args
        ----
        node:      BinaryNode object (or None if our key/value has
                   not been packaged as such)
        key:       indexes the value that we want to store
        value_ref: address of data value stored in this node
                   (number of bytes from start of file on disk)
        
        Returns
        -------
        A BinaryNodeRef object that points to the new node.
        """
        # create a tree if there was none so far
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
        else: # create a new node to represent this data
            new_node = BinaryNode.from_node(node, value_ref=value_ref)
        return BinaryNodeRef(referent=new_node)

    def delete(self, key):
        """
        Deletes node with specified key, creating a new tree and 
        reconstructed paths for any nodes directly associated with 
        the deleted node.
        
        Args
        ----
        key:       indexes the value that we want to delete        
        """
        if self._storage.lock(): # returns true if it was unlocked
            self._refresh_tree_ref() # pragma: no cover
        node = self._follow(self._tree_ref)
        self._tree_ref = self._delete(node, key)

    def _delete(self, node, key):
        """
        Underlying implementation of node deletion
        (called by delete() method).
        
        Args
        ----
        node:      BinaryNode object (or None if our key/value has
                   not been packaged as such)
        key:       indexes the value that we want to store      
        """
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
        """
        Get a node value from a reference.
        
        Args
        ----
        ref: the address where the desired value is located.
        
        Returns
        -------
        The string located at at the specified address.
        """
        # calls BinaryNodeRef.get()
        return ref.get(self._storage)

    def _find_max(self, node):
        """
        Gives the node that represents the right-most maximum, relative to
        the given node. If the given node is a terminal node, then
        we return it. 
        
        Args
        ----
        node: the node that we want to find the relative maximum against
        
        Returns
        -------
        The BinaryNode object that is the maximum, relative to `node`.
        """
        while True:
            next_node = self._follow(node.right_ref)
            if next_node is None:
                return node
            node = next_node      
            
            
class RedBlackTree(BinaryTree):
    """
    Red Black Binary Tree class. 
    Inherits from BinaryTree class, so is immutable as well 
      (i.e., constructs new tree on changes).
    """

    def _refresh_tree_ref(self):
        """
        Gets reference to new tree if it has changed.
        """
        self._tree_ref = RedBlackNodeRef(
            address=self._storage.get_root_address())        

    def set(self, key, value): # Have questions about this one
        """
        Sets a new value in the tree, causing a new tree to be created
        (b/c of immutability).
        
        Args
        ----
        key:   indexes the value that we want to store
        value: the data we want to store, under `key`
        """
        # try to lock the tree. If we succeed make sure
        # we don't lose updates from any other process
        if self._storage.lock():
            self._refresh_tree_ref()
        # get current top-level node and make a value-ref
        node = self._follow(self._tree_ref)
        value_ref = ValueRef(value)
        # insert and get new tree ref
        self._tree_ref = self._insert(node, key, value_ref)
        # add coloring
        self._tree_ref = self._blacken(self._follow(self._tree_ref))

    def _blacken(self, node):
        """
        Changes a node's color to black.
        
        Args
        ----
        node:      RedBlackNode-like object (or None if our key/value has
                   not been packaged as such)
        
        Returns
        -------
        A RedBlackNodeRef object that points to the new node.
        """ 
        if node is None:
            return RedBlackNodeRef(node)
            
        return RedBlackNodeRef(
                     RedBlackNode.from_node(node, color=Color.BLACK)   
               )
        
    def rotate_left(self, node): 
        """
        Rotates the specified node "to the left", in order to ensure compliance
          with red-black tree invariants (see module README), in particular 
          "No red node has a red parent." This method is used when `node` has
          a red parent. 
        
        A "left rotation" is when we switch the positions of `node` and
          its right child (call it RC) -- so `node` becomes the left child of RC.
          
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        
        Returns
        -------
        A RedBlackNodeRef object that points to the new node.
        """
        
        # get the right child
        rightChild = self._follow(node.right_ref)
        
        # if there's a value in the left grandchild...
        if self._follow(rightChild.left_ref) is not None:
            # copy the grandchild
            newNode = RedBlackNode.from_node(self._follow(rightChild.left_ref),
                                             left_ref  = RedBlackNodeRef(),
                                             right_ref = RedBlackNodeRef(),
                                             color     = node.color)
            newNodeRef = RedBlackNodeRef(referent = newNode)
        else: 
            # otherwise just make an empty node
            newNodeRef = RedBlackNodeRef()
        
        # create a new node, whose right child the node we just created
        newChild = RedBlackNode.from_node(node, 
                                          right_ref = newNodeRef)
        
        # create another node, who left child is the node we just created
        rotatedChild = RedBlackNode.from_node(rightChild,
                                              left_ref = RedBlackNodeRef(referent=newChild))
        
        return rotatedChild
        
    def rotate_right(self, node):
        """
        Rotates the specified node "to the right", in order to ensure compliance
          with red-black tree invariants (see module README), in particular 
          "No red node has a red parent." This method is used when `node` has
          a red parent. 
        
        A "right rotation" is when we switch the positions of `node` and
          its left child (call it LC) -- so `node` becomes the right child of LC.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        
        Returns
        -------
        A RedBlackNodeRef object that points to the new node.
        """
        
        # get the right child
        leftChild = self._follow(node.left_ref)
        
        # if there's a value in the right grandchild...
        if self._follow(leftChild.right_ref) is not None:
            # copy the grandchild
            newNode = RedBlackNode.from_node(self._follow(leftChild.right_ref),
                                             left_ref  = RedBlackNodeRef(),
                                             right_ref = RedBlackNodeRef(),
                                             color     = node.color)
            newNodeRef = RedBlackNodeRef(referent = newNode)
        else: 
            # otherwise just make an empty node
            newNodeRef = RedBlackNodeRef()
        
        # create a new node, whose right child the node we just created
        newChild = RedBlackNode.from_node(node, 
                                          left_ref = newNodeRef)
        
        # create another node, who left child is the node we just created
        rotatedChild = RedBlackNode.from_node(leftChild,
                                              right_ref = RedBlackNodeRef(referent=newChild))
        
        return rotatedChild        
        
    def recolor(self, node):
        """
        Sets `node` color to red and the color of its children to black.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        
        Returns
        -------
        The new recolored node.
        
        """
        leftChild  = self._blacken(self._follow(node.left_ref))
        rightChild = self._blacken(self._follow(node.right_ref))        
        
        return RedBlackNode.from_node(node,
                                      left_ref  = leftChild,
                                      right_ref = rightChild,
                                      color     = Color.RED)
    
    def balance(self, node): 
        """
        Add a new node to the tree, then balance.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        
        Returns
        -------
        The node that was passed to the function.   
        """
        # if new node is already red, we're done.
        if self._isRed(node) | (node is None):
            return node
        
        leftChild  = self._follow(node.left_ref)
        rightChild = self._follow(node.right_ref)
        
        if self._isRed(leftChild): 
            # if the left and right children are red, 
            # make `node` red and its children black (i.e., recolor)
            if self._isRed(rightChild): 
                return self.recolor(node)
            # if this particular grandchild is red,
            #   rotate then recolor
            if self._isRed(self._follow(leftChild.left_ref)):
                return self.recolor(self.rotate_right(node))
            # if this particular grandchild is red,
            #   rotate then recolor
            if self._isRed(self._follow(leftChild.right_ref)):
                new_leftChild = self.rotate_left(leftChild)
                newNode = RedBlackNode.from_node(node,
                                                 left_ref = RedBlackNodeRef(referent = new_leftChild))
                return self.recolor(self.rotate_right(newNode))
        
        # the process we did above for the left child, we repeat for the right
        if self._isRed(rightChild):
            if self._isRed(self._follow(rightChild.right_ref)):
                return self.recolor(self.rotate_left(node))
            if self._isRed(self._follow(rightChild.left_ref)):
                new_rightChild = self.rotate_right(rightChild)
                newNode = RedBlackNode.from_node(node,
                                                 right_ref = RedBlackNodeRef(referent = new_rightChild))
                return self.recolor(self.rotate_left(newNode))
        
        return node 
    
    def rootKey(self):
        """
        Returns the key stored in the root.
        """
        return self._follow(self._tree_ref).key
    
    def _insert(self, node, key, value_ref):
        """
        Insert a new node creating a new path from tree root.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        key:       indexes the value that we want to store
        value_ref: address of data value stored in this node
                   (number of bytes from start of file on disk)
        
        Returns
        -------
        A RedBlackNodeRef object that points to the new node.
        """
        # create a tree if there was none so far
        if node is None:
            new_node = RedBlackNode(
                RedBlackNodeRef(), key, value_ref, RedBlackNodeRef())
        elif key < node.key:
            newLeft_ref = self._insert(self._follow(node.left_ref), 
                                       key,
                                       value_ref)
            newLeft     = self.balance(self._follow(newLeft_ref))
            new_node    = self.balance(RedBlackNode.from_node(node,
                            left_ref = RedBlackNodeRef(referent=newLeft)))
        elif key > node.key:
            newRight_ref = self._insert(self._follow(node.right_ref), 
                                        key, 
                                        value_ref)
            newRight     = self.balance(self._follow(newRight_ref))
            new_node     = self.balance(RedBlackNode.from_node(node,
                            right_ref = RedBlackNodeRef(referent=newRight)))
        else: # create a new node to represent this data
            new_node = RedBlackNode.from_node(node, value_ref=value_ref)
        return RedBlackNodeRef(referent=new_node)   
        
    def _isRed(self, node):
        """
        Checks whether the specified node is red.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        """
        if node is None:
            return False
        else:
            return node.color == Color.RED  
            
    def _isBlack(self, node):
        """
        Checks whether the specified node is black.
        
        Args
        ----
        node:      RedBlackNode object (or None if our key/value has
                   not been packaged as such)
        """
        if node is None:
            return False
        else:
            return node.color == Color.BLACK          

            
class Storage(object):
    """
    Storage class to interact with the file on disk.
    Manages writing to file, locking/unlocking for editing, and closing the file."
    """
    
    SUPERBLOCK_SIZE = 4096
    INTEGER_FORMAT  = "!Q"
    INTEGER_LENGTH  = 8

    def __init__(self, f):
        """
        `f` is an open file object (e.g., returned by built-in method open())
        The constructor stores `f`, sets the object state to unlocked, and
          ensures we start storage within the sector boundary.
        """
        self._f = f
        self.locked = False
        self._ensure_superblock()

    def _ensure_superblock(self):
        "Guarantees that the next write will start on a sector boundary."
        self.lock()
        self._seek_end()
        end_address = self._f.tell()
        if end_address < self.SUPERBLOCK_SIZE:
            self._f.write(b'\x00' * (self.SUPERBLOCK_SIZE - end_address))
        self.unlock()

    def lock(self):
        "If not locked, lock the file for writing and return True."
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
        "Move pointer to the end of the file."
        self._f.seek(0, os.SEEK_END)

    def _seek_superblock(self):
        "Go to beginning of file which is on the sector boundary."
        self._f.seek(0)

    def _bytes_to_integer(self, integer_bytes):
        "Use struct to unpack bytes into an integer."
        return struct.unpack(self.INTEGER_FORMAT, integer_bytes)[0]

    def _integer_to_bytes(self, integer):
        "Use struct to pack an integer into bytes."
        return struct.pack(self.INTEGER_FORMAT, integer)

    def _read_integer(self):
        "Read the next 8 bytes and return the unpacked integer."
        return self._bytes_to_integer(self._f.read(self.INTEGER_LENGTH))

    def _write_integer(self, integer):
        "Lock the file and write integer to file."
        self.lock()
        self._f.write(self._integer_to_bytes(integer))

    def write(self, data):
        "Write data to disk, returning the address at which you wrote it."
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
        "Read data from given address in file."
        self._f.seek(address)         # Move pointer in file
        length = self._read_integer() # Get the next integer from the file
        data = self._f.read(length) 
        return data

    def commit_root_address(self, root_address):
        """
        Atomically commit changes by writing the new root address to beginning
        of the next superblock and unlocking the file.
        """
        self.lock()     # lock self
        self._f.flush() # finish off sector
        
        # make sure you write root address at position 0
        self._seek_superblock() # move pointer to next superblock
        # write is atomic because we store the address on a sector boundary.
        self._write_integer(root_address) # write the root address to file
        self._f.flush() # finish off sector
        self.unlock()   # unlock the file for writing

    def get_root_address(self):
        "Get the root address, as measured from the beginning of the file."
        #read the first integer in the file
        #your code here
        self._seek_superblock()
        root_address = self._read_integer()
        return root_address

    def close(self):
        "Unlock and close the file."
        self.unlock()
        self._f.close()

    @property
    def closed(self):
        "Returns true if database is closed."
        return self._f.closed

    
class DBDB(object):
    """
    Database class to manage Storage and RedBlackTree operations.

    Attributes:
    ----------
    _storage: Storage object to manage file writes/reads
    _tree: RedBlackTree object to manage a Red Black Tree

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
        self._tree = RedBlackTree(self._storage)

    def _assert_not_closed(self):
        "Confirm the storage database is closed."
        if self._storage.closed:
            raise ValueError('Database closed.')

    def close(self):
        "Close the storage object."
        self._storage.close()

    def commit(self):
        "Confirm storage is closed and commit."
        self._assert_not_closed()
        self._tree.commit()

    def get(self, key):
        "Confirm storage is open and get a value for a key."
        self._assert_not_closed()
        return self._tree.get(key)

    def set(self, key, value):
        "Confirm storage is open and set a value for a key."
        self._assert_not_closed()
        return self._tree.set(key, value)

    def delete(self, key):
        "Confirm storage is open and delete node with key."
        self._assert_not_closed()
        return self._tree.delete(key)
    
    def rootKey(self):
        return self._tree.rootKey()