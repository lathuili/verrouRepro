#!/bin/bash

cd $1
echo "\begin{tabular}{ll}"
echo "\\toprule"
echo "ddmin & task\\\\"
echo "\\midrule"
for exline in ddmin*
do

    echo "${exline}& \verb+$(cat ${exline}/dd.task.include)+\\\\"
done
echo "\bottomrule"
echo "\end{tabular}"
