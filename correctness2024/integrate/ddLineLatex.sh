#!/bin/bash

cd $1
echo "\begin{tabular}{lll}"
echo "\\toprule"
echo "ddmin & filename:line & demangled symbol name\\\\"
echo "\\midrule"
for exline in ddmin*
do
    fileName=$(cat ${exline}/dd.line.include| cut -f 1)
    lineNum=`cat ${exline}/dd.line.include| cut -f 2`
    sym=`cat ${exline}/dd.line.include| cut -f 3 | xargs c++filt | sed "s/&/ \\\\\&/" `
    echo "${exline}" "&" "\texttt{${fileName}":"${lineNum}}"  "&" " ${sym}" "\\\\"
done
echo "\bottomrule"
echo "\end{tabular}"
