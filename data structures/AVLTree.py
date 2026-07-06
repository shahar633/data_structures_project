# id1: 209410356
# name1: Tal Shaubi
# username1: talshaubi
# id2: 213670573
# name2: Shahar Cohen
# username2: shahrcohen8


"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int
    @param key: key of your node
    @type value: string
    @param value: data of your node
    """

    def __init__(self, key, value, is_real=True):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.is_real = is_real

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.is_real
    
    def __str__(self):
        if not self.is_real_node():
            return "Virtual Node"
        return f"({self.key}, {self.value})"

    def __repr__(self):
        return self.__str__()


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    @type is_avl: boolean
    @param is_avl: If True then tree is AVL, otherwise it is just a "regular" binary search tree, without rotations.
    """
    VIRTUAL_NODE = AVLNode(None, None, False)

    def __init__(self, is_avl):
        self.root = self.VIRTUAL_NODE
        self.is_avl = is_avl
        self._size = 0

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
        while cur.is_real_node():
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

    def rebalance(self, node):
        bf = node.left.height - node.right.height
        if bf == -2:
            right_child_bf = node.right.left.height - node.right.right.height
            if right_child_bf == 1:
                self.right_rotation(node.right)
                self.left_rotation(node)
                return 2
            else:
                self.left_rotation(node)
                return 1
        
        if bf == 2:
            left_child_bf = node.left.left.height - node.left.right.height
            if left_child_bf == -1:
                self.left_rotation(node.left)
                self.right_rotation(node)
                return 2
            else:
                self.right_rotation(node)
                return 1
        return 0



    def insert(self, key, val):
        if self.root is self.VIRTUAL_NODE:
            self.root = AVLNode(key, val)
            self.root.left = self.VIRTUAL_NODE
            self.root.right = self.VIRTUAL_NODE
            self.root.parent = self.VIRTUAL_NODE
            self.root.height = 0
            self._size += 1
            return self.root, 1, 0, 0
        tmp = self.root
        search_time = 0       
        while tmp.is_real_node():
            if key < tmp.key:
                if not tmp.left.is_real_node():
                    tmp.left = AVLNode(key, val)
                    tmp.left.parent = tmp
                    tmp = tmp.left
                    break
                else:
                    tmp = tmp.left
                    search_time += 1
            else:
                if not tmp.right.is_real_node():
                    tmp.right = AVLNode(key, val)
                    tmp.right.parent = tmp
                    tmp = tmp.right
                    break
                else:
                    tmp = tmp.right
                    search_time += 1
        tmp.left = self.VIRTUAL_NODE
        tmp.right = self.VIRTUAL_NODE
        tmp.height = 0
        self._size += 1
        if self.is_avl:
            fix_from = tmp.parent
            rotations = 0
            height_changes = 0
            while fix_from.is_real_node():
                real_height = 1 + max(fix_from.left.height, fix_from.right.height)
                if fix_from.height == real_height:
                    break
                bf = abs(fix_from.left.height - fix_from.right.height)
                if bf < 2:
                    fix_from.height = real_height
                    height_changes += 1
                else:
                    rotations += self.rebalance(fix_from)
                    #fix_from.height = 1 + max(fix_from.left.height, fix_from.right.height)
                    #if fix_from.parent.is_real_node():
                    #    fix_from.parent.height = 1 + max(fix_from.parent.left.height, fix_from.parent.right.height)
                    break
                fix_from = fix_from.parent

            return tmp, search_time + 2, rotations, height_changes

        else:
            return tmp, search_time + 2, 0, 0

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

    #our code
    def delete(self, node):
        fix_from = self.VIRTUAL_NODE
        if not node.is_real_node():
            return
        self._size -= 1
        
        if not node.right.is_real_node() and not node.left.is_real_node(): # If the node doesn't have any children
            if node.parent.is_real_node():
                if node == node.parent.left:
                    node.parent.left = self.VIRTUAL_NODE
                    fix_from = node.parent
                else:
                    node.parent.right = self.VIRTUAL_NODE
                    fix_from = node.parent
            else:
                self.root = self.VIRTUAL_NODE

        elif node.right.is_real_node() and node.left.is_real_node(): # If the node have both children
            succ = self.successor(node)

            if succ.parent.left == succ:
                succ.parent.left = succ.right
            else:
                succ.parent.right = succ.right
            
            if succ.right.is_real_node():
                succ.right.parent = succ.parent
            
            fix_from = succ.parent

            if fix_from == node:
                fix_from = succ
            
            succ.left = node.left
            if succ.left.is_real_node():
                succ.left.parent = succ
            
            succ.right = node.right
            if succ.right.is_real_node():
                succ.right.parent = succ
            
            succ.parent = node.parent
            if node.parent.is_real_node():
                if node == node.parent.left:
                    node.parent.left = succ
                else:
                    node.parent.right = succ
            else:
                self.root = succ
            
            succ.height = node.height


        else: # If the node has exactly 1 child (left or right)
            if node.right.is_real_node():
                tmp = node.right
            else:
                tmp = node.left
            
            fix_from = node.parent
            tmp.parent = node.parent
            if node.parent.is_real_node():
                if node == node.parent.left:
                    node.parent.left = tmp
                else:
                    node.parent.right = tmp
            else:
                self.root = tmp

        if self.is_avl:
            if fix_from is self.VIRTUAL_NODE:
                return
            

            while fix_from.is_real_node():
                real_height = 1 + max(fix_from.right.height, fix_from.left.height)
                BF = abs(fix_from.left.height - fix_from.right.height)
                if BF < 2 and fix_from.height == real_height:
                    break
                elif BF < 2 and fix_from.height != real_height:
                    fix_from.height = real_height
                    fix_from = fix_from.parent
                    continue
                else:
                    self.rebalance(fix_from)
                    fix_from.height = 1 + max(fix_from.right.height, fix_from.left.height)
                    fix_from = fix_from.parent
                    continue
                    
                

        """while fix_from.height != real_height:
            fix_from.height = real_height
            if abs(fix_from.left.height - fix_from.right.height) > 1:
                self.rebalance(fix_from)
            if fix_from.parent == self.VIRTUAL_NODE:
                break

            fix_from = fix_from.parent
            real_height = 1 + max(fix_from.right.height, fix_from.left.height)
            """


        return
    #ai
    def delete_avl(self, node):
        if not node.is_real_node():
            return

        self._size -= 1

        if not node.left.is_real_node() and not node.right.is_real_node():
            fix_from = self._detach_leaf(node)
        elif node.left.is_real_node() and node.right.is_real_node():
            fix_from = self._delete_two_children(node)
        else:
            fix_from = self._delete_single_child(node)

        if fix_from is not None:
            self._fix_delete_path(fix_from)
    #ai
    def _detach_leaf(self, node):
        parent = node.parent
        if parent.is_real_node():
            if node == parent.left:
                parent.left = self.VIRTUAL_NODE
            else:
                parent.right = self.VIRTUAL_NODE
            return parent

        self.root = self.VIRTUAL_NODE
        return None
    #ai
    def _delete_single_child(self, node):
        child = node.left if node.left.is_real_node() else node.right
        parent = node.parent
        child.parent = parent

        if parent.is_real_node():
            if node == parent.left:
                parent.left = child
            else:
                parent.right = child
            return parent

        self.root = child
        return child
    #ai
    def _delete_two_children(self, node):
        successor = self.successor(node)
        fix_from = successor.parent

        if successor.parent.left == successor:
            successor.parent.left = successor.right
        else:
            successor.parent.right = successor.right

        if successor.right.is_real_node():
            successor.right.parent = successor.parent

        if fix_from == node:
            fix_from = successor

        successor.left = node.left
        if successor.left.is_real_node():
            successor.left.parent = successor

        successor.right = node.right
        if successor.right.is_real_node():
            successor.right.parent = successor

        successor.parent = node.parent
        if node.parent.is_real_node():
            if node == node.parent.left:
                node.parent.left = successor
            else:
                node.parent.right = successor
        else:
            self.root = successor

        successor.height = node.height
        return fix_from
    #ai
    def _fix_delete_path(self, node):
        cur = node
        while cur is not None and cur.is_real_node():
            old_height = cur.height
            left_height = cur.left.height
            right_height = cur.right.height
            new_height = 1 + max(left_height, right_height)
            balance = left_height - right_height

            if balance > 1:
                if cur.left.left.height < cur.left.right.height:
                    self._rotate_left_delete(cur.left)
                cur = self._rotate_right_delete(cur)
            elif balance < -1:
                if cur.right.right.height < cur.right.left.height:
                    self._rotate_right_delete(cur.right)
                cur = self._rotate_left_delete(cur)
            else:
                cur.height = new_height

            if cur.parent is not None and cur.parent.is_real_node():
                cur = cur.parent
            else:
                if self.root.is_real_node():
                    self.root.height = 1 + max(self.root.left.height, self.root.right.height)
                break

            if balance == 0 and old_height == new_height:
                break
    #ai
    def _rotate_left_delete(self, pivot):
        child = pivot.right
        pivot.right = child.left
        if pivot.right.is_real_node():
            pivot.right.parent = pivot

        child.left = pivot
        child.parent = pivot.parent
        if child.parent.is_real_node():
            if child.parent.left == pivot:
                child.parent.left = child
            else:
                child.parent.right = child
        else:
            self.root = child

        pivot.parent = child
        pivot.height = 1 + max(pivot.left.height, pivot.right.height)
        child.height = 1 + max(child.left.height, child.right.height)
        return child
    #ai
    def _rotate_right_delete(self, pivot):
        child = pivot.left
        pivot.left = child.right
        if pivot.left.is_real_node():
            pivot.left.parent = pivot

        child.right = pivot
        child.parent = pivot.parent
        if child.parent.is_real_node():
            if child.parent.left == pivot:
                child.parent.left = child
            else:
                child.parent.right = child
        else:
            self.root = child

        pivot.parent = child
        pivot.height = 1 + max(pivot.left.height, pivot.right.height)
        child.height = 1 + max(child.left.height, child.right.height)
        return child

    """returns a list representing dictionary 

    @rtype: list
    @returns: a list of (key, value) tuples sorted by key, representing the data structure
    """

    def avl_to_list(self):
        res = []
        self.avl_to_list_rec(self.root, res)
        return res

    def avl_to_list_rec(self, node, res):
        if not node.is_real_node():
            return
        
        self.avl_to_list_rec(node.left, res)
        res.append((node.key, node.value))
        self.avl_to_list_rec(node.right, res)

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self._size
    
    def size_rec(self, node):
        if node == self.VIRTUAL_NODE:
            return 0
        return 1 + self.size_rec(node.left) + self.size_rec(node.right)

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        if self.root.is_real_node():
            return self.root
        return None

    """returns the height of the tree

        @rtype: int
        @returns: the height of the tree 
        """

    def get_height(self):
        if self.is_avl:
            return self.root.height
        
        return self.get_height_rec(self.root)
        

    def get_height_rec(self, node):
        if node == self.VIRTUAL_NODE:
            return -1
        return 1 + max(self.get_height_rec(node.left), self.get_height_rec(node.right))


    #@pre need B.left.is_real_node() == True for right rotation 
    def right_rotation(self, B):
        A = B.left
        B.left = A.right
        if B.left.is_real_node():
            B.left.parent = B
        A.right = B
        A.parent = B.parent
        if A.parent.is_real_node():
            if A.parent.left == B:
                A.parent.left = A
            else:
                A.parent.right = A
        else:
            self.root = A
        B.parent = A
        B.height = 1 + max(B.left.height, B.right.height)
        A.height = 1 + max(A.left.height, A.right.height)

    #@pre need B.right.is_real_node() == True for left rotation
    def left_rotation(self, B):
        A = B.right
        B.right = A.left
        if B.right.is_real_node():
            B.right.parent = B
        A.left = B
        A.parent = B.parent
        if A.parent.is_real_node():
            if A.parent.left == B:
                A.parent.left = A
            else:
                A.parent.right = A
        else:
            self.root = A
        B.parent = A
        B.height = 1 + max(B.left.height, B.right.height)
        A.height = 1 + max(A.left.height, A.right.height)