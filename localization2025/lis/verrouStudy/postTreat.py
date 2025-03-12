#!/usr/bin/python3
import os
import glob
import sys
import re

def getSubSet(data,line):
    for i in data:
        if line in data[i]:
            return i
    return None    

def parseStdout(rep):
    refBrut=open(os.path.join(rep,"ref","dd.IOMatch")).readlines()
    ref=[x.replace("\n","")  for x in refBrut]
    
    ddminTab=glob.glob(os.path.join(rep, "ddmin*/"))
    ddminData={}
    for ddminRep in ddminTab:
        subsetDDmin= ddminRep.replace(rep,"")
        subsetDDmin=subsetDDmin.replace("/","")
        data=open(os.path.join(ddminRep, "dd.IOMatch.include")).readlines()
        ddminData[subsetDDmin]=[x.replace("\n","") for x in data]

    res=[]
    for refLine in ref:
        subset=getSubSet(ddminData, refLine)
        if subset==None:
            res+=[("OK", refLine)]
        else:
            res+=[(subset, refLine)]
    return res

matchCompiled=re.compile("(outer-\d*) (.*)$")    
def latexStr(line):
    #res=line.replace("*", "{\color{blue} *}")
    res=line
    if res.startswith("outer "):
        end=res.replace("outer ","")
        return"{\color{red}outer}" + "$\,$" + end  

    resMatch=matchCompiled.match(res)
    if resMatch==None:
        return res
    else:
        beg=resMatch.group(1)
        end=resMatch.group(2)
        return "{\color{red} "+beg+"}"+"$\,$"+end

def toLatex(res):
    print("\\begin{tabular}{ll}\n")
    print("\\toprule\n")    
    print("search space & ddmin subset\\\\\n")
    print("\\midrule\n")    
    for refLine in res:
        print( latexStr(refLine[1]) +  "\t&\t" + refLine[0]+ "\\\\\n")

    print("\\bottomrule\n")
    print("\end{tabular}\n")


def toLatex2(res, res2):
    print("\\begin{tabular}{lcc}\n")
    print("\\toprule\n")
    print("search space & \multicolumn{2}{c}{ddmin subset}  \\\\\n")
    print("             &all & all \\textbackslash \{dot\} \\\\\n")
    print("\\midrule\n")

    j=0
    for i in range(len(res)):
        refLine=res[i]
        bisLine=res2[j]
        if bisLine[1]==refLine[1]:
            print(latexStr(refLine[1]) +  "\t&\t" + refLine[0] + "\t&\t"+  bisLine[0]+ "\\\\\n")            
            j+=1
        else:
            print(latexStr(refLine[1]) +  "\t&\t" + refLine[0] + "\t&\t"+ "Void"+ "\\\\\n")

    if j!=len(res2):
        print("error")
        
    print("\\bottomrule\n")
    print("\end{tabular}\n")

    
    
    
if __name__=="__main__":
    res=parseStdout(sys.argv[1])
    res2=parseStdout(sys.argv[2])
    toLatex2(res,res2)

             
             
    
