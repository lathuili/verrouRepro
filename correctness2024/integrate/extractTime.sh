#!/usr/bin/sh

echo "#nb rectangle\tvalue"
awk  '{print $1 " " $2}' $1/res.dat


