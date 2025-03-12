workList=unitTest unitTestTask dd.line dd.line.post dd.line.post.dump dd.task dd.stdout postTabDDMin0.tex postTabDDMin1.tex postTabDDMin1Dump.tex unittest.output.txt plotStat.png dd.line.result.tex dd.stdout.tab.result.tex dd.stdout.result.tex dd.stdout.tab dd.task.result.tex postTabDDMin1-large.tex postTabDDMin1-large-short.tex postTabDDMin0-large.tex postTabDDMin1Dump-large-short.tex codeCoverage.tex

.PHONY:

FLAGS=-Wall -g -O3


all: ${workList}


unitTest: unitTest.cxx integrate.hxx
	g++ $(FLAGS) -o $@ $<

unitTest-cover: unitTest.cxx integrate.hxx
	g++ -Wall -g -O3 --coverage -o $@ $<

coverage: unitTest-cover
	mkdir -p coverage
	rm -f *.gcda
	./unitTest-cover
	gcov *.cxx
	mv integrate.hxx.gcov coverage
	rm -f *.gcda
	valgrind --tool=verrou --rounding-mode=random --libm=instrumented --vr-seed=1 ./unitTest-cover
	gcov *.cxx
	mv integrate.hxx.gcov coverage/integrate.hxx-random.gcov
	rm -f *.gcda *.gcov

codeCoverage.tex: coverage
	./meldLatex.py coverage/integrate.hxx.gcov  coverage/integrate.hxx-random.gcov  codeCoverage.tex 100 49 24 --verb --filter-before=template --left-name="nearest coverage" --right-name="random coverage"


plotStat.png: unitTest
	verrou_plot_stat --nruns=20 --num-threads=5  --time --time-ref=1 --png=plotStat.png --log-scalx --rounding=nearest,random  --seed=42 ./statRun.sh ./extractTime.sh

plotStatConv.png: unitTest
	verrou_plot_stat --nruns=1 --time --time-ref=1 --png=plotStatConv.png --log-scalx --rounding=nearest  --seed=42 ./statRun.sh ./extractTime.sh

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
unittest.output_random_1.txt:unitTest
	valgrind --tool=verrou --rounding-mode=random --libm=instrumented  --vr-seed=1 ./unitTest > unittest.output_random_1.txt
unittest.output_random_2.txt:unitTest
	valgrind --tool=verrou --rounding-mode=random --libm=instrumented  --vr-seed=2 ./unitTest > unittest.output_random_2.txt

diffOutput.tex: unittest.output.txt  unittest.output_random_1.txt
	 ./meldOutput.py unittest.output.txt  unittest.output_random_1.txt > diffOutput.tex



postTabDDMin1.tex: dd.line.post meldLatex.py
	./meldLatex.py dd.line.post/ddmin1-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin1.tex 8 35 --left-name="ddmin1(random)" --right-name="nearest"

postTabDDMin0.tex: dd.line.post meldLatex.py
	./meldLatex.py dd.line.post/ddmin0-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin0.tex 8 35 --left-name="ddmin0(random)" --right-name="nearest"

postTabDDMin1-large.tex: dd.line.post meldLatex.py Makefile
	./meldLatex.py dd.line.post/ddmin1-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin1-large.tex 7 55 200 --left-name="ddmin1 (integrate.hxx:16) | random" --right-name="nearest"

postTabDDMin1-large-short.tex: dd.line.post meldLatex.py Makefile
	./meldLatex.py dd.line.post/ddmin1-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin1-large-short.tex 6 55 200 --left-name="ddmin1 (integrate.hxx:16) | random" --right-name="nearest"


postTabDDMin0-large.tex: dd.line.post meldLatex.py Makefile
	./meldLatex.py dd.line.post/ddmin0-trace/default/dd.run0/cover/cover00000-seqCount0  dd.line.post/NoPerturbation-trace/default/dd.run0/cover/cover00000-seqCount0 postTabDDMin0-large.tex 7 55 200 --left-name="ddmin0 (integrate.hxx:17) | random" --right-name="nearest"


postTabDDMin1Dump.tex:dd.line.post.dump
	./meldLatex.py dd.line.post.dump/ddmin1-trace/default/dd.run0/cover/cover00001-seqCount0  dd.line.post.dump/NoPerturbation-trace/default/dd.run0/cover/cover00001-seqCount0 postTabDDMin1Dump.tex 8 35 --left-name="partial (last iter) ddmin1 (integrate.hxx:16) |random" --right-name="nearest"

postTabDDMin1Dump-large-short.tex:dd.line.post.dump
	./meldLatex.py dd.line.post.dump/ddmin1-trace/default/dd.run0/cover/cover00001-seqCount0  dd.line.post.dump/NoPerturbation-trace/default/dd.run0/cover/cover00001-seqCount0 postTabDDMin1Dump-large-short.tex 5 55 200 --left-name="partial (last iter) ddmin1 (integrate.hxx.16) | random" --right-name="partial (last iter) | nearest"

dd.line.result.tex: dd.line ./ddLineLatex.sh
	./ddLineLatex.sh dd.line > dd.line.result.tex

dd.stdout.result.tex: dd.stdout ./ddStoutLatex.sh
	./ddStoutLatex.sh dd.stdout > dd.stdout.result.tex

dd.stdout.tab.result.tex: dd.stdout.tab ./ddStoutLatex.sh
	./ddStoutLatex.sh dd.stdout.tab > dd.stdout.tab.result.tex

dd.task.result.tex:
	./ddTaskLatex.sh dd.task > dd.task.result.tex


clean:
	rm -rf ${workList} verrou.stat *.aux *~ coverage
