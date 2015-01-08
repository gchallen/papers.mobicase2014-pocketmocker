START = noxxxnote nodraft blue
PYTEX = $(shell pwd)/pytex/
CLASS = $(PYTEX)/cls/IEEEtran.cls
END = missing

all: paper ABSTRACT

figures:
	@make -C figures

ABSTRACT: $(PYTEX)/bin/clean $(PYTEX)/bin/lib.py abstract.tex
	@$(PYTEX)/bin/clean abstract.tex ABSTRACT

# 16 Nov 2010 : GWA : Add other cleaning rules here.

clean: rulesclean
	@rm -f ABSTRACT

include $(PYTEX)/make/Makerules
