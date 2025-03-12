#!/usr/bin/python3
import sys
import os.path
import re

def extractTab(rep):
    lines=(open(os.path.join(rep, "res.dat"))).readlines()
    return [float(re.split(" ",line.strip())[1]) for line in lines]
    
if __name__=="__main__":
    refValueTab=extractTab(sys.argv[1])
    valueTab=extractTab(sys.argv[2])      
    relDistTab= [ abs((valueTab[i] - refValueTab[i])/refValueTab[i])
                  for i in range(len(refValueTab))]
    if max(relDistTab) < 1e-5 : sys.exit(0)
    else: sys.exit(1)
