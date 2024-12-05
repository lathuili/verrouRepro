#!/bin/bash

valgrind --tool=verrou --float=yes ../lis/test/etest2 100 100 1 res.dat rh.dat -e ii -i bicgstab -p ilu -ilu_fill 2 -print out -eprint out > $1/res.out


