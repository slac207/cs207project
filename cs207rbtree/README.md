# Immutable Read-Black Tree Implementation

## Purpose
According to [Scott Lobdell](http://scottlobdell.me/2016/02/purely-functional-red-black-trees-python/), 
> a red-black tree is a variant of a standard binary tree that will re-balamce the tree every time [we] insert or delete a node. 

Here we have implemented a red-black tree (although it does not support node deletion).  It obeys the following invariants:
1. No red node has a red parent.
2. Every path from the root to an empty node contains the same number of black nodes.
3. All terminal leaf nodes are black.
4. The root node is black. 
5. Empty nodes are black.

When a new node is added to the tree, it is colored red. This triggers an invariant violation, causing the tree to rebalance to get back into compliance. These invariants ensure that operations on this tree (i.e., value retrieval and insertion) take no more than O(log n) time [[1]](https://dl.dropboxusercontent.com/u/75194/okasakiredblack99.pdf).

Our code is an amalgamation of the [immutable binary search tree implementation](https://github.com/iacs-cs207/cs207-2016/blob/master/labs/lab10.ipynb) from Lab 10 of CS207 @ Harvard SEAS and the Functional [Red-Black Tree implementation](http://scottlobdell.me/2016/02/purely-functional-red-black-trees-python/) by Scott Lobdell. 

## Installation
Before running any files, `python setup.py install` must be run from the top level directory, cs207project. 

## Contents
The directory `RedBlackTree` contains the module files.
  - `RedBlackTree.py` contains our red-black tree implementation, which defined the following classes:
     - `Color`
     - `ValueRef`
     - `RedBlackNodeRef` 
     - `RedBlackNode` 
     - `RedBlackTree` 
     - `Storage`
     - `DBDB`

`setup.py` is to construct the module from our Python scripts. 

`demo_RedBlackTree.ipynb` demonstrates the functionality of our module.

## Usage
```
db = RedBlackTree.connect("/tmp/test1.dbdb")
db.set(0.5, "courtney")
db.set(2, "sarah")
db.set(4, "andrew")
db.set(3, "laura")
db.commit()
db.close() #set up database, commit and close

newdb = RedBlackTree.connect("/tmp/test1.dbdb")
newdb.get(4) #query on our database
newdb.get_nodes_less_than(3) #find nodes with key less than given value
newdb.close()

```

## Testing
There is one testing file for the code in this module and it is contained in the [test folder](https://github.com/slac207/cs207project/tree/master/tests). These files can be run using `python setup.py test`. 

1. test_RedBlackTree.py: tests for correct behavior of inserting and querying our database. Also checks to make sure the portalocking behavior works. 


