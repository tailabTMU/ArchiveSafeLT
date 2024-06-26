#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno
import random
import secrets
import subprocess
import string
from random import *





def main():
    currdir = os.getcwd()
    for i in range (1001,2025):
        currfile = currdir + '/sample/1K_' + str(i) + '.txt'
        allchar = string.ascii_letters + string.digits
        fillstr = "".join(choice(allchar) for x in range(1024))
        f = open(currfile,"w+")
        f.write(fillstr)
        f.close
    for i in range (1001,2025):
        currfile = currdir + '/sample/1M_' + str(i) + '.txt'
        allchar = string.ascii_letters + string.digits
        fillstr = "".join(choice(allchar) for x in range(1048576))
        f = open(currfile,"w+")
        f.write(fillstr)
        f.close    
    for i in range (1001,2025):
        currfile = currdir + '/sample/10M_' + str(i) + '.txt'
        allchar = string.ascii_letters + string.digits
        fillstr = "".join(choice(allchar) for x in range(10485760))
        f = open(currfile,"w+")
        f.write(fillstr)
        f.close







if __name__ == '__main__':
    main()  
