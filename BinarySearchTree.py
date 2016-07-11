# -*- coding: utf-8 -*-
"""
Created on Sun May  8 20:26:26 2016

@author: kurmanbek
"""

class TreeNode:
    def __init__(self, key, val, left = None, right = None, parent = None):
        self.key        = key
        self.payload    = val
        self.leftChild  = left
        self.rightChild = right
        self.parent     = parent
        
    def hasLeftChild(self):
        return self.leftChild
        
    def hasRightChild(self):
        return self.rightChild
        
    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self
        
    def isRightChild(self):
        return self.parent and self.parent.rightChild == self
        
    def isRoot(self):
        return not self.parent
        
    def isLeaf(self):
        return not ( self.rightChild or self.leftChild )
        
    def hasAnyChildren(self):
        return self.rightChild or self.leftChild
        
    def hasBothChildren(self):
        return self.rightChild and self.leftChild
        
    def replaceNodeData(self, key, value, lc, rc):
        self.key = key
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self
            
            
class BinarySearchTree:
    
    def __init__(self):
        self.root = None
        self.size = 0
        self.inorderTraversal   = []
        self.preorderTraversal  = []
        self.postorderTraversal = []
        
    def length(self):
        return self.size
        
    def __len__(self):
        return self.size
     
    #Adds node to a binary tree
    def put(self, key, val):
        if self.root: #if tree has root
            self._put(key, val, self.root)
        else:
            self.root = TreeNode(key, val)
        self.size = self.size + 1
    
    #Helper method that adds node to a correct location in a BST
    def _put(self, key, val, currentNode):
        if( key < currentNode.key ): #if key is smaller than current key
            if(currentNode.hasLeftChild()):
                self._put(key, val, currentNode.leftChild)
            else:
                currentNode.leftChild = TreeNode(key, val, parent = currentNode)
        else:
            if( currentNode.hasRightChild() ):
                self._put(key, val, currentNode.rightChild)
            else:
                currentNode.rightChild = TreeNode(key, val, parent = currentNode)
                
    def __setitem__(self, k, v):
        self.put(k, v)
        
    def get(self, key):
        if self.root:
            res = self._get(key, self.root)
            if res:
                return res.payload
            else:
                return None
        else:
            return None
            
    def _get(self, key, currentNode):
        if not currentNode:
            return None
        elif currentNode.key == key:
            return currentNode
        elif key < currentNode.key:
            return self._get(key, currentNode.leftChild)
        else:
            return self._get(key, currentNode.rightChild)
            
    def __getitem__(self, key):
        return self.get(key)
        
    def __contains__(self, key):
        if self._get(key, self.root):
            return True
        else:
            return False
            
    def delete(self, key):
        if self.size > 1:
            nodeToRemove = self._get(key, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size = self.size - 1
            else:
                raise KeyError('Error, key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size = self.size - 1
        else:
            raise KeyError('Error, key not in tree')
            
    def __delitem__(self, key):
        self.delete(key)
        
    def findSuccessor(self, key):
        succ = None
        currentNode = self._get(key, self.root)
        if currentNode.hasRightChild():
            succ = self.findMin(currentNode.rightChild)
        else:
            succ = currentNode.parent
            while succ is not None and currentNode == succ.rightChild:
                currentNode = succ
                succ = succ.parent
        return succ
        
    def findMin(self, currentNode):
        current = currentNode
        while current.hasLeftChild():
            current = current.leftChild
        return current
    
    def findMax(self, currentNode):
        current = currentNode
        while current.hasRightChild():
            current = current.rightChild
        return current
        
    def transplant(self, firstNode, secondNode):
        ''' Replaces the one subtree as a child of its parent
        with another subtree. When "transplant" replaces the subtree rooted at firstNode with the subtree
        rooted at secondNode, firstNode's parent becomes secondNode's parent, and firstNode's parent ends
        up having secondNode as its appropriate child.
        '''
        if firstNode.parent is None:
            self.root = secondNode
        elif firstNode is firstNode.parent.leftChild:
            firstNode.parent.leftChild = secondNode
        else:
            firstNode.parent.rightChild = secondNode
        if secondNode is not None:
            secondNode.parent = firstNode.parent
                
    def remove(self, currentNode):
        '''Deletes a node from a BST
        '''
        if currentNode.leftChild is None:
            self.transplant(currentNode, currentNode.rightChild)
        elif currentNode.rightChild is None:
            self.transplant(currentNode, currentNode.leftChild)
        else:
            scc = self.findMin(currentNode.rightChild)
            if scc.parent is not currentNode:
                self.transplant(scc, scc.rightChild)
                scc.rightChild = currentNode.rightChild
                scc.rightChild.parent = scc
            self.transplant(currentNode, scc)
            scc.leftChild = currentNode.leftChild
            scc.leftChild.parent = scc
    
    
    def inorder(self, currentNode):
        if currentNode is None:
            return
        self.inorder(currentNode.leftChild)
        print(currentNode.key)
        self.inorder(currentNode.rightChild)
        
    def iterativeInorder(self, currentNode):
        s = []
        #reinitialize inorder traversal array
        if len(self.inorderTraversal) != 0:
            self.inorderTraversal = []
            
        while not (len(s) == 0) or currentNode is not None:
            if currentNode is not None:
                s.append(currentNode)
                currentNode = currentNode.leftChild
            else:
                currentNode = s.pop()
                self.inorderTraversal.append(currentNode.key)
                print(currentNode.key)
                currentNode = currentNode.rightChild
        
        return self.inorderTraversal
        
    def preorder(self, currentNode):
        if currentNode is None:
            return
        print(currentNode.key)
        self.preorder(currentNode.leftChild)
        self.preorder(currentNode.rightChild)
    
    def iterativePreorder(self, currentNode):
        s = []
        #reinitialize preorder traversal array
        if len(self.preorderTraversal) != 0:
            self.preorderTraversal = []
            
        while not (len(s) == 0) or currentNode is not None:
            if currentNode is not None:
                self.preorderTraversal.append(currentNode.key)
                if currentNode.rightChild is not None:
                    s.append(currentNode.rightChild)
                currentNode = currentNode.leftChild
            else:
                currentNode = s.pop()
        
        return self.preorderTraversal
                
    def postorder(self, currentNode):
        if currentNode is None:
            return
        self.postorder(currentNode.leftChild)
        self.postorder(currentNode.rightChild)
        print(currentNode.key)
    
    def iterativePostorder(self, currentNode):
        s = []
        lastNodeVisited = None
        if len(self.postorderTraversal) != 0:
            self.postorderTraversal = []
            
        while not (len(s) == 0) or currentNode is not None:
            if currentNode is not None:
                s.append(currentNode)
                currentNode = currentNode.leftChild
            else:
                peekNode = s[len(s) - 1]
                #if right child exists and traversing node
                #from left child, then move right
                if peekNode.rightChild is not None and lastNodeVisited != peekNode.rightChild:
                    currentNode = peekNode.rightChild
                else:
                    self.postorderTraversal.append(peekNode.key)
                    lastNodeVisited = s.pop()
        
        return self.postorderTraversal
        
    def isBST(self, curNode, minKey = -1, maxKey = 15):
        if curNode is None:
            return True
        if curNode.key < minKey or curNode.key >= maxKey:
            return False
        return self.isBST( curNode.leftChild, minKey, curNode.key) and self.isBST(curNode.rightChild, curNode.key, maxKey )
                                    
'''
mytree = BinarySearchTree()
mytree.put(5, "five")
mytree.put(2, "zero")
mytree.put(7, "seven")
mytree.put(6, "six")
mytree.delete(5)
#scc = mytree.findSuccessor(5)
#print('successor', scc.key)

print("inorder")
mytree.inorder(mytree.root)
print("iterative inorder")
mytree.iterativeInorder(mytree.root)
print("preorder traversal")
mytree.preorder(mytree.root)
print("iterative preorder traversal")
mytree.iterativePreorder(mytree.root)
print("postorder traversal")
mytree.postorder(mytree.root)
print("iterative postorder traversal")
mytree.iterativePostorder(mytree.root)
mytree.inorder(mytree.root)
'''


            
        
           
            