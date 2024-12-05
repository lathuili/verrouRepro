#!/bin/bash

CMD="../lis/test/etest2 100 100 1 res.dat rh.dat -e ii -i bicgstab -p ilu -ilu_fill 2 -print out -eprint out"

PERFDIR=perfDir
IOMATCHREP=$PERFDIR/iomatchRep

TIMECMD="/usr/bin/time -q -f %e -o "

FLOAT="--rounding=float"
FLOAT="--float=yes"

mkdir -p  $PERFDIR
mkdir -p  $IOMATCHREP


cat dd.stdout.all/rddmin-cmp/vr_iomatch.txt |sed "s/verbose: 2/verbose: 0/" >  vr_iomatch_hard.txt
cat dd.stdout.all/rddmin-cmp/vr_iomatch.txt |sed "s/verbose: 2/verbose: 0/" | sed "s/stop/stop_soft/" | sed "s/start/start_soft/" > vr_iomatch_soft.txt

for i in `seq 1 30`;
do
#    $TIMECMD $PERFDIR/timeNative.$i $CMD > $PERFDIR/res-Native-$i.out

    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatch.$i  valgrind --tool=verrou $FLOAT --IOmatch-clr=IomatchStandAlone --output-IOmatch-rep=$IOMATCHREP  $CMD > $PERFDIR/res-IOmatch-$i.out

#    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchRandom.$i  valgrind --tool=verrou --rounding-mode=random --IOmatch-clr=IomatchStandAlone --output-IOmatch-rep=$IOMATCHREP  $CMD > $PERFDIR/res-IOmatchRandom-$i.out

 #   $TIMECMD $PERFDIR/timeNone.$i  valgrind --tool=none $CMD > $PERFDIR/res-None-$i.out

#    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchExclude.$i valgrind --tool=verrou $FLOAT --IOmatch-clr=IomatchStandAlone --output-IOmatch-rep=$IOMATCHREP --exclude=all.ex $CMD > $PERFDIR/res-IOmatchExclude-$i.out

    $TIMECMD $PERFDIR/timeExclude.$i valgrind --tool=verrou $FLOAT --exclude=all.ex  $CMD > $PERFDIR/res-Exclude-$i.out

    $TIMECMD $PERFDIR/timeAll.$i valgrind --tool=verrou $FLOAT --exclude=Wtime.ex $CMD > $PERFDIR/res-All-$i.out
#    $TIMECMD $PERFDIR/timeAllRandom.$i valgrind --tool=verrou --rounding-mode=random --exclude=Wtime.ex $CMD > $PERFDIR/res-AllRandom-$i.out

    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchDDCMP.$i valgrind --tool=verrou $FLOAT --IOmatch-clr=vr_iomatch_hard.txt --output-IOmatch-rep=$IOMATCHREP $CMD > $PERFDIR/res-IOmatchDDCMP-$i.out

#    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchDDCMPRandom.$i valgrind --tool=verrou --rounding-mode=random --vr-seed=42 --IOmatch-clr=vr_iomatch_hard.txt --output-IOmatch-rep=$IOMATCHREP $CMD > $PERFDIR/res-IOmatchDDCMPRandom-$i.out

    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchDDCMP_soft.$i valgrind --tool=verrou $FLOAT --IOmatch-clr=vr_iomatch_soft.txt --output-IOmatch-rep=$IOMATCHREP $CMD > $PERFDIR/res-IOmatchDDCMP_soft-$i.out

#    LD_PRELOAD=verrouUnbuffered.so $TIMECMD $PERFDIR/timeIOmatchDDCMPRandom_soft.$i valgrind --tool=verrou --rounding-mode=random --vr-seed=42 --IOmatch-clr=vr_iomatch_soft.txt --output-IOmatch-rep=$IOMATCHREP $CMD > $PERFDIR/res-IOmatchDDCMPRandom_soft-$i.out

done;
