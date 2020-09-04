#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Red-Black tree implementation based on Introduction to Algorithms 3rd Ed., Chap 12 & 13
# by Cormen, Leiserson, Rivest, and Stein.
# Inline comments are minimum as the book gives the best explanation of each function.

from graphviz import Digraph
from functools import total_ordering

@total_ordering
class RedBlackNode(object):

    def __init__( self, comparable ):

        self.left        = self
        self.right       = self
        self.p           = self
        self._rbtype     = 1 # -1: NIL 0: Black 1 : Red
        self._comparable = comparable


    def __eq__( self, other ):

        return self._comparable == other._comparable


    def __ne__( self, other ):

        return not (self == other)


    def __lt__( self, other ):
        return self._comparable < other._comparable


    def __repr__(self):

        if self.is_nil():
            return f"[N]: {self._comparable}"

        if self.is_black():
            return f"[B]: {self._comparable}"

        else:
            return f"[R]: {self._comparable}"


    def is_RED(self):
        return self._rbtype == 1


    def is_BLACK(self):
        # NIL or Black
        return self._rbtype < 1


    def is_nil(self):
        return self._rbtype == -1


    def set_nil(self):
        self._rbtype = -1


    def set_BLACK(self):
        if self._rbtype != -1:
            self._rbtype = 0


    def set_RED(self):
        if self._rbtype != -1:
            self._rbtype = 1


    def color(self):
        return self._rbtype


    def set_color( self, rbtype ):
        self._rbtype = rbtype


    def __iter__(self):

        if not self.left.is_nil():

            yield from self.left.__iter__()

        yield self._comparable

        if not self.right.is_nil():

            yield from self.right.__iter__()

    def draw( self, dot, node_id ):

        if self.is_nil():

            dot.node( str(node_id),label='', 
                      shape='box', style='filled', color='black', height='0.1', width='0.1', fixedsize='true')

        elif self.is_RED(): 

            dot.node( str(node_id), label='%.2f' % self._comparable, 
                      shape='circle', style='filled', color='pink', height='0.5', width='0.5', fixedsize='true')

        else:
            dot.node( str(node_id), label='%.2f' % self._comparable, 
                      shape='circle', style='filled', color='grey', height='0.5', width='0.5', fixedsize='true')


class RedBlackTree(object):

    def __init__(self):

        self._T_nil  = RedBlackNode( 0 )
        self._T_nil.set_nil()
        self._T_root = self._T_nil
        self._size   = 0

    # Public Functions. See Cormen, Leiserson, Rivest, and Stein for descriptions
    # 
    # NIL()
    # ROOT()
    # RB_INSERT( z )
    # RB_DELETE( z )
    # TREE_MAXIMUM( x )
    # TREE_MINIMUM( x )
    # TREE_SUCCESSOR( x )
    # TREE_PREDECESSOR( x )
    #
    # draw( tree_name, view_now = True/False, out_format ="svg/pdf", orientation ="vertical/horizontal" ):


    def _LEFT_ROTATE( self, x ):

        #  xP            xP
        #  ||            ||
        #   x            y
        #  / \\         // \
        #xL   y    =>   x yRR
        #   // \       / \\
        #  yRL yRR   xL yRL
        #
        # three links above marked by double line
        # are altered.

        # This check is not in the book but needed to avoid
        # self._T_root = y below.
        if x is self._T_nil:
            # y is already the root.
            return

        y = x.right

        x.right = y.left

        if not y.left is self._T_nil:

            y.left.p = x

        y.p = x.p

        if x.p is self._T_nil:

            self._T_root = y

        elif x is x.p.left:

            x.p.left = y

        else:
            x.p.right = y

        y.left = x

        x.p = y


    def _RIGHT_ROTATE( self, x ):

        #    xP            xP
        #    ||            ||
        #     x             y
        #   // \           / \\
        #   y   xR   =>  yLL  x
        #  / \\             // \
        #yLL yLR           yLR xR
        #
        # three links above marked by double line
        # are altered.

        # This check is not in the book but needed to avoid
        # self._T_root = y below.
        if x is self._T_nil:
            # y is already the root.
            return

        y = x.left

        x.left = y.right

        if not y.right is self._T_nil:

            y.right.p = x

        y.p = x.p

        if x.p is self._T_nil:

            self._T_root = y

        elif x is x.p.right:

            x.p.right = y

        else:
            x.p.left = y

        y.right = x

        x.p = y


    def RB_INSERT(self, z):

        y = self._T_nil

        x = self._T_root

        while not x is self._T_nil:

            y = x

            if z < x:
                x = x.left

            else:
                x = x.right

        z.p = y

        if y is self._T_nil:

            self._T_root = z

        elif z < y:
            y.left = z

        else:
            y.right = z       

        z.left  = self._T_nil

        z.right = self._T_nil

        z.set_RED()

        self._RB_INSERT_FIXUP(z)

        self._size += 1


    def _RB_INSERT_FIXUP( self, z ):

        while z.p.is_RED():

            if z.p is z.p.p.left:

                y = z.p.p.right

                if y.is_RED():

                    z.p.set_BLACK()

                    y.set_BLACK()

                    z.p.p.set_RED()

                    z = z.p.p

                else:
                    # z.p.p == BLACK, z.p.p.right = NIL, or z.p = root
                    if z is z.p.right:

                        z = z.p

                        self._LEFT_ROTATE( z )

                    z.p.set_BLACK()

                    z.p.p.set_RED()

                    self._RIGHT_ROTATE( z.p.p )

            else: # z.p is z.p.p.right:

                y = z.p.p.left

                if y.is_RED():

                    z.p.set_BLACK()

                    y.set_BLACK()

                    z.p.p.set_RED()

                    z = z.p.p

                else:
                    # z.p.p == BLACK, z.p.p.left = NIL, or z.p = root
                    if z is z.p.left:

                        z = z.p

                        self._RIGHT_ROTATE( z )

                    z.p.set_BLACK()

                    z.p.p.set_RED()

                    self._LEFT_ROTATE( z.p.p )

        self._T_root.set_BLACK()


    def _RB_TRANSPLANT( self, u, v ):

        if u.p is self._T_nil:

            self._T_root = v

        elif u is u.p.left:

            u.p.left = v

        else:
            u.p.right = v

        v.p = u.p


    def _is_BLACK( self, color ):
        # NIL or Black
        return color < 1


    def TREE_MAXIMUM( self, x ):

        while not x.right is self._T_nil:

            x = x.right

        return x


    def TREE_MINIMUM( self, x ):

        while not x.left is self._T_nil:
            x = x.left

        return x


    def ROOT(self):
        return self._T_root


    def NIL(self):
        return self._T_nil


    def size(self):
        return self._size


    def TREE_SUCCESSOR( self, x ):

        if not x.right is self._T_nil:

            return self.TREE_MINIMUM(x.right)

        y = x.p
        while ( not y is self._T_nil ) and ( x is y.right ):
            x = y
            y = y.p

        return y


    def TREE_PREDECESSOR( self, x ):

        if not x.left is self._T_nil:

            return self.TREE_MAXIMUM(x.left)

        y = x.p
        while ( not y is self._T_nil ) and ( x is y.left ):
            x = y
            y = y.p

        return y


    def RB_DELETE( self, z ):

        self._size -= 1

        y = z
        y_original_color = y.color()

        if z.left is self._T_nil:

            x = z.right

            self._RB_TRANSPLANT( z, z.right )
       
        elif z.right is self._T_nil:

            x = z.left

            self._RB_TRANSPLANT( z, z.left )

        else:

            y = self.TREE_MINIMUM( z.right )

            y_original_color = y.color()

            x = y.right

            if y.p is z:

                x.p = y

            else:

                self._RB_TRANSPLANT( y, y.right )

                y.right = z.right

                y.right.p = y


            self._RB_TRANSPLANT( z, y )

            y.left = z.left

            y.left.p = y

            y.set_color( z.color() )

        if self._is_BLACK(y_original_color):

            self._RB_DELETE_FIXUP( x )


    def _RB_DELETE_FIXUP( self, x ):

        while ( not x is self._T_root ) and x.is_BLACK():

            if x is x.p.left:

                w = x.p.right

                if w.is_RED():

                    w.set_BLACK()

                    x.p.set_RED()

                    self._LEFT_ROTATE( x.p )

                    w = x.p.right

                if w.left.is_BLACK() and w.right.is_BLACK():

                    w.set_RED()

                    x = x.p

                else:
                    if w.right.is_BLACK():

                        w.left.set_BLACK()

                        w.set_RED()

                        self._RIGHT_ROTATE( w )

                        w = x.p.right

                    w.set_color( x.p.color() )

                    x.p.set_BLACK()

                    w.right.set_BLACK()

                    self._LEFT_ROTATE( x.p )

                    x = self._T_root

            else: # x is x.p.right:

                w = x.p.left

                if w.is_RED():

                    w.set_BLACK()

                    x.p.set_RED()

                    self._RIGHT_ROTATE( x.p )

                    w = x.p.left

                if w.left.is_BLACK() and w.right.is_BLACK():

                    w.set_RED()

                    x = x.p

                else:
                    if w.left.is_BLACK():

                        w.right.set_BLACK()

                        w.set_RED()

                        self._LEFT_ROTATE( w )

                        w = x.p.left

                    w.set_color( x.p.color() )

                    x.p.set_BLACK()

                    w.left.set_BLACK()

                    self._RIGHT_ROTATE( x.p )

                    x = self._T_root

        x.set_BLACK()


    def __iter__( self ):

        if self.NIL() is self.ROOT():
            return []

        yield from self._T_root.__iter__()
            

    def draw( self, tree_name, view_now = True, out_format ="svg", orientation ="vertical" ):

        g_dot = Digraph( comment = tree_name )

        if orientation == 'horizontal':
            g_dot.graph_attr['rankdir'] = 'LR'

        self._node_id = 0

        if not self._T_root is self._T_nil:        

            node_id = self._node_id
            self._node_id += 1
            self._T_nil.draw( g_dot, node_id )

            self._visit_and_draw( self._T_root, g_dot , node_id )

        g_dot.render(tree_name.strip('<>'), view=view_now, format=out_format)


    def _visit_and_draw( self, n, dot , parent_id ):

        node_id = self._node_id
        self._node_id += 1
        n.draw( dot, node_id )

        if parent_id != -1:
            dot.edge( str(parent_id), str(node_id) )

        if not n is self._T_nil:

            n._node_id = node_id
        
            node_id_left  = self._visit_and_draw( n.left ,  dot, n._node_id )
            node_id_right = self._visit_and_draw( n.right , dot, n._node_id )

            # Add horizontal edges to force ordering among children.

            dot.edge( str(node_id_left), str(node_id_right) ,style='invis' )

            with dot.subgraph() as s:

                s.attr(rank = 'same')
                s.node(str(node_id_left))
                s.node(str(node_id_right))

        return node_id





