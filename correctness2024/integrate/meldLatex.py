#!/usr/bin/python3
import sys

def loadFile(fileName, filterBefore=None):
    linesBrut=open(fileName).readlines()
    res=[]
    if filterBefore!=None:
        index=0
        for i in range(len(linesBrut)):
            if filterBefore in linesBrut[i]:
                index=i
                break
        lines=linesBrut[i:]
    else:
        lines=linesBrut

    for line in lines:
        spline=line.split(":",1)
        bb=spline[1]
        bbRename=bb.replace("unamed_filename_verrou(0)","??")
        bbRename=bbRename.replace("_","\_")
        res+=[{"count": (spline[0].strip()), "bb":bb,"bbRename":bbRename.strip()}]
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

def splitLeftStr(name, maxChar):
    if len(name)< maxChar:
        return [unknownConv(name)]
    else:
        for i in range(maxChar-2,0,-1):
            if name[i] in [')',' ']:
                return [unknownConv(name[0:i+1])] + splitLeftStr(name[i+1:],maxChar)
        print("maxChar not satified")
        for i in range(maxChar-1, len(name)-2): #-2 to avoid unuseful cut
            if name[i]in [')',' ']:
                return [unknownConv(name[0:i+1])] + splitLeftStr(name[i+1:],maxChar)
        print("maxChar not satified and backup")
        return [unknownConv(name)]


def generateDiffLatex(data, outputName, maxLine, maxChar, rightShort=6, verb=False, leftName=None, rightName=None):
    handler=open(outputName,"w+")
    handler.write("\\begin{tabular}{ll|ll}\n")
    handler.write("\\toprule\n")
    if leftName!=None or rightName!=None:
        if leftName!=None:
            handler.write("\multicolumn{2}{c|}{" + leftName+"}&" )
        else:
            handler.write("&&" )
        if rightName!=None:
            handler.write("\multicolumn{2}{c}{" + rightName+"}\\\\ \n" )
        else:
            handler.write("&\\\\ \n" )
        handler.write("\midrule\n")

    splitChar=" $\hookleftarrow$ "
    shortChar="\ding{34}"
    for i in range(len(data)):
        splitRightChar=splitChar
        splitLeftChar=splitChar
        line=data[i]
        strNameLeftTab=splitLeftStr(line["bbRename"], maxChar)

        if len(strNameLeftTab)==1:
            splitLeftChar=""

        strNameRight=unknownConv(line["bbRename"])
        cut=False
        if len(strNameRight)>= rightShort:
            cut=True
            strNameRightTab=[strNameRight[0:rightShort]]
            splitRightChar=shortChar
        else:
            strNameRightTab=strNameLeftTab
            splitRightChar=splitLeftChar

        tupleCountStr= strDiffInt(line["count"])
        leftStr=tupleCountStr[0]
        rightStr=tupleCountStr[1]

#        if leftStr!=rightStr:
#            handler.write("\\rowcolor{red!15}\n")
        strLine="%s &:%s%s & %s &:%s%s\\\\ \n"%(leftStr, strNameLeftTab[0], splitLeftChar, rightStr,strNameRightTab[0],splitRightChar)
        if verb:
            strLine="%s &:\\verb|%s|%s & %s &:\\verb|%s|%s\\\\ \n"%(leftStr, strNameLeftTab[0], splitLeftChar,rightStr,strNameRightTab[0],splitRightChar)
        if i< maxLine:
            if leftStr!=rightStr:
                handler.write("\\rowcolor{red!15}\n")
            handler.write(strLine )
        else:
            if leftStr!=rightStr:
                handler.write("%\\rowcolor{red!15}\n")
            handler.write("%"+strLine )
        for indexInner in range(1, len(strNameLeftTab)):
            if indexInner== len(strNameLeftTab)-1:
                splitLeftChar=""
            if indexInner== len(strNameRightTab)-1:
                splitRightChar=""

            followingLine =strNameLeftTab[indexInner]
            followingLineRight=""
            if not cut:
                followingLineRight=strNameRightTab[indexInner]
            else:
                splitRightChar=""
            if leftStr!=rightStr:
                handler.write("\\rowcolor{red!15}\n")
            strLine="%s &$\quad$%s%s & %s &$\quad$%s%s\\\\ \n"%("", followingLine, splitLeftChar,"",followingLineRight,splitRightChar)
            if verb:
                strLine="%s &$\quad\quad$\\verb|%s|%s & %s &$\quad\quad$\\verb|%s|%s\\\\ \n"%("", followingLine, splitLeftChar,"", followingLineRight, splitRightChar)
            if i< maxLine:
                handler.write(strLine )
            else:
                handler.write("%"+strLine )
    if len(data)>maxLine:
        nbLineSkipped=len(data)-maxLine
        handler.write(" \multicolumn{4}{c}{\ding{34}%i lines skipped \ding{34}}\\\\ \n"%(nbLineSkipped))
    handler.write("\\bottomrule")
    handler.write("\end{tabular}\n")


if __name__=="__main__":
    maxLine=100
    charMax=1000
    rightShort=6
    verb=False
    localArgv=[arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if len(localArgv)>3:
        maxLine=int(localArgv[3])

    if len(localArgv)>4:
        charMax=int(localArgv[4])
    if len(localArgv)>5:
        rightShort=int(localArgv[5])

    if "--verb" in sys.argv:
        verb=True

    filterBefore=None
    leftName=None
    rightName=None
    for opt in sys.argv:
        if opt.startswith("--filter-before="):
            filterBefore=(opt.split("=",1))[1]
        if opt.startswith("--left-name="):
            leftName=(opt.split("=",1))[1]
        if opt.startswith("--right-name="):
            rightName=(opt.split("=",1))[1]


    generateDiffLatex(merge( loadFile(localArgv[0], filterBefore),
                             loadFile(localArgv[1], filterBefore)),
                      localArgv[2],
                      maxLine,
                      charMax,
                      rightShort,
                      verb,
                      leftName,
                      rightName
                      )
