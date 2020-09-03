# CLRS Red-Black-Tree Algorithm in Python

<a href="sample.png"> <img src="sample.png"></a>

A python implementation of the Red-black-tree algorithm by Cormen, Leiserson, Rivest, and Stein [CLRS]

I find the description by [CLRS] the most accurate, concise, and easiest to understand.
The only two changes I made are the extra checks for NIL parameter in the beginning of LEFT_ and RIGHT_ROTATE().

# Usage
See Chap. 13 & 14 [CLRS]

* **Create a Tree** ```python t = rbtree.RedBlackTree()```

* **Create a Node** ```python n = rbtree.RedBlackNode(0.0)```

* **Insert a node to a tree** ```python t.RB_INSERT(n)```

* **Remove a node from a tree** ```python t.RB_DELETE(n)```

* **Root node** n = ```python rbtree.ROOT()```

* **Minimum node** n = ```python rbtree.TREE_MINIMUM()```

* **Maximum node** n = ```python rbtree.TREE_MAXIMUM()```

* **Iterate ascending**

```python
n = t.TREE_MINIMUM(t.ROOT())
while not n is t.NIL():
    n = t.TREE_SUCCESSOR(n)
```

* **Iterate ascending**

```python
n = t.TREE_MAXIMUM(t.ROOT())
while not n is t.NIL():
    n = t.TREE_PREDECESSOR(n)
```

* **draw tree** ```python t.draw('filename_wo_ext', True, 'pdf', 'vertical' )```

See [unit_tests_rbtree.py](unit_tests_rbtree.py) for sample usage.


# References

* [CLRS] Introduction to Algorithms 3rd Ed. Cormen, Thomas H. and Leiserson, Charles E. and Rivest, Ronald L. and Stein, Clifford, The MIT Press, 2001

