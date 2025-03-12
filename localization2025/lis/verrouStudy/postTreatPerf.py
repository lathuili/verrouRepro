#!/usr/bin/python3
import os
import glob
import sys
import re


def avgMeasure(tab, num, discard):
    if None in tab:
        return None
    localTab=tab[discard:-discard]
    if discard==0:
        localTab=tab
    return sum(localTab) /len(localTab)

def parseTime(rep, name, num, discard=0):
    resExt=[]
    resIn=[]
    for i in range(1, num+1):
        fileName=os.path.join(rep, "time"+name+"."+str(num))
        resLine=open(fileName).readline()
        timeExt=float(resLine)

        fileName=os.path.join(rep, "res-"+name+"-"+str(num)+".out")
        lineTab=open(fileName).readlines()
        timeIn=None
        for line in lineTab:
            if line.startswith("Inverse: elapsed time"):
                timeIn=float((line.partition("=")[2]).replace("sec.","").strip())

        resExt+=[timeExt]
        resIn+=[timeIn]

    return (avgMeasure(resExt,num,discard), avgMeasure(resIn,num,discard))

def parseTab(rep, tabName, num, discard=0):
    res={name:parseTime(rep, name,num,discard) for name in tabName}
    return res

def toLatex(res, ref, valNone, listOfVerrou):
    print("\\begin{tabular}{ccccc}\n")
    print("\\toprule\n")
    print("\multicolumn{3}{c}{Instrumentation} & time & total time \\\\\n")
    print("\\midrule\n")
    refValue=res[ref][0]
    refInValue=res[ref][1]

    print("\multicolumn{3}{c}{Native} & %.2fs & %.2fs\\\\\n"%(refInValue, refValue))
    valueNone=res[valNone][0]
    valueNoneIn=res[valNone][1]
    valueStr="%.2fs "%(valueNone)
    slowDown="(x%.1f)"%(valueNone/ refValue)
    valueStrIn="%.2fs "%(valueNoneIn)
    slowDownIn="(x%.1f)"%(valueNoneIn/ refInValue)

    print("\multicolumn{3}{c}{tool:none} & %s & %s \\\\\n"%(valueStrIn+slowDownIn, valueStr+slowDown ))

    print("\\midrule\n")
    print(" Symbols & IOmatch & rounding & & \\\\\n")
    print("\\midrule\n")
    for name in listOfVerrou:
        conf=listOfVerrou[name]
        confStr=conf[1]+"\t&\t" +  conf[0]+"\t&\t"+ conf[2] +"\t&\t"

        value=res[name][0]
        valueIn=res[name][1]
        valueStr="%.2fs "%(value)
        slowDown="(x%.1f)"%(value/ refValue)

        valueInStr="$\O$"
        slowInDown=""
        if valueIn!=None:
            valueInStr="%.2fs "%(valueIn)
            slowInDown="(x%.1f)"%(valueIn/ refInValue)
        if name==ref:
            slowDown=""
            slowInDown=""

        print( confStr + valueInStr + " "+slowInDown+ "\t&\t"
                       + valueStr +" "+ slowDown + "\\\\\n")

    print("\\bottomrule\n")
    print("\end{tabular}\n")


if __name__=="__main__":

    res=parseTab("perfDir",
                 [   "Native",
                     "None",
                     "IOmatchExclude",
                     "All",
                     "AllRandom",
                     "Exclude",
                     "IOmatch",
                     "IOmatchRandom",
                     "IOmatchDDCMP",
                     "IOmatchDDCMP_soft",
                     "IOmatchDDCMPRandom",
                     "IOmatchDDCMPRandom_soft"
                  ]
                 , 30,5)

    convTab={
             "Exclude":("No", "None", "*") ,
             "IOmatchExclude":("earlyExit","None","*"),
             "All":("No","all","float"),
             "AllRandom":("No","all","random"),
             "IOmatch":("earlyExit","all","float"),
             "IOmatchRandom": ("earlyExit","all","random"),
             "IOmatchDDCMP":  ("rddCmp","all","float"),
             "IOmatchDDCMPRandom":  ("rddCmp","all","random"),
             "IOmatchDDCMP_soft": ("rddCmp(soft)","all","float"),
             "IOmatchDDCMPRandom_soft": ("rddCmp(soft)","all","random")
             }

    toLatex(res, "Native", "None", convTab)
#    toLatex2(res,res2)

