



# The main latex file
THESIS_MAIN_FILE = main

# This will be the pdf generated
THESIS_OUTPUT_NAME = thesis

# This is the folder where the temporary files are going to be
CACHE_FOLDER = cache
LATEX_MAIN_FILE := $(THESIS_MAIN_FILE).tex

# Find all files ending with `.tex`
LATEX_SOURCE_FILES := $(shell /bin/find -regex ".*\.\(tex\)" -not -path "./ufscthesisx**")

# Create a new variable within file name ending with `.pdf`
PDF_MAIN_FILE := $(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf

# https://tex.stackexchange.com/questions/206695/latexmk-outdir-with-include
CACHE_DIRECTORIES := $(shell /bin/find \
-not -path "./**.git**" -not -path "./ufscthesisx**" -not -path "./cache**" -not -path "./pictures**" -type d)

CACHE_DIRECTORIES_TO_CREATE := $(foreach DIR, $(CACHE_DIRECTORIES), $(addprefix $(CACHE_FOLDER),$(subst .,,$(DIR))))
USELESS := $(shell mkdir -p $(CACHE_DIRECTORIES_TO_CREATE))


# Where to find official (!) and extended documentation for tex/latex's commandline options (especially -interaction modes)?
# https://tex.stackexchange.com/questions/91592/where-to-find-official-and-extended-documentation-for-tex-latexs-commandlin
PDF_LATEX_COMMAND = pdflatex --time-statistics --synctex=1 --halt-on-error --file-line-error
LATEX =	$(PDF_LATEX_COMMAND)\
--interaction=batchmode\
--output-directory="$(CACHE_FOLDER)"\
--aux-directory="$(CACHE_FOLDER)"


# Font:
# https://tex.stackexchange.com/questions/40738/how-to-properly-make-a-latex-project
#
# You want latexmk to *always* run, because make does not have all the info.
# Also, include non-file targets in .PHONY so they are run regardless of any
# file of the given name existing.
.PHONY: all help biber start_timer biber_hook pdflatex_hook2 pdflatex_hook1 latex thesis thesis_verbose clean clean_thesis

# How do I write the 'cd' command in a makefile?
# http://stackoverflow.com/questions/1789594/how-do-i-write-the-cd-command-in-a-makefile
.ONESHELL:

# GNU Make silent by default
# https://stackoverflow.com/questions/24005166/gnu-make-silent-by-default
MAKEFLAGS += --silent


##
## Usage:
##   make <target>
##
## Targets:
##   all               generate all assets
##   biber             build the `thesis` main file with bibliography pass
##   latex             build the `thesis` main file with no bibliography pass
##   thesis            build the `thesis` to the `thesis.pdf` file with no bibliography pass
##   thesis_verbose    build the `thesis` to the `thesis.pdf` file with maximum output logs
##   clean             remove all cache folders and generated pdf files
##   veryclean         same as `clean`, but searches for all generated files outside
##                     the cache folders.
##

# Print the usage instructions
# https://gist.github.com/prwhite/8168133
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'


# The first rule in a Makefile is the one executed by default ("make"). It
# should always be the "all" rule, so that "make" and "make all" are identical.
all: thesis_verbose


# Run pdflatex, biber, pdflatex
biber: start_timer biber_hook pdflatex_hook2

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Copies the PDF to the current folder
	cp $(PDF_MAIN_FILE) $(current_dir)/$(THESIS_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	. ./scripts/timer_calculator.sh
	showTheElapsedSeconds "$(current_dir)"


start_timer:

	# Start counting the elapsed seconds to print them to the screen later
	. ./scripts/timer_calculator.sh


# Internally called rule which does not attempt to show the elapsed time
biber_hook:

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Call biber to process the bibliography
	echo "Running biber quietly..."

	# https://www.mankier.com/1/biber --debug
	biber --quiet --input-directory="$(CACHE_FOLDER)" --output-directory="$(CACHE_FOLDER)" $(THESIS_MAIN_FILE).bcf


# How to call Makefile recipe/rule multiple times?
# https://stackoverflow.com/questions/46135614/how-to-call-makefile-recipe-rule-multiple-times
pdflatex_hook1 pdflatex_hook2:

	# Call pdflatex to build the PDF
	@$(LATEX) $(THESIS_MAIN_FILE).tex


# This rule will be called for every latex file and pdf associated
latex:

	# Start counting the compilation time and import its shell functions
	. ./scripts/timer_calculator.sh

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Call pdflatex to build the PDF
	@$(LATEX) $(THESIS_MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf $(current_dir)/$(THESIS_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


thesis:

	# Start counting the compilation time and import its shell functions
	. ../scripts/timer_calculator.sh

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Call the latex specialized make file
	latexmk \
	--pdf \
	--silent \
	--output-directory="$(CACHE_FOLDER)" \
	--aux-directory="$(CACHE_FOLDER)" \
	--pdflatex="$(PDF_LATEX_COMMAND) --interaction=batchmode" \
	$(THESIS_MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf $(current_dir)/$(THESIS_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


thesis_verbose:

	# Start counting the compilation time and import its shell functions
	. ../scripts/timer_calculator.sh

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# What is the difference between “-interaction=nonstopmode” and “-halt-on-error”?
	# https://tex.stackexchange.com/questions/258814/what-is-the-difference-between-interaction-nonstopmode-and-halt-on-error
	#
	# What reasons (if any) are there for compiling in interactive mode?
	# https://tex.stackexchange.com/questions/25267/what-reasons-if-any-are-there-for-compiling-in-interactive-mode
	latexmk \
	--pdf \
	--output-directory="$(CACHE_FOLDER)" \
	--aux-directory="$(CACHE_FOLDER)" \
	--pdflatex="$(PDF_LATEX_COMMAND) --interaction=nonstopmode" \
	$(THESIS_MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf $(current_dir)/$(THESIS_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


clean: clean_thesis


clean_thesis:
	$(RM) -rv $(CACHE_FOLDER)
	$(RM) -v $(THESIS_OUTPUT_NAME).pdf
	$(RM) -v $(THESIS_OUTPUT_NAME).pdf


# Using Makefile to clean subdirectories
# https://stackoverflow.com/questions/26007005/using-makefile-to-clean-subdirectories
#
# Exclude directory from find . command
# https://stackoverflow.com/questions/4210042/exclude-directory-from-find-command
GARBAGE_TYPES := "*.gz(busy)" *.aux *.log *.aux *.bbl *.log *.out *.toc *.dvi *.blg\
*.synctex.gz *.fdb_latexmk *.fls *.lot *.lol *.lof *.idx *.bcf *.mw *.run.xml

DIRECTORIES_TO_CLEAN  := $(shell /bin/find -not -path "./**.git**" -not -path "./pictures**" -type d)
GARBAGE_TYPED_FOLDERS := $(foreach DIR, $(DIRECTORIES_TO_CLEAN), $(addprefix $(DIR)/,$(GARBAGE_TYPES)))

veryclean: clean_thesis
	$(RM) -v $(GARBAGE_TYPED_FOLDERS)

