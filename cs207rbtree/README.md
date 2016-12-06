# Immutable Read-Black Tree Implementation

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


## Contents
The directory `RedBlackTree` contains the module files.
  - `RedBlackTree.py` contains our red-black tree implementation, which defined the following classes:
     - `Color`
     - `ValueRef`
     - `BinaryNodeRef` (inherits from `ValueRef`)
     - `RedBlackNodeRef` (inherits from `BinaryNodeRef`)
     - `BinaryNode`
     - `RedBlackNode` (inherits from `BinaryNode`)
     - `BinaryTree`
     - `RedBlackTree` (inherits from `BinaryTree`)
     - `Storage`
     - `DBDB`
  - `test_RedBlackTree.py` contains unit tests for our tree implementation.

`setup.py` is to construct the module from our Python scripts. 

`demo_RedBlackTree.ipynb` demonstrates the functionality of our module.