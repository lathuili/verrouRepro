#!/usr/bin/python3
import sys

def loadFile(fileName):
    lines=open(fileName).readlines()
    res=[]
    for line in lines:
        spline=line.split(":")
        bb=spline[1]
        bbRename=bb.replace("unamed_filename_verrou(0)","??")
        bbRename=bbRename.replace("_","\_")
        res+=[{"count": int(spline[0].strip()), "bb":bb,"bbRename":bbRename.strip()}]
    return res

def merge(data1, data2):
    if len(data1)!=len(data2):
        print("Merge error:", invalidSize)
    data=[]
    for i in range(len(data1)):
        if data1[i]["bb"]==data2[i]["bb"]:
            data+=[{"bb":data1[i]["bb"],
                    "bbRename":data1[i]["bbRename"],
                    "count":(data1[i]["count"],data2[i]["count"]) 
                    }]
        else:
            print("Merge error:", invalidSize)
    return data


def strDiffInt(countTuple):
    left=countTuple[0]
    right=countTuple[1]
    if left==right:
        return(str(left),str(right))
    else:
        strLeft=str(left)
        strRight=str(right)

        minSize=min(len(strLeft), len(strRight))
        for i in range(minSize):
            if strLeft[i]!=strRight[i]:
                resLeft=strLeft[0:i]+"\\textbf{"+strLeft[i:]+"}"
                resRight=strRight[0:i]+"\\textbf{"+strRight[i:]+"}"
                return (resLeft,resRight)
        resLeft=strLeft[0:minSize]+"\\textbf{"+strLeft[minSize:]+"}"
        resRight=strRight[0:minSize]+"\\textbf{"+strRight[minSize:]+"}"
        return (resLeft,resRight)

def unknownConv(name):
    return name.replace("??","\\faQuestionCircle[regular]")
    
def splitLeftStr(name, maxChar, splitRightChar=" $\hookleftarrow$ "):
    if len(name)< maxChar:
        return [unknownConv(name)]
    else:
        for i in range(maxChar-2,0,-1):
            if name[i]==')':
                return [unknownConv(name[0:i+1])+splitRightChar] + splitLeftStr(name[i+1:],maxChar)
        print("maxChar not satified")
        for i in range(maxChar-1, len(name)-2): #-2 to avoid unuseful cut
            if name[i]==')':
                return [unknownConv(name[0:i+1])] + splitLeftStr(name[i+1:],maxChar)
        print("maxChar not satified and backup")
        return [unknownConv(name)]
    
    
def generateDiffLatex(data, outputName, maxLine, maxChar):
    handler=open(outputName,"w+")
    handler.write("\\begin{tabular}{ll|ll}\n")
    handler.write("\\toprule")
    
    for i in range(len(data)):
        line=data[i]
        strNameLeftTab=splitLeftStr(line["bbRename"], maxChar)
        strNameRight=unknownConv(line["bbRename"][0:6])+"..."
        tupleCountStr= strDiffInt(line["count"])
        leftStr=tupleCountStr[0]
        rightStr=tupleCountStr[1]

        if leftStr!=rightStr:
            handler.write("\\rowcolor{red!15}\n") 
        strLine="%s &:%s & %s &:%s\\\\ \n"%(leftStr, strNameLeftTab[0], rightStr,strNameRight)
        if i< maxLine:
            handler.write(strLine )
        else:
            handler.write("%"+strLine )
        for followingLine in strNameLeftTab[1:]:
            if leftStr!=rightStr:
                handler.write("\\rowcolor{red!15}\n")
            strLine="%s &$\quad$%s & %s &%s\\\\ \n"%("", followingLine, "","")
            if i< maxLine:
                handler.write(strLine )
            else:
                handler.write("%"+strLine )
    if len(data)>maxLine:
        nbLineSkipped=len(data)-maxLine
        handler.write(" &$\dots$%i lines skipped $\dots$&  &\\\\ \n"%(nbLineSkipped))
    handler.write("\\bottomrule")
    handler.write("\end{tabular}\n")
        

if __name__=="__main__":
    maxLine=100
    charMax=1000
    if len(sys.argv)>=5:
        maxLine=int(sys.argv[4])

    if len(sys.argv)==6:
        charMax=int(sys.argv[5])

    generateDiffLatex(merge( loadFile(sys.argv[1]),
                             loadFile(sys.argv[2])),
                      sys.argv[3],
                      maxLine,
                      charMax
                      )
