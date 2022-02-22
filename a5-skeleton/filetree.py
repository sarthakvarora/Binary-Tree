import os
import sys
from stat import *
from mystat import *
from mylist import *
from random import randrange
# os.chdir("/Users/sarthak/Downloads/a4-skeleton/")

def find_fid(obj, path, fobj):
    if obj.objid == fobj.objid:
        fobj.path = path
        raise Exception("SarthakException")

def count_files(obj, path, dobj):
    if obj.dir != 1:
    #     dobj.directories += 1
    # else:
        dobj.files += 1
    return dobj.files

def count_dirs(obj, path, dobj):
    if obj.dir == 1:
        dobj.directories += 1
    # else:
    #     dobj.files += 1
    return dobj.directories

# cmp function for list lookups
# cmp node objects 
def node_obj_cmp(node, obj):
    if node.nobj == obj:
        return True
    else:
        return False

# compare object names

def node_objname_cmp(node, name):
    if node.nobjname == name:
        return True
    else:
        return False

def node_objid_cmp(node, id):
    if node.nobjid == id:
        return True
    else:
        return False

# file objects 
# mandatory to have these members.
# name - file name (not the full path)
# objid - file object is this is the inode no. in the stat
# stat - stat object of the file returned by os.stat api.
# dir 0 (default) implies it is not directory but a regular file.
# dir 1 implies it is a directory.

class myfile():

    # look above for argument descriptions.
    # raise exception if dir is 1 and not a dir
    # raise exception if dir is 0 and not a regular file.
    # DO NOT CHANGE THIS. 
    # you can add additional members if required.

    def __init__(self, objid, name=None, stat=None, dir=0):

        # leave the following in there.
        if name and '/' in name:
            raise Exception("Bad name in file")
        if dir and stat and not S_ISDIR(stat.st_mode):
            s=f'{name} is not a directory'
            raise Exception(s)
        if not dir and stat and not S_ISREG(stat.st_mode):
            s=f'{name} is not a file'
            raise Exception(s)
        self.name = name
        self.objid = objid
        self.stat=stat
        self.dir=dir
        #YOUR CODE
        self.path = None
        #raise NotImplementedError

    
    # return the file path from root of the tree to which it belongs.
    # eg., I will create a file object with
    # fobj=myfile(241573) ie. only with objectid.
    # print(fobj.path(tree))
    # where this file is part of the tree. 
    # Note: not this instance of the object but the same objectid.
    # it should print the file path.
    # the objectid is found by "ls -i1" in any of the subdirectory
    # of the kernel-0 folder sent to you.  you can do that even on windows with powershell i believe.
    # this function should print the full path of that objectid starting
    # from the kernel-0 folder.
    # eg., if the file kernel-0/mm/f1.c and its objectid is 241573
    # then fobj.file_path(tree) should print kernel-0/mm/f1.c
    # Note: this has to be recalculated from the tree when this function
    # is called. Tree was the object obtained from convert_to_tree function
    # at the end of this file.

    def file_path(self, tree):
        #YOUR CODE
        try:
            tree.func_traverse(find_fid, self)
        except Exception as SarthakException:
            return self.path
        
        #raise NotImplementedError

    # return the file size
    # required for the binary tree organization of these file objects.
    # for assignment 6.

    def file_size(self):
        #YOUR CODE
        return self.stat.st_size
        #raise NotImplementedError

    # this is just a helper. feel free to modify the way you want it to help you.

    def __str__(self):
        return self.name

# directory objects inherit from file, uses all of what file has plus some more interfaces.

class mydir(myfile):

    # DO NOT CHANGE THIS.
    # you can add any members below this.

    def __init__(self, objid, name=None, stat=None, ):
        super().__init__(objid, name, stat, 1)
        #YOUR CODE
        self.directories = 0
        self.files = 0
        #raise NotImplementedError

    # find the total no. of files underneath this directory including the directories (as they are also files) as well. 
    # eg., if you have a folder : kernel-0/mm/f1.c and kernel-0/mm/f2.c
    # dir_total_files of the directory kernel-0 will print : 3. two regular
    # files and one directory file "mm".
    # use case will be :
    # dir = mydir(245173)
    # dir.dir_total_files(tree) where this directory is part of the tree.  
    # Note: not this instance of the object but the same objectid.
    # Note this has to be "calculated" every time the function is called from the passed tree. 


    def dir_total_files(self, tree):
        #YOUR CODE
        path = self.file_path(tree)
        nodename = path.split("/")[-1].strip()
        pobj = tree.root
        node = tree.lookup(pobj, nodename)
        tree.func_node_traverse(node, path, count_files, self)
        return self.files
        #raise NotImplementedError
        
    # the below function is similar as above but should print  only the total
    # no. of directories underneath this directory.
    # Note this has to be "calculated" every time the function is called
    # from the passed tree. 

    def dir_total_dirs(self, tree):
        #YOUR CODE
        path = self.file_path(tree)
        nodename = path.split("/")[-1].strip()
        pobj = tree.root
        node = tree.lookup(pobj, nodename)
        tree.func_node_traverse(node, path, count_dirs, self)
        return self.directories
        #raise NotImplementedError
        
    def __str__(self):
        return self.name

class mynode():

    # pobj - parent object
    # obj - this object
    # objname - name of this object
    # objid - unique id of this object. for file and dir it is inode numbes.
    # Do not change this.

    def __init__(self, pobj, obj, objname, objid):
        self.child_list=mylist("list")
        self.nobj = obj
        self.nobjname = objname
        self.nobjid = objid
        self.npobj = pobj

class mytree():

# init functionf or root object and name and its object id.
# (object id for these objects are all inode numbers).
# Do not change this.

    def __init__(self, obj, root_name, id):
        self.root=mynode(None, obj, root_name, id)
        self.total_nodes=1

# the following two functions are helper functions for 
# constructing the tree, insertions etc..

# Lookup objname from a parent node, if found return node object. 
# If it does not  exist, create a node for that objname,
# objid combinations, ensure to add it to the appropriate child
# list.

    def lookup_create(self, pobj:mynode, objname, objid, obj):
        #YOUR CODE
        assert(pobj != None)
        if self.lookup(pobj, objname) != None:
            return self.lookup(pobj, objname)
        else:
            node = mynode(pobj, obj, objname, objid)
            pobj.child_list.add(node)
            self.total_nodes += 1
        return node
        #raise NotImplementedError

# Lookup objname from a parent node, if found return
# node object. If not, return None.

    def lookup(self, pobj:mynode, objname):
        #YOUR CODE
        for node in pobj.child_list:    
            assert(node != None)
            if node.nobj.name == objname:
                return node
        return None
        #raise NotImplementedError

# Method on the tree object to traverse and it will call the function func with the passed arguments (variable argument args), for 
# every line of the object it will generate as output corresponding 
# to the input file in function convert_input_to_tree().
#
# for the eg. mentioned in the comments of that function
# the function func() will get called for each of the
# lines given there. And that string will be passed as first argument to the
# function.

# func_traverse(tree, test_func, argobj) returned by convert_input_to_tree() will call 
# test_func(fobj, "kernel-0", argobj) where fobj is the mydir obj for kernel-0.
# test_func(fobj, "kernel-0/arch", argobj) where fobj is the mydir obj for kernel-0/arch.
# test_func(fobj, "kernel-0/arch/boot", argobj) where fobj is the mydir obj for kernel-0/arch/boot.
# test_func(fobj, "kernel-0/arch/boot/bootloader.lds", argobj) where fobj is the  myfile obj 
# for kernel-0/arch/boot/bootloader.lds.

# you can test this function by putting the string in some file or std output
# and then compare the entire output with the original input file (sort both to
# avoid any ordering issues).

    def func_traverse(self, func, *args):
        #YOUR CODE
        # for child in self.root:
        #     self.func_traverse(func, *args)
        self.func_node_traverse(self.root, "", func, *args)
        return
        #raise NotImplementedError

# exactly same as above function except that the traversal starts
# from an intermediary mynode() object ie., an interior node.

    def func_node_traverse(self, node, prefix, func, *args):
        #YOUR CODE
        if prefix == "":
            path = node.nobjname
        else:
            path = prefix + "/" + node.nobjname
        func(node.nobj, path, *args)
        for i in node.child_list:
            self.func_node_traverse(i, path, func, *args)
        return
        # raise NotImplementedError

# some debug stuff may be useful.

    def dump1(self, root):
        print(root.nobj)
        print(f'{root.nobj} Child: ', end="")
        for i in root.child_list:
            print(f'{i.nobj}, ', end="")
        print('\n')
        for i in root.child_list:
            self.dump1(i)

    def dump2(self, root, obj):
        for i in root.child_list:
            if i.obj == obj:
                return i
            else:
                self.dump2(i.obj,obj)

# some debug stuff may be useful.

    def dump(self):
        print(f'Total Nodes: {self.total_nodes}')
        self.dump1(self.root)

# NEWWWW

# Function takes an input file name 
# and converts that into an object instance of 
# the tree class as defined above.
# you can only use the operations given above to construct the tree.
# no other functions should be added.
# input file will be of the form:

#kernel-0
#kernel-0/arch
#kernel-0/arch/alpha
#kernel-0/arch/alpha/boot
#kernel-0/arch/alpha/boot/bootloader.lds

# the above should be converted to tree with root object being the directory object - kernel-0, 
# and there are arch, alpha and boot as directory objects below and bootloader.lds as a file object below.
# construct the appropriate hierarchy. The mynode.obj should be either a mydir or myfile object as defined above.

# returns "tree" object.

# hint use readlines, strip, and split if required and os.stat

def convert_input_to_tree(filename):
    #YOUR CODE
    f = open(filename, "r")
    lines = f.readlines()
    
    # Creating the tree with root
    root = lines[0].strip()
    stat = mystat(root)
    obj = mydir(stat.st_ino, root, stat)
    tree = mytree(obj, root, stat.st_ino)
    
    # Code for other nodes
    for line in lines[1:]:
        item = line.split("/")
        for i in range(len(item)):
            name = item[i].strip()
            if i == 0:
                path = name
                pobj = tree.root
                continue
            if i > 0:
                path = path + "/" + item[i]
                # print('path for stat', path)
                stat = mystat(path.strip())
                # print("stat", S_ISREG(stat.st_mode))
                if S_ISREG(stat.st_mode):
                    obj = myfile(stat.st_ino, name, stat)
                else:
                    obj = mydir(stat.st_ino, name, stat)
                pobj = tree.lookup_create(pobj, name, stat.st_ino, obj)
    return tree

# filename = 'kernel-01.txt'
# tree = convert_input_to_tree(filename)
# print(tree.dump1(tree.root))