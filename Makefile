LATEXMK ?= latexmk
MAIN    ?= clio.tex
OUTDIR  ?= build

.PHONY: all quick figures check clean distclean

all: figures check
	$(LATEXMK) -r .latexmkrc -pdf $(MAIN)

quick: figures
	$(LATEXMK) -r .latexmkrc -pdf -interaction=nonstopmode $(MAIN)

figures:
	python scripts/manuscript/build_figures.py

check:
	python scripts/manuscript/check_labels.py --root .

clean:
	$(LATEXMK) -r .latexmkrc -c $(MAIN)
	rm -rf $(OUTDIR)

distclean: clean
	$(LATEXMK) -r .latexmkrc -C $(MAIN)
