#!/usr/bin/python3
import sys
import os

def extractValue(rep):
     """This parse function has to be adapted to each case"""
     lines=(open(os.path.join(rep,"res.out")).readlines())
     for line in lines:
         if line.startswith("Inverse: eigenvalue"):
             return float(line.partition("=")[2])
     return None

if __name__=="__main__":
     if len(sys.argv)==2:
           print(extractValue(sys.argv[1]))
     if len(sys.argv)==3:
          valueRef=extractValue(sys.argv[1])
          value=extractValue(sys.argv[2])

          relDiff=abs((value-valueRef)/valueRef)
          #the tolerance has to be adapted
          if relDiff < 1.e-4: sys.exit(0)
          else: sys.exit(1)
