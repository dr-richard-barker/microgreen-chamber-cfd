# Makefile for npj Microgravity manuscript compilation

PYTHON := /Users/drb_laptop/Documents/AIRI_to_AIR/Circadian_decoder/.venv/bin/python

.PHONY: all figures pdf latex clean

all: figures pdf

figures:
	@echo "Generating all publication figures..."
	MPLCONFIGDIR=figures/output $(PYTHON) figures/generate_all_figures.py

pdf:
	@echo "Compiling manuscript to PDF..."
	MPLCONFIGDIR=figures/output $(PYTHON) compile_manuscript_pdf.py

latex:
	@echo "Compiling LaTeX manuscript with pdflatex..."
	@which pdflatex >/dev/null 2>&1 && ( \
		pdflatex -interaction=nonstopmode npj_manuscript.tex && \
		bibtex npj_manuscript && \
		pdflatex -interaction=nonstopmode npj_manuscript.tex && \
		pdflatex -interaction=nonstopmode npj_manuscript.tex && \
		pdflatex -interaction=nonstopmode npj_supplementary.tex && \
		pdflatex -interaction=nonstopmode npj_supplementary.tex \
	) || echo "pdflatex not found in local PATH. Please compile on a system with TeXLive or Overleaf."

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.synctex.gz
