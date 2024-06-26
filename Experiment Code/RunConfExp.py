#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import random
import math
import secrets
import subprocess
import string
import random
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



#hash_object = hashlib.sha256(b'Hello World')
#hex_dig = hash_object.hexdigest()

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


BLOCK_SIZE = 16
pad = lambda s: s + bytes(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]









SampleCount = 1024


InitialCreationStartTime = 0
InitialCreationEndTime = 0
    
FirstEvolutionStartTime = 0
FirstEvolutionEndTime = 0

SecondEvolutionStartTime = 0
SecondEvolutionEndTime = 0

ThirdEvolutionStartTime = 0
ThirdEvolutionEndTime = 0


InitialRetrievalStartTime = 0
InitialRetrievalEndTime = 0
    
FirstRetrievalStartTime = 0
FirstRetrievalEndTime = 0

SecondRetrievalStartTime = 0
SecondRetrievalEndTime = 0

ThirdRetrievalStartTime = 0
ThirdRetrievalEndTime = 0


repfilename = 'Report.txt'
repfile = open(repfilename,"w+")
currdir = os.getcwd()

DESKey = b'abcdabcd'
DES3Key = DES3.adjust_key_parity(get_random_bytes(24))
AES128Key = b'abcdabcdabcdabcd'
AES192Key = b'abcdabcdabcdabcdabcdabcd'
AES256Key = b'abcdabcdabcdabcdabcdabcdabcdabcd'



def InitialCreation(fsize):
    leaves = []
    nodes = []
    leaves2 = []
    nodes2 = []

    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)

    InitialCreationStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/sample/' + fsize + str(i) + '.txt'
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        data = DES_Obj.encrypt(data)
        data = DES3_Obj.encrypt(data)
        Hash_Obj_MD2 = MD2.new(data=data)
        Hash_Obj_MD5 = MD5.new(data=data)
        leaves.append(Hash_Obj_MD2.hexdigest())
        leaves2.append(Hash_Obj_MD5.hexdigest())
        cfilename = currdir + '/Initial/' + fsize + str(i)
        cfile = open(cfilename,"wb")
        cfile.write(data)
        cfile.close


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
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
            Hash_Obj_MD2 = MD2.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes[j].parent = v
            nodes[j+1].parent = v
            nodes[j].parentIndex = len(nodes)
            nodes[j+1].parentIndex = len(nodes)
            data = Hash_Obj_MD2.hexdigest()
            nodes.append(MerkleTreeNode(v,data,'None',0,nodes[j].name,j,nodes[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
    j = 1 
       
    for i in leaves2:
        nodes2.append(MerkleTreeNode(str(l) + '-' + str(j),i,'None',0,'None',0,'None',0))
        j += 1


    first = 0
    last = m
    jump = m / 2
    start = first
    end = last
    
    while l!=0:
        loc = 1
        for j in range (start,end,2):
            data = str(nodes2[j].hashValue) + str(nodes2[j+1].hashValue)
            data = str.encode(data) #hex(int(data,16))
            Hash_Obj_MD5 = MD5.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes2[j].parent = v
            nodes2[j+1].parent = v
            nodes2[j].parentIndex = len(nodes2)
            nodes2[j+1].parentIndex = len(nodes2)
            data = Hash_Obj_MD5.hexdigest()
            nodes2.append(MerkleTreeNode(v,data,'None',0,nodes2[j].name,j,nodes2[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)



    InitialCreationEndTime = time.time()
    repstr = 'Total Initial Creation Time ' + fsize + ': ' + str(InitialCreationEndTime - InitialCreationStartTime) + '\n'
    repfile.write(repstr)




def InitialRetrival(fsize):
    DESKey = b'abcdabcd'
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)    
    InitialRetrievalStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/Initial/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        Hash_Obj_MD2 = MD2.new(data=data)
        Hash_Obj_MD5 = MD5.new(data=Hash_Obj_MD2.digest())
        data = DES3_Obj.decrypt(data)
        data = DES_Obj.decrypt(data)
        rfilename = currdir + '/InitialRet/' + fsize + str(i)
        rfile = open(rfilename,"wb")
        rfile.write(data)
        rfile.close
    InitialRetrievalEndTime = time.time()
    repstr = 'Total Initial Retrieval Time ' + fsize + ': ' + str(InitialRetrievalEndTime - InitialRetrievalStartTime) + '\n'
    repfile.write(repstr)


def FirstEvolution(fsize):
    leaves = []
    nodes = []
    leaves2 = []
    nodes2 = []    
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)
    FirstEvolutionStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/Initial/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        data = AES128_Obj.encrypt(data)
        Hash_Obj_MD5 = MD5.new(data=data)
        Hash_Obj_SHA256 = SHA256.new(data=data)
        leaves2.append(Hash_Obj_SHA256.hexdigest())
        leaves.append(Hash_Obj_MD5.hexdigest())
        cfilename = currdir + '/FirstEvol/' + fsize + str(i)
        cfile = open(cfilename,"wb")
        cfile.write(data)
        cfile.close


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
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
            Hash_Obj_MD5 = MD5.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes[j].parent = v
            nodes[j+1].parent = v
            nodes[j].parentIndex = len(nodes)
            nodes[j+1].parentIndex = len(nodes)
            data = Hash_Obj_MD5.hexdigest()
            nodes.append(MerkleTreeNode(v,data,'None',0,nodes[j].name,j,nodes[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
    j = 1 
       
    for i in leaves2:
        nodes2.append(MerkleTreeNode(str(l) + '-' + str(j),i,'None',0,'None',0,'None',0))
        j += 1


    first = 0
    last = m
    jump = m / 2
    start = first
    end = last
    
    while l!=0:
        loc = 1
        for j in range (start,end,2):
            data = str(nodes2[j].hashValue) + str(nodes2[j+1].hashValue)
            data = str.encode(data) #hex(int(data,16))
            Hash_Obj_SHA256 = SHA256.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes2[j].parent = v
            nodes2[j+1].parent = v
            nodes2[j].parentIndex = len(nodes2)
            nodes2[j+1].parentIndex = len(nodes2)
            data = Hash_Obj_SHA256.hexdigest()
            nodes2.append(MerkleTreeNode(v,data,'None',0,nodes2[j].name,j,nodes2[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)



    FirstEvolutionEndTime = time.time()
    repstr = 'Total First Evolution Time ' + fsize + ': ' + str(FirstEvolutionEndTime - FirstEvolutionStartTime) + '\n'
    repfile.write(repstr)




def FirstRetrival(fsize):
    DESKey = b'abcdabcd'
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)    
    FirstRetrievalStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/FirstEvol/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        Hash_Obj_SHA256 = SHA256.new(data=data)
        data = AES128_Obj.decrypt(data)
        data = DES3_Obj.decrypt(data)
        data = DES_Obj.decrypt(data)
        rfilename = currdir + '/FirstRet/' + fsize + str(i)
        rfile = open(rfilename,"wb")
        rfile.write(data)
        rfile.close
    FirstRetrievalEndTime = time.time()
    repstr = 'Total First Retrieval Time ' + fsize + ': ' + str(FirstRetrievalEndTime - FirstRetrievalStartTime) + '\n'
    repfile.write(repstr)






def SecondEvolution(fsize):
    leaves = []
    nodes = []
    leaves2 = []
    nodes2 = []    
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)
    SecondEvolutionStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/FirstEvol/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        data = AES192_Obj.encrypt(data)
        Hash_Obj_SHA256 = SHA256.new(data=data)
        Hash_Obj_SHA384 = SHA384.new(data=data)
        leaves.append(Hash_Obj_SHA256.hexdigest())
        leaves2.append(Hash_Obj_SHA384.hexdigest())
        cfilename = currdir + '/SecondEvol/' + fsize + str(i)
        cfile = open(cfilename,"wb")
        cfile.write(data)
        cfile.close


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
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


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
    j = 1 
       
    for i in leaves2:
        nodes2.append(MerkleTreeNode(str(l) + '-' + str(j),i,'None',0,'None',0,'None',0))
        j += 1


    first = 0
    last = m
    jump = m / 2
    start = first
    end = last
    
    while l!=0:
        loc = 1
        for j in range (start,end,2):
            data = str(nodes2[j].hashValue) + str(nodes2[j+1].hashValue)
            data = str.encode(data) #hex(int(data,16))
            Hash_Obj_SHA384 = SHA384.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes2[j].parent = v
            nodes2[j+1].parent = v
            nodes2[j].parentIndex = len(nodes2)
            nodes2[j+1].parentIndex = len(nodes2)
            data = Hash_Obj_SHA384.hexdigest()
            nodes2.append(MerkleTreeNode(v,data,'None',0,nodes2[j].name,j,nodes2[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)


    SecondEvolutionEndTime = time.time()
    repstr = 'Total Second Evolution Time ' + fsize + ': ' + str(SecondEvolutionEndTime - SecondEvolutionStartTime) + '\n'
    repfile.write(repstr)




def SecondRetrival(fsize):
    DESKey = b'abcdabcd'
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)    
    SecondRetrievalStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/SecondEvol/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        Hash_Obj_SHA384 = SHA384.new(data=data)
        data = AES192_Obj.decrypt(data)
        data = AES128_Obj.decrypt(data)
        data = DES3_Obj.decrypt(data)
        data = DES_Obj.decrypt(data)
        rfilename = currdir + '/SecondRet/' + fsize + str(i)
        rfile = open(rfilename,"wb")
        rfile.write(data)
        rfile.close
    SecondRetrievalEndTime = time.time()
    repstr = 'Total Second Retrieval Time ' + fsize + ': ' + str(SecondRetrievalEndTime - SecondRetrievalStartTime) + '\n'
    repfile.write(repstr)





def ThirdEvolution(fsize):
    leaves = []
    nodes = []
    leaves2 = []
    nodes2 = []    
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)
    ThirdEvolutionStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/SecondEvol/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        data = AES256_Obj.encrypt(data)
        Hash_Obj_SHA384 = SHA384.new(data=data)
        Hash_Obj_SHA3_512 = SHA3_512.new(data=data)
        leaves.append(Hash_Obj_SHA384.hexdigest())
        leaves2.append(Hash_Obj_SHA3_512.hexdigest())
        cfilename = currdir + '/ThirdEvol/' + fsize + str(i)
        cfile = open(cfilename,"wb")
        cfile.write(data)
        cfile.close


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
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
            Hash_Obj_SHA384 = SHA384.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes[j].parent = v
            nodes[j+1].parent = v
            nodes[j].parentIndex = len(nodes)
            nodes[j+1].parentIndex = len(nodes)
            data = Hash_Obj_SHA384.hexdigest()
            nodes.append(MerkleTreeNode(v,data,'None',0,nodes[j].name,j,nodes[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)


    l = int(math.log(SampleCount,2))
    m = SampleCount
        
    j = 1 
       
    for i in leaves2:
        nodes2.append(MerkleTreeNode(str(l) + '-' + str(j),i,'None',0,'None',0,'None',0))
        j += 1


    first = 0
    last = m
    jump = m / 2
    start = first
    end = last
    
    while l!=0:
        loc = 1
        for j in range (start,end,2):
            data = str(nodes2[j].hashValue) + str(nodes2[j+1].hashValue)
            data = str.encode(data) #hex(int(data,16))
            Hash_Obj_SHA3_512 = SHA3_512.new(data)
            v = str(int(l-1)) + '-' + str(loc)
            nodes2[j].parent = v
            nodes2[j+1].parent = v
            nodes2[j].parentIndex = len(nodes2)
            nodes2[j+1].parentIndex = len(nodes2)
            data = Hash_Obj_SHA3_512.hexdigest()
            nodes2.append(MerkleTreeNode(v,data,'None',0,nodes2[j].name,j,nodes2[j+1].name,j+1))
            loc += 1
        first = last
        last = first + int(jump)
        start = first
        end = last
        jump = jump / 2
        l -= 1 
        m = int(m / 2)




    ThirdEvolutionEndTime = time.time()
    repstr = 'Total Third Evolution Time ' + fsize + ': ' + str(ThirdEvolutionEndTime - ThirdEvolutionStartTime) + '\n'
    repfile.write(repstr)




def ThirdRetrival(fsize):
    DESKey = b'abcdabcd'
    DES_Obj = DES.new(DESKey,DES.MODE_CBC)
    DES3_Obj = DES3.new(DES3Key,DES3.MODE_CBC)
    AES128_Obj = AES.new(AES128Key,AES.MODE_CBC)
    AES192_Obj = AES.new(AES192Key,AES.MODE_CBC)
    AES256_Obj = AES.new(AES256Key,AES.MODE_CBC)    
    ThirdRetrievalStartTime = time.time()
    for i in range (1001,1001 + SampleCount):
        currfile = currdir + '/ThirdEvol/' + fsize + str(i)
        f = open(currfile,"rb")
        data = f.read()  #Plain Data Sector
        f.close
        Hash_Obj_SHA3_512 = SHA3_512.new(data=data)
        data = AES256_Obj.decrypt(data)
        data = AES192_Obj.decrypt(data)
        data = AES128_Obj.decrypt(data)
        data = DES3_Obj.decrypt(data)
        data = DES_Obj.decrypt(data)
        rfilename = currdir + '/ThirdRet/' + fsize + str(i)
        rfile = open(rfilename,"wb")
        rfile.write(data)
        rfile.close
    ThirdRetrievalEndTime = time.time()
    repstr = 'Total Third Retrieval Time ' + fsize + ': ' + str(ThirdRetrievalEndTime - ThirdRetrievalStartTime) + '\n'
    repfile.write(repstr)










def main():

    InitialCreation('1K_')
    InitialRetrival('1K_')
    InitialCreation('1M_')
    InitialRetrival('1M_')
    InitialCreation('10M_')
    InitialRetrival('10M_')

    FirstEvolution('1K_')
    FirstRetrival('1K_')
    FirstEvolution('1M_')
    FirstRetrival('1M_')
    FirstEvolution('10M_')
    FirstRetrival('10M_')

    SecondEvolution('1K_')
    SecondRetrival('1K_')
    SecondEvolution('1M_')
    SecondRetrival('1M_')
    SecondEvolution('10M_')
    SecondRetrival('10M_')

    ThirdEvolution('1K_')
    ThirdRetrival('1K_')
    ThirdEvolution('1M_')
    ThirdRetrival('1M_')
    ThirdEvolution('10M_')
    ThirdRetrival('10M_')   
    
    repfile.close 



if __name__ == '__main__':
    main()  
