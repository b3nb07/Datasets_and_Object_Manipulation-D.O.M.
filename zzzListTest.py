class ilyaLinkedListNode:
    def __init__(self, thread, i):
        self.thread = thread
        self.next = None
        self.id = i
            
    def __str__(self):
        return ("string of id {i}").format(i = self.id)

    def setNext(self, next):
        self.next = next


t = ilyaLinkedListNode("a", 1)
tt = ilyaLinkedListNode("b", 2)
ttt = ilyaLinkedListNode("c", 3)



class testLink:
    def __init__(self):
        self.currentNode = None
        self.lastNode = None

    def addQueue(self, node):
        if self.currentNode == None:
            self.currentNode = node
            self.lastNode = node
        else:
            self.lastNode.next = node
            self.lastNode = node

    def next(self):
        self.currentNode = self.currentNode.next
        return self.currentNode

    def allList(self):
        curr = self.currentNode
        while (curr != None):
            print(curr)
            curr = curr.next



q = []

q.append("Wazza")
print(q[0])
print(q.pop(0))
print(q)