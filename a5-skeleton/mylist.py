import os
import sys

# as discussed in the class and subsequent discussions 
# have an ADT for this and you can use this to create (Abstract data type)
# whatever you want.
# you are welcome to implement this in a way you want and use it.
# I am giving you a template where a single linked list
# can be used for multiple objects .. 
# to share code as much as possible in a single ADT.
# l1 = mylist(list) --> behaves like a list
# l2 = mylist(stack) --> supports stack and other operations(like push, pop
# etc.)  are disallowed.
# l3 = mylist(queue) --> same here. (like enqueue, dequeue etc.)

# you are welcome to use your own ADT whatever way.

class myelem():            

    def __init__(self, obj):
        self.next=self
        self.prev=self
        self.obj=obj

class mylist():
    list_type=['stack', 'list', 'queue']

    # init function do not change this.

    def __init__(self, type):
        self.header=myelem(self)
        self.size=0
        if type not in self.list_type:
            raise Exception("List type incorrect")
        self.type=type
        self.tail=self.header

    # cmp function is sent some time for users of
    # the lookup to return the right object. See usage
    # below. See same_
    # see comment in mycrm.py above server_same and vm_same.. functions.
    # the cmp method is used if it is not None to check for object
    # equality. 
    # for each element in list:
    #        if (cmp(val, element) is true:
    # return object

    def lookup(self, val, cmp=None):
        #YOUR CODE
        current = self.header.next
        if (self.header == None):
            return
        while (current != self.header):
            if cmp != None:
                if cmp(current.obj, val) == True:
                    return current.obj
            if (current.obj == val):    
                    return current.obj
            current = current.next
        return
        raise NotImplementedError
    
    # returns true if list is not empty
    # if it is empty, returns False.

    def not_empty(self):
        #YOUR CODE
        if self.size>0:
            return True
        else:
            return False
        raise NotImplementedError

    #  returns first element

    def first(self):
        #YOUR CODE
        return self.header.next
        raise NotImplementedError

    # returns last element

    def last(self):
        #YOUR CODE
        return self.tail
        raise NotImplementedError

    # adds the element to 
    def add(self, obj):
        if self.type != 'list':
            raise Exception("Add op supported only for list")
        #YOUR CODE
        node = myelem(obj)
        if self.not_empty() == False:
            self.header.next = node
            node.prev = self.header
            self.tail = node
            self.header.prev = node
            node.next = self.header
        else:
            old_next = self.header.next

            self.header.next = node
            node.prev = self.header

            old_next.prev = node
            node.next = old_next
        self.size = self.size + 1
        return
        raise NotImplementedError

        # If it is Queue - Enqueue Dequeue (remove from header add to tail)
        # If it is Stack - Push Pop (remove from tail add to tail)
        # If it is List - Add Delete (add to header; delete is applicable for all)

    def push(self, obj):
        if self.type != 'stack':
            raise Exception("push op supported only for stack")
        #YOUR CODE
        node = myelem(obj)
        if self.not_empty() == False:
            self.header.next = node
            node.prev = self.header
            self.tail = node
            self.header.prev = node
            node.next = self.header
        else:
            old_next = self.header.next
            self.header.next = node
            node.prev = self.header
            old_next.prev = node
            node.next = old_next
        self.size = self.size + 1
        return
        raise NotImplementedError
    
    def pop(self):
        if self.type != 'stack':
            raise Exception("pop op supported only for stack")
        #YOUR CODE
        if self.not_empty() == False:
            # raise Exception("Popping from an empty stack")
            return None
        if self.size == 1:
            self.tail = self.header
        remove = self.header.next
        self.header.next = self.header.next.next
        remove.next.prev = self.header
        self.size = self.size - 1
        return remove.obj
        raise NotImplementedError

# Gets top item of stack

    def peek(self):
        if self.type != 'stack':
            raise Exception("peek op supported only for stack")
        #YOUR CODE
        if self.not_empty() == False:
            # raise Exception("Peeking from an empty stack")
            return None
        return self.header.next.obj
        raise NotImplementedError

    def enqueue(self, obj):             # or do I copy code for add, cos same type of addition
        if self.type != 'queue':
            raise Exception("Enqueue op supported only for queue")
        #YOUR CODE
        node = myelem(obj)
        if self.not_empty() == False:
            self.header.next = node
            node.prev = self.header
            self.tail = node
            self.header.prev = node
            node.next = self.header
        else:
            node.prev = self.tail
            self.tail.next = node
            node.next = self.header
            self.header.prev = node
            self.tail = node
        self.size = self.size + 1
        return
        raise NotImplementedError

    def dequeue(self):
        if self.type != 'queue':
            raise Exception("Dequeue op supported only for queue")
        #YOUR CODE
        if self.not_empty() == False:
            # raise Exception("Dequeuing from an empty queue")
            return None
        if self.size == 1:
            self.tail = self.header
        remove = self.header.next
        self.header.next = self.header.next.next
        remove.next.prev = self.header
        self.size = self.size - 1
        return remove.obj
        raise NotImplementedError
   
   # works for all of the three types.

    def delete(self, obj):
        #YOUR CODE
        if self.not_empty() == False:
            raise Exception("Deleting from an empty data object.")
        current = self.header.next
        while (current != self.header):       
            if (current.obj == obj):
                if (current == self.tail):   
                    self.tail = current.prev
                current.prev.next = current.next   
                current.next.prev = current.prev
                current = None
                if self.size == 1:
                    self.tail = self.header
                self.size = self.size - 1
                break
            current = current.next
        return
        raise NotImplementedError

    # iterator objects for all.

    def __iter__(self):
        #YOUR CODE
        self.i = -1
        return self
        raise NotImplementedError

    def __next__(self):
        #YOUR CODE
        self.i = self.i + 1
        return
        raise NotImplementedError

    def __str__(self):
        s=''
        h=self.header
        e=self.header.next
        s=f'List size: {self.size}'
        s += '\n'
        while e != h:
            s += f'{e.obj}'
            if (e.next != h):
                s += '\n'
            e = e.next
        s += '\n'
#       if e.prev != self.tail:
#            s += f'tail corrupt: tail: {self.tail.obj} list tail: {e.prev.obj}'

        if self.tail != self.header:
            s += f'Tail: {self.tail.obj}'
        s += '\n'
        return s
             

def main():
    pass

if __name__ == "__main__":
    main()

l1 = mylist("list")
l2 = mylist("stack") 
l3 = mylist("queue")

# l1.add(1)
# l1.add(2)
# l1.add(3)
# l1.add(4)
# l1.delete(1)
# print(l1)

# # Done

# l2.push(1)
# l2.push(2)
# l2.push(3)
# l2.push(4)
# print("lookup 3",l2.lookup(3))
# print("peek is", l2.peek())
# # LIFO - remove 4
# l2.pop()
# print(l2)
# print("peek is", l2.peek())

# l3.enqueue(1)
# l3.enqueue(2)
# l3.enqueue(3)
# l3.enqueue(4)
# l3.enqueue(5)
# # FIFO - remove 1
# print(l3.dequeue())
# # print(l3)
# print(l3.dequeue())
# # print(l3)
# print(l3.dequeue())
# # print(l3)
# print(l3.dequeue())
# # print(l3)
# print(l3.dequeue())
# # print(l3)

# l=['a', 'aa', 'aaa', 'aachen', 'aardvark', 'aardvarks', 'aaron', 'ab', 'aba', 'ababa', 'abaci', 'aback', 'abactor', 'abactors', 'abacus', 'abacuses', 'abaft', 'abalone']
# que = mylist('queue')
# # print(myl.header == myl.tail)
# # myenqueue(myl,'aza')
# # mydequeue(myl)
# # print(myl.header == myl.tail)

# for i in l:
#     myqpush(que,i)
# print(que)
# # for i in que:
# #     print(i.obj)

# myqpop(que)
# print(que)
# print(myqpeek(que))