



# The main latex file
THESIS_MAIN_FILE   = main
PROPOSAL_MAIN_FILE = main

# The folder where the `PROPOSAL_MAIN_FILE` file is on
THESIS_FOLDER   = thesis
PROPOSAL_FOLDER = proposal

# This will be the pdf generated
THESIS_OUTPUT_NAME   = thesis
PROPOSAL_OUTPUT_NAME = proposal

# This is the folder where the temporary files are going to be
CACHE_FOLDER = cache
LATEX_MAIN_FILE := $(THESIS_FOLDER)/$(THESIS_MAIN_FILE).tex

# Find all files ending with `.tex`
LATEX_SOURCE_FILES := $(shell /bin/find -regex ".*\.\(tex\)" -not -path "./$(THESIS_FOLDER)/ufscthesisx**" -not -path "./$(PROPOSAL_FOLDER)**")

# Create a new variable within file name ending with `.pdf`
PDF_MAIN_FILE := $(THESIS_FOLDER)/$(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf


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
.PHONY: all help biber start_timer biber_hook pdflatex_hook2 pdflatex_hook1 latex proposal thesis thesis_verbose clean clean_thesis clean_proposal

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
##   proposal          build the `proposal` to the `proposal.pdf` file
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
all: proposal thesis_verbose


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

	# Enters to the thesis folder to build the files
	cd ./$(THESIS_FOLDER)

	# Call biber to process the bibliography
	echo "Running biber quietly..."

	# https://www.mankier.com/1/biber --debug
	biber --quiet --input-directory="$(CACHE_FOLDER)" --output-directory="$(CACHE_FOLDER)" $(THESIS_MAIN_FILE).bcf


# How to call Makefile recipe/rule multiple times?
# https://stackoverflow.com/questions/46135614/how-to-call-makefile-recipe-rule-multiple-times
pdflatex_hook1 pdflatex_hook2:

	# Enters to the thesis folder to build the files
	cd ./$(THESIS_FOLDER)

	# Call pdflatex to build the PDF
	@$(LATEX) $(THESIS_MAIN_FILE).tex


# This rule will be called for every latex file and pdf associated
latex:

	# Start counting the compilation time and import its shell functions
	. ./scripts/timer_calculator.sh

	# Enters to the thesis folder to build the files
	cd ./$(THESIS_FOLDER)

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Call pdflatex to build the PDF
	@$(LATEX) $(THESIS_MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(THESIS_MAIN_FILE).pdf $(current_dir)/$(THESIS_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


# MAIN LATEXMK RULE
#
# -pdf tells latexmk to generate PDF directly (instead of DVI).
#
# -pdflatex="" tells latexmk to call a specific backend with specific options.
#
# -use-make tells latexmk to call make for generating missing files. When after a run of latex or
# pdflatex, there are warnings about missing files (e.g., as requested by the LaTeX \input,
# \include, and \includgraphics commands), latexmk tries to make them by a custom dependency. If no
# relevant custom dependency with an appropriate source file is found, and if the -use-make option
# is set, then as a last resort latexmk will try to use the make program to try to make the missing
# files.
#
# -interaction=nonstopmode keeps the pdflatex backend from stopping at a missing file reference and
# interactively asking you for an alternative.
#
# https://www.ctan.org/pkg/latexmk
# http://docs.miktex.org/manual/texfeatures.html#auxdirectory
proposal:

	# Start counting the compilation time and import its shell functions
	. ./scripts/timer_calculator.sh

	# Enters to the proposal folder to build the files
	cd ./$(PROPOSAL_FOLDER)

	# Creates the shell variable `current_dir` within the current folder path
	$(eval current_dir := $(shell pwd)) echo $(current_dir) > /dev/null

	# Where to find official (!) and extended documentation for tex/latex's commandline options (especially -interaction modes)?
	# https://tex.stackexchange.com/questions/91592/where-to-find-official-and-extended-documentation-for-tex-latexs-commandlin
	#
	# Call the latex specialized make file
	latexmk \
	--pdf \
	--output-directory="$(CACHE_FOLDER)" \
	--aux-directory="$(CACHE_FOLDER)" \
	--pdflatex="$(PDF_LATEX_COMMAND) --interaction=nonstopmode" \
	$(PROPOSAL_MAIN_FILE).tex

	# Copy the generated PDF file from the cache folder
	cp $(CACHE_FOLDER)/$(PROPOSAL_MAIN_FILE).pdf $(current_dir)/$(PROPOSAL_OUTPUT_NAME).pdf

	# Calculate the elapsed seconds and print them to the screen
	showTheElapsedSeconds "$(current_dir)"


thesis:

	# Start counting the compilation time and import its shell functions
	. ./scripts/timer_calculator.sh

	# Enters to the thesis folder to build the files
	cd ./$(THESIS_FOLDER)

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
	. ./scripts/timer_calculator.sh

	# Enters to the proposal folder to build the files
	cd ./$(THESIS_FOLDER)

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


clean: clean_proposal clean_thesis


clean_thesis:
	$(RM) -rv $(THESIS_FOLDER)/$(CACHE_FOLDER)
	$(RM) -v $(THESIS_FOLDER)/$(THESIS_OUTPUT_NAME).pdf
	$(RM) -v $(THESIS_OUTPUT_NAME).pdf


clean_proposal:
	$(RM) -rv $(PROPOSAL_FOLDER)/$(CACHE_FOLDER)
	$(RM) -v $(PROPOSAL_FOLDER)/$(PROPOSAL_OUTPUT_NAME).pdf
	$(RM) -v $(PROPOSAL_OUTPUT_NAME).pdf


# Using Makefile to clean subdirectories
# https://stackoverflow.com/questions/26007005/using-makefile-to-clean-subdirectories
#
# Exclude directory from find . command
# https://stackoverflow.com/questions/4210042/exclude-directory-from-find-command
GARBAGE_TYPES := "*.gz(busy)" *.aux *.log *.aux *.bbl *.log *.out *.toc *.dvi *.blg\
*.synctex.gz *.fdb_latexmk *.fls *.lot *.lol *.lof *.idx *.bcf *.mw

DIRECTORIES_TO_CLEAN  := $(shell /bin/find -not -path "./**.git**" -not -path "./pictures**" -type d)
GARBAGE_TYPED_FOLDERS := $(foreach DIR, $(DIRECTORIES_TO_CLEAN), $(addprefix $(DIR)/,$(GARBAGE_TYPES)))

veryclean: clean_proposal clean_thesis
	$(RM) -v $(GARBAGE_TYPED_FOLDERS)


