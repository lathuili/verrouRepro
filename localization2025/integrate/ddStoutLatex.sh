#!/bin/bash

cd $1
echo "\begin{tabular}{ll}"
echo "\\toprule"
echo "ddmin & match line\\\\"
echo "\\midrule"
for exline in ddmin*
do

    echo "${exline}& \verb+$(cat ${exline}/dd.IOMatch.include)+\\\\"
done
echo "\bottomrule"
echo "\end{tabular}"
