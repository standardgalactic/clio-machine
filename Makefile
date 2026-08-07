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
	python scripts/manuscript/validate_scaffold.py --root .
	python scripts/manuscript/generate_dependency_graph.py --root . --check

clean:
	$(LATEXMK) -r .latexmkrc -c $(MAIN)
	rm -rf $(OUTDIR)

distclean: clean
	$(LATEXMK) -r .latexmkrc -C $(MAIN)
