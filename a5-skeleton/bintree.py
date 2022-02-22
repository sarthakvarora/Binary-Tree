import os
import sys
import math
from stat import *
from mylist import *
from random import randrange
from filetree import *
# os.chdir("/Users/sarthak/Downloads/a4-skeleton/")

# different comparison functions for the 
# file objects.
# object equality of myfile objects is based on objectid
# which is the inode number

def myfile_cmp(obj1, obj2):
    if obj1.objid == obj2.objid:
        return True
    return False

# size based comparison between two myfile objects

def myfile_size_cmp(obj1, obj2):
    if obj1.file_size() == obj2.file_size():
        return 0
    if obj1.file_size() < obj2.file_size():
        return -1
    if obj1.file_size() > obj2.file_size():
        return 1

# size comparison but val is "int" and obj is myfile object.

def myfile_val_cmp(val, obj):
    if val == obj.file_size():
        return 0
    if val < obj.file_size():
        return -1
    if val > obj.file_size():
        return 1

# return a list of sorted objects only by using the public functions of 
# the binary tree.
# the methods given below. No internal members are seen by this.
# use any of the methods defined in the tree as given below. No new methods
# can be added for this.

def sorted_bintree(tree):
    #YOUR CODE
    list = []
    tree.traverse(list_files, list)
    return list
    raise NotImplementedError

def list_files(obj_list, *args):
    tlist=args[0]
    for i in obj_list:
        tlist.append(i)

# binary node
# with left and right child

class mybnode(mynode):
    # pnode - parent node
    # obj - this object
    # left and right and obj add the way you want
    # Do not change this.
    # you can add more members if you want

    def __init__(self, pnode, obj):
        self.left = None
        self.right = None
        self.pnode = pnode
        #YOUR CODE
        self.obj_list = mylist("list")
        if obj != None:
            self.obj_list.add(obj)
        return
        raise NotImplementedError

#mybintree class. 

# it stores objects of myfile. but it can be general.
# objcmp, objvalcmp, and valcmp are the functions
# for checking. see the comparison functions above.
# objcmp -- for comparing two object ids returns true if
# they are equal.
# objvalcmp(obj1, obj2) -- for comparing value of two objects 
# returns 0, -1 or 1. 0 if equal, -1 if obj1 < obj2, and 1 if obj1 > obj2. 
# valcmp(val, obj)--. compares val (in this case it represents 
# the size ) with object value.

class mybintree():

# init functionf or root object and name and its object id.
# (object id for these objects are all inode numbers).
# Do not change this.

    def __init__(self, obj):
        self.root = mybnode(None, obj)
        self.total_nodes=1
        #YOUR CODE
        return
        raise NotImplementedError

# insert object into the binary tree. objcmp and objvalcmp corresponds to the
# definitions listed above.
# if the same object is trying to get inserted twice, raise exception
# ensure all the objects from the file list kernel-0.files are inserted here appropriately.

    def recurse_insert(self, obj, objcmp, objvalcmp, pnode):

        # Root is equal to the object
        if objvalcmp(obj, pnode.obj_list.first()) == 0:
            for nobj in pnode.obj_list:
                if objcmp(obj, nobj) == True:
                    raise Exception("Same object inserted twice.")
            pnode.obj_list.add(obj)
    
        # Object is bigger than root. obj > pnode
        elif objvalcmp(obj, pnode.obj_list.first()) > 0:
            if pnode.right == None:
                node = mybnode(pnode, obj)
                pnode.right = node
                self.total_nodes += 1
            else:
                pnode = pnode.right
                self.recurse_insert(obj, objcmp, objvalcmp, pnode)

        # Object is smaller than root. obj < pnode
        elif objvalcmp(obj, pnode.obj_list.first()) < 0:
            if pnode.left == None:
                node = mybnode(pnode, obj)
                pnode.left = node
                self.total_nodes += 1
            else:
                pnode = pnode.left
                self.recurse_insert(obj, objcmp, objvalcmp, pnode)
        return

    def insert(self, obj, objcmp, objvalcmp):
        #YOUR CODE
        pnode = self.root
        if self.root.obj_list.size == 0:
            self.root.obj_list.add(obj)
        else:
            self.recurse_insert(obj, objcmp, objvalcmp, pnode)
        return
        # raise NotImplementedError

# traverse the binary tree func is the passed function has to be invoked with
# the object and the variable args *args passed here.

    def traverse(self, func, *args):
        #YOUR CODE
        self.travers_from_node(self.root, func, *args)
        # raise NotImplementedError

    # def travers_from_node(self, node, prefix, func, *args):
    def travers_from_node(self, node, func, *args):
        #YOUR CODE
        # if node != None:
        if node == None:
            return 
        self.travers_from_node(node.left, func, *args)
        func(node.obj_list, *args)
        self.travers_from_node(node.right, func, *args)
        
        # raise NotImplementedError

# returns the height of the binary tree

    def height(self):
        #YOUR CODE
        pnode = self.root
        return max(self.myheight(pnode.left), self.myheight(pnode.right))
        # raise NotImplementedError

    def myheight(self, node):
        #YOUR CODE
        if node == None:
            return 0
        return 1 + max(self.myheight(node.left), self.myheight(node.right))
        # raise NotImplementedError

# returns the count of the binary tree nodes.

    def count(self):
        #YOUR CODE
        pnode = self.root
        return self.mycount(pnode)
        raise NotImplementedError

    def mycount(self, node):
        #YOUR CODE
        if node == None:
            return 0
        return node.obj_list.size + self.mycount(node.left) + self.mycount(node.right)
        raise NotImplementedError

    def recursion_leq(self, node, val, valcmp):
        #YOUR CODE
        count = 0
        if node == None:
            return 0
        # if the value = node, counts that element and the full tree to the left 
        if valcmp(val, node.obj_list.first()) == 0:
            count += self.mycount(node.left)
            count += node.obj_list.size
            return count
        # if the value > node, counts that element and the full tree to the left, and checks for elements in the right tree via recursion
        elif valcmp(val, node.obj_list.first()) > 0:
            count += self.mycount(node.left)
            count += node.obj_list.size
            return count + self.recursion_leq(node.right, val, valcmp)
        # if the value < node, checks for elements in the left tree via recursion
        else:
            return count + self.recursion_leq(node.left, val, valcmp)

    def recursion_geq(self, node, val, valcmp):
        #YOUR CODE
        count = 0
        if node == None:
            return 0
        # if the value = node, counts that element and the full tree to the right 
        if valcmp(val, node.obj_list.first()) == 0:
            count += self.mycount(node.right)
            count += node.obj_list.size
            return count
        # if the value < node, counts that element and the full tree to the right, and checks for elements in the left tree via recursion
        elif valcmp(val, node.obj_list.first()) < 0:
            count += self.mycount(node.right)
            count += node.obj_list.size
            return count + self.recursion_geq(node.left, val, valcmp)
        # if the value > node, checks for elements in the right tree via recursion
        else:
            return count + self.recursion_geq(node.right, val, valcmp)

    def recursion_eq(self, node, val, valcmp):
        #YOUR CODE
        count = 0
        if node == None:
            return 0
        # if the value = node, counts that element
        if valcmp(val, node.obj_list.first()) == 0:
            count += node.obj_list.size
            return count
        # if the value > node, looks for node in the right tree via recursion
        elif valcmp(val, node.obj_list.first()) > 0:
            return self.recursion_eq(node.right, val, valcmp)
        # if the value < node, looks for node in the left tree via recursion
        else:
            return self.recursion_eq(node.left, val, valcmp)

# returns the count of the binary tree nodes less than or equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.

    def count_leq(self, val, valcmp):
        #YOUR CODE
        node = self.root
        return self.recursion_leq(node, val, valcmp)
        raise NotImplementedError

# returns the count of the binary tree nodes greater than or equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.

    def count_geq(self, val, valcmp):
        #YOUR CODE
        node = self.root
        return self.recursion_geq(node, val, valcmp)
        raise NotImplementedError

# returns the count of the binary tree nodes equal to val.
# Note: This cannot use the traverse function has to calculate from the
# current tree by going through it. cannot use any other public functions.

    def count_eq(self, val, valcmp):
        #YOUR CODE
        node = self.root
        return self.recursion_eq(node, val, valcmp)
        raise NotImplementedError



# bst = mybintree(6)
# bst.insert_basic(4)
# bst.insert_basic(2)
# bst.insert_basic(8)
# bst.insert_basic(10)

# filename = 'kernel-01.txt'
# tree = convert_input_to_tree(filename)
# tree2 = sorted_bintree(tree)