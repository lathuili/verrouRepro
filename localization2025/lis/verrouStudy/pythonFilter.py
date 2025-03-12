#!/usr/bin/python3 -u
import sys


#global variable
fusionParam=1
outer=False
outerCounter=-1
outerFusion=False
outerFusionParam=1
nextItIsOuter=False

def outerPrefix(strLine):
    if outer:
        return "outer-%i "%((outerCounter//outerFusionParam)*outerFusionParam )+strLine
    else:
        return strLine
    
def fusionFilter(strLine):
    global nextItIsOuter
    if line.startswith("linear solver status  : normal end"):
        nextItIsOuter=True
        return outerPrefix(strLine)
    if strLine.startswith("matrix storage format : CSR"):
        global outerCounter
        outerCounter+=1
        return outerPrefix(strLine)
        
    if strLine.startswith("iteration:"):
        if nextItIsOuter:
            nextItIsOuter=False
            if outer:
                it=int( ((strLine.split(":")[1]).strip()).split()[0])
                return "outer "+strLine.replace(str(it),
                                                str(((it//outerFusionParam)*outerFusionParam )))
            else:
                return strLine
        else:
            #inner loop fusion by keeping only 1/fusionParam line
            it=int( ((strLine.split(":")[1]).strip()).split()[0])
            if it%fusionParam==0:
                #outer loop fusion by prefixing line by a prefix (common for each fusionned iteration)
                return outerPrefix(strLine)
            else:
                return ""
    else:
        return strLine

#read line char by char: important to take this version (coming from verrou documentation)
#Indeed with readline, you will get synchronisation troubles. 
def getLineCharByChar():
    line=""
    while True:
        c=sys.stdin.read(1)
        if line== "\x00": #EOF detected
            return None
        if c=='\n':
            return line
        line+=c

def applyFilter(strLine,filterList):
    res=strLine
    for filterFnc in filterList:
        res=filterFnc(res)
    return res
        
if __name__=="__main__":
    fusion=False
    if len(sys.argv)>1:
        for arg in sys.argv:
            if arg.startswith("--loop-fusion="):
                fusion=True
                fusionParam=int(arg.partition("=")[2])
            if arg=="--outer":
                outer=True
            if arg.startswith("--outer-loop-fusion="):
                outerFusion=True
                outerFusionParam=int(arg.partition("=")[2])

    while True:
        line=getLineCharByChar()
        if line==None:
            sys.exit(0)
        if fusion or outerFusion:
            print(applyFilter(line, [fusionFilter]))
        else:
            print(line)
        

