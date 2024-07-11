workList=unitTest unitTestTask dd.line dd.line.post dd.line.post.dump dd.task dd.stdout postTabDDMin0.tex postTabDDMin1.tex postTabDDMin1Dump.tex unittest.output.txt plotStat.png dd.line.result.tex dd.stdout.tab.result.tex dd.stdout.result.tex dd.stdout.tab dd.task.result.tex

.PHONY:

FLAGS=-Wall -g -O3


all: ${workList}


unitTest: unitTest.cxx integrate.hxx
	g++ $(FLAGS) -o $@ $<

plotStat.png: unitTest
	verrou_plot_stat --nruns=20 --time --time-ref=1 --png=plotStat.png --log-scalx --rounding=nearest,random  --seed=42 ./statRun.sh ./extractTime.sh

unitTestTask: unitTestTask.cxx integrate.hxx
	g++ $(FLAGS) -o $@ $< -lverrouTask

dd.line: unitTest ddRun.sh ddCmp.py
	verrou_dd_line --seed=42 ./ddRun.sh ./ddCmp.py

dd.line.post: dd.line
	cp -r dd.line dd.line.post
	post_verrou_dd --rep=dd.line.post --trace-bin --seed=42 ./ddRun.sh ./ddCmp.py
	touch dd.line.post

dd.line.post.dump: dd.line
	cp -r dd.line dd.line.post.dump
	post_verrou_dd --rep=dd.line.post.dump --trace-bin --seed=42 ./postDDWithDumpCoverRun.sh ./ddCmp.py

dd.stdout: unitTest
	verrou_dd_stdout --seed=42 ./ddRun.sh ./ddCmp.py

dd.stdout.tab: unitTest
	verrou_dd_stdout --rep=dd.stdout.tab --seed=42 --nruns=10 --num-threads=5 ./ddRunStep.sh ./ddCmpTab.py

dd.task: unitTestTask ddRunTask.sh ddCmp.py
	verrou_dd_task --seed=42  ddRunTask.sh ./ddCmp.py



#post-treatment for LatexInclude
unittest.output.txt:unitTest
	./unitTest > unittest.output.txt

postTabDDMin1.tex: dd.line.post meldLatex.py
	./meldLatex.py dd.line.post/ddmin1-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin1.tex 8 35

postTabDDMin0.tex: dd.line.post meldLatex.py
	./meldLatex.py dd.line.post/ddmin0-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin0.tex 8 35


postTabDDMin1Dump.tex:dd.line.post.dump
	./meldLatex.py dd.line.post.dump/ddmin1-trace/default/dd.run0/cover/cover00001-seqCount0  dd.line.post.dump/NoPerturbation-trace/default/dd.run0/cover/cover00001-seqCount0 postTabDDMin1Dump.tex 8 35

dd.line.result.tex: dd.line ./ddLineLatex.sh
	./ddLineLatex.sh dd.line > dd.line.result.tex

dd.stdout.result.tex: dd.stdout ./ddStoutLatex.sh
	./ddStoutLatex.sh dd.stdout > dd.stdout.result.tex

dd.stdout.tab.result.tex: dd.stdout.tab ./ddStoutLatex.sh
	./ddStoutLatex.sh dd.stdout.tab > dd.stdout.tab.result.tex

dd.task.result.tex:
	./ddTaskLatex.sh dd.task > dd.task.result.tex


clean:
	rm -rf ${workList} verrou.stat *.aux *~
