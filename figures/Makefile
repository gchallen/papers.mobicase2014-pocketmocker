TARGETS = summarytable.tex surveytable.tex screenshot.pdf overhead.pdf

all: $(TARGETS)
	@echo > /dev/null

screenshot.pdf: $(PYTEX)/bin/blank
	@$< $@ 1.11 1.77

overhead.pdf: $(PYTEX)/bin/blank
	@$< $@ 7.5 2.0

surveytable.tex summarytable.tex: surveydata.py data.csv
	@./$< data.csv

clean:
	@rm -f $(TARGETS)

.PHONY: clean all
