
all: cmpInnerOuter.tex

dd.line:
	verrou_dd_line --cache=clean --num-threads=4  --dicho-granularity=4 ./runStandAlone.sh ./extractCmp.py

dd.stdout.exclude:
	verrou_dd_stdout  --rep=dd.stdout.exclude --cache=clean  --filter-cmd="./pythonFilter.py --loop-fusion=10 --outer --outer-loop-fusion=5" --nruns=1 --num-threads=4  --dicho-granularity=4   --IOmatch-header=Iomatch  runWithExclude.sh extractCmp.py

dd.stdout.all:
	verrou_dd_stdout  --rep=dd.stdout.all --cache=clean  --filter-cmd="./pythonFilter.py --loop-fusion=10 --outer --outer-loop-fusion=5" --nruns=1 --num-threads=4  --dicho-granularity=4   --IOmatch-header=Iomatch  run.sh extractCmp.py

cmpInnerOuter.tex:./postTreat.py dd.stdout.all dd.stdout.exclude
	./postTreat.py dd.stdout.all dd.stdout.exclude > cmpInnerOuter.tex

clean:
	rm -rf dd.line dd.stdout.exclude dd.stdout.all IomatchStandAlone.log-*
