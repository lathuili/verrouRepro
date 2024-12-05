#!/usr/bin/python3

import sys


def diffLine(lineTab):
    refLine=lineTab[0]
    cmpLine=lineTab[1]
    refSize=len(refLine)
    cmpSize=len(cmpLine)
    refRes=""
    cmpRes=""

    for i in range(min(refSize, cmpSize)):
        refChar=refLine[i]
        cmpChar=cmpLine[i]
        if refChar==cmpChar:
            localChar=refChar
            if refChar==" ":
                localChar="\phantom{0}"
            refRes+=localChar
            cmpRes+=localChar
        else:
            latexPrefix="\only<3>{\colorbox{red!30}}{"
            latexPostfix="}"
            refRes+=latexPrefix+refChar+latexPostfix
            cmpRes+=latexPrefix+cmpChar+latexPostfix
    return refRes + "  &  \n"+ "\visible<2->{"+cmpRes +"}\\\n"


def countSpaceInit(line):
    incIndex=0
    while line[incIndex]==" ":
        incIndex+=1
    return incIndex




def diffFileOutput(fileTab):
    res="{\n\color{black}\setlength{\fboxsep}{0pt}\n\begin{tabular}{l|l}\n"
    #res+=("&".join(fileTab)).replace("_","\_")+"\\\n"
    res+= fileTab[0].replace("_","\_")+ "& " + "\visible<2->{"+fileTab[1].replace("_","\_")+"}" + "\\\n"

    linesTabBrut=[open(fileName).readlines() for fileName in fileTab]

    spaceToRemove=min([ min([countSpaceInit(line) for line in lines]) for lines in linesTabBrut ])
    linesTab=[[ line[spaceToRemove:] for line in lines]  for lines in linesTabBrut]

    for i in range(len(linesTab[0])):
        lineTab=[lines[i] for lines in linesTab]
        res+=diffLine(lineTab)

    res+="\end{tabular}\n}\n"
    return res



def printLatex(str):
    res=str.replace("\\\n","\\\\\n")
    res=res.replace("\b","\\b")
    res=res.replace("\f","\\f")
    res=res.replace("\v","\\v")
    print(res)


if __name__=="__main__":
    printLatex(diffFileOutput(sys.argv[1:]))

