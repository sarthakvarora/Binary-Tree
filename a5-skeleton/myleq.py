
# returns the count of the binary tree nodes less than or equal to val.
# you can write your own sub-functions any for recursion or whatever. 
# the following are the variables and functions that you can access
# from the tree object.
# the tree object you will have access to tree.root variable.
# variables for access tree.root
# tree.root --> root node (mybnode object)
# each tree node is of class mybnode(). The only function you have to access
# in this is mynode.first() -> that will return the "object in the node". 
# mynode.first() --> returns the "first object in the node" 
#eg.
# node.obj_list.size -- >this will return the no. of objects in this node that
# has the same value. which means a binary tree node has multiple different objects if 
# they all have the same value. any counts should include this appropriately.
# valcmp--> function passed and should be called like "valcmp(val, obj)"
# this function returns 0 if the val is equal to value of the object
# returns <0 if the val is less than object value
# returns >0 if the val is greater than object value

# Other tree functions that you can use for this problem is given below:
# the left and right mybnode objects  are accessible via :

# the following are tree object functions (not of mybnode objects): 
# tree.myleft(node) -- returns left node
# tree.myright(node) -- returns right node
# tree.myleaf(node)-- returns True if node is a leaf node.
# Note: if node is None, does not MEAN it is a leaf node. So, dont 
# use this to special case anything. Use  tree.myleaf(node) to check
# for leaf node.
# No other functions should be used. 

# tree.count() counts the no of nodes in subtree

# no need to import any thing except to use the above functions.

def recursion(tree, node, val, valcmp):
    #YOUR CODE
    count = 0
    if node == None:
        return 0
        
    # if the value = node, counts that element and the full tree to the left 
    if valcmp(val, node.first()) == 0:
        count += tree.mycount(tree.myleft(node))
        count += node.obj_list.size
        return count

    # if the value > node, counts that element and the full tree to the left, and checks for elements in the right tree via recursion
    elif valcmp(val, node.first()) > 0:
        count += tree.mycount(tree.myleft(node))
        count += node.obj_list.size
        return count + recursion(tree, tree.myright(node), val, valcmp)

    # if the value < node, checks for elements in the left tree via recursion
    else:
        return count + recursion(tree, tree.myleft(node), val, valcmp)
    


def mycount_leq(tree, val, valcmp):
    #YOUR CODE
    node = tree.root
    return recursion(tree, node, val, valcmp)
    raise NotImplementedError
