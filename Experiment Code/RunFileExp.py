#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import math
import random
import secrets
import subprocess
import string
from Cryptodome.Cipher import AES, DES3, DES
from Cryptodome.Hash import MD2, MD5, SHA256, SHA384, SHA3_512
from Cryptodome.Random import get_random_bytes
from Cryptodome import Random
from base64 import b64encode, b64decode
import base64
import hashlib
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes)

import datetime
import time



class MerkleTreeNode:
    def __init__(self,name,hashValue,parent,parentIndex,left,leftIndex,right,rightIndex):
        self.left = left
        self.right = right
        self.leftIndex = leftIndex
        self.rightIndex = rightIndex        
        self.parent = parent
        self.name = name
        self.hashValue = hashValue
        self.parentIndex = parentIndex


UpdateStartTime = 0
UpdateEndTime = 0

repfilename = 'Report.txt'
repfile = open(repfilename,"w+")

nodes = []
    
    
def CreateTree(n):
    l = int(math.log(n,2))
    m = n

    leaves = []
    
    for i in range (1001,1001 + n):
        data = secrets.token_bytes(1000)
        Hash_Obj_SHA256 = SHA256.new(data=data)
        leaves.append(Hash_Obj_SHA256.hexdigest())
        
    j = 1 
       
    for i in leaves:
        nodes.append(MerkleTreeNode(str(l) + '-' + str(j),i,'None',0,'None',0,'None',0))
        j += 1


    first = 0
    last = m
    jump = m / 2
    start = first
    end = last
    
    while l!=0:
        loc = 1
        for j in range (start,end,2):
            data = str(nodes[j].hashValue) + str(nodes[j+1].hashValue)
            data = str.encode(data) #hex(int(data,16))
            Hash_Obj_SHA256 = SHA256.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes[j].parent = v
            nodes[j+1].parent = v
            nodes[j].parentIndex = len(nodes)
            nodes[j+1].parentIndex = len(nodes)
            data = Hash_Obj_SHA256.hexdigest()
            nodes.append(MerkleTreeNode(v,data,'None',0,nodes[j].name,j,nodes[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)


#    for k in range(0,len(nodes)):
#        repstr = str(nodes[k].name) + ',' + str(nodes[k].parent) + ',' + str(nodes[k].parentIndex) + ',' + str(nodes[k].left) + ',' + str(nodes[k].leftIndex) + ',' + str(nodes[k].right) + ',' + str(nodes[k].rightIndex) + ',' + str(nodes[k].hashValue) + ',' + str(k) + '\n'
#        repfile.write(repstr)
    


def main():

    n = 1048576
    
    CreateTree(n)
  

    l = int(math.log(n,2))

    for i in range(0,1000):
        j = random.randint(0, n-1)
        data = secrets.token_bytes(1000)
        UpdateStartTime = time.time()
        Hash_Obj_SHA256 = SHA256.new(data=data)
        nodes[j].hashValue = Hash_Obj_SHA256.hexdigest()
        parentIndex = nodes[j].parentIndex
        parent = nodes[j].parent
        while parent != 'None':
            leftIndex = nodes[parentIndex].leftIndex
            rightIndex = nodes[parentIndex].rightIndex
            data = str(nodes[leftIndex].hashValue) + str(nodes[rightIndex].hashValue)
            data = str.encode(data)
            Hash_Obj_SHA256 = SHA256.new(data)
            nodes[parentIndex].hashValue = Hash_Obj_SHA256.hexdigest()
            parent = nodes[parentIndex].parent
            parentIndex = nodes[parentIndex].parentIndex
        UpdateEndTime = time.time()
        repstr = str(UpdateEndTime - UpdateStartTime) + '\n'
        repfile.write(repstr)
    

        repfile.close
    




if __name__ == '__main__':
    main()  
