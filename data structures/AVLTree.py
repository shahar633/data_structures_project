# id1:
# name1:
# username1:
# id2:
# name2:
# username2:


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return False


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """

    def __init__(self, is_avl):
        self.root = None

    """searches for a node in the dictionary corresponding to the key (starting at the root)

    @type key: int
    @param key: a key to be searched
    @rtype: (AVLNode,int)
    @returns: a tuple (x, search_time) where x is the node corresponding to key (or None if not found)
    and search_time is the search time, as defined and explained in the assignment.
    """

    def search(self, key):
        cur = self.root
        search_time = 0
        while cur != None:
            if key == cur.key:
                return cur, search_time + 1
            
            elif key > cur.key:
                search_time += 1
                cur = cur.right
            
            else:
                search_time += 1
                cur = cur.left
        
        return None, search_time + 1

    """inserts a new node into the dictionary with corresponding key and value (starting at the root)

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: string
    @param val: the value of the item
    @rtype: (AVLNode,int,int,int)
    @returns: a 4-tuple (x, search_time, rotations, height_changes), where x is the new node
    and the other 3 return values are as defined and explained in the assignment.
    """

    def insert(self, key, val):
        if self.root is None:
            self.root = AVLNode(key, val)
            return self.root, 0, 0, 0            
        tmp = self.root       
        while tmp is not None:
            if key < tmp.key:
                if tmp.left is None:
                    tmp.left = AVLNode(key, val)
                    tmp.left.parent = tmp
                    tmp = tmp.left
                else:
                    tmp = tmp.left
            else:
                if tmp.right is None:
                    tmp.right = AVLNode(key, val)
                    tmp.right.parent = tmp
                    tmp = tmp.right
                else:
                    tmp = tmp.right
        if self.is_avl:
            pass
        else:
            return tmp, -1, -1, -1
        return None, -1, -1, -1

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    """

    def successor(self, x):
        if x.right.is_real_node():
            cur = x.right

            while cur.left.is_real_node():
                cur = cur.left
            
            return cur
        
        cur = x

        while cur.parent.is_real_node() and cur == cur.parent.right:
            cur = cur.parent
        
        return cur.parent


    def delete(self, node):
        return

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        return None

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return -1

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        return None

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        return -1
