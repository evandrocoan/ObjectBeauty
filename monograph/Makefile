



# The main latex file
MAIN_FILE = main

# The folder where the `MAIN_FILE` file is on
MAIN_FILE_FOLDER = proposal

# This will be the pdf generated
OUTPUT_FILE_NAME = proposta

# This is the folder where the temporary files are going to be
CACHE_FOLDER = .cache


# Font:
# https://tex.stackexchange.com/questions/40738/how-to-properly-make-a-latex-project
#
# You want latexmk to *always* run, because make does not have all the info.
# Also, include non-file targets in .PHONY so they are run regardless of any
# file of the given name existing.
.PHONY: proposal thesis all clean help

# How do I write the 'cd' command in a makefile?
# http://stackoverflow.com/questions/1789594/how-do-i-write-the-cd-command-in-a-makefile
.ONESHELL:

##
## Usage:
##   make <target>
##
## Targets:
##   all           generate all assets
##   proposal      build the `proposal` to the `proposta.pdf` file
##   thesis        build the `thesis` to the `monografia.pdf` file
##

# Print the usage instructions
# https://gist.github.com/prwhite/8168133
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


# The first rule in a Makefile is the one executed by default ("make"). It
# should always be the "all" rule, so that "make" and "make all" are identical.
all: proposal thesis


# MAIN LATEXMK RULE
#
# -pdf tells latexmk to generate PDF directly (instead of DVI).
# -pdflatex="" tells latexmk to call a specific backend with specific options.
# -use-make tells latexmk to call make for generating missing files.
#
# -interaction=nonstopmode keeps the pdflatex backend from stopping at a
# missing file reference and interactively asking you for an alternative.
#
# http://docs.miktex.org/manual/texfeatures.html#auxdirectory
proposal: $(MAIN_FILE_FOLDER)/$(MAIN_FILE).tex

	# Start counting the compilation time and import its shell functions
	. ./scripts/timer_calculator.sh

	# Enters to the proposal folder to build the files
	cd ./$(MAIN_FILE_FOLDER)

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Call the latex specialized make file
	latexmk \
	-pdf \
	-jobname="$(OUTPUT_FILE_NAME)" \
	-output-directory="$(CACHE_FOLDER)" \
	-aux-directory="$(CACHE_FOLDER)" \
	-pdflatex="pdflatex -interaction=nonstopmode" \
	-use-make $(MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(OUTPUT_FILE_NAME).pdf $(current_dir)/$(OUTPUT_FILE_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


clean: veryclean

veryclean: clean_proposal

clean_proposal:
	$(RM) -r $(MAIN_FILE_FOLDER)/$(CACHE_FOLDER)
	$(RM) -r $(MAIN_FILE_FOLDER)/$(OUTPUT_FILE_NAME).pdf
	$(RM) $(OUTPUT_FILE_NAME).aux
	$(RM) $(OUTPUT_FILE_NAME).bbl
	$(RM) $(OUTPUT_FILE_NAME).blg
	$(RM) $(OUTPUT_FILE_NAME).fls
	$(RM) $(OUTPUT_FILE_NAME).dvi
	$(RM) $(OUTPUT_FILE_NAME).fdb_latexmk
	$(RM) $(OUTPUT_FILE_NAME).synctex.gz
	$(RM) $(OUTPUT_FILE_NAME).log
	$(RM) $(OUTPUT_FILE_NAME).out
	$(RM) $(OUTPUT_FILE_NAME).pdf
	$(RM) $(OUTPUT_FILE_NAME).toc

clean_thesis:




