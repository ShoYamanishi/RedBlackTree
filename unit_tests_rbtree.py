#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Unit Tests for rbtree """

import unittest
import random
import rbtree

class test_rbtree( unittest.TestCase ):


    def test_empty(self):

        t01 = rbtree.RedBlackTree()
        n_nil = t01._T_nil
        self.assertEqual( n_nil.p,           n_nil )
        self.assertEqual( n_nil.left,        n_nil )
        self.assertEqual( n_nil.right,       n_nil )
        self.assertEqual( n_nil._rbtype,     -1    )
        self.assertEqual( n_nil._comparable, 0     )

        self.assertEqual( t01._T_root,       n_nil )
        self.assertEqual( t01.size(),        0     )
#        t01.draw('test_empty', True, 'pdf', 'vertical' )


    def test_one_node(self):

        t01 = rbtree.RedBlackTree()
        n01 = rbtree.RedBlackNode(0)
        t01.RB_INSERT(n01)

        self.assertEqual( t01._T_root,       n01   )
        self.assertEqual( n01.p,             t01._T_nil )
        self.assertEqual( n01.left,          t01._T_nil )
        self.assertEqual( n01.right,         t01._T_nil )

        self.assertEqual( t01.size(),        1     )

#        t01.draw('test_one_node', True, 'pdf', 'vertical' )

        t01.RB_DELETE(n01)

        self.assertEqual( t01._T_root,       t01._T_nil )
        self.assertEqual( t01.size(),        0     )

        self.assertEqual( n01.p,             t01._T_nil )
        self.assertEqual( n01.left,          t01._T_nil )
        self.assertEqual( n01.right,         t01._T_nil )
        self.assertEqual( t01.size(),        0     )

#        t01.draw('test_empty_again', True, 'pdf', 'vertical' )

    def test_insertions_and_then_deletions(self):

        NUM_INSERTS = 100000
        NUM_DELETES =  99950

        t01 = rbtree.RedBlackTree()
        num_list = []
        num_set = set()
        node_list = []
        for i in range(0, NUM_INSERTS):
            while True:
                num = random.uniform(-100, 100)
                if num not in num_set:
                    num_set.add(num)
                    break;
            node = rbtree.RedBlackNode(num)
            t01.RB_INSERT(node)
            node_list.append(node)
            num_list.append(num)           


        num_list_from_min = []
        n_cur = t01.TREE_MINIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_min.append(n_cur._comparable)
            n_cur = t01.TREE_SUCCESSOR(n_cur)

        num_list_from_max = []
        n_cur = t01.TREE_MAXIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_max.append(n_cur._comparable)
            n_cur = t01.TREE_PREDECESSOR(n_cur)

        for i, n in enumerate(sorted(num_list)):
            self.assertEqual(n, num_list_from_min[i])

        for i, n in enumerate(sorted(num_list, reverse=True)):
            self.assertEqual(n, num_list_from_max[i])

        self.assertEqual( t01.size(), NUM_INSERTS )

        random.shuffle(node_list)

        for i in range(0, NUM_DELETES):
            n_remove = node_list[i]        
            t01.RB_DELETE(n_remove)

        node_list_2 = node_list[NUM_DELETES:]
        num_list_2 = [n._comparable for n in node_list_2]

        num_list_from_min_2 = []
        n_cur = t01.TREE_MINIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_min_2.append(n_cur._comparable)
            n_cur = t01.TREE_SUCCESSOR(n_cur)

        num_list_from_max_2 = []
        n_cur = t01.TREE_MAXIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_max_2.append(n_cur._comparable)
            n_cur = t01.TREE_PREDECESSOR(n_cur)

        for i, n in enumerate(sorted(num_list_2)):
            self.assertEqual(n, num_list_from_min_2[i])

        for i, n in enumerate(sorted(num_list_2, reverse=True)):
            self.assertEqual(n, num_list_from_max_2[i])

        self.assertEqual( t01.size(), NUM_INSERTS - NUM_DELETES )

        t01.draw('test_100000_insertions_and_then_99900_deletions', True, 'pdf', 'vertical' )


    def test_random(self):

        NUM_OPERATIONS = 10000
        RATIO_INSERTS_OVER_DELETES = 0.5

        t01 = rbtree.RedBlackTree()
        node_list = []
        num_set = set()

        for i in range(0, NUM_OPERATIONS):

            r_ops = random.uniform(0.0, 1.0)

            if r_ops <= RATIO_INSERTS_OVER_DELETES:
          
                while True:
                    num = random.uniform(-100, 100)
                    if num not in num_set:
                        num_set.add(num)
                        break;
                node = rbtree.RedBlackNode(num)
                t01.RB_INSERT(node)
                node_list.append(node)

            else:
                if len(node_list) > 0:
                    r_index = random.randint(0, len(node_list)-1)
                    n = node_list[r_index]
                    node_list.remove(n)
                    num_set.remove(n._comparable)
                    t01.RB_DELETE(n)

        num_list_from_min = []
        n_cur = t01.TREE_MINIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_min.append(n_cur._comparable)
            n_cur = t01.TREE_SUCCESSOR(n_cur)

        num_list_from_max = []
        n_cur = t01.TREE_MAXIMUM(t01.ROOT())
        while not n_cur is t01.NIL():
            num_list_from_max.append(n_cur._comparable)
            n_cur = t01.TREE_PREDECESSOR(n_cur)

        num_list = list(num_set)
        for i, n in enumerate(sorted(num_list)):
            self.assertEqual(n, num_list_from_min[i])

        for i, n in enumerate(sorted(num_list, reverse=True)):
            self.assertEqual(n, num_list_from_max[i])

        self.assertEqual( t01.size(), len(num_list) )

        t01.draw('test_random_10000_operations', True, 'pdf', 'vertical' )

