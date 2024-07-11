
.PHONY: installLis
all: installLis

lis:
	git clone https://github.com/lathuili/lis/ --branch bl/correctness24

installLis: lis
	cd lis; \
	./configure --prefix=${PWD}/installLis &&\
	make
#no need to install: we use only a test cas 

clean:
	rm -rf lis installLis
