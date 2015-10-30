LATEX=latexmk
LATEX_OPTS=-pdf -pdflatex="pdflatex --synctex=1 --shell-escape"
PYTHON=python

.PHONY: clean print

happyhour_generated.pdf: happyhour_generated.tex
	@$(LATEX) $(LATEX_OPTS) happyhour_generated.tex

happyhour_generated.tex: beers.pkl
	@$(PYTHON) make_pricelist.py $(beer)

beers.pkl:
	mkdir -p fig
	@$(PYTHON) parse_beers.py

print: happyhour_generated.pdf
	lpr happyhour_generated.pdf

clean:
	rm -rf *.pdf
	rm -rf *.pkl
	rm -rf fig/*
