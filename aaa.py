class Node:
    def __init__(self,item):
        self.item=item
        self.next=None

class dxxhlb:
    def __init__(self,node=None):
        self.__head=node
        if node:
            node.next=node
    def is_empty(self):
        return self.__head==None

    def get_lenth(self):
        if self.is_empty():
            return 0
        else:
            count=1
            curl=self.__head
            while curl.next !=self.__head:
                count=count+1
                curl=curl.next
            return count
    def travel(self):
        if self.is_empty():
            print('单项循环列表为空')
            return

        curl=self.__head
        while curl.next!=self.__head:
            print(f'当前的值为:{curl.item}')
            curl=curl.next
        print(f'最后的值为{curl.item}')
    def append(self,item):
        node=Node(item)
        if self.is_empty():
            self.__head=node
            node.next=self.__head
        else:
            curl = self.__head
            while curl.next != self.__head:
                curl = curl.next
            curl.next=node
            node.next=self.__head

    def add(self,item):
        node=Node(item)
        if self.is_empty():
            self.__head=node
            node.next=self.__head

        else:
            curl=self.__head
            while curl.next!=self.__head:
                curl=curl.next
            node.next=self.__head
            self.__head=node
            curl.next=node
    def insert(self,item,p):
        if p<=0:
            self.add(item)
        if p>=self.get_lenth()-1:
            self.append(item)
        else:
            index=0
            pre=self.__head
            while index!=p-1:
                index+=1
                pre=pre.next
            Node(item).next=pre.next
            pre.next=Node(item)



a=dxxhlb()
a.append(233)
a.append(123123)
a.append(12331)
a.insert(7,1)
a.travel()


